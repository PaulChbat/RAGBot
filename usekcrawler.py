from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re

class UsekSpider(CrawlSpider):
    name = 'usek'
    allowed_domains = ['usek.edu.lb']
    start_urls = ['https://www.usek.edu.lb/en/home']

    # Variables to store `topMenuCont` and `<header>` content only once
    top_menu_content = ''
    header_content = ''

    rules = (
        Rule(
            LinkExtractor(
                allow=r'(/[^?#]*$|\.html|\.htm)',
                deny_extensions=['pdf', 'doc', 'docx', 'xls', 'xlsx', 'png', 'jpg', 'jpeg', 'gif', 'zip', 'rar']
            ),
            callback='parse_page',
            follow=False  # Do not follow links automatically
        ),
    )

    def parse_page(self, response):
        # Get the depth of the current response
        depth = response.meta.get('depth', 0)

        # Only proceed if we're within the two-level depth
        if depth <= 2:
            # Extract `topMenuCont` and `<header>` content only once
            if not self.top_menu_content:
                self.top_menu_content = ''.join(response.xpath('//*[@class="topMenuCont"]//text()').getall()).strip()
            
            if not self.header_content:
                self.header_content = ''.join(response.xpath('//header//text()').getall()).strip()
            
            # Extract the page text, excluding `topMenuCont` and `<header>` content
            raw_text = response.xpath('//body//*[not(self::script or self::style)]/text()').getall()
            page_text = ''.join(raw_text).strip()

            # Remove `topMenuCont` and `<header>` from the main body text
            main_content = page_text.replace(self.top_menu_content, '').replace(self.header_content, '').strip()

            # Clean up text by removing unwanted whitespace
            clean_text = re.sub(r'\s+', ' ', main_content)

            # Yield the cleaned text for each page
            yield {
                'url': response.url,
                'text': clean_text,
            }

            # Manually follow links only if the current depth is less than 2
            if depth < 2:
                for link in LinkExtractor().extract_links(response):
                    yield response.follow(link.url, self.parse_page, meta={'depth': depth + 1})

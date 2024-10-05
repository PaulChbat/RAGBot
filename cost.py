import streamlit as st

def cost_page():
    conversion_rates = {
        "USD": 1.00,  # Base currency
        "Euro": 0.95,
        "GBP": 0.80,
        "LBP": 89000
    }
    st.title("Cost")
    base_cost = 10
    selected_currency = st.selectbox("Choose your currency:", list(conversion_rates.keys()))
    converted_cost = base_cost * conversion_rates[selected_currency]
    st.write(f"Here is the cost of your previous prompt: {converted_cost:.2f} {selected_currency}")

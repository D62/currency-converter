import streamlit as st
from forex_python.converter import CurrencyRates
from forex_python.converter import CurrencyCodes
import yfinance as yf

# Create an instance of the CurrencyRates class
c = CurrencyRates()

# Get the list of all available currencies
currency_list = list(c.get_rates("").keys())

# Sort the currency list alphabetically
currency_list.sort()

# Add EUR to the currency list if it is not already present
if "EUR" not in currency_list:
    currency_list.append("EUR")
    currency_list.sort()

# Streamlit page config & title
title = "Currency converter"
st.set_page_config(
    page_title=title,
    page_icon=":money_with_wings:",
    menu_items={"About": "https://github.com/D62/currency-converter"},
)
st.title(title)

# Create the 3 columns
col1, col2, col3 = st.columns(3)

# Create the dropdown menus to choose the currencies
with col2:
    from_currency = st.selectbox("From Currency", currency_list)

with col3:
    to_currency = st.selectbox("To Currency", currency_list)

# Get the exchange rate for the conversion
exchange_rate = c.get_rate(from_currency, to_currency)

# Create the input field to enter the amount
with col1:
    amount = st.number_input("Amount", value=1.00)

# Convert the amount to the destination currency
converted_amount = c.convert(from_currency, to_currency, amount)

# Display the conversion result
if from_currency != to_currency:
    st.subheader(
        f"{amount} {from_currency} is equal to {converted_amount:.2f} {to_currency} (exchange rate: {exchange_rate:.4f})"
    )
else:
    st.warning("Please select two different currencies")

# Add a chart of the exchange rate history
if from_currency != to_currency:
    chart_period = st.radio("Select a time period for the exchange rate history", ["5d", "1mo", "1y", "5y", "max"], horizontal=True)
    chart_data = yf.download(f"{from_currency}{to_currency}=X", period=chart_period)
    st.line_chart(chart_data["Close"])
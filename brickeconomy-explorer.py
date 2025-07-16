import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="BrickEconomy Explorer", layout="wide")
st.title("BrickEconomy Explorer")

# Hardcoded for testing
set_number = "10236-1"
url = "https://www.brickeconomy.com/api/v1/set/{set_number}"
headers = {
    "accept": "application/json",
    "x-apikey": "a6f1f7a7-aa75-4126-bba3-b6e10a7afda6",
    "User-Agent": "ReUseBot/1.0"
}

response = requests.get(url, headers=headers)
if response.status_code == 200:
    raw = response.json()
    data = raw.get("data", {})

    # Flatten and rename relevant fields
    table_data = {
        "Set Number": data.get("set_number"),
        "Name": data.get("name"),
        "Theme": data.get("theme"),
        "Subtheme": data.get("subtheme"),
        "Year": data.get("year"),
        "Retired": data.get("retired"),
        "Pieces": data.get("pieces_count"),
        "Minifigs Count": data.get("minifigs_count"),
        "Minifigs": ", ".join(data.get("minifigs", [])),
        "Availability": data.get("availability"),
        "Retail Price (US)": data.get("retail_price_us"),
        "Retail Price (UK)": data.get("retail_price_uk"),
        "Retail Price (EU)": data.get("retail_price_eu"),
        "Retail Price (AU)": data.get("retail_price_au"),
        "Retail Price (CA)": data.get("retail_price_ca"),
        "Current Value (New)": data.get("current_value_new"),
        "Current Value (Used)": data.get("current_value_used"),
        "Used Value Range": f"{data.get('current_value_used_low')} - {data.get('current_value_used_high')}",
        "Forecast (2yr)": data.get("forecast_value_new_2_years"),
        "Forecast (5yr)": data.get("forecast_value_new_5_years"),
        "Growth Last Year (%)": data.get("rolling_growth_lastyear"),
        "Growth Last 12 Mo (%)": data.get("rolling_growth_12months"),
        "Released": data.get("released_date"),
        "Retired Date": data.get("retired_date"),
        "EAN": data.get("ean"),
        "UPC": data.get("upc"),
        "Currency": data.get("currency")
    }

    df = pd.DataFrame(table_data.items(), columns=["Field", "Value"])
    st.table(df)

else:
    st.error(f"API returned {response.status_code}: {response.text}")


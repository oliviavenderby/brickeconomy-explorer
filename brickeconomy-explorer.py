import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="BrickEconomy Explorer", layout="centered")
st.title("BrickEconomy Explorer")

# --- USER INPUT ---
set_number = st.text_input("Enter LEGO Set Number (e.g. 10236-1)")

# --- API CALL ---
url = f"https://www.brickeconomy.com/api/v1/set/{set_number}"
headers = {
    "accept": "application/json",
    "x-apikey": "a6f1f7a7-aa75-4126-bba3-b6e10a7afda6",
    "User-Agent": "ReUseBot/1.0"
}

try:
    response = requests.get(url, headers=headers, timeout=10)

    try:
        raw = response.json()
    except ValueError:
        st.error("❌ Response is not valid JSON.")
        st.text(response.text)
        st.stop()

    data = raw.get("data", {})
    if not data:
        st.warning("No data returned for that set number.")
        st.stop()

    # --- INFO TABLE ---
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

    st.markdown("### Set Details")
    for field, value in table_data.items():
        st.markdown(f"**{field}**: {value}")


    # --- PRICE CHART (NEW) ---
    price_events = data.get("price_events_new", [])
    if price_events:
        price_df = pd.DataFrame(price_events)
        price_df["date"] = pd.to_datetime(price_df["date"])
        fig = px.line(price_df, x="date", y="value", markers=True,
                      title="Price Trend: The last 12 interesting price events that put various pressure on price.",
                      labels={"value": f"Price ({data.get('currency', 'USD')})", "date": "Date"})
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No price trend data available for this set.")

except requests.exceptions.RequestException as e:
    st.error(f"API request failed: {e}")




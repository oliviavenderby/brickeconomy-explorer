import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="BrickEconomy Growth Stats", layout="centered")
st.title("BrickEconomy Growth Statistics")

# --- User Input ---
input_text = st.text_input("Enter LEGO Set Numbers (e.g. 10236-1, 75192-1) to extract growth statistics from BrickEconomy.")

# --- API Setup ---
headers = {
    "accept": "application/json",
    "x-apikey": "a6f1f7a7-aa75-4126-bba3-b6e10a7afda6",
    "User-Agent": "ReUseBot/1.0"
}

# --- Process if input exists ---
if input_text:
    set_numbers = [s.strip() for s in input_text.split(",")]
    growth_data = []
    trend_rows = []  # <-- Make sure this is initialized before use

    for set_number in set_numbers:
        url = f"https://www.brickeconomy.com/api/v1/set/{set_number}"
        try:
            response = requests.get(url, headers=headers, timeout=10)
            data = response.json().get("data", {})

            name = data.get("name", "N/A")
            growth_data.append({
                "Set": set_number,
                "Name": name,
                "Growth Last Year (%)": data.get("rolling_growth_lastyear", "N/A"),
                "Growth Last 12 Mo (%)": data.get("rolling_growth_12months", "N/A")
            })

            # --- Collect price trend data ---
            for event in data.get("price_events_new", []):
                trend_rows.append({
                    "Set": name or set_number,
                    "Date": event["date"],
                    "Price": event["value"]
                })

        except Exception as e:
            growth_data.append({
                "Set": set_number,
                "Name": "Error",
                "Growth Last Year (%)": "N/A",
                "Growth Last 12 Mo (%)": "N/A"
            })

    # --- Show Table ---
    df = pd.DataFrame(growth_data)
    st.dataframe(df, use_container_width=True)

    # --- CSV Export Button ---
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name="lego_growth_stats.csv",
        mime="text/csv"
    )

    # --- Show Price Trend Chart ---
    if trend_rows:
        trend_df = pd.DataFrame(trend_rows)
        trend_df["Date"] = pd.to_datetime(trend_df["Date"])
        fig = px.line(
            trend_df,
            x="Date",
            y="Price",
            color="Set",
            markers=True,
            title="Price Trend for Each Set",
            labels={"Price": "Price (USD)", "Date": "Date"}
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No price trend data available for any of the sets.")



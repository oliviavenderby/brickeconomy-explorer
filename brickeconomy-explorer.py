import streamlit as st
import requests
import pandas as pd

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

    for set_number in set_numbers:
        url = f"https://www.brickeconomy.com/api/v1/set/{set_number}"
        try:
            response = requests.get(url, headers=headers, timeout=10)
            data = response.json().get("data", {})

            growth_data.append({
                "Set": set_number,
                "Name": data.get("name", "N/A"),
                "Growth Last Year (%)": data.get("rolling_growth_lastyear", "N/A"),
                "Growth Last 12 Mo (%)": data.get("rolling_growth_12months", "N/A")
            })

        except Exception as e:
            growth_data.append({
                "Set": set_number,
                "Name": "Error",
                "Growth Last Year (%)": "N/A",
                "Growth Last 12 Mo (%)": "N/A"
            })

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




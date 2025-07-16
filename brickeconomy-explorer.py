import streamlit as st
import requests

API_KEY = "a6f1f7a7-aa75-4126-bba3-b6e10a7afda6"

def get_set_data(set_number):
    url = f"https://www.brickeconomy.com/api/v1/set/{set_number}"
    headers = {
        "accept": "application/json",
        "x-apikey": API_KEY,
        "User-Agent": "ReUseBot/1.0"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"❌ API request failed: {e}")
        return None

st.set_page_config(page_title="BrickEconomy Explorer", layout="centered")
st.title("🧱 ReUseBricks BrickEconomy Explorer")

set_number = st.text_input("Enter LEGO Set Number (e.g. 10236-1)")

if set_number:
    data = get_set_data(set_number.strip())
    if data:
        st.subheader(data.get("name", "Unknown Set"))
        st.image(data.get("image_url", ""), use_column_width=True)
        st.markdown(f"**Theme:** {data.get('theme', 'N/A')}")
        st.markdown(f"**Year:** {data.get('year', 'N/A')}")
        st.markdown(f"**New Price (USD):** ${data.get('price_new', {}).get('usd', 'N/A')}")
        st.markdown(f"**Used Price (USD):** ${data.get('price_used', {}).get('usd', 'N/A')}")
    else:
        st.warning("Set not found or error fetching data.")

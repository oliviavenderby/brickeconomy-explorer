import streamlit as st
import requests
import json

st.set_page_config(page_title="BrickEconomy Debug", layout="wide")
st.title("🧱 BrickEconomy Set Debugger")

# Hardcoded for testing
url = "https://www.brickeconomy.com/api/v1/set/30687"
headers = {
    "accept": "application/json",
    "x-apikey": "a6f1f7a7-aa75-4126-bba3-b6e10a7afda6",
    "User-Agent": "ReUseBot/1.0"
}

try:
    response = requests.get(url, headers=headers, timeout=10)
    st.markdown(f"### Response Status Code: `{response.status_code}`")

    if response.status_code == 200:
        data = response.json()
        
        # Full JSON output
        st.markdown("### Full API Response (Raw JSON):")
        st.json(data)

        # Only display known fields safely
        st.markdown("### Key Fields:")
        st.write("**Name:**", data.get("name", "N/A"))
        st.write("**Theme:**", data.get("theme", "N/A"))
        st.write("**Year:**", data.get("year", "N/A"))
        st.write("**New Price (USD):**", data.get("price_new", {}).get("usd", "N/A"))
        st.write("**Used Price (USD):**", data.get("price_used", {}).get("usd", "N/A"))

        # Safe image load
        image_url = data.get("image_url")
        if image_url:
            st.image(image_url, caption=data.get("name"), use_column_width=True)
        else:
            st.warning("No image URL found.")

    else:
        st.error(f"❌ API Error: {response.status_code} - {response.text}")

except requests.exceptions.RequestException as e:
    st.error(f"❌ Request failed: {e}")


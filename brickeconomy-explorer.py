import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_KEY = "a6f1f7a7-aa75-4126-bba3-b6e10a7afda6"

def get_set_data(set_number):
    url = f"https://api.brickeconomy.com/v1/sets/{set_number}?key={API_KEY}"
    response = requests.get(url)
    return response.json()

st.title("ReUseBricks BrickEconomy Explorer")

set_number = st.text_input("Enter LEGO Set Number (e.g. 75301)")

if set_number:
    data = get_set_data(set_number)
    if 'name' in data:
        st.subheader(data['name'])
        st.image(data['image_url'])
        st.markdown(f"**Theme:** {data['theme']}")
        st.markdown(f"**Year:** {data['year']}")
        st.markdown(f"**Current New Price:** ${data['price_new']['usd']}")
        st.markdown(f"**Current Used Price:** ${data['price_used']['usd']}")

        # Optional: chart price history if available
        if 'price_history' in data:
            df = pd.DataFrame(data['price_history'])
            fig = px.line(df, x='date', y='price', title='Price History')
            st.plotly_chart(fig)
    else:
        st.error("Set not found or error fetching data.")

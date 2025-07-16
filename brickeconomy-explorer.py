import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_KEY = "a6f1f7a7-aa75-4126-bba3-b6e10a7afda6"

import requests

API_KEY = "a6f1f7a7-aa75-4126-bba3-b6e10a7afda6"
set_number = "10236-1"  # use correct format (with dash)
url = f"https://www.brickeconomy.com/api/v1/set?number={set_number}"

headers = {
    "Accept": "application/json",
    "User-Agent": "ReUseBot/1.0",
    "x-apikey": API_KEY
}

response = requests.get(url, headers=headers)
print(response.status_code)
print(response.json())

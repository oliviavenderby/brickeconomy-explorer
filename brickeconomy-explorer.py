import streamlit as st
import requests

import requests

url = "https://www.brickeconomy.com/api/v1/set/30687"
headers = {
    "accept": "application/json",
    "x-apikey": "a6f1f7a7-aa75-4126-bba3-b6e10a7afda6",
    "User-Agent": "ReUseBot/1.0"
}

response = requests.get(url, headers=headers)
print(response.status_code)
print(response.json())


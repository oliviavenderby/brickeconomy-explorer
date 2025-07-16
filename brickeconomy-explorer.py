import requests

url = "https://www.brickeconomy.com/api/v1/set/10226"
headers = {
    "accept": "application/json",
    "x-apikey": "a6f1f7a7-aa75-4126-bba3-b6e10a7afda6",
    "User-Agent": "ReUseBot/1.0"
}

try:
    response = requests.get(url, headers=headers, timeout=10)
    print("Status code:", response.status_code)
    print("Response text:", response.text)

    if response.status_code == 200:
        data = response.json()
        print("✅ Success:", data)
    else:
        print("❌ Failed:", response.status_code)

except requests.exceptions.RequestException as e:
    print("❌ Request error:", e)


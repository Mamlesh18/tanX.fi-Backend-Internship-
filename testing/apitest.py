import requests

url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?CMC_PRO_API_KEY=ad723eca-82b7-49f8-a5f5-2ff83836edc6"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()

    
    for crypto in data['data']:
        if crypto['symbol'] == 'BTC':
            btc_price = crypto['quote']['USD']['price']
            print(f"Bitcoin (BTC) price: ${btc_price}")
            break
else:
    print(f"Failed to retrieve data: {response.status_code}, {response.text}")

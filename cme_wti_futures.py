import requests
import json
import pandas as pd


date = "04/09/2020"
raw_data = "https://www.cmegroup.com/CmeWS/mvc/Settlements/Futures/Settlements/425/FUT?tradeDate=" + date

url = raw_data
response = requests.get(url)


json_data = json.loads(response.content)

settlement_data = pd.DataFrame(json_data)
settlements = [pd.DataFrame(settlement, index=[i]) for (i, settlement) in enumerate(settlement_data['settlements'])]
monthly_price_data = pd.concat(settlements)
# print(monthly_price_data)

monthly_price_data.to_excel("cme_wti_future_prices.xlsx")

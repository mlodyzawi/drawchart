import argparse
import requests
import pandas as pd
import plotly.express as px
import json

parser = argparse.ArgumentParser(description='Draw a chart of given stock\'s ticker.')
parser.add_argument('-a', '--api_key', required=True, metavar='', help='your alpha vantage api key')
parser.add_argument(
        '-t', '--ticker',
        type=str,
        help='your stock, eg. FB, TSLA, AAPL', metavar='',
        required=True
    )
args = parser.parse_args()
api_key = getattr(args, 'api_key')
ticker = getattr(args, 'ticker')

if not ticker:
    exit("You've provided wrong ticker")

url = "https://alpha-vantage.p.rapidapi.com/query"
querystring = {"function":"TIME_SERIES_DAILY","symbol":ticker.upper(),"outputsize":"compact","datatype":"json"}
headers = {"X-RapidAPI-Host": "alpha-vantage.p.rapidapi.com", "X-RapidAPI-Key": api_key}
response = requests.request("GET", url, headers=headers, params=querystring)

ticker = json.loads(response.text)
time_series = ticker['Time Series (Daily)']
dates = list(time_series.keys())[::-1]
prices = []
for i in dates:
    prices.append(float(time_series[i]['4. close']))

df = pd.DataFrame({'Dates': dates, 'Price in USD': prices})
chart = px.line(df, x='Dates', y='Price in USD', title='your ticker\'s graph')
if __name__ == '__main__':
    chart.show()

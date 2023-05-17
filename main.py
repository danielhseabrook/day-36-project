from twilio.rest import Client
import requests
from datetime import date, timedelta
from os import environ
STOCK = "TSLA"
COMPANY_NAME = "Tesla"
newsapi = environ['NEWSAPI_KEY']
alphavapi = environ['ALPHAVAPI_KEY']
twilio_number = environ['TWILIO_NUMBER']
my_number = environ['MY_NUMBER']
twilio_authtoken = environ['TWILIO_AUTHTOKEN']
twilio_account_sid = environ['TWILIO_ACCSID']
client = Client(twilio_account_sid, twilio_authtoken)
date_1 = date.today() - timedelta(days=1)
date_2 = date.today() - timedelta(days=2)

# API Parameters
stock_parameters = {
    'function': 'TIME_SERIES_DAILY_ADJUSTED',
    'symbol': STOCK,
    'apikey': alphavapi,
}
news_parameters = {
    'q': COMPANY_NAME,
    'from': date_2,
    'sortBy': 'popularity',
    'apiKey': newsapi,
    'searchIn': 'title'
}
# Obtaining and manipulating stock price data
alphav_response = requests.get(url='https://www.alphavantage.co/query', params=stock_parameters)
alphav_response.raise_for_status()
stock_date_1 = alphav_response.json()['Time Series (Daily)'][str(date_1)]['4. close']
stock_date_2 = alphav_response.json()['Time Series (Daily)'][str(date_2)]['4. close']

stock_difference = float(stock_date_1) / float(stock_date_2) * 100 - 100
if stock_difference < 0:
    stock_difference_percent = "🔻" + str(("%.2f" % round(stock_difference, 2))) + "%"
else:
    stock_difference_percent = "🔺" + str(("%.2f" % round(stock_difference, 2))) + "%"

# Obtaining and manipulating news data
news_response = requests.get(url='https://newsapi.org/v2/everything', params=news_parameters)
news_response.raise_for_status()
news_data = news_response.json()['articles'][:3]

# Checking stock variance and notifying of movement greater than +-5%
if stock_difference >= 5 or stock_difference <= -5:
    for _ in news_data:
        client.messages.create(
            body=f"{STOCK}: {stock_difference_percent}\nHeadline:{_['title']}\nBrief:{_['description']}"
                 f"\nLink:{_['url']}",
            from_=twilio_number,
            to=my_number
        )
        print(f"{STOCK}: {stock_difference_percent}\nHeadline:{_['title']}\nBrief:{_['description']}"
              f"\nLink:{_['url']}")

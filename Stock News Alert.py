import requests
from twilio.rest import Client

VIRTUAL_TWILIO_NUMBER = "Your vitual twilio number"
RECIEPT_MSG_NUMBER = "Your pone or receiver"

# Trgae stock track price
STOCK_NAME = "AMD"
COMPANY_NAME = "Advanced Micro Devices, Inc."

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "STOCK API LEY"
NEWS_API_KEY = "NEWS_API_KEY"
TWILIO_SID = "YOUR TWILIO_SID "
TWILIO_AUTH_TOKEN = "YOUR TWILIO_AUTH_TOKEN"


stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

stock_connect = requests.get(STOCK_ENDPOINT, params=stock_params)
data = stock_connect.json()["Time Series (Daily)"]

# Get news when stock prices change 1% compared with the day before yesterday and yesterday
# Get yesterday's closing stock price
data_list = [value for value in data.values()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
print(yesterday_closing_price)
# Get the day before yesterday's closing stock price
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
print(day_before_yesterday_closing_price)

# Calculate %change
percent_change = round(((float(yesterday_closing_price)/float(day_before_yesterday_closing_price)-1)*100),2) 
up_down = None
if percent_change > 0:
    up_down = "🔺"
else:
    up_down = "🔻"
print(f"{percent_change}% change from the day before yesterday")

# get articles related to the COMPANY_NAME if  %change more than 1
if abs(percent_change) > 1:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }
    
    news_connect = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_connect.json()["articles"]

    # Selected from last update 3 articles
    three_articles = articles[:3]
    print(three_articles)

    # Create a new list of the first 3 article's headline and description using list comprehension.
    formatted_articles = [f"{STOCK_NAME}: {up_down}{percent_change}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]
    print(formatted_articles)
    # Send each article as a separate message via Twilio.
    
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_=VIRTUAL_TWILIO_NUMBER,
            to=RECIEPT_MSG_NUMBER
        )

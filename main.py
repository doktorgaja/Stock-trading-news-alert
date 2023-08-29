import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
apikey = "GQF32LMURBJ6T93I"
news_apikey = "ea5d587a130040e9931d1aed78337999"
TWILIO_SID = "AC1728d85efe54abf0e2e78fa31910a459"
AUTH_TOKEN = "cc25fa3a418308970f0d54f4d3c38a01"
MY_NUMBER = "+381692298722"
    ## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

stock_params = {
    "function":"TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": apikey
}

response = requests.get(url=STOCK_ENDPOINT, params=stock_params)
response.raise_for_status()
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]

yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
print(yesterday_closing_price)

day_before_yesterday_data = data_list[1]
day_before_yesterday_data_closing_price = day_before_yesterday_data["4. close"]
print(day_before_yesterday_data_closing_price)

positive_difference = float(yesterday_closing_price) - float(day_before_yesterday_data_closing_price)
if positive_difference > 0:
    up_down = "EMOJI"
else:
    up_down = "EMOJI"

difference_percentage = round(positive_difference / float(yesterday_closing_price)) * 100
print(difference_percentage)

if abs(difference_percentage) > 1:
    news_params = {
        "apikey": news_apikey,
        "q": COMPANY_NAME,
    }

    response1 = requests.get(url=NEWS_ENDPOINT, params=news_params)
    response1.raise_for_status()
    data1 = response1.json()["articles"]

    ## STEP 2: https://newsapi.org/
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

    three_articles = data1[:3]
    print(three_articles)

    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    #to send a separate message with each article's title and description to your phone number. 

#TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.
    formated_articles = [f"{STOCK_NAME}: {up_down}{difference_percentage}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]
#TODO 9. - Send each article as a separate message via Twilio.
    client = Client(TWILIO_SID, AUTH_TOKEN)

    for article in formated_articles:

        message = client.messages.create(
            body=article,
            from_=+12187353820,
            to=MY_NUMBER
        )

#Optional TODO: Format the message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""


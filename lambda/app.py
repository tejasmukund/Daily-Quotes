import http.client
import json
import random
import boto3 # preinstalled in lambda
import requests
import os

client = boto3.client('sns')


def fetch_quotes_from_api():
    response = requests.get("https://zenquotes.io/api/quotes")
    quotes = response.json()
    return quotes


def find_random_quote(quotes):
    index = random.randint(0, len(quotes) - 1)
    return quotes[index]


def send_email(quote):
    client.publish(
        TopicArn=os.getenv('TopicArn'),
        Message=f"""

        Hi! This is your motivation quote of the day.

        "{quote}"

        Powered by DailyQyotes@honey.com

        """,
        Subject='Quote Of The Day!',
    )


def lambda_handler(event, context):
    quotes = fetch_quotes_from_api()
    random_quote = find_random_quote(quotes)
    send_email(random_quote)
    print(f"\n\n Successfully sent quote {random_quote['q']} via email")



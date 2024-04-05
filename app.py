import http.client
import json
import random
import boto3
from dotenv import dotenv_values 
from dotenv import load_dotenv
load_dotenv()
config = dotenv_values(".env") 
 


client = boto3.client(
    "sns",
    aws_access_key_id=config["aws_access_key_id"],
    aws_secret_access_key= config["aws_secret_access_key"],
    region_name=config["region_name"],
)

def fetch_quotes_from_api():
    conn = http.client.HTTPSConnection("zenquotes.io")
    conn.request("GET", "/api/quotes")
    res = conn.getresponse()
    data = res.read()
    quotes = json.loads(data.decode("utf-8"))
    return quotes


def find_random_quote(quotes):
    index = random.randint(0, len(quotes) - 1)
    return quotes[index]

def send_email(random_quote):
    response = client.publish(
        TopicArn=config["TopicArn"],        
        Message=random_quote['q'],
        Subject='Quote of the Day from Tejas Mukund!',
   )


def main():
    quotes = fetch_quotes_from_api()
    random_quote = find_random_quote(quotes)
    send_email(random_quote)
    print(f"\n\n{random_quote['q']=}")


main()

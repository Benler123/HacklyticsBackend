import pymongo
import json
from pymongo import MongoClient


# # MongoDB 
# username = "tinderforstocks"
# password = "9w0rICnGSUESKqeM"

# uri = f"mongodb+srv://{username}:{password}@hacklytics.pz7w1jr.mongodb.net/?retryWrites=true&w=majority"
# client = MongoClient(uri, server_api=ServerApi('1'))
# database = client.tinder_for_stocks

password = "Boris123"


uri = f"mongodb+srv://tkwok123:{password}@cluster0.ab0yi.mongodb.net/?retryWrites=true&w=majority"

cluster = MongoClient(uri)

db = cluster["StockData"]
tickers_collections = db["Tickers"]
swipes_collection = db["Swipes"]
sentiment_collections = db["Sentiments"]

def add_ticker_info(): 
    tickers_collections.insert_one({"_id":0, "user_name":"Soumi"})
    tickers_collections.insert_one({"_id":100, "user_name":"Ravi"})

def add_swipe(ticker, swiped):
    swipes_collection.insert_one({"ticker": ticker, "swiped":swiped})

def add_sentiment(ticker, sentiment_score): 
    sentiment_collections.insert_one({"ticker": ticker, "percentage": sentiment_score})

def add_all_sentiments(): 
    with open("sentiments.json", mode='r') as file_object:
        loaded_sentiments = json.load(file_object)
        for sentiment in loaded_sentiments: 
            print(sentiment)
            #add_sentiment()
    


portfolio = []
swipes = swipes_collection.find()
for swipe in swipes: 
    ticker = swipe['ticker']
    ticker_info = tickers_collections.find({"ticker": ticker})
    beta = ticker_info['beta']
    sector = ticker_info['sector']
    get_annual
    portfolio.append({
        ticker: {
            "beta": beta, 
            "sector": sector, 
            "annual_return": annual_return
        }
    })



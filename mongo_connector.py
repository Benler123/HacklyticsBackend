import pymongo
import json
from pymongo import MongoClient
import pandas as pd

password = "Boris123"


uri = f"mongodb+srv://tkwok123:{password}@cluster0.ab0yi.mongodb.net/?retryWrites=true&w=majority"

cluster = MongoClient(uri)

db = cluster["StockData"]
tickers_collections = db["Tickers"]
swipes_collection = db["Swipes"]
sentiment_collections = db["Sentiments"]
accounts_collection = db["Account"]

def clear_tickers():
    tickers_collections.delete_many({})

def clear_swipes():
    swipes_collection.delete_many({})

def add_ticker_info(ticker, pe, marketCap, forwardPE, beta, sector, headlines): 
    tickers_collections.insert_one({"ticker": ticker, "PE": pe, "forwardPE":forwardPE, "MarketCap":marketCap, "Beta": beta, "Sector": sector, "headlines": headlines})

def add_swipe(ticker, swiped):
    swipes_collection.insert_one({"ticker": ticker, "swiped":swiped})

def add_sentiment(ticker, sentiment_score): 
    sentiment_collections.insert_one({"ticker": ticker, "percentage": sentiment_score})

def add_all_sentiments(): 
    with open("sentiments.json", mode='r') as file_object:
        loaded_sentiments = json.load(file_object)
        for sentiment in loaded_sentiments: 
            print(sentiment)
            add_sentiment(sentiment)
    


def return_ticker_df():
    tickers_collections.find({})
    df = pd.DataFrame(list(tickers_collections.find({})))
    return df

def add_account(risk_level, sectors, companyAge, companySize):
    accounts_collection.delete_many({})
    clear_swipes()
    accounts_collection.insert_one({"risk_level": risk_level, "sectors":sectors, "companyAge":companyAge, "companySize":companySize})

def return_account_df():
    df = pd.DataFrame(list(accounts_collection.find({})))
    return df

def get_seen():
    return pd.DataFrame(list(swipes_collection.find({})))["ticker"].tolist()

def get_chosen():
    df = pd.DataFrame(list(swipes_collection.find({})))
    tickers = df.loc[df["swiped"] == "right", "ticker"].tolist()
    return tickers


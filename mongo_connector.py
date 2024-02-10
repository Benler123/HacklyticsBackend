import pymongo
from pymongo import MongoClient
import pandas as pd

password = "Boris123"


uri = f"mongodb+srv://tkwok123:{password}@cluster0.ab0yi.mongodb.net/?retryWrites=true&w=majority"

cluster = MongoClient(uri)

db = cluster["StockData"]
tickers_collections = db["Tickers"]
swipes_collection = db["Swipes"]

def clear_tickers():
    tickers_collections.delete_many({})

def add_ticker_info(ticker, pe, marketCap, forwardPE, beta, sector, headlines): 
    tickers_collections.insert_one({"ticker": ticker, "pe": pe, "forwardPE":forwardPE, "marketCap":marketCap, "beta": beta, "sector": sector, "headlines": headlines})


def add_swipe(ticker, swiped):
    swipes_collection.insert_one({"ticker": ticker, "swiped":swiped})

def return_ticker_df():
    tickers_collections.find({})
    df = pd.DataFrame(list(tickers_collections.find({})))
    return df

print(return_ticker_df().head())
                             
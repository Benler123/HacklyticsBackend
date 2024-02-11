import pymongo
from pymongo import MongoClient
import pandas as pd

password = "Boris123"


uri = f"mongodb+srv://tkwok123:{password}@cluster0.ab0yi.mongodb.net/?retryWrites=true&w=majority"

cluster = MongoClient(uri)

db = cluster["StockData"]
tickers_collections = db["Tickers"]
swipes_collection = db["Swipes"]
accounts_collection = db["Account"]

def clear_tickers():
    tickers_collections.delete_many({})

def add_ticker_info(ticker, pe, marketCap, forwardPE, beta, sector, headlines): 
    tickers_collections.insert_one({"ticker": ticker, "PE": pe, "forwardPE":forwardPE, "MarketCap":marketCap, "Beta": beta, "Sector": sector, "headlines": headlines})

def add_swipe(ticker, swiped):
    swipes_collection.insert_one({"ticker": ticker, "swiped":swiped})

def return_ticker_df():
    tickers_collections.find({})
    df = pd.DataFrame(list(tickers_collections.find({})))
    return df

def add_account(risk_level, sectors, companyAge, companySize):
    accounts_collection.delete_many({})
    accounts_collection.insert_one({"risk_level": risk_level, "sectors":sectors, "companyAge":companyAge, "companySize":companySize})

def return_account_df():
    df = pd.DataFrame(list(accounts_collection.find({})))
    return df

def get_seen():
    return  pd.DataFrame(list(swipes_collection.find({})))["ticker"].tolist()



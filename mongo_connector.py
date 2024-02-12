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
accounts_collection = db["Account"]

def clear_swipes():
    swipes_collection.delete_many({})

def add_ticker_info(ticker, pe, marketCap, forwardPE, beta, sector, sentiment, headlines, companyName, companySize, description, consolidatedVolume, marketOpen, previousClose, dividentYield, annualReturn): 
    tickers_collections.insert_one({"ticker": ticker, "PE": pe, "forwardPE":forwardPE, "MarketCap":marketCap, "Beta": beta, "Sector": sector, "Sentiment": sentiment, "headlines": headlines, "CompanyName": companyName, "CompanySize": companySize, "Description": description, "ConsolidatedVolume": consolidatedVolume, "MarketOpen": marketOpen, "PreviousClose": previousClose, "DividentYield": dividentYield, "AnnualReturn": annualReturn})

def add_swipe(ticker, swiped):
    swipes_collection.insert_one({"ticker": ticker, "swiped":swiped})

def return_ticker_df():
    tickers_collections.find({})
    df = pd.DataFrame(list(tickers_collections.find({})))
    return df

def add_account(risk_level, sectors, companyAge, companySize):
    accounts_collection.delete_many({})
    clear_swipes()
    accounts_collection.insert_one({"risk_level":risk_level, "sectors":sectors, "companyAge":companyAge, "companySize":companySize})

def return_account_df():
    df = pd.DataFrame(list(accounts_collection.find({})))
    print(df['sectors'])
    return df

def get_seen():
    swipes =  pd.DataFrame(list(swipes_collection.find({})))
    if(swipes.empty):
        return []
    else:
        return swipes["ticker"].tolist()

def get_chosen():
    df = pd.DataFrame(list(swipes_collection.find({})))
    tickers = df.loc[df["swiped"] == "right", "ticker"].tolist()
    return tickers


def replace_nan_divident_yield():
    tickers_collections.update_many(
        {"DividentYield": float('nan')},
        {"$set": {"DividentYield": 0}}
    )

def get_beta_mdb(ticker): 
    ticker_data = tickers_collections.find_one({"ticker": ticker})
    beta = ticker_data.get("Beta")
    return beta

def get_annual_return_mdb(ticker): 
    ticker_data = tickers_collections.find_one({"ticker": ticker})
    annual_return = ticker_data.get("AnnualReturn")
    return annual_return

def get_sector_mdb(ticker): 
    ticker_data = tickers_collections.find_one({"ticker": ticker})
    sector = ticker_data.get("Sector")
    return sector


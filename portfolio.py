import pymongo
from pymongo import MongoClient
import iex_connector
import mongo_connector

password = "Boris123"

uri = f"mongodb+srv://tkwok123:{password}@cluster0.ab0yi.mongodb.net/?retryWrites=true&w=majority"

cluster = MongoClient(uri)
db = cluster["StockData"]
swipes_collection = db["Swipes"]

def get_portfolio():
    portfolio = {}
    tickers = mongo_connector.get_seen()
    for ticker in tickers: 
        beta = mongo_connector.get_beta_mdb(ticker)
        annual_return = mongo_connector.get_annual_return_mdb(ticker)
        sector = mongo_connector.get_sector_mdb(ticker)
        if ticker not in portfolio.keys():
            portfolio[ticker] = {
                "Sector": sector, 
                "Beta": beta, 
                "Annual Return": annual_return
            }
    return portfolio


import pymongo
from pymongo import MongoClient
import iex_connector
import app


password = "Boris123"

uri = f"mongodb+srv://tkwok123:{password}@cluster0.ab0yi.mongodb.net/?retryWrites=true&w=majority"

cluster = MongoClient(uri)
db = cluster["StockData"]
swipes_collection = db["Swipes"]

def get_portfolio():
    portfolio = {}
    swipes = swipes_collection.find()
    for swipe in swipes: 
        ticker = swipe['ticker']
        pe, beta, forwardPE, marketCap = iex_connector.get_advanced_stats(ticker)
        annual_return = app.get_annualreturn(ticker)
        sector = app.get_sector(ticker)
        if ticker not in portfolio.keys():
            print(ticker)
            portfolio[ticker] = {
                "sector": sector, 
                "beta": beta, 
                "annual_return": annual_return
            }
    return portfolio

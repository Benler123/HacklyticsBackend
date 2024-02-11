from fastapi import FastAPI, HTTPException, Body, BackgroundTasks
import requests
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import mongo_connector
import iex_connector
import json

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ticker_df = mongo_connector.return_ticker_df()
account_df = mongo_connector.return_account_df()

token = "pk_6dcff48d8ea347d8aaafcbc3c123073e"
url = "https://api.iex.cloud/v1/data/core"

@app.get('/')
def index():
    return 'Hello, World!'

@app.get('/CompanyName/{ticker}')
def get_companyname(ticker):
    cn = (requests.get(url + f"/company/{ticker}?token={token}").json())[0]["companyName"]
    return cn

@app.get('/CompanySize/{ticker}')
def get_companysize(ticker):
    cs = (requests.get(url + f"/company/{ticker}?token={token}").json())[0]["employees"]
    return cs

@app.get('/Description/{ticker}')
def get_description(ticker):
    cs = (requests.get(url + f"/company/{ticker}?token={token}").json())[0]["shortDescription"]
    return cs

@app.get('/Sector/{ticker}')
def get_sector(ticker):
    sec = (requests.get(url + f"/company/{ticker}?token={token}").json())[0]["sector"]
    return sec

@app.get('/graph/{ticker}')
def get_graph(ticker):
    six_month_data = requests.get(url + f"/historical_prices/{ticker}?range=6m&token={token}").json()
    one_month_data = requests.get(url + f"/historical_prices/{ticker}?range=1m&token={token}").json()
    ytd_data = requests.get(url + f"/historical_prices/{ticker}?range=ytd&token={token}").json()

    six_month_prices = {day["priceDate"]: day["close"] for day in six_month_data}
    one_month_prices = {day["priceDate"]: day["close"] for day in one_month_data}
    ytd_prices =  {day["priceDate"]: day["close"] for day in ytd_data}

    return {"six_month": six_month_prices,"one_month": one_month_prices, "ytd": ytd_prices}


# https://api.iex.cloud/v1/data/CORE/INTRADAY_PRICES/SPY?token=pk_6dcff48d8ea347d8aaafcbc3c123073e

@app.get('/intraday/{ticker}')
def get_intraday(ticker):
    print(url + f"/intraday_prices/{ticker}?token={token}")
    print("TICKER " + ticker)
    intraday_json = requests.get(url + f"/intraday_prices/{ticker}?token={token}").json()
    intraday_dict = {day["minute"]: day["average"] for day in intraday_json}
    i = 0
    while intraday_dict[list(intraday_dict.keys())[i]] == None:
        i += 1
    last_val = intraday_dict[list(intraday_dict.keys())[i]]
    for key, value in intraday_dict.items():
        if(intraday_dict[key] == None):
            intraday_dict[key] = last_val
        else:
            last_val = intraday_dict[key]
    return intraday_dict
    
@app.get('/PE/{ticker}')
def get_PE(ticker):
    PE = (requests.get(url + f"/quote/{ticker}?token={token}").json())[0]["peRatio"]
    return PE #single element list with dictionary in it

@app.get('/news/{ticker}')
def get_news(ticker):
    newsList = []
    for listEntry in (requests.get(url + f"/news/{ticker}?last=10&token={token}").json()):
        dict = {}
        dict["Headline"] = listEntry["headline"]
        dict["Summary"] = listEntry["summary"]
        date = listEntry["datetime"]
        timestamp_seconds = date / 1000; # seconds since epoch
        date_time = datetime.utcfromtimestamp(timestamp_seconds)
        date_str = date_time.strftime('%Y-%m-%d')  
        dict["Date"] = date_str
        newsList.append(dict)


    return newsList #single element list with dictionary in it

@app.get('/PreviousClose/{ticker}')
def get_previousClose(ticker):
    pc = (requests.get(url + f"/quote/{ticker}?token={token}").json())[0]["previousClose"]
    return pc #returns integer

@app.get('/MarketOpen/{ticker}')
def get_marketopen(ticker):
    mo = (requests.get(url + f"/quote/{ticker}?token={token}").json())[0]["open"]
    return mo # returns integer

@app.get('/RealTimeConsolidatedVolume/{ticker}')
def get_consolidatedvolume(ticker):
    rtcv = (requests.get(url + f"/quote/{ticker}?token={token}").json())[0]["latestVolume"]
    return rtcv # Required: If you display the latestVolume value, you must display Consolidated Volume in Real-time near that value.

@app.get('/MarketCap/{ticker}')
def get_marketcap(ticker):
    mc = (requests.get(url + f"/quote/{ticker}?token={token}").json())[0]["marketCap"]
    return mc

@app.get('/DividentYield/{ticker}')
def get_dividentyield(ticker):
    dy = (requests.get(url + f"/fundamental_valuations/{ticker}?token={token}").json())[0]["dividendYield"]
    return dy #returns integer

@app.get('/AnnualReturn/{ticker}')
def get_annualreturn(ticker):
    dy = (requests.get(url + f"/advanced_stats/{ticker}?token={token}").json())[0]["year1ChangePercent"]
    return dy #returns integer

@app.put('/add_swipe/{swiped}')
def add_swipe(ticker, swiped):
    mongo_connector.add_swipe(ticker, swiped)



def compile_data(ticker):
    graph_data = get_graph(ticker)
    intraday_data = get_intraday(ticker)
    marketcap_data = get_marketcap(ticker)
    pe_data = get_PE(ticker)
    consolidatedvolume_data = get_consolidatedvolume(ticker)
    marketOpen_data = get_marketopen(ticker)
    previousClose_data = get_previousClose(ticker)
    name_data = get_companyname(ticker)
    size_data = get_companysize(ticker)
    sector_data = get_sector(ticker)
    description_data = get_description(ticker)
    dividend_data = get_dividentyield(ticker)
    annualReturn_data = get_annualreturn(ticker)
    sentiment = get_sentiment(ticker)
    data = {
        'ticker': ticker,
        'graph_data': graph_data,
        'intraday_data': intraday_data,
        'marketcap_data': marketcap_data,
        'pe_data': pe_data,
        'consolidatedvolume_data': consolidatedvolume_data,
        'marketOpen_data': marketOpen_data,
        'previousClose_data': previousClose_data,
        'name_data': name_data,
        'size_data': size_data,
        'sector_data': sector_data,
        'description_data': description_data,
        'annualReturn_data': annualReturn_data,
        'dividend_data': dividend_data
    }
    return data

#Only need these three endpoints
@app.get('/create_account/{risk_level}/{sectors}/{companyAge}/{companySize}') 
def add_account(risk_level, sectors, companyAge, companySize):
    mongo_connector.add_account(risk_level, sectors, companyAge, companySize)


@app.get('/get_next_ticker')
def get_first_ticker():
    ticker = iex_connector.cold_start(ticker_df, account_df['risk_level'].tolist()[0], account_df['sectors'].tolist()[0])
    json_data = json.dumps(compile_data(ticker))
    return json_data

@app.get('/get_next_ticker/{this_ticker}/{swiped}')
def get_next_ticker(this_ticker, swiped):
    sectors = account_df['sectors'].tolist()[0]
    risk_level = account_df['risk_level'].tolist()[0] 
    seen = set(mongo_connector.get_seen())
    if(not seen):
        return mongo_connector.cold_start(ticker_df, risk_level, sectors)
    stock = iex_connector.recommend_stocks(this_ticker, ticker_df, sectors, seen)
    add_swipe(this_ticker, swiped)
    return compile_data(stock)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)


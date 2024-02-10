from fastapi import FastAPI, HTTPException, Body, BackgroundTasks
import requests
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime


app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
    print("HIII\n\n\n\n\n")
    print(url + f"/intraday_prices/{ticker}?token={token}")

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





def predict_sentiment(): 
    # for ticker in SP_tickers: 
        # fetch all articles headline for that ticker
        # headlines = fetch_headlines(ticker)
    headlines = []
    for headline in headlines: 
        payload = { "inputs": headline }
        response = requests.post(API_URL, headers=headers, json=headline)
        response = response.json()
        
        return response.json()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)


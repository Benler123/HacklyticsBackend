from fastapi import FastAPI, HTTPException, Body, BackgroundTasks
import requests
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

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
    PE = requests.get(url + f"/PE_RATIO/{ticker}?token={token}").json()
    
    return PE

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001, debug=True)

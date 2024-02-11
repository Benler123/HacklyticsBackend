from fastapi import FastAPI, HTTPException, Body, BackgroundTasks
import requests
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import mongo_connector
import iex_connector
import portfolio
import json
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
import gpt_chatbot
import random


sector_averages = {'Manufacturing': 27.128207770965183, 'Information': 102.45399150817262, 'Utilities': 18.260429501527625, 'Finance and Insurance': 23.883056669680943, 'Administrative and Support and Waste Management and Remediation Services': 12.773875751491111, 'Retail Trade': 26.22744648757113, '': 40.36302307724007, 'Transportation and Warehousing': 23.774693737012072, 'Mining, Quarrying, and Oil and Gas Extraction': 10.798852278405514, 'Professional, Scientific, and Technical Services': 33.64500411865372, 'Accommodation and Food Services': 58.81457808263933, 'Real Estate and Rental and Leasing': 301.6988717606318, 'Wholesale Trade': 22.95699642519311, 'Public Administration': 43.94384020145358, 'Health Care and Social Assistance': 21.418444120490307, 'Construction': 17.58605288694844, 'Other Services (except Public Administration)': 17.21779153778833}

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://marketmatch.tech", "https://market-match.vercel.app", "https://www.marketmatch.tech"],
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
    return iex_connector.get_companyname(ticker)

@app.get('/CompanySize/{ticker}')
def get_companysize(ticker):
    return iex_connector.get_companysize(ticker)

@app.get('/Description/{ticker}')
def get_description(ticker):
    return iex_connector.get_description(ticker)

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
    return iex_connector.get_previousClose(ticker)

@app.get('/MarketOpen/{ticker}')
def get_marketopen(ticker):
    return iex_connector.get_marketopen(ticker)

@app.get('/RealTimeConsolidatedVolume/{ticker}')
def get_consolidatedvolume(ticker):
    return iex_connector.get_consolidatedvolume(ticker)

@app.get('/DividentYield/{ticker}')
def get_dividentyield(ticker):
    return iex_connector.get_dividentyield(ticker)

@app.get('/AnnualReturn/{ticker}')
def get_annualreturn(ticker):
    return iex_connector.get_annualreturn(ticker)

@app.put('/add_swipe/{swiped}')
def add_swipe(ticker, swiped):
    mongo_connector.add_swipe(ticker, swiped)

def compile_data(ticker):
    graph_data = get_graph(ticker)
    intraday_data = get_intraday(ticker)
    marketcap_data = ticker_df[ticker_df['ticker'] == ticker]['MarketCap'].tolist()[0]
    pe_data = ticker_df[ticker_df['ticker'] == ticker]['PE'].tolist()[0]
    consolidatedvolume_data = ticker_df[ticker_df['ticker'] == ticker]['ConsolidatedVolume'].tolist()[0]
    marketOpen_data = ticker_df[ticker_df['ticker'] == ticker]['MarketOpen'].tolist()[0]
    previousClose_data = ticker_df[ticker_df['ticker'] == ticker]['PreviousClose'].tolist()[0]
    name_data = ticker_df[ticker_df['ticker'] == ticker]['CompanyName'].tolist()[0]
    size_data = ticker_df[ticker_df['ticker'] == ticker]['CompanySize'].tolist()[0]
    sector_data = ticker_df[ticker_df['ticker'] == ticker]['Sector'].tolist()[0]
    description_data = ticker_df[ticker_df['ticker'] == ticker]['Description'].tolist()[0]
    dividend_data = ticker_df[ticker_df['ticker'] == ticker]['DividentYield'].tolist()[0]
    annualReturn_data = ticker_df[ticker_df['ticker'] == ticker]['AnnualReturn'].tolist()[0]
    sentiment_data = ticker_df[ticker_df['ticker'] == ticker]['Sentiment'].tolist()[0]
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
        'dividend_data': dividend_data,
        'sentiment': sentiment_data
    }
    return data

@app.get('/RecommendedPortfolio/{RiskProfile}/')
def get_allocation(RiskProfile):
    if RiskProfile == "low":
        desiredRisk = 0.8
        desiredReturn = 0.07
    elif RiskProfile == "medium":
        desiredRisk = 1
        desiredReturn = 0.11
    elif RiskProfile == "high":
        desiredRisk = 1.2
        desiredReturn = 0.14
    
    stockDict = portfolio.get_portfolio()
    #print(stockDict)
    #print("\n\n\n")
    sectorDict = {}
    allocDict = {}
    riskVector = []
    returnVector = []
    tickerVector = []
    A = []
    B = []
    numStocks = len(stockDict)
    for ticker, stockData in stockDict.items():
        allocDict[ticker] = 0
        tickerVector.append(ticker)
        sector = stockData["Sector"] # dictionary returning sector of stock
        if (sector in sectorDict):
            sectorDict[sector].append(ticker)
        else:
            sectorDict[sector] = [ticker, ]
        riskVector.append(stockData["Beta"])
        returnVector.append(stockData["Annual Return"])
    
    #print(sectorDict)
    #print(tickerVector)
    numSectors = len(sectorDict)
    sectorWeight = 1 / numSectors
    for sector in sectorDict:
        #print("\n\n")
        #print(sector)
        sectorVector = [0] * numStocks
        B.append(sectorWeight)
        weight = round((1 / (numSectors * len(sectorDict[sector]))), 5)
        #print(weight)
        for j in sectorDict[sector]:
            allocDict[j] = weight
    
    actualRisk = 0
    actualReturn = 0
    i = 0
    for ticker in tickerVector:
        actualRisk += allocDict[ticker] * riskVector[i]
        actualReturn += allocDict[ticker] * returnVector[i]
        i += 1
        j = 0
    iters = 0
    while ((abs(desiredRisk - actualRisk) > 0.2) or ((desiredReturn - actualReturn > 0.02))):
           iters += 1
           j += 1
           index1 = random.randrange(len(allocDict))
           index2 = random.randrange(len(allocDict))
           allocChange = random.uniform(0, 0.05)
           if (iters == 20):
               break
           if (allocDict[tickerVector[index2]] - allocChange > 0):
                allocDict[tickerVector[index1]] += allocChange
                allocDict[tickerVector[index2]] -= allocChange
                actualRisk = 0
                actualReturn = 0
                i = 0
                for ticker in tickerVector:
                        actualRisk += allocDict[ticker] * riskVector[i]
                        actualReturn += allocDict[ticker] * returnVector[i]
                        i += 1

    #print(allocDict)
    actualAlloc = {}
    totalFundsInvested = 0
    '''for tick in allocDict:
        amtInStock = round(allocDict[tick] * funds, 2)
        totalFundsInvested += amtInStock
        actualAlloc[tick] = amtInStock
        '''
       
    rd = {}
    rd["Allocation"] = allocDict
    rd["Desired risk"] = desiredRisk
    rd["Actual risk"] =  round(actualRisk, 5)
    rd["Desired return"] = desiredReturn
    rd["Actual return"] = round(actualReturn, 5)

    return(rd)


#Only need these three endpoints
@app.get('/create_account/{risk_level}/{sectors}/{companyAge}/{companySize}') 
def add_account(risk_level, sectors, companyAge, companySize):
    sector_list = sectors.replace('"', '').replace(' ', '').split(",")
    mongo_connector.add_account(risk_level, sector_list, companyAge, companySize)


@app.get('/get_next_ticker')
def get_first_ticker():
    ticker = iex_connector.cold_start(ticker_df, account_df['risk_level'].tolist()[0], account_df['sectors'].tolist())
    return compile_data(ticker)

@app.get('/get_next_ticker/{this_ticker}/{swiped}')
def get_next_ticker(this_ticker, swiped):
    add_swipe(this_ticker, swiped)
    sectors = account_df['sectors'].tolist()[0]
    risk_level = account_df['risk_level'].tolist()[0] 
    seen = set(mongo_connector.get_seen())
    if(not seen):
        return iex_connector.cold_start(ticker_df, risk_level, sectors)
    stock = iex_connector.recommend_stocks(this_ticker, ticker_df, sectors, seen)
    return compile_data(stock)

@app.get('/gpt_chat/{ticker}/{prompt}')
def get_gpt_chat(ticker, prompt):
    news = ticker_df[ticker_df['ticker'] == ticker]['headlines'].tolist()
    beta = ticker_df[ticker_df['ticker'] == ticker]['Beta'].tolist()
    pe = ticker_df[ticker_df['ticker'] == ticker]['PE'].tolist()
    sector = ticker_df[ticker_df['ticker'] == ticker]['Sector'].tolist()
    sectorPE = sector_averages[get_sector(ticker)]
    return gpt_chatbot.answer_question_ticker(ticker, prompt, news, beta, pe, sector, sectorPE)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)

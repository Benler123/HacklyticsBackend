import requests
import time
import pandas as pd
from sklearn.preprocessing import StandardScaler
from scipy.spatial.distance import euclidean
import numpy as np
import mongo_connector

sector_averages = {'Manufacturing': 27.128207770965183, 'Information': 102.45399150817262, 'Utilities': 18.260429501527625, 'Finance and Insurance': 23.883056669680943, 'Administrative and Support and Waste Management and Remediation Services': 12.773875751491111, 'Retail Trade': 26.22744648757113, '': 40.36302307724007, 'Transportation and Warehousing': 23.774693737012072, 'Mining, Quarrying, and Oil and Gas Extraction': 10.798852278405514, 'Professional, Scientific, and Technical Services': 33.64500411865372, 'Accommodation and Food Services': 58.81457808263933, 'Real Estate and Rental and Leasing': 301.6988717606318, 'Wholesale Trade': 22.95699642519311, 'Public Administration': 43.94384020145358, 'Health Care and Social Assistance': 21.418444120490307, 'Construction': 17.58605288694844, 'Other Services (except Public Administration)': 17.21779153778833}

api_token = "pk_6dcff48d8ea347d8aaafcbc3c123073e"

ticker_df = mongo_connector.return_ticker_df()

token = "pk_6dcff48d8ea347d8aaafcbc3c123073e"
url = "https://api.iex.cloud/v1/data/core"

SP_tickers =['MMM', 'AOS', 'ABT', 'ABBV', 'ACN', 'ADBE', 'AMD', 'AES', 'AFL', 'A', 'APD', 'ABNB', 'AKAM', 'ALB', 'ARE', 'ALGN', 'ALLE', 'LNT', 'ALL', 'GOOGL', 'GOOG', 'MO', 'AMZN', 'AMCR', 'AEE', 'AAL', 'AEP', 'AXP', 'AIG', 'AMT', 'AWK', 'AMP', 'AME', 'AMGN', 'APH', 'ADI', 'ANSS', 'AON', 'APA', 'AAPL', 'AMAT', 'APTV', 'ACGL', 'ADM', 'ANET', 'AJG', 'AIZ', 'T', 'ATO', 'ADSK', 'ADP', 'AZO', 'AVB', 'AVY', 'AXON', 'BKR', 'BALL', 'BAC', 'BK', 'BBWI', 'BAX', 'BDX', 'BRK.B', 'BBY', 'BIO', 'TECH', 'BIIB', 'BLK', 'BX', 'BA', 'BKNG', 'BWA', 'BXP', 'BSX', 'BMY', 'AVGO', 'BR', 'BRO', 'BF.B', 'BLDR', 'BG', 'CDNS', 'CZR', 'CPT', 'CPB', 'COF', 'CAH', 'KMX', 'CCL', 'CARR', 'CTLT', 'CAT', 'CBOE', 'CBRE', 'CDW', 'CE', 'COR', 'CNC', 'CNP', 'CF', 'CHRW', 'CRL', 'SCHW', 'CHTR', 'CVX', 'CMG', 'CB', 'CHD', 'CI', 'CINF', 'CTAS', 'CSCO', 'C', 'CFG', 'CLX', 'CME', 'CMS', 'KO', 'CTSH', 'CL', 'CMCSA', 'CMA', 'CAG', 'COP', 'ED', 'STZ', 'CEG', 'COO', 'CPRT', 'GLW', 'CTVA', 'CSGP', 'COST', 'CTRA', 'CCI', 'CSX', 'CMI', 'CVS', 'DHR', 'DRI', 'DVA', 'DAY', 'DE', 'DAL', 'XRAY', 'DVN', 'DXCM', 'FANG', 'DLR', 'DFS', 'DG', 'DLTR', 'D', 'DPZ', 'DOV', 'DOW', 'DHI', 'DTE', 'DUK', 'DD', 'EMN', 'ETN', 'EBAY', 'ECL', 'EIX', 'EW', 'EA', 'ELV', 'LLY', 'EMR', 'ENPH', 'ETR', 'EOG', 'EPAM', 'EQT', 'EFX', 'EQIX', 'EQR', 'ESS', 'EL', 'ETSY', 'EG', 'EVRG', 'ES', 'EXC', 'EXPE', 'EXPD', 'EXR', 'XOM', 'FFIV', 'FDS', 'FICO', 'FAST', 'FRT', 'FDX', 'FIS', 'FITB', 'FSLR', 'FE', 'FI', 'FLT', 'FMC', 'F', 'FTNT', 'FTV', 'FOXA', 'FOX', 'BEN', 'FCX', 'GRMN', 'IT', 'GEHC', 'GEN', 'GNRC', 'GD', 'GE', 'GIS', 'GM', 'GPC', 'GILD', 'GPN', 'GL', 'GS', 'HAL', 'HIG', 'HAS', 'HCA', 'PEAK', 'HSIC', 'HSY', 'HES', 'HPE', 'HLT', 'HOLX', 'HD', 'HON', 'HRL', 'HST', 'HWM', 'HPQ', 'HUBB', 'HUM', 'HBAN', 'HII', 'IBM', 'IEX', 'IDXX', 'ITW', 'ILMN', 'INCY', 'IR', 'PODD', 'INTC', 'ICE', 'IFF', 'IP', 'IPG', 'INTU', 'ISRG', 'IVZ', 'INVH', 'IQV', 'IRM', 'JBHT', 'JBL', 'JKHY', 'J', 'JNJ', 'JCI', 'JPM', 'JNPR', 'K', 'KVUE', 'KDP', 'KEY', 'KEYS', 'KMB', 'KIM', 'KMI', 'KLAC', 'KHC', 'KR', 'LHX', 'LH', 'LRCX', 'LW', 'LVS', 'LDOS', 'LEN', 'LIN', 'LYV', 'LKQ', 'LMT', 'L', 'LOW', 'LULU', 'LYB', 'MTB', 'MRO', 'MPC', 'MKTX', 'MAR', 'MMC', 'MLM', 'MAS', 'MA', 'MTCH', 'MKC', 'MCD', 'MCK', 'MDT', 'MRK', 'META', 'MET', 'MTD', 'MGM', 'MCHP', 'MU', 'MSFT', 'MAA', 'MRNA', 'MHK', 'MOH', 'TAP', 'MDLZ', 'MPWR', 'MNST', 'MCO', 'MS', 'MOS', 'MSI', 'MSCI', 'NDAQ', 'NTAP', 'NFLX', 'NEM', 'NWSA', 'NWS', 'NEE', 'NKE', 'NI', 'NDSN', 'NSC', 'NTRS', 'NOC', 'NCLH', 'NRG', 'NUE', 'NVDA', 'NVR', 'NXPI', 'ORLY', 'OXY', 'ODFL', 'OMC', 'ON', 'OKE', 'ORCL', 'OTIS', 'PCAR', 'PKG', 'PANW', 'PARA', 'PH', 'PAYX', 'PAYC', 'PYPL', 'PNR', 'PEP', 'PFE', 'PCG', 'PM', 'PSX', 'PNW', 'PXD', 'PNC', 'POOL', 'PPG', 'PPL', 'PFG', 'PG', 'PGR', 'PLD', 'PRU', 'PEG', 'PTC', 'PSA', 'PHM', 'QRVO', 'PWR', 'QCOM', 'DGX', 'RL', 'RJF', 'RTX', 'O', 'REG', 'REGN', 'RF', 'RSG', 'RMD', 'RVTY', 'RHI', 'ROK', 'ROL', 'ROP', 'ROST', 'RCL', 'SPGI', 'CRM', 'SBAC', 'SLB', 'STX', 'SRE', 'NOW', 'SHW', 'SPG', 'SWKS', 'SJM', 'SNA', 'SO', 'LUV', 'SWK', 'SBUX', 'STT', 'STLD', 'STE', 'SYK', 'SYF', 'SNPS', 'SYY', 'TMUS', 'TROW', 'TTWO', 'TPR', 'TRGP', 'TGT', 'TEL', 'TDY', 'TFX', 'TER', 'TSLA', 'TXN', 'TXT', 'TMO', 'TJX', 'TSCO', 'TT', 'TDG', 'TRV', 'TRMB', 'TFC', 'TYL', 'TSN', 'USB', 'UBER', 'UDR', 'ULTA', 'UNP', 'UAL', 'UPS', 'URI', 'UNH', 'UHS', 'VLO', 'VTR', 'VLTO', 'VRSN', 'VRSK', 'VZ', 'VRTX', 'VFC', 'VTRS', 'VICI', 'V', 'VMC', 'WRB', 'WAB', 'WBA', 'WMT', 'DIS', 'WBD', 'WM', 'WAT', 'WEC', 'WFC', 'WELL', 'WST', 'WDC', 'WRK', 'WY', 'WHR', 'WMB', 'WTW', 'GWW', 'WYNN', 'XEL', 'XYL', 'YUM', 'ZBRA', 'ZBH', 'ZION', 'ZTS']

SP_tickers
def get_stock_quote(ticker):
    ticker_quote_json = requests.get(f"https://api.iex.cloud/v1/data/CORE/QUOTE/{ticker}?token={api_token}").json()
    return ticker_quote_json[0]["peRatio"]

def get_sector(ticker):
    url = f"https://api.iex.cloud/v1/data-points/{ticker}/SECTOR?token={api_token}"
    response = requests.get(url)
    return response.json()

def get_advanced_stats(ticker):
    url = f"https://api.iex.cloud/v1/data/CORE/ADVANCED_STATS/{ticker}?token={api_token}"
    ticker_quote_json = requests.get(url).json()
    return ticker_quote_json[0]["peRatio"], ticker_quote_json[0]["beta"], ticker_quote_json[0]["forwardPERatio"], ticker_quote_json[0]["marketcap"]

def get_headers(ticker):
    url = f"https://api.iex.cloud/v1/data/core/news/{ticker}?last=5&token={api_token}"
    response = requests.get(url)
    return [article['headline'] for article in response.json()]

def get_companysize(ticker):
    cs = (requests.get(url + f"/company/{ticker}?token={token}").json())[0]["employees"]
    return cs

def get_description(ticker):
    cs = (requests.get(url + f"/company/{ticker}?token={token}").json())[0]["shortDescription"]
    return cs

def scale_df(df):
    scaler = StandardScaler()
    df[['Beta', 'PE', 'forwardPE', "MarketCap"]] = scaler.fit_transform(df[['Beta', 'PE', 'forwardPE', "MarketCap"]]) 

def cold_start(df, risk_levels, sectors):
    # Randomly select a stock from the given sectors
    sector_df = df[df['Sector'].isin(sectors)]
    differences = (df['PE'] - df['forwardPE']).tolist()
    sorted_indices = np.argsort(differences)[::-1]   
    return df.iloc[sorted_indices[int(risk_levels / 10.01 * len(df))]]['ticker'] 

import json
def load_sentiments(): 
    with open("sentiments.json", mode='r') as file_object:
        sentiments = json.load(file_object)
        return sentiments
    
def get_companyname(ticker):
    cn = (requests.get(url + f"/company/{ticker}?token={token}").json())[0]["companyName"]
    return cn

def get_consolidatedvolume(ticker):
    rtcv = (requests.get(url + f"/quote/{ticker}?token={token}").json())[0]["latestVolume"]
    return rtcv # Required: If you display the latestVolume value, you must display Consolidated Volume in Real-time near that value.


def get_marketopen(ticker):
    mo = (requests.get(url + f"/quote/{ticker}?token={token}").json())[0]["open"]
    return mo # returns integer

def get_previousClose(ticker):
    pc = (requests.get(url + f"/quote/{ticker}?token={token}").json())[0]["previousClose"]
    return pc #returns integer

def get_dividentyield(ticker):
    p = requests.get(url + f"/fundamental_valuations/{ticker}?token={token}").json()
    if(len(p) == 0):
        return 0
    dy = (p)[0]["dividendYield"]
    return dy #returns integer

def get_annualreturn(ticker):
    dy = (requests.get(url + f"/advanced_stats/{ticker}?token={token}").json())[0]["year1ChangePercent"]
    return dy #returns integer

# https://api.iex.cloud/v1/data/core/news/aapl?last=100&token=pk_6dcff48d8ea347d8aaafcbc3c123073e
def create_df():
    tickers = SP_tickers
    not_good = []
    PE_list = []
    Beta_list = []
    forwardPE_list = []
    sector_list = []
    marketCap_list = []
    headers_list = []
    sentiments_list = []
    companynames_list = []
    descriptions_list = []
    companysize_list = []
    consolidatedvolume_list = []
    marketopen_list = []
    previousClose_list = []
    dividentyield_list = []
    annualreturn_list = []

    count = 0
    sentiments = load_sentiments()
    for i, ticker in enumerate(tickers):
        sentiment = sentiments[i]['sentiment_score']
        pe, beta, forwardPE, marketCap = get_advanced_stats(ticker)
        time.sleep(0.2)
        if pe == None or beta == None:
            not_good.append(ticker)
        else:
            companynames_list.append(get_companyname(ticker))
            descriptions_list.append(get_description(ticker))
            time.sleep(0.2)
            companysize_list.append(get_companysize(ticker))
            consolidatedvolume_list.append(get_consolidatedvolume(ticker))
            time.sleep(0.2)
            marketopen_list.append(get_marketopen(ticker))
            previousClose_list.append(get_previousClose(ticker))
            time.sleep(0.2)
            dividentyield_list.append(get_dividentyield(ticker))
            annualreturn_list.append(get_annualreturn(ticker))
            PE_list.append(pe)
            Beta_list.append(beta)
            forwardPE_list.append(forwardPE)
            sector_list.append(get_sector(ticker))
            marketCap_list.append(marketCap)
            sentiments_list.append(sentiment)
            headers_list.append(get_headers(ticker))
        count += 1
        if count % 10 == 0:
            print(count)

    tickers = [ticker for ticker in tickers if ticker not in not_good]

    data = {
        "ticker": tickers,
        "PE": PE_list,
        "forwardPE":  forwardPE_list,
        "MarketCap": marketCap_list,
        "Beta": Beta_list,
        "Sector": sector_list,
        "Sentiment": sentiments_list,
        "Headers": headers_list,
        "CompanyName": companynames_list,
        "CompanySize": companysize_list,
        "Description": descriptions_list,
        "ConsolidatedVolume": consolidatedvolume_list,
        "MarketOpen": marketopen_list,
        "PreviousClose": previousClose_list,
        "DividentYield": dividentyield_list,
        "AnnualReturn": annualreturn_list
    }

    df = pd.DataFrame(data)
    return df

    

def recommend_stocks(stock_id, stocks_df, sectors, seen, top_n=1, sector_penalty=1, min_distance=0):
    # Extract the feature vector and sector for the chosen stock
    sector_penalty = {}
    selected_tickers = mongo_connector.get_chosen()
    for ticker in selected_tickers:
        sector_penalty[get_sector(ticker)] = sector_penalty.get(ticker, 0) + 1
    chosen_stock_features = stocks_df.loc[stocks_df['ticker'] == stock_id, ['Beta', 'PE', "forwardPE", "MarketCap"]].values[0]
    chosen_stock_sector = stocks_df.loc[stocks_df['ticker'] == stock_id, 'Sector'].values[0]
    stocks_df = stocks_df[stocks_df['Sector'].isin(sectors)]

    # Calculate the distance between the chosen stock and all others, including sector penalty
    def adjusted_distance(row):
        if(np.isnan(row['forwardPE'])):
            row['forwardPE'] = row['PE']
        # Basic Euclidean distance for Beta and PE
        distance = euclidean(chosen_stock_features, [row['Beta'], row['PE'], row['forwardPE'], row['MarketCap']])
        # Apply penalty if sectors match
        distance += sector_penalty.get(row['Sector'],0)
        return distance
    
    distances = stocks_df.apply(adjusted_distance, axis=1)
    filtered_stocks_df = stocks_df[~stocks_df['ticker'].isin(seen)]
    
    # Apply minimum distance filtering on the remaining stocks
    filtered_distances = distances[filtered_stocks_df.index]
    filtered_distances = filtered_distances[distances > min_distance]
    if(len(filtered_distances) == 0):
        return cold_start(stocks_df, 5, sectors)
    # Get the top_n closest stocks, adjusted for sector penalty
    recommended_indices = np.argsort(filtered_distances)[1]  # Exclude the first one (itself)
    recommended_stocks = stocks_df.iloc[recommended_indices]

    return recommended_stocks['ticker']

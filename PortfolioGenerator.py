import numpy as np

def allocate(funds, stockDict, desiredRisk, desiredReturn):
    sectorDict = {}
    riskVector = []
    returnVector = []
    tickerVector = []
    A = []
    B = []
    numStocks = stockDict.length
    for ticker, stockData in stockDict:
        tickerVector.append(ticker)
        sector = stockData["Sector"] # dictionary returning sector of stock
        if (sector in sectorDict):
            sectorDict[sector].append(ticker)
        else:
            sectorDict[sector] = [ticker, ]
        riskVector.append(stockData["Beta"])
        returnVector.append(stockData["Annual Return"])
    
    for sector in sectorDict:
        sectorVector = np.zeros(numStocks)
        sectorWeight = 1/sectorDict.length
        B.append(sectorWeight)
        weight = 1 / (sectorDict.length * sectorDict[sector].length) 
        for i in range (numStocks):
            if (sector == tickerVector[i]):
                sectorVector[i] = weight
        A.append(sectorVector)
    
    A.append(riskVector)
    A.append(returnVector)
    A.append(np.ones(numStocks))
    A = np.array(A)
    B.append(desiredRisk)
    B.append(desiredReturn)
    B.append(1)
    B = np.array(B)
    x = np.linalg.solve(A, B)
    print("Solution:", x)



        


# stockDict is a dictionary whose key is TICKER and its value is a dictionary containing sector, beta, annual return
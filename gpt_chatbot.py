import requests
import os


def answer_question(question, api_key=os.environ.get("OPENAI_API_KEY")):
    # print(api_key)
    prompt = "The following question is from a beginning investor looking to learn more about stocks. Please answer in one paragraph in a way that is easily understandable."

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
            "model": "gpt-3.5-turbo-0125",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt + "\n" + question
                        }
                    ]
                }
            ],
            "max_tokens": 512
        }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload).json()
    return response["choices"][0]["message"]["content"]



def answer_question_ticker(ticker, question, news, beta, pe, sector, sectorPE, api_key=os.environ.get("OPENAI_API_KEY")):
    # print(api_key)
    prompt = "The following question is from a beginning investor looking to learn more about stocks. Please answer in one paragraph in a way that is easily understandable."

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    i = 1
    newsString = ""
    for newsArticle in news:
        newsString = newsString + "\nArticle headline {i}: " + newsArticle["Headline"]
        i+=1
    
    text =  """{prompt} The ticker for the stock which prompted the question was {ticker}.
            The parameters for this stock are beta(risk factor) = {beta}, P/E ratio = {pe}, sector name = {sector}.
            The sector P/E ratio was {sectorPE} (if the question asks about PE value, explain why the stock's ratio is
            higher, lower, or on par with the sector average). Recent news headlines are {newsString}. I know you are not able 
            to provide real time data, but you can generally analyze the stock based on these provided parameters.
            Keeping this background information in mind, please answer the question: {question}""".format(prompt = prompt, 
            ticker = ticker, beta = beta, pe = pe, sector = sector, sectorPE = sectorPE, newsString = newsString, question = question)
    
    # print(text)

    payload = {
            "model": "gpt-3.5-turbo-0125",
            "messages": [
                {
                   
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": text
                            
                        }
                    ]
                }
            ],
            "max_tokens": 512
        }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload).json()
    return response["choices"][0]["message"]["content"]


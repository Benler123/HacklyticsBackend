import requests
import os


prompt = "The following question is from a beginning investor looking to learn more about stocks. Please answer in one paragraph in a way that is easily understandable."



def answer_question(question, api_key=os.environ.get("OPENAI_API_KEY")):
    # print(api_key)
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

print(answer_question("What is a good beta value"))
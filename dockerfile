FROM python:3.12

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app
COPY ./chatbot_integ /code/chatbot_integ
COPY ./iex_connector /code/iex_connector
COPY ./mongo_connector /code/mongo_connector
COPY ./gpt_chatbot /code/gpt_chatbot
COPY ./PortfolioGenerator /code/PortfolioGenerator

EXPOSE 80

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

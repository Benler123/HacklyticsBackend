FROM python:3.9

WORKDIR /app

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 80

CMD ["uvicorn", "app:app", "--host", ".0.0.0", "--port", "8001"]

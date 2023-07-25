FROM python:3.11.4

WORKDIR /app

COPY . .

RUN python -m venv venv

RUN pip install -r requirements.txt

CMD [ "python", "__main__.py" ]
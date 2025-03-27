FROM python:3.12-slim

WORKDIR /app

COPY Pipfile Pipfile.lock /app/

RUN pip install --upgrade pip && pip install pipenv && pipenv install --deploy

COPY . /app/

EXPOSE 80

CMD ["pipenv", "run", "streamlit"]

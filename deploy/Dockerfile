from python:3.8

WORKDIR /app

COPY Pipfile Pipfile.lock /app/
RUN pip install pipenv==2018.11.26 && pipenv install --system --deploy

COPY ./src /app/src/

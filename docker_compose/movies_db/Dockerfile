FROM python:3.10-alpine

WORKDIR /usr/src/movies_db

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --no-cache-dir --upgrade pip
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/movies_db/entrypoint.sh
RUN chmod +x /usr/src/movies_db/entrypoint.sh

COPY . .

ENTRYPOINT ["/usr/src/movies_db/entrypoint.sh"]
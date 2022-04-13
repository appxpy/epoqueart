FROM python:3.9.10-alpine

WORKDIR /usr/src/epoqueart

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add --update  gcc python3-dev jpeg-dev zlib-dev musl-dev postgresql-dev build-base openjdk17 libstdc++ nodejs npm

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/epoqueart/entrypoint.sh
RUN chmod +x /usr/src/epoqueart/entrypoint.sh

RUN npm install -g postcss-cli autoprefixer

RUN chmod +x /usr/src/epoqueart/entrypoint.sh

COPY . .



ENTRYPOINT ["/usr/src/epoqueart/entrypoint.sh"]
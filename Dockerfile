FROM python:3.13.7

RUN apt-get update && apt-get install -qq -y --no-install-recommends

ENV INSTALL_PATH=/poke_api

RUN mkdir "$INSTALL_PATH"

WORKDIR $INSTALL_PATH

COPY . .

RUN pip install -r requirements.txt

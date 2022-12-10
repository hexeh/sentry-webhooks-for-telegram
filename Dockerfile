FROM python:3.11

WORKDIR /app

ADD requirements.txt /app

RUN python3 -m pip install -r /app/requirements.txt

ADD app /app/app
#ADD libs /app/libs

ENV CMD_ARGS="--factory app:create_web_app --host 0.0.0.0 --port 9901 --workers 4 --loop asyncio"

EXPOSE 9901
CMD uvicorn $CMD_ARGS
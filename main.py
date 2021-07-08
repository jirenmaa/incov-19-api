from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from aggregator import (
    aggregate_9news,
    aggregate_medicalnewstoday,
    aggregate_msn,
    websites,
)

app = FastAPI()
origins = [
    "http://localhost:3000", # local
    "https://incov-19.netlify.app/", # main website
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/medicalnewstoday")
def fetch_from_medicalnewstoday():
    try:
        datas = aggregate_medicalnewstoday(websites.get("medicalnewstoday"))

        payload = {"data": datas}
        return ORJSONResponse(content=payload)
    except Exception as ex:
        return ORJSONResponse(
            {"msg": str(ex.args)}, status_code=status.HTTP_400_BAD_REQUEST
        )


@app.get("/msn")
def fetch_from_msn():
    try:
        datas = aggregate_msn(websites.get("msn"))

        payload = {"data": datas}
        return ORJSONResponse(content=payload)
    except Exception as ex:
        return ORJSONResponse(
            {"msg": str(ex.args)}, status_code=status.HTTP_400_BAD_REQUEST
        )


@app.get("/9news")
def fetch_from_9news():
    try:
        datas = aggregate_9news(websites.get("9news"))

        payload = {"data": datas}
        return ORJSONResponse(content=payload)
    except Exception as ex:
        return ORJSONResponse(
            {"msg": str(ex.args)}, status_code=status.HTTP_400_BAD_REQUEST
        )

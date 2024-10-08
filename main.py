from typing import Union
from fastapi import FastAPI, Query
from typing import List
from pydantic import BaseModel
from database import database, engine
from racket import recommend_racket
from match import user_match_analysis
from personal_analysis import personal_analysis
import warnings
warnings.filterwarnings(action='ignore')

# FastAPI 앱 생성
app = FastAPI()

# 앱이 시작될 때 PostgreSQL 연결
@app.on_event("startup")
async def startup():
    await database.connect()

# 앱이 종료될 때 PostgreSQL 연결 해제
@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()

import pandas as pd
### 이건 맨 처음에 FastAPI 연습해본다고 넣어둔거에요. 지워도 됨
async def get():
    # query = "SELECT * FROM racket WHERE racket_id = 3"
    # data = await database.fetch_all(query)
    # print(list(data[0]['color'].split(',')))
    racket_id =[i for i in range(1, 5)]
    where_sql = f"SELECT * FROM racket WHERE racket_id = {racket_id[0]}"
    for r in racket_id[1:]:
        where_sql += f" OR racket_id = {r}"
    data = await database.fetch_all(where_sql)
    return data
 

@app.get("/rackets/")
#async def root():
async def read_racket():
    return await get()

@app.get("/rackets/{balance}/{weight}/{price}/{shaft}/")
async def show_racket_recommend(balance:str, weight:str, price:int, shaft:str, racket_id: List[int] = Query(None)):
    if racket_id is None:
        racket_id = []
    return await recommend_racket(balance, weight, price, shaft, racket_id)

@app.get("/{user_id}/")
async def show_personal_analysis(user_id:int):
    return await personal_analysis(user_id)
    
@app.get("/{user_id}/{match_id}/")
async def read_set(user_id:int, match_id:int):
    return await user_match_analysis(user_id, match_id)
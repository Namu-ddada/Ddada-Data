from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from database import database, engine
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
async def get():
    query = "SELECT * FROM racket"
    data = await database.fetch_all(query)
    dict_rows = [dict(row) for row in data]
    df = pd.DataFrame(dict_rows)
    print(df)
    return data
 

@app.get("/rackets/")
#async def root():
async def read_racket():
    return await get()

@app.get("/{user_id}/")
async def show_personal_analysis(user_id:int):
    return await personal_analysis(user_id)
    
@app.get("/{user}/{match_id}/")
async def read_set(user:int, match_id:int):
    return await user_match_analysis(user, match_id)

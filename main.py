from typing import Union
from fastapi import FastAPI, Query
from typing import List
from pydantic import BaseModel
from database import database, engine
import models
from racket import recommend_racket
from show_match_analysis import user_match_analysis
from save_match_analysis import upload_match_analysis
from personal_analysis import personal_analysis
import warnings
warnings.filterwarnings(action='ignore')

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import SessionLocal, engine, sync_engine

# 데이터베이스 테이블 생성
models.Base.metadata.create_all(bind=sync_engine)

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
    
# 데이터베이스 세션 의존성 주입
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
async def get_db():
    async with SessionLocal() as session:
        yield session


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

@app.post("/add_match_analysis/{user_id}/{match_id}/")
async def add_match_analysis(user_id:int, match_id:int, db: AsyncSession = Depends(get_db)):
    return await upload_match_analysis(user_id, match_id, db)
    
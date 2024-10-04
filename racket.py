import pandas as pd
from sqlalchemy import select
from database import database, engine  # 이미 설정한 database 객체 가져오기
from sqlalchemy import MetaData, Table
from fastapi import FastAPI
import asyncio

app = FastAPI()

# 테이블 메타데이터 설정
metadata = MetaData()


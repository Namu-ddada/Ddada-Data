from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from databases import Database
from config import DATABASE_URL

# 데이터베이스 URL 설정

# SQLAlchemy 데이터베이스 엔진 생성
engine = create_async_engine(DATABASE_URL, pool_size=10, max_overflow=20)

# 세션을 관리하는 세션 메이커
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base 클래스 생성 (metadata를 포함)
Base = declarative_base()

# metadata 생성 (테이블 구조를 반영)
metadata = Base.metadata


# 비동기 데이터베이스 연결을 위한 databases 라이브러리 설정
database = Database(DATABASE_URL)
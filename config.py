import os
from dotenv import load_dotenv

# .env 파일을 로드하여 환경 변수로 설정
load_dotenv()

# 환경 변수 불러오기
DATABASE_URL = os.getenv("DATABASE_URL")
SYNC_DATABASE_URL = os.getenv("SYNC_DATABASE_URL")
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
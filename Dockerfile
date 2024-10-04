FROM python:3.9.13

# 작업 디렉토리 설정
WORKDIR /Data

# 필요 패키지 설치
COPY ./requirements.txt /Data/
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY ./Data /Data/

# 환경 변수 설정
ENV PYTHONUNBUFFERED 1

# Django 설정 파일의 경로와 서버 실행
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0"]
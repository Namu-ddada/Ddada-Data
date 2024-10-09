from sqlalchemy import Column, Integer, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# 이미 존재하는 테이블을 위한 최소한의 모델 정의
class Match(Base):
    __tablename__ = "match"
    match_id = Column(Integer, primary_key=True, autoincrement=True)

class Player(Base):
    __tablename__ = "player"
    player_id = Column(Integer, primary_key=True, autoincrement=True)

# 매치 분석 테이블 정의
class MatchAnalysis(Base):
    __tablename__ = "match_analysis"
    
    # 1. 기본 키
    analysis_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # 2. 득점율, 실점율
    mean_score_rate = Column(Float, nullable=False)
    my_score_rate = Column(Float, nullable=False)
    mean_lose_rate = Column(Float, nullable=False)
    my_lose_rate = Column(Float, nullable=False)
    
    # 3. 스킬 다양성
    score_middle_smash = Column(Float, nullable=False)
    score_middle_serve = Column(Float, nullable=False)
    score_middle_net = Column(Float, nullable=False)
    score_middle_pushs = Column(Float, nullable=False)
    score_middle_drops = Column(Float, nullable=False)
    score_middle_clears = Column(Float, nullable=False)
    score_my_smash = Column(Float, nullable=False)
    score_my_serve = Column(Float, nullable=False)
    score_my_net = Column(Float, nullable=False)
    score_my_pushs = Column(Float, nullable=False)
    score_my_drops = Column(Float, nullable=False)
    score_my_clears = Column(Float, nullable=False)
    score_my_smash_text = Column(Text, nullable=False)
    score_my_serve_text = Column(Text, nullable=False)
    score_my_net_text = Column(Text, nullable=False)
    score_my_pushs_text = Column(Text, nullable=False)
    score_my_drops_text = Column(Text, nullable=False)
    score_my_clears_text = Column(Text, nullable=False)
    score_my_message = Column(Text, nullable=False)
    lose_middle_smash = Column(Float, nullable=False)
    lose_middle_serve = Column(Float, nullable=False)
    lose_middle_net = Column(Float, nullable=False)
    lose_middle_pushs = Column(Float, nullable=False)
    lose_middle_drops = Column(Float, nullable=False)
    lose_middle_clears = Column(Float, nullable=False)
    lose_my_smash = Column(Float, nullable=False)
    lose_my_serve = Column(Float, nullable=False)
    lose_my_net = Column(Float, nullable=False)
    lose_my_pushs = Column(Float, nullable=False)
    lose_my_drops = Column(Float, nullable=False)
    lose_my_clears = Column(Float, nullable=False)
    lose_my_smash_text = Column(Text, nullable=False)
    lose_my_serve_text = Column(Text, nullable=False)
    lose_my_net_text = Column(Text, nullable=False)
    lose_my_pushs_text = Column(Text, nullable=False)
    lose_my_drops_text = Column(Text, nullable=False)
    lose_my_clears_text = Column(Text, nullable=False)
    lose_my_message = Column(Text, nullable=False)
    
    # 4. 전략
    loser1_num = Column(Integer, nullable=False)
    loser1_worst = Column(Text)
    loser1_bad = Column(Text)
    loser1_soso = Column(Text)
    loser1_good = Column(Text)
    loser1_best = Column(Text)
    loser1_I_did_worst = Column(Float, nullable=False)
    loser1_I_did_bad = Column(Float, nullable=False)
    loser1_I_did_soso = Column(Float, nullable=False)
    loser1_I_did_good = Column(Float, nullable=False)
    loser1_I_did_best = Column(Float, nullable=False)
    loser1_message = Column(Text, nullable=False)
    loser1_number = Column(Float, nullable=False)
    
    loser2_num = Column(Integer)
    loser2_worst = Column(Text)
    loser2_bad = Column(Text)
    loser2_soso = Column(Text)
    loser2_good = Column(Text)
    loser2_best = Column(Text)
    loser2_I_did_worst = Column(Float)
    loser2_I_did_bad = Column(Float)
    loser2_I_did_soso = Column(Float)
    loser2_I_did_good = Column(Float)
    loser2_I_did_best = Column(Float)
    loser2_message = Column(Text)
    loser2_number = Column(Float, nullable=False)
    
    # 5. 멘탈
    mental1_mean = Column(Float, nullable=False)
    mental1_user = Column(Float, nullable=False)
    mental1_message = Column(Text, nullable=False)
    mental2_mean = Column(Float, nullable=False)
    mental2_user = Column(Float, nullable=False)
    mental2_message = Column(Text, nullable=False)
    mental3_mean_score = Column(Float, nullable=False)
    mental3_user_score = Column(Float, nullable=False)
    mental3_mean_lose = Column(Float, nullable=False)
    mental3_user_lose = Column(Float, nullable=False)
    mental3_message = Column(Text, nullable=False)
    
    # FK
    match_id = Column(Integer, ForeignKey("match.match_id"), nullable=True)
    player_id = Column(Integer, ForeignKey("player.player_id"), nullable=True)

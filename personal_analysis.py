from typing import Union
from database import database

async def personal_analysis(user_id):
    query = f"""SELECT * FROM match_analysis 
                WHERE player_id = {user_id};"""
    data = await database.fetch_all(query)
    
    
    result = {
        "match": 3,
        "rate":{
                "score_rate": 70,
                "lose_rate": 10,
                "skills": 30,
                "strategy": 60,
                "recovery": 30
                },
                "type": "공격적 플레이어",
                "type_message": "득점에 집중하고 빠르게 반격하는 공격형 스타일"
        }
    return result
from typing import Union
from database import database

import pandas as pd
async def get():
    player = 9
    query = f"""SELECT m.match_id
            FROM match m
            JOIN team t1 ON m.team1_id = t1.team_id
            JOIN team t2 ON m.team2_id = t2.team_id
            WHERE (t1.player1_id = {player} OR t1.player2_id = {player})
            OR (t2.player1_id = {player} OR t2.player2_id = {player});"""
    data = await database.fetch_all(query)
    return data


# query = f"""SELECT s.*
#                 FROM score s
#                 JOIN set st ON s.set_id = st.set_id
#                 JOIN match m ON st.match_id = m.match_id
#                 JOIN team t1 ON m.team1_id = t1.team_id
#                 JOIN team t2 ON m.team2_id = t2.team_id
#                 WHERE (t1.player1_id = {user_id} OR t1.player2_id = {user_id})
#                 OR (t2.player1_id = {user_id} OR t2.player2_id = {user_id});"""

async def personal_analysis(user_id):
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
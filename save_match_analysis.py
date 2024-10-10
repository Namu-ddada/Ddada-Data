from database import database
from analysis.flow import flow
from analysis.make_dataframe import change_df
from analysis.score_lose_rate import checking_number2
from analysis.skill import checking_number3
from analysis.strategy import checking_number4
from analysis.mental import checking_number5
import models


import pandas as pd
import numpy as np

def safe_convert(value):
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return float(value)
    return value

async def upload_match_analysis(match_id, db):
    # 원본 데이터
    query = "SELECT * FROM score s JOIN set se ON s.set_id = se.set_id"
    data = await database.fetch_all(query)
    dict_rows = [dict(row) for row in data]
    match_df = change_df(pd.DataFrame(dict_rows))
    # player
    query = """SELECT t.player1_id, t.player2_id
            FROM team t
            JOIN match m
            ON (t.team_id = m.team1_id OR t.team_id = m.team2_id)
            WHERE m.match_id = :match_id"""
    data = await database.fetch_all(query, values={"match_id": match_id})
    player = []
    for i in data:
        for _, v in dict(i).items():
            player.append(v)
    
    result = []
    
                
    for user_id in player:
        # 기존 데이터가 있는지 없는지
        exist_query = """SELECT EXISTS (
                        SELECT 1
                        FROM match_analysis
                        WHERE match_id = :match_id
                        AND player_id = :user_id);"""
        data = await database.fetch_all(exist_query, values={"match_id": match_id, 'user_id': user_id})
        
        if data:
            result.append({"status": "already exists", "data": f"{match_id} 경기의 {user_id} 선수 분석 결과가 이미 존재합니다."})
        else:
            # 유저 데이터
            query = f"""SELECT s.*,
                            CASE 
                                WHEN t1.player1_id = :user_id THEN 11
                                WHEN t1.player2_id = :user_id THEN 12
                                WHEN t2.player1_id = :user_id THEN 21
                                WHEN t2.player2_id = :user_id THEN 22
                                ELSE 0
                            END AS match_condition
                        FROM score s
                        JOIN set st ON s.set_id = st.set_id
                        JOIN match m ON st.match_id = m.match_id
                        JOIN team t1 ON m.team1_id = t1.team_id
                        JOIN team t2 ON m.team2_id = t2.team_id
                        WHERE m.match_id = :match_id
                        AND (
                            (t1.player1_id = :user_id OR t1.player2_id = :user_id)
                            OR (t2.player1_id = :user_id OR t2.player2_id = :user_id)
                        );
                        """
            data = await database.fetch_all(query, values={"match_id": match_id, 'user_id': user_id})
            user = data[0]['match_condition']
            dict_rows = [dict(row) for row in data]
            df = change_df(pd.DataFrame(dict_rows))
            
            ## 2. 득점율, 실점율
            print("2. 득점율, 실점율")
            score_lose_rate =checking_number2(df, user)

            ## 3. 기술력
            print("3. 기술력")
            skill = checking_number3(match_df, df, user)
            
            ## 4. 전략
            print("4. 전략")
            ##################################시간되면 기여도 여기에 추가하기
            strategy = checking_number4(match_df, df, user)

            ## 5. 집중력
            print("5. 집중력")
            mental = checking_number5(match_df, df, user)
            
            
            # match_analysis 테이블에 데이터 삽입
            new_analysis = models.MatchAnalysis(
                # 2. 득점율, 실점율
                mean_score_rate = score_lose_rate['mean_score_rate'],
                my_score_rate = score_lose_rate['my_score_rate'],
                mean_lose_rate = score_lose_rate['mean_lose_rate'],
                my_lose_rate = score_lose_rate['my_lose_rate'],
                
                # 3. 스킬 다양성
                score_middle_smash = skill['score']['middle_skill_rate']['smash'],
                score_middle_serve = skill['score']['middle_skill_rate']['serve'],
                score_middle_net = skill['score']['middle_skill_rate']['net'],
                score_middle_pushs = skill['score']['middle_skill_rate']['pushs'],
                score_middle_drops = skill['score']['middle_skill_rate']['drops'],
                score_middle_clears = skill['score']['middle_skill_rate']['clears'],
                score_my_smash = skill['score']['skill_rate']['smash'],
                score_my_serve = skill['score']['skill_rate']['serve'],
                score_my_net = skill['score']['skill_rate']['net'],
                score_my_pushs = skill['score']['skill_rate']['pushs'],
                score_my_drops = skill['score']['skill_rate']['drops'],
                score_my_clears = skill['score']['skill_rate']['clears'],
                score_my_smash_text = skill['score']['skill_rate_text']['smash'],
                score_my_serve_text = skill['score']['skill_rate_text']['serve'],
                score_my_net_text = skill['score']['skill_rate_text']['net'],
                score_my_pushs_text = skill['score']['skill_rate_text']['pushs'],
                score_my_drops_text = skill['score']['skill_rate_text']['drops'],
                score_my_clears_text = skill['score']['skill_rate_text']['clears'],
                score_my_message = skill['score']['message'],
                lose_middle_smash = skill['lose']['middle_lose_skill_rate']['smash'],
                lose_middle_serve = skill['lose']['middle_lose_skill_rate']['serve'],
                lose_middle_net = skill['lose']['middle_lose_skill_rate']['net'],
                lose_middle_pushs = skill['lose']['middle_lose_skill_rate']['pushs'],
                lose_middle_drops = skill['lose']['middle_lose_skill_rate']['drops'],
                lose_middle_clears = skill['lose']['middle_lose_skill_rate']['clears'],
                lose_my_smash = skill['lose']['lose_skill_rate']['smash'],
                lose_my_serve = skill['lose']['lose_skill_rate']['serve'],
                lose_my_net = skill['lose']['lose_skill_rate']['net'],
                lose_my_pushs = skill['lose']['lose_skill_rate']['pushs'],
                lose_my_drops = skill['lose']['lose_skill_rate']['drops'],
                lose_my_clears = skill['lose']['lose_skill_rate']['clears'],
                lose_my_smash_text = skill['lose']['lose_skill_rate_text']['smash'],
                lose_my_serve_text = skill['lose']['lose_skill_rate_text']['serve'],
                lose_my_net_text = skill['lose']['lose_skill_rate_text']['net'],
                lose_my_pushs_text = skill['lose']['lose_skill_rate_text']['pushs'],
                lose_my_drops_text = skill['lose']['lose_skill_rate_text']['drops'],
                lose_my_clears_text = skill['lose']['lose_skill_rate_text']['clears'],
                lose_my_message = skill['lose']['message'],
                
                # 4. 전략
                loser1_num = strategy[0]['loser'],
                loser1_worst = ','.join(strategy[0]['lose_skill'][0]),
                loser1_bad = ','.join(strategy[0]['lose_skill'][1]),
                loser1_soso = ','.join(strategy[0]['lose_skill'][2]),
                loser1_good = ','.join(strategy[0]['lose_skill'][3]),
                loser1_best = ','.join(strategy[0]['lose_skill'][4]),
                loser1_I_did_worst = strategy[0]['I_did'][0],
                loser1_I_did_bad = strategy[0]['I_did'][1],
                loser1_I_did_soso = strategy[0]['I_did'][2],
                loser1_I_did_good = strategy[0]['I_did'][3],
                loser1_I_did_best = strategy[0]['I_did'][4],
                loser1_message = strategy[0]['message'],
                loser1_number = strategy[0]['number'],
                
                loser2_num = strategy[1]['loser'],
                loser2_worst = ','.join(strategy[1]['lose_skill'][0]),
                loser2_bad = ','.join(strategy[1]['lose_skill'][1]),
                loser2_soso = ','.join(strategy[1]['lose_skill'][2]),
                loser2_good = ','.join(strategy[1]['lose_skill'][3]),
                loser2_best = ','.join(strategy[1]['lose_skill'][4]),
                loser2_I_did_worst = strategy[1]['I_did'][0],
                loser2_I_did_bad = strategy[1]['I_did'][1],
                loser2_I_did_soso = strategy[1]['I_did'][2],
                loser2_I_did_good = strategy[1]['I_did'][3],
                loser2_I_did_best = strategy[1]['I_did'][4],
                loser2_message = strategy[1]['message'],
                loser2_number = strategy[1]['number'],
                
                # 5. 멘탈
                mental1_mean = mental[0]['mean_speed'],
                mental1_user = mental[0]['user_speed'],
                mental1_message = mental[0]['message'],
                mental2_mean = mental[1]['mean_speed'],
                mental2_user = mental[1]['user_speed'],
                mental2_message = mental[1]['message'],
                mental3_mean_score = mental[2]['mean_speed'][0],
                mental3_user_score = mental[2]['user_speed'][0],
                mental3_mean_lose = mental[2]['mean_speed'][1],
                mental3_user_lose = mental[2]['user_speed'][1],
                mental3_message = mental[2]['message'],
                
                # FK
                match_id = match_id,
                player_id = user_id
            )

            db.add(new_analysis)
            await db.commit()
            await db.refresh(new_analysis)
        
            result.append({"status": "success", "data": f"{match_id} 경기의 {user_id} 선수 분석 결과가 업로드 되었습니다."})
    return result
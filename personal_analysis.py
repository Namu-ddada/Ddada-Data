from typing import Union
from database import database
import pandas as pd
import numpy as np
from total_analysis import generate

async def personal_analysis(user_id):
    query = """SELECT mean_score_rate, mean_lose_rate
                FROM match_analysis"""
    data = await database.fetch_all(query)
    dict_rows = [dict(row) for row in data]
    all_df = pd.DataFrame(dict_rows)
    
    query = f"""SELECT my_score_rate, my_lose_rate,
                score_my_smash_text, score_my_serve_text, score_my_net_text, score_my_pushs_text, score_my_drops_text, score_my_clears_text, 
                lose_my_smash_text, lose_my_serve_text, lose_my_net_text, lose_my_pushs_text, lose_my_drops_text, lose_my_clears_text,
                loser1_number, loser2_number, mental1_mean, mental1_user, mental2_mean, mental2_user, mental3_mean_score, mental3_user_score, mental3_mean_lose, mental3_user_lose
                FROM match_analysis 
                WHERE player_id = :user_id;"""
    data = await database.fetch_all(query, values={'user_id': user_id})
    dict_rows = [dict(row) for row in data]
    df = pd.DataFrame(dict_rows)
    
    
    # 득점율, 실점율
    my_score = (np.mean(df['my_score_rate'])/np.mean(all_df['mean_score_rate'])*0.5)*100
    my_lose = (np.mean(df['my_lose_rate'])/np.mean(all_df['mean_lose_rate'])*0.5)*100
    
    # 기술력
    skill = ['smash', 'serve', 'net', 'pushs', 'drops', 'clears']
    score_skill = [0, 0, 0, 0, 0, 0]
    lose_skill = [0, 0, 0, 0, 0, 0]
    # 전략력
    strategy_number = [0, 0]
    cnt = [0, 0]
    # 멘탈
    mental = [[],[],[]]
    
    for i in range(len(df)):
        ## 기술력
        for sk in range(len(skill)):
            me_score = df[f'score_my_{skill[sk]}_text'][i]
            me_lose = df[f'lose_my_{skill[sk]}_text'][i]
            if me_score == "매우 우수":
                score_skill[sk] += 1
            elif me_score == "우수":
                score_skill[sk] += 0.7
            elif me_score == "평균":
                score_skill[sk] += 0.5
            elif me_score == "약간 부족":
                score_skill[sk] += 0.3
            elif me_score == "매우 부족":
                score_skill[sk] += 0.1
            
            if me_lose == "매우 우수":
                lose_skill[sk] += 1
            elif me_lose == "우수":
                lose_skill[sk] += 0.7
            elif me_lose == "평균":
                lose_skill[sk] += 0.5
            elif me_lose == "약간 부족":
                lose_skill[sk] += 0.3
            elif me_lose == "매우 부족":
                lose_skill[sk] += 0.1

        ## 전략력
        if df['loser1_number'][i] != 0:
            strategy_number[0] += df['loser1_number']
            cnt[0] += 1
        if df['loser2_number'][i] != 0:
            strategy_number[1] += df['loser2_number']
            cnt[1] += 1
            
        ## 멘탈
        for number in range(1, 3):
            if df[f'mental{number}_mean'][i] < df[f'mental{number}_user'][i]:
                mental[number-1].append(1)
            elif df[f'mental{number}_mean'][i] > df[f'mental{number}_user'][i]:
                mental[number-1].append(0)
            else:
                mental[number-1].append(0.5)
        for sl in ['score','lose']:
            if df[f'mental3_mean_{sl}'][i] < df[f'mental3_user_{sl}'][i]:
                mental[number-1].append(1)
            elif df[f'mental3_mean_{sl}'][i] > df[f'mental3_user_{sl}'][i]:
                mental[number-1].append(0)
            else:
                mental[number-1].append(0.5)
        
    my_skill = round((np.mean(score_skill) + np.mean(lose_skill)) / 2 *100)
    my_strategy = round(((np.mean(strategy_number[0]) / cnt[0]) + (np.mean(strategy_number[1]) / cnt[1])) / 2 * 100)
    
    my_mental = 0
    for m in mental:
        if len(m) == 0:
            m.append(0)
        my_mental += np.mean(m)
    my_mental = round(my_mental / 3 * 100)
    
    gemini = generate(my_score, my_lose, my_skill, my_strategy, my_mental)
    print(gemini)
    
    
    result = {
        "match": len(df),
        "rate":{
                "score_rate": my_score,
                "lose_rate": my_lose,
                "skills": my_skill,
                "strategy": my_strategy,
                "recovery": my_mental
                },
                "type": gemini.split(': ')[1].split(',')[0],
                "type_message": gemini.split(': ')[2].split('}')[0]
        }
    return result
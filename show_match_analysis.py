from database import database
from analysis.flow import flow
from analysis.make_dataframe import change_df
from analysis.score_lose_rate import checking_number2
from analysis.skill import checking_number3
from analysis.strategy import checking_number4
from analysis.mental import checking_number5


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

async def user_match_analysis(user_id, match_id):
    # 분석 데이터
    query = f"SELECT * FROM match_analysis WHERE match_id = {match_id} AND player_id = {user_id};"
    analysis_data = await database.fetch_all(query)
    
    # 유저 데이터
    query = f"""SELECT s.*,
                    CASE 
                        WHEN t1.player1_id = {user_id} THEN 11
                        WHEN t1.player2_id = {user_id} THEN 12
                        WHEN t2.player1_id = {user_id} THEN 21
                        WHEN t2.player2_id = {user_id} THEN 22
                        ELSE 0
                    END AS match_condition
                FROM score s
                JOIN set st ON s.set_id = st.set_id
                JOIN match m ON st.match_id = m.match_id
                JOIN team t1 ON m.team1_id = t1.team_id
                JOIN team t2 ON m.team2_id = t2.team_id
                WHERE m.match_id = {match_id}
                AND (
                    (t1.player1_id = {user_id} OR t1.player2_id = {user_id})
                    OR (t2.player1_id = {user_id} OR t2.player2_id = {user_id})
                );
                """
    data = await database.fetch_all(query)
    user = data[0]['match_condition']
    dict_rows = [dict(row) for row in data]
    df = change_df(pd.DataFrame(dict_rows))
    
    
    set_info=[]
    for set_number in df.set_id.unique():
        imsi_df = df.query(f"set_id == {set_number}")
        set_info_dict = {
            "set_number":safe_convert(set_number),
            "earned_player": safe_convert(list(imsi_df['earned_player'])),
            "missed_player1": safe_convert(list(imsi_df['missed_player1'])),
            "missed_player2": safe_convert(list(imsi_df['missed_player2'])),
            "earned_type": safe_convert(list(imsi_df['earned_type'])),
            "score1":safe_convert(list(imsi_df['score1'])),
            "score2":safe_convert(list(imsi_df['score2'])),
          }
        set_info.append(set_info_dict)
        
        
        
    if len(df)//4 > len(df.loc[df[f'{user}_flow'] != 0]):
        print("기여도가 너무 적어 분석이 정확하지 않을 수 있어요.") 
        print(f"기여도: {len(df)} 중 {len(df.loc[df[f'{user}_flow'] != 0])}번의 기록으로 {len(df.loc[df[f'{user}_flow'] != 0]) / len(df) * 100}%에 불과해요.")
        
    result = {}

    ## 1. 흐름에 따른 성향 태그
    print("1. 흐름 시각화")
    flow_ = flow(df, user)
    
    ## 2. 득점율, 실점율
    print("2. 득점율, 실점율")
    score_lose_rate = {
        'mean_score_rate': analysis_data[0]['mean_score_rate'],
        'my_score_rate': analysis_data[0]['my_score_rate'],
        'mean_lose_rate': analysis_data[0]['mean_lose_rate'],
        'my_lose_rate': analysis_data[0]['my_lose_rate']
    }

    ## 3. 기술력
    print("3. 기술력")
    score_my_skill = {}
    score_my_skill_text = {}
    lose_my_skill = {}
    lose_my_skill_text = {}
    for sk in ['smash','serve','net','pushs','drops','clears']:
        if analysis_data[0][f'score_my_{sk}'] != 0:
            score_my_skill[sk] = analysis_data[0][f'score_my_{sk}']
        if analysis_data[0][f'score_my_{sk}_text'] != "알수없음":
            score_my_skill_text[sk] = analysis_data[0][f'score_my_{sk}_text']
        if analysis_data[0][f'lose_my_{sk}'] != 0:
            lose_my_skill[sk] = analysis_data[0][f'lose_my_{sk}']
        if analysis_data[0][f'lose_my_{sk}_text'] != "알수없음":
            lose_my_skill_text[sk] = analysis_data[0][f'lose_my_{sk}_text']
    skill = {
        'score': {
            'middle_skill_rate': {
                'smash': analysis_data[0]['score_middle_smash'],
                'serve': analysis_data[0]['score_middle_serve'],
                'net': analysis_data[0]['score_middle_net'],
                'pushs': analysis_data[0]['score_middle_pushs'],
                'drops': analysis_data[0]['score_middle_drops'],
                'clears': analysis_data[0]['score_middle_clears']
            },
            'skill_rate': score_my_skill,
            'skill_rate_text': score_my_skill_text,
            'message': analysis_data[0]['score_my_message']
        },
        'lose': {
            'middle_lose_skill_rate': {
                'smash': analysis_data[0]['lose_middle_smash'],
                'serve': analysis_data[0]['lose_middle_serve'],
                'net': analysis_data[0]['lose_middle_net'],
                'pushs': analysis_data[0]['lose_middle_pushs'],
                'drops': analysis_data[0]['lose_middle_drops'],
                'clears': analysis_data[0]['lose_middle_clears']
            },
            'lose_skill_rate': lose_my_skill,
            'lose_skill_rate_text': lose_my_skill_text,
            'message': analysis_data[0]['lose_my_message']
        }
    }
    
    ## 4. 전략
    print("4. 전략")
    strategy_list = []
    for i in range(1, 3):
        if analysis_data[0][f'loser{i}_num'] != 0:
            strategy_list.append(
                {
                    'loser': analysis_data[0][f'loser{i}_num'],
                    'lose_skill': [
                        list(analysis_data[0][f'loser{i}_worst'].split(',')),
                        list(analysis_data[0][f'loser{i}_bad'].split(',')),
                        list(analysis_data[0][f'loser{i}_soso'].split(',')),
                        list(analysis_data[0][f'loser{i}_good'].split(',')),
                        list(analysis_data[0][f'loser{i}_best'].split(','))
                    ],
                    'I_did': [
                        analysis_data[0][f'loser{i}_I_did_worst'],
                        analysis_data[0][f'loser{i}_I_did_bad'],
                        analysis_data[0][f'loser{i}_I_did_soso'],
                        analysis_data[0][f'loser{i}_I_did_good'],
                        analysis_data[0][f'loser{i}_I_did_best']
                    ],
                    'message': analysis_data[0][f'loser{i}_message']
                }
            )
    strategy = strategy_list

    ## 5. 집중력
    print("5. 집중력")
    mental = [
        {
            'type': "접전 상황 집중력",
            "explanation": "접전 상황에서의 득점 수로 긴박한 상황에서의 집중력을 확인할 수 있는 지표에요.",
            "mean_speed": analysis_data[0]['mental1_mean'],
            "user_speed": analysis_data[0]['mental1_user'],
            "message": analysis_data[0]['mental1_message']
        },
        {
            'type': "회복 속도",
            "explanation": "연속 실점 후 다시 득점을 하기까지 얼마나 걸렸는지 확인할 수 있는 지표에요.",
            "mean_speed": analysis_data[0]['mental2_mean'],
            "user_speed": analysis_data[0]['mental2_user'],
            "message": analysis_data[0]['mental2_message']
        },
        {
            'type': "클러치 상황 득점율/실점율",
            "explanation": "경기를 결정짓는 후반부의 클러치 상황에서 얼마나 경기를 주도할 수 있는지 확인할 수 있는 지표에요.",
            "mean_speed": [analysis_data[0]['mental3_mean_score'], analysis_data[0]['mental3_mean_lose']],
            "user_speed": [analysis_data[0]['mental3_user_score'], analysis_data[0]['mental3_user_lose']],
            "message": analysis_data[0]['mental3_message']
        }
    ]
    
    result = {
        "set_info":set_info,
        'flow':flow_,
        'score_lose_rate':score_lose_rate,
        'skill':skill,
        'strategy':strategy,
        'mental': mental
    }
    return result
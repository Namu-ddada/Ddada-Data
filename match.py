from database import database
from analysis.flow import flow
from analysis.make_dataframe import change_df
from analysis.score_lose_rate import checking_number2
from analysis.skill import checking_number3
from analysis.strategy import checking_number4
from analysis.mental import mental_1, mental_2


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
    # 원본 데이터
    query = "SELECT * FROM score s JOIN set se ON s.set_id = se.set_id"
    data = await database.fetch_all(query)
    dict_rows = [dict(row) for row in data]
    match_df = change_df(pd.DataFrame(dict_rows))
    
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
    for set in df.set_id.unique():
        print(mental_1(df.query(f"set_id == {set}").reset_index(drop=True)))
        print(mental_2(df.query(f"set_id == {set}").reset_index(drop=True)))
    
    result = {
        "set_info":set_info,
        'flow':flow_,
        'score_lose_rate':score_lose_rate,
        'skill':skill,
        'strategy':strategy   
    }
    return result
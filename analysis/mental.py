import pandas as pd
import numpy as np
from analysis.score_lose_rate import score_lose

## 집중력 1
# 10점 이상인 경우, 1점이나 2점 차이일 대 득점하는 수
def mental_1(df):
    df['score_diff'] = abs(df['score1'] - df['score2'])
    check10 = df.query('score1 >= 10 or score2 >= 10').reset_index(drop=True)
    
    cnt_11, cnt_12, cnt_21, cnt_22 = [], [], [], []
    i = 0
    
    while i < len(check10):
        flag = True
        if check10['score_diff'][i] <= 3:
            if check10['11_flow'][i+1] > 0:
                while check10['11_flow'][i+1] > 0:
                    cnt_11.append(check10['11_flow'][i+1])
                    i += 1
                    flag = False
                if flag:
                    i += 1
                else:
                    pass
            elif check10['12_flow'][i+1] > 0:
                while check10['12_flow'][i+1] > 0:
                    cnt_12.append(check10['12_flow'][i+1])
                    i += 1
                    flag = False
                if flag:
                    i += 1
                else:
                    pass
            elif check10['21_flow'][i+1] > 0:
                while check10['21_flow'][i+1] > 0:
                    cnt_21.append(check10['21_flow'][i+1])
                    i += 1
                    flag = False
                if flag:
                    i += 1
                else:
                    pass
            elif check10['22_flow'][i+1] > 0:
                while check10['22_flow'][i+1] > 0:
                    cnt_22.append(check10['22_flow'][i+1])
                    i += 1
                    flag = False
                if flag:
                    i += 1
                else:
                    pass
            else:
                i += 1
        else:
            i += 1
    for ii in [cnt_11, cnt_12, cnt_21, cnt_22]:
        if not ii:
            ii.append(0)
    return [np.mean(cnt_11), np.mean(cnt_12), np.mean(cnt_21), np.mean(cnt_22)]


## 집중력 2
# 회복력 - 2점 이상 연속 실점한 후 다시 득점하는데까지 걸린 수
def mental_2(df):
    cnt_11, cnt_12, cnt_21, cnt_22 = [], [], [], []
    for player, l in zip([11, 12, 21, 22], [cnt_11, cnt_12, cnt_21, cnt_22]):
        lst =list(df[f'{player}_flow'])
        i = 0
        while i < len(lst):
            flag = True
            cnt = 0
            if lst[i] <= -2:
                i += 1
                while lst[i] <= 0:
                    if flag:
                        if lst[i] < 0:
                            i +=1
                        else:
                            flag = False
                            cnt += 1
                            i += 1
                    else:
                        cnt += 1
                        i += 1
                        
                    if i >= len(lst):
                        break
                i += 1
            else:
                i+= 1
            if cnt > 0:
                l.append(cnt)
    for ii in [cnt_11, cnt_12, cnt_21, cnt_22]:
        if not ii:
            ii.append(0)
    return [np.mean(cnt_11), np.mean(cnt_12), np.mean(cnt_21), np.mean(cnt_22)]

## 집중력 3
# 마지막 6점에 대한 득점율과 실점율 계산
def mental_3(df):
    if df.iloc[-1, :]['score1'] > df.iloc[-1, :]['score2']:
        num = df.iloc[-1, :]['score1'] - 6
    else:
        num = df.iloc[-1, :]['score2'] - 6
    mean_score_rate, mean_lose_rate, s_r, l_r, _ = score_lose(df.query(f'(score1 >= {num}) or (score2 >= {num})'))
    result = {
        'score':s_r,
        'lose': l_r
    }
    return result

# 전체 데이터에 대해 집중력 계산
def total_mental(match_df):
    m1, m2, m3_score, m3_lose = [[], [], [], []], [[], [], [], []], [[], [], [], []], [[], [], [], []]
    for set in match_df.set_id.unique():
        result1 = mental_1(match_df.query(f"set_id == {set}").reset_index(drop=True))
        for i in range(4):
            m1[i].append(result1[i])
        result2 = mental_2(match_df.query(f"set_id == {set}").reset_index(drop=True))
        for i in range(4):
            m2[i].append(result2[i])
        result3 = mental_3(match_df.query(f"set_id == {set}").reset_index(drop=True))
        for i in range(4):
            m3_score[i].append(result3['score'][i])
            m3_lose[i].append(result3['lose'][i])
    for i in range(4):
        m1[i] = np.mean(m1[i])
        m2[i] = np.mean(m2[i])
        m3_score[i] = np.mean(m3_score[i])
        m3_lose[i] = np.mean(m3_lose[i])
    result = [np.mean(m1), np.mean(m2), np.mean(m3_score), np.mean(m3_lose)]
    return result

def checking_number5(match_df, df, user):
    user_dict = {11:0, 12:1, 21:2, 22:3}
    idx = user_dict[user]
    m1, m2, m3_score, m3_lose = [[], [], [], []], [[], [], [], []], [[], [], [], []], [[], [], [], []]
    for set in df.set_id.unique():
        result1 = mental_1(df.query(f"set_id == {set}").reset_index(drop=True))
        for i in range(4):
            m1[i].append(result1[i])
        result2 = mental_2(df.query(f"set_id == {set}").reset_index(drop=True))
        for i in range(4):
            m2[i].append(result2[i])
        result3 = mental_3(df.query(f"set_id == {set}").reset_index(drop=True))
        for i in range(4):
            m3_score[i].append(result3['score'][i])
            m3_lose[i].append(result3['lose'][i])
    for i in range(4):
        m1[i] = np.mean(m1[i])
        m2[i] = np.mean(m2[i])
        m3_score[i] = np.mean(m3_score[i])
        m3_lose[i] = np.mean(m3_lose[i])
    
    user_mental = [m1[idx], m2[idx], m3_score[idx], m3_lose[idx]]
    all_mental = total_mental(match_df)
    
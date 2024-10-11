import pandas as pd
import numpy as np

# 득점율, 실점율
def score_lose(df):
    if df.iloc[-1, :]['score1'] > df.iloc[-1, :]['score2']:
        winner = 1
    else:
        winner = 2
            
    player_lst = [11, 12, 21, 22]
    # 득점
    score_point = []
    for player in player_lst:
        score_point.append(len(df.loc[df[f'{player}_flow'] > 0]))
    score_rate = list(map(lambda x: round(x/len(df), 2), score_point))

    # 실점
    lose_point = []
    for player in player_lst:
        lose_point.append(len(df.loc[df[f'{player}_flow'] < 0]))
    lose_rate = list(map(lambda x: round(x/len(df), 2), lose_point))
        
    mean_score_rate, mean_lose_rate = round(np.mean(score_rate), 2), round(np.mean(lose_rate), 2)

    return mean_score_rate, mean_lose_rate, score_rate, lose_rate, winner


#### 2. 득점율, 실점율 정리 함수
def checking_number2(df, user):
    user_dict = {11:0, 12:1, 21:2, 22:3}
    mean_score_rate, mean_lose_rate, score_rate, lose_rate, winner = [], [], [[], [], [], []], [[], [], [], []], []
    for set in df.set_id.unique():
        s, l, s_r, l_r, w = score_lose(df.query(f"set_id == {set}").reset_index(drop=True))
        mean_score_rate.append(s)
        mean_lose_rate.append(l)
        for i in range(4):
            score_rate[i].append(s_r[i])
            lose_rate[i].append(l_r[i])
        winner.append(w)
    mean_score_rate.sort()
    if len(mean_score_rate)%2 == 0:
        idx = len(mean_score_rate) // 2
        msr = (mean_score_rate[idx-1] + mean_score_rate[idx])/2
    else:
        idx = len(mean_score_rate) // 2
        msr = mean_score_rate[idx]
    mean_lose_rate.sort()
    if len(mean_lose_rate)%2 == 0:
        idx = len(mean_lose_rate) // 2
        mlr = (mean_lose_rate[idx-1] + mean_lose_rate[idx])/2
    else:
        idx = len(mean_lose_rate) // 2
        mlr = mean_lose_rate[idx]
    sr = [np.mean(score_rate[0]), np.mean(score_rate[1]), np.mean(score_rate[2]), np.mean(score_rate[3])]
    lr = [np.mean(lose_rate[0]), np.mean(lose_rate[1]), np.mean(lose_rate[2]), np.mean(lose_rate[3])]
    result = {
        "mean_score_rate": msr, "my_score_rate": sr[user_dict[user]],
        "mean_lose_rate": mlr, "my_lose_rate": lr[user_dict[user]]
        }
    return result
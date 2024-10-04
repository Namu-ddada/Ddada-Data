import pandas as pd
import numpy as np
from .skill import lose_people_skill, total_lose_skill, my_lose_skill

# 전략
# match_df는 전체 데이터, df는 현재 경기 데이터(set 상관없이 전부)
def strategy(df, user, match_df):
    result = []
    imsi_df = df.loc[df['earned_player']==user]
    lose_list = list(imsi_df.missed_player1.unique()) + list(imsi_df.missed_player2.unique())
    lose_list = list(pd.unique(lose_list))
    try:
        lose_list.remove(0)
    except ValueError:
        pass
    score_df = df.loc[df['earned_player']==user]
    for lose in lose_list:
        lose_dict = my_lose_skill(match_df, lose, *total_lose_skill(match_df, lose_people_skill(match_df), lose))
        worst, bad, middle, better, best = [], [], [], [], []
        for k, v in lose_dict['lose_skill_rate_text'].items():
            if v == "매우 부족":
                worst.append(k)
            elif v == "약간 부족":
                bad.append(k)
            elif v == "평균":
                middle.append(k)
            elif v == "우수":
                better.append(k)
            else:
                best.append(k)
        cl = score_df.query(f'missed_player1 == {lose} or missed_player2 == {lose}').groupby(['earned_type'])[[f'{lose}_flow']].count()
        calculate_lose = round(cl/cl.sum()[f'{lose}_flow'], 2).reset_index().sort_values(by=f'{lose}_flow', ascending=False)
        
        for k, v, in {"SMASH":"smash", "DROP":"drops", "SERVE":"serve", "CLEAR":"clears","PUSH":"pushs", "HAIRPIN":"net"}.items():
            calculate_lose.loc[calculate_lose['earned_type']==k, "earned_type"] = v
        
        b1, b2, m, g2, g1 = 0, 0, 0, 0, 0
        for k, v in zip(list(calculate_lose['earned_type']), list(calculate_lose[f'{lose}_flow'])):
            if (k in worst):
                b1 += v
            elif (k in bad):
                b2 += v
            elif (k in better):
                g2 += v
            elif (k in best):
                g1 += v
            else:
                m += v
        
        result.append({"loser":lose, "lose_skill":[worst, bad, middle, better, best], "I_did":[b1, b2, m, g2, g1]}) 

    return result

def safe_convert(value):
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return float(value)
    return value


def checking_number4(df, user, match_df):
    strategy_list = strategy(df, user, match_df)

    converted_result = [
        {
            'loser': safe_convert(item['loser']),
            'lose_skill': [safe_convert(skill) for skill in item['lose_skill']],
            'I_did': [safe_convert(i_did) for i_did in item['I_did']],
            'message': "상대가 상대적으로 취약한 드롭과 스매시에 대해 너무 적은 득점율을 보였어요. 상대를 조금 더 분석해서 취약한 기술이 어떤 것인지 고민해보세요."
        }
        for item in strategy_list
    ]

    return converted_result
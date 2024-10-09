import pandas as pd
import numpy as np
from .skill import lose_people_skill, total_lose_skill, my_lose_skill

# 전략
# match_df는 전체 데이터, df는 현재 경기 데이터(set 상관없이 전부)
def strategy(match_df, df, user):
    result = []
    imsi_df = df.loc[df['earned_player']==user]
    lose_list = list(imsi_df.missed_player1.unique()) + list(imsi_df.missed_player2.unique())
    lose_list = list(pd.unique(lose_list))
    try:
        lose_list.remove(0)
    except ValueError:
        pass
    score_df = df.loc[df['earned_player']==user]
    if len(lose_list) != 0:
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
        if len(lose_list) == 1:
            result.append({"loser":0, "lose_skill":[[], [], [], [], []], "I_did":[[], [], [], [], []]})
    else:
        result = [
                {"loser":0, "lose_skill":[[], [], [], [], []], "I_did":[[], [], [], [], []]},
                {"loser":0, "lose_skill":[[], [], [], [], []], "I_did":[[], [], [], [], []]}
                ]
    return result

def safe_convert(value):
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return float(value)
    return value


#### 4. 전략 정리 함수
def checking_number4(match_df, df, user):
    strategy_list = strategy(match_df, df, user)
    for strategy_dict in strategy_list:
        if strategy_dict['loser'] == 0:
            strategy_dict['message'] = ""
        else:
            bad_num = len(strategy_dict['lose_skill'][0])+len(strategy_dict['lose_skill'][1])
            soso_num = len(strategy_dict['lose_skill'][2])
            good_num = len(strategy_dict['lose_skill'][3])+len(strategy_dict['lose_skill'][4])
            all = bad_num
            if soso_num == 6:
                strategy_dict['message'] = "상대가 상대적으로 취약한 기술이 없었어요."
            elif bad_num == 6:
                strategy_dict['message'] = "상대가 모든 기술에 취약한 선수였어요."
            elif good_num == 6:
                strategy_dict['message'] = "상대가 모든 기술에 우수한 선수였음에도 득점을 이끌어냈어요.😎🍀"
            elif soso_num + good_num == 6:
                strategy_dict['message'] = "상대가 모든 기술에 대해 평균 이상의 실력을 지닌 선수였음에도 득점을 이끌어내는 성과를 보였어요.👍"
            else:
                if (0.15 * bad_num) <= (strategy_dict['I_did'][0] + strategy_dict['I_did'][1]) <= (0.17 * bad_num):
                    strategy_dict['message'] = "상대의 취약점을 적절히 공략하여 균형 잡힌 공격을 펼쳤어요! 상대의 약점을 적절하게 활용하면서 다양한 기술을 섞어 사용한 점이 인상적입니다. 앞으로도 상황에 맞는 유연한 전술로 경기를 이끌어가세요!"
                elif (0.17 * bad_num) < (strategy_dict['I_did'][0] + strategy_dict['I_did'][1]):
                    strategy_dict['message'] = "상대의 취약점을 날카롭게 파고든 전략적인 플레이를 보여주었어요! 상대를 세심히 분석하여 취약한 부분을 집중적으로 공략하는 모습이 인상적입니다. 다음 경기에서도 상대를 분석하면서 득점율을 더욱 높일 수 있을 것이라 기대됩니다."
                elif (strategy_dict['I_did'][0] + strategy_dict['I_did'][1]) < (0.15 * bad_num):
                    strategy_dict['message'] = "상대의 취약점을 공략할 기회를 놓친 경향이 있습니다. 다양한 기술을 사용한 점은 좋지만, 상대의 약점을 조금 더 세심히 분석하여 공략하는 전략이 필요할 것 같아요. 다음 경기에서는 상대의 약점을 더 잘 파악해 공략하는 데 집중해보세요!"

    converted_result = [
        {
            'loser': safe_convert(item['loser']),
            'lose_skill': [safe_convert(skill) for skill in item['lose_skill']],
            'I_did': [safe_convert(i_did) for i_did in item['I_did']],
            'message': item['message']
        }
        for item in strategy_list
    ]

    return converted_result
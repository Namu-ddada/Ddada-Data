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
            if (len(check10) > i+1) and (check10['11_flow'][i+1] > 0):
                while (len(check10) > i+1) and (check10['11_flow'][i+1] > 0):
                    cnt_11.append(check10['11_flow'][i+1])
                    i += 1
                    flag = False
                if flag:
                    i += 1
                else:
                    pass
            elif (len(check10) > i+1) and (check10['12_flow'][i+1] > 0):
                while (len(check10) > i+1) and (check10['12_flow'][i+1] > 0):
                    cnt_12.append(check10['12_flow'][i+1])
                    i += 1
                    flag = False
                if flag:
                    i += 1
                else:
                    pass
            elif (len(check10) > i+1) and (check10['21_flow'][i+1] > 0):
                while (len(check10) > i+1) and (check10['21_flow'][i+1] > 0):
                    cnt_21.append(check10['21_flow'][i+1])
                    i += 1
                    flag = False
                if flag:
                    i += 1
                else:
                    pass
            elif (len(check10) > i+1) and (check10['22_flow'][i+1] > 0):
                while (len(check10) > i+1) and (check10['22_flow'][i+1] > 0):
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
                while (len(lst) > i) and (lst[i] <= 0):
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
    result = [round(np.mean(m1), 2), round(np.mean(m2), 2), round(np.mean(m3_score), 2), round(np.mean(m3_lose), 2)]
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
    # mental1
    mental1 = {
        'type': '접전 상황 집중력',
        'explanation': '접전 상황에서의 득점 수로 긴박한 상황에서의 집중력을 확인할 수 있는 지표에요.',
        'mean_speed': all_mental[0],
        'user_speed': user_mental[0]
    }
    if user_mental[0] > all_mental[0]:
        mental1['message'] = "접전 상황에서도 뛰어난 집중력을 발휘하며 중요한 순간에 경기를 주도하였습니다. 박빙의 순간에서 빛나는 집중력이 돋보였으며, 앞으로도 이러한 집중력을 유지하여 더 많은 득점을 이끌어보세요!"
    elif user_mental[0] < all_mental[0]:
        mental1['message'] = "접전 상황에서 집중력이 다소 떨어져 중요한 순간에 득점을 이어나가지 못하는 경향이 있습니다. 이러한 순간에 더 침착하게 경기를 풀어나갈 수 있도록 심리적인 안정과 전술적인 대비가 필요합니다. 다음 경기에서는 중요한 순간에 집중력을 유지해 더 많은 득점을 노려보세요!"
    else:
        mental1['message'] = "접전 상황에서 평균적인 집중력을 유지하며 경기를 풀어나갔습니다. 안정적인 경기 운영이 돋보였지만, 조금 더 집중력을 높여 결정적인 순간에 경기를 주도할 수 있는 기회를 늘려보세요!"
    
    # mental2
    mental2 = {
        'type': '회복 속도',
        'explanation': '연속 실점 후 다시 득점을 하기까지 얼마나 걸렸는지 확인할 수 있는 지표에요.',
        'mean_speed': all_mental[1],
        'user_speed': user_mental[1]
    }
    if user_mental[1] > all_mental[1]:
        mental2['message'] = "연속 실점 후 회복하는 데 다소 시간이 걸렸습니다. 경기 중 집중력을 잃지 않고 더 빨리 회복할 수 있도록, 실점 후의 심리적 안정과 대응 전략을 강화해보세요. 다음 경기에서는 더 빠른 회복을 통해 경기 흐름을 주도해보세요!"
    elif user_mental[1] < all_mental[1]:
        mental2['message'] = "연속 실점 후 빠르게 회복하며 멋진 대응을 보여주었습니다! 경기 흐름을 빠르게 되찾는 능력이 뛰어나며, 앞으로도 빠른 회복 속도로 더 많은 득점을 이끌어보세요!"
    else:
        mental2['message'] = "평균적인 회복 속도를 보여주었어요. 상대의 흐름에 휘둘리지 않고 잘 대응했지만, 조금 더 빠른 회복을 목표로 하여 경기 주도권을 확실히 가져올 수 있도록 노력해보세요!"
    
    # mental3
    mental3 = {
        'type': '클러치 상황 득점율/실점율',
        'explanation': '경기를 결정짓는 후반부의 클러치 상황에서 얼마나 경기를 주도할 수 있는지 확인할 수 있는 지표에요.',
        'mean_speed': [all_mental[2],all_mental[3]],
        'user_speed': [user_mental[2],user_mental[3]]
    }
    if user_mental[2] > all_mental[2]:
        if user_mental[3] > all_mental[3]:
            mental3['message'] = "클러치 상황에서 득점력은 뛰어나지만, 실점이 많아 안정적인 경기 운영이 어려웠습니다. 중요한 순간에 공격은 잘 이끌어갔지만, 수비에서도 더 집중력을 유지해 실점을 줄여보세요. 공격과 수비의 균형이 맞춰진다면 더 완벽한 경기를 보여줄 수 있을 거에요!"
        elif user_mental[3] < all_mental[3]:
            mental3['message'] = "클러치 상황에서 득점과 수비 모두 탁월했습니다. 중요한 순간에 집중력을 발휘해 경기를 완벽하게 지배했으며, 상대에게 거의 틈을 주지 않는 안정적인 경기 운영이 인상적입니다. 앞으로도 이러한 경기력을 유지해 나가세요!"
        else:
            mental3['message'] = "클러치 상황에서 높은 득점력을 보여주었고, 실점율도 평균 수준으로 잘 방어했습니다. 중요한 순간에 경기 흐름을 잘 이끌어가는 모습이 돋보였으며, 수비를 조금만 더 강화한다면 더욱 완벽한 경기를 펼칠 수 있을 거에요!"
    elif user_mental[2] < all_mental[2]:
        if user_mental[3] > all_mental[3]:
            mental3['message'] = "클러치 상황에서 득점력이 부족하고 실점율이 높아 중요한 순간에 경기를 주도하지 못했습니다. 공격과 수비 모두에서 개선이 필요하며, 집중력을 키워 중요한 순간에 더 나은 결과를 만들어내도록 노력해보세요!"
        elif user_mental[3] < all_mental[3]:
            mental3['message'] = "클러치 상황에서 득점력과 실점율 모두 낮았습니다. 수비는 안정적이지만, 중요한 순간에 득점을 이끌어내는 데 어려움을 겪고 있습니다. 공격적인 전략을 보완해 득점력을 높여보세요!"
        else:
            mental3['message'] = "클러치 상황에서 득점력이 부족한 경향이 있으며, 실점율은 평균 수준입니다. 중요한 순간에 득점을 이끌어내는 능력을 조금 더 키워 경기 흐름을 유리하게 가져가 보세요!"
    else:
        if user_mental[3] > all_mental[3]:
            mental3['message'] = "클러치 상황에서 평균적인 득점력을 보였지만, 실점율이 높아 중요한 순간에 수비에 어려움을 겪었습니다. 수비에 더 많은 집중을 기울여 실점을 줄여보세요!"
        elif user_mental[3] < all_mental[3]:
            mental3['message'] = "클러치 상황에서 득점은 평균적이었으나, 실점율이 낮아 수비력이 빛났습니다. 안정적인 경기 운영을 바탕으로 득점력을 조금만 더 강화하여 득점을 이끌어보세요!"
        else:
            mental3['message'] = "클러치 상황에서 득점과 실점 모두 평균적인 모습을 보여주었습니다. 중요한 순간에 실점을 줄이면서 득점을 더 많이 이끌어내는 전략을 세운다면, 경기에서 더욱 유리한 흐름을 가져갈 수 있을 거에요!"
    
    result = [mental1, mental2, mental3]
    return result
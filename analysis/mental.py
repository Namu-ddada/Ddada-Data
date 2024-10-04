import pandas as pd

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
    return cnt_11, cnt_12, cnt_21, cnt_22


## 집중력 2
# 회복력
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

    return cnt_11, cnt_12, cnt_21, cnt_22

## 집중력 3 추가 필요해요.
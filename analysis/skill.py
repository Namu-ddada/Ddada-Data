import pandas as pd
# 득점 기술력
def people_skill(match_df):
    smash, serve, net, pushs, drops, clears = [], [], [], [], [], []
    skill_list = ['SMASH','SERVE','HAIRPIN','PUSH','DROP','CLEAR']
    for people in [11, 12, 21, 22]:
        for match in match_df.match_id.unique():
            df = match_df.query(f'match_id == {match} and earned_player == {people}').reset_index(drop=True)
            new = df.groupby(['earned_type'])[['match_id']].count().reset_index()
            for s in skill_list:
                if s not in list(new['earned_type']):
                    if s == "SMASH":
                        smash.append(0)
                    elif s == "SERVE":
                        serve.append(0)
                    elif s == "HAIRPIN":
                        net.append(0)
                    elif s == "PUSH":
                        pushs.append(0)
                    elif s == "DROP":
                        drops.append(0)
                    elif s == "CLEAR":
                        clears.append(0)

            for i in range(len(new)):
                doing = new['earned_type'][i]
                if doing == "SMASH":
                    smash.append(new['match_id'][i])
                elif doing == "SERVE":
                    serve.append(new['match_id'][i])
                elif doing == "HAIRPIN":
                    net.append(new['match_id'][i])
                elif doing == "PUSH":
                    pushs.append(new['match_id'][i])
                elif doing == "DROP":
                    drops.append(new['match_id'][i])
                elif doing == "CLEAR":
                    clears.append(new['match_id'][i])
                        
    people_skill = pd.DataFrame({'smash':smash,'serve':serve,'net':net,'push':pushs,'drop':drops, 'clear':clears})
    people_skill['cnt'] = people_skill['smash'] + people_skill['serve'] + people_skill['net'] + people_skill['push'] + people_skill['drop'] + people_skill['clear']
    return people_skill

def total_skill(df, people_skill, user):
    smash, serve, net, pushs, drops, clears = [], [], [], [], [], []
    df = df.loc[df['earned_player'] == user].reset_index(drop=True)
    for i in range(len(people_skill)):
        people_skill.iloc[i,:] = people_skill.iloc[i,:] / (people_skill['cnt'][i]/len(df))
    min_quat = dict(people_skill.quantile(0.75) - ((people_skill.quantile(0.75)-people_skill.quantile(0.25))*(1.5)))
    quat1 = dict(people_skill.quantile(0.25))
    quat2 = dict(people_skill.quantile(0.5))
    quat3 = dict(people_skill.quantile(0.75))
    max_quat = dict(people_skill.quantile(0.25) + ((people_skill.quantile(0.75)-people_skill.quantile(0.25))*(1.5)))
    for d in [min_quat, quat1, quat2, quat3, max_quat]:
        for k, v in d.items():
            if k == "smash":
                smash.append(v)
            elif k == "serve":
                serve.append(v)
            elif k == "net":
                net.append(v)
            elif k == "push":
                pushs.append(v)
            elif k == "drop":
                drops.append(v)
            elif k == "clear":
                clears.append(v)
    return smash, serve, net, pushs, drops, clears

def my_skill(df, user, smash, serve, net, pushs, drops, clears):
    df = df.loc[df['earned_player'] == user].reset_index(drop=True)        
    df = df.groupby(['earned_type'])['earned_player'].count().reset_index()
    
    skill_rate = {}
    message = {}
    for i in range(len(df)):
        if df['earned_type'][i] == "SMASH":
            skill_rate['smash'] = df['earned_player'][i]
            if (df['earned_player'][i] < smash[0]):
                message['smash'] = "매우 부족"
            elif (df['earned_player'][i] < smash[1]):
                message['smash'] = "약간 부족"
            elif (df['earned_player'][i] < smash[2]):
                message['smash'] = "평균"
            elif (df['earned_player'][i] < smash[3]):
                message['smash'] = "우수"
            else:
                message['smash'] = "매우 우수"
        elif df['earned_type'][i] == "SERVE":
            skill_rate['serve'] = df['earned_player'][i]
            if (df['earned_player'][i] < serve[0]):
                message['serve'] = "매우 부족"
            elif (df['earned_player'][i] < serve[1]):
                message['serve'] = "약간 부족"
            elif (df['earned_player'][i] < serve[2]):
                message['serve'] = "평균"
            elif (df['earned_player'][i] < serve[3]):
                message['serve'] = "우수"
            else:
                message['serve'] = "매우 우수"
        elif df['earned_type'][i] == "HAIRPIN":
            skill_rate['net'] = df['earned_player'][i]
            if (df['earned_player'][i] < net[0]):
                message['net'] = "매우 부족"
            elif (df['earned_player'][i] < net[1]):
                message['net'] = "약간 부족"
            elif (df['earned_player'][i] < net[2]):
                message['net'] = "평균"
            elif (df['earned_player'][i] < net[3]):
                message['net'] = "우수"
            else:
                message['net'] = "매우 우수"
        elif df['earned_type'][i] == "PUSH":
            skill_rate['pushs'] = df['earned_player'][i]
            if (df['earned_player'][i] < pushs[0]):
                message['pushs'] = "매우 부족"
            elif (df['earned_player'][i] < pushs[1]):
                message['pushs'] = "약간 부족"
            elif (df['earned_player'][i] < pushs[2]):
                message['pushs'] = "평균"
            elif (df['earned_player'][i] < pushs[3]):
                message['pushs'] = "우수"
            else:
                message['pushs'] = "매우 우수"
        elif df['earned_type'][i] == "DROP":
            skill_rate['drops'] = df['earned_player'][i]
            if (df['earned_player'][i] < drops[0]):
                message['drops'] = "매우 부족"
            elif (df['earned_player'][i] < drops[1]):
                message['drops'] = "약간 부족"
            elif (df['earned_player'][i] < drops[2]):
                message['drops'] = "평균"
            elif (df['earned_player'][i] < drops[3]):
                message['drops'] = "우수"
            else:
                message['drops'] = "매우 우수"
        elif df['earned_type'][i] == "CLEAR":
            skill_rate['clears'] = df['earned_player'][i]
            if (df['earned_player'][i] < clears[0]):
                message['clears'] = "매우 부족"
            elif (df['earned_player'][i] < clears[1]):
                message['clears'] = "약간 부족"
            elif (df['earned_player'][i] < clears[2]):
                message['clears'] = "평균"
            elif (df['earned_player'][i] < clears[3]):
                message['clears'] = "우수"
            else:
                message['clears'] = "매우 우수"
        else:
            print(df['earned_type'][i], "너는 뭐니?")
            
    
    skill_rate_value = list(map(lambda x: round(x/sum(list(skill_rate.values())), 2)*100, list(skill_rate.values())))
    result = {
            "middle_skill_rate": {'smash':smash[2], 'serve':serve[2], 'net':net[2], 'pushs':pushs[2], 'drops':drops[2], 'clears':clears[2]},
            "skill_rate" : dict(zip(skill_rate.keys(), skill_rate_value)),
            "skill_rate_text" : message
            }
    return result

# 실점 기술력
def lose_people_skill(match_df):
    smash, serve, net, pushs, drops, clears, miss = [], [], [], [], [], [], []
    skill_list = ['SMASH','SERVE','HAIRPIN','PUSH','DROP','CLEAR','SERVE_MISS']
    for people in [11, 12, 21, 22]:
        for match in match_df.match_id.unique():
            df = match_df.query(f'match_id == {match}').query(f'missed_player1 == {people} or missed_player2 == {people}').reset_index(drop=True)
            df.loc[df['earned_type'].isna(), 'earned_type'] = 'SERVE_MISS'
            new = df.groupby(['earned_type'])[['match_id']].count().reset_index()
            for s in skill_list:
                if s not in list(new['earned_type']):
                    if s == "SMASH":
                        smash.append(0)
                    elif s == "SERVE":
                        serve.append(0)
                    elif s == "HAIRPIN":
                        net.append(0)
                    elif s == "PUSH":
                        pushs.append(0)
                    elif s == "DROP":
                        drops.append(0)
                    elif s == "CLEAR":
                        clears.append(0)
                    else:
                        miss.append(0)

            for i in range(len(new)):
                doing = new['earned_type'][i]
                if doing == "SMASH":
                    smash.append(new['match_id'][i])
                elif doing == "SERVE":
                    serve.append(new['match_id'][i])
                elif doing == "HAIRPIN":
                    net.append(new['match_id'][i])
                elif doing == "PUSH":
                    pushs.append(new['match_id'][i])
                elif doing == "DROP":
                    drops.append(new['match_id'][i])
                elif doing == "CLEAR":
                    clears.append(new['match_id'][i])
                else:
                    miss.append(new['match_id'][i])

    lose_people_skill = pd.DataFrame({'smash':smash,'serve':serve,'net':net,'push':pushs,'drop':drops, 'clear':clears, 'miss':miss})
    lose_people_skill['cnt'] = lose_people_skill['smash'] + lose_people_skill['serve'] + lose_people_skill['net'] + lose_people_skill['push'] + lose_people_skill['drop'] + lose_people_skill['clear'] + lose_people_skill['miss']
    return lose_people_skill

def total_lose_skill(df, lose_people_skill, user):
    smash, serve, net, pushs, drops, clears, miss = [], [], [], [], [], [], []
    df = df.query(f'missed_player1 == {user} or missed_player2 == {user}').reset_index(drop=True)
    for i in range(len(lose_people_skill)):
        lose_people_skill.iloc[i,:] = lose_people_skill.iloc[i,:] / (lose_people_skill['cnt'][i]/len(df))
    min_quat = dict(lose_people_skill.quantile(0.75) - ((lose_people_skill.quantile(0.75)-lose_people_skill.quantile(0.25))*(1.5)))
    quat1 = dict(lose_people_skill.quantile(0.25))
    quat2 = dict(lose_people_skill.quantile(0.5))
    quat3 = dict(lose_people_skill.quantile(0.75))
    max_quat = dict(lose_people_skill.quantile(0.25) + ((lose_people_skill.quantile(0.75)-lose_people_skill.quantile(0.25))*(1.5)))
    for d in [min_quat, quat1, quat2, quat3, max_quat]:
        for k, v in d.items():
            if k == "smash":
                smash.append(v)
            elif k == "serve":
                serve.append(v)
            elif k == "net":
                net.append(v)
            elif k == "push":
                pushs.append(v)
            elif k == "drop":
                drops.append(v)
            elif k == "clear":
                clears.append(v)
            else:
                miss.append(v)
    return smash, serve, net, pushs, drops, clears, miss

def my_lose_skill(df, user, smash, serve, net, pushs, drops, clears, miss):
    df = df.query(f'missed_player1 == {user} or missed_player2 == {user}').reset_index(drop=True)
    df = df.groupby(['earned_type'])['earned_player'].count().reset_index()
    skill_rate = {}
    message = {}
    for i in range(len(df)):
        if df['earned_type'][i] == "SMASH":
            skill_rate['smash'] = df['earned_player'][i]
            if (df['earned_player'][i] < smash[0]):
                message['smash'] = "매우 우수"
            elif (df['earned_player'][i] < smash[1]):
                message['smash'] = "우수"
            elif (df['earned_player'][i] < smash[2]):
                message['smash'] = "평균"
            elif (df['earned_player'][i] < smash[3]):
                message['smash'] = "약간 부족"
            else:
                message['smash'] = "매우 부족"
        elif df['earned_type'][i] == "SERVE":
            skill_rate['serve'] = df['earned_player'][i]
            if (df['earned_player'][i] < serve[0]):
                message['serve'] = "매우 우수"
            elif (df['earned_player'][i] < serve[1]):
                message['serve'] = "우수"
            elif (df['earned_player'][i] < serve[2]):
                message['serve'] = "평균"
            elif (df['earned_player'][i] < serve[3]):
                message['serve'] = "약간 부족"
            else:
                message['serve'] = "매우 부족"
        elif df['earned_type'][i] == "HAIRPIN":
            skill_rate['net'] = df['earned_player'][i]
            if (df['earned_player'][i] < net[0]):
                message['net'] = "매우 우수"
            elif (df['earned_player'][i] < net[1]):
                message['net'] = "우수"
            elif (df['earned_player'][i] < net[2]):
                message['net'] = "평균"
            elif (df['earned_player'][i] < net[3]):
                message['net'] = "약간 부족"
            else:
                message['net'] = "매우 부족"
        elif df['earned_type'][i] == "PUSH":
            skill_rate['pushs'] = df['earned_player'][i]
            if (df['earned_player'][i] < pushs[0]):
                message['pushs'] = "매우 우수"
            elif (df['earned_player'][i] < pushs[1]):
                message['pushs'] = "우수"
            elif (df['earned_player'][i] < pushs[2]):
                message['pushs'] = "평균"
            elif (df['earned_player'][i] < pushs[3]):
                message['pushs'] = "약간 부족"
            else:
                message['pushs'] = "매우 부족"
        elif df['earned_type'][i] == "DROP":
            skill_rate['drops'] = df['earned_player'][i]
            if (df['earned_player'][i] < drops[0]):
                message['drops'] = "매우 우수"
            elif (df['earned_player'][i] < drops[1]):
                message['drops'] = "우수"
            elif (df['earned_player'][i] < drops[2]):
                message['drops'] = "평균"
            elif (df['earned_player'][i] < drops[3]):
                message['drops'] = "약간 부족"
            else:
                message['drops'] = "매우 부족"
        elif df['earned_type'][i] == "CLEAR":
            skill_rate['clears'] = df['earned_player'][i]
            if (df['earned_player'][i] < clears[0]):
                message['clears'] = "매우 우수"
            elif (df['earned_player'][i] < clears[1]):
                message['clears'] = "우수"
            elif (df['earned_player'][i] < clears[2]):
                message['clears'] = "평균"
            elif (df['earned_player'][i] < clears[3]):
                message['clears'] = "약간 부족"
            else:
                message['clears'] = "매우 부족"
        else:
            skill_rate['miss'] = df['earned_player'][i]
            if (df['earned_player'][i] < miss[0]):
                message['miss'] = "매우 우수"
            elif (df['earned_player'][i] < miss[1]):
                message['miss'] = "우수"
            elif (df['earned_player'][i] < miss[2]):
                message['miss'] = "평균"
            elif (df['earned_player'][i] < miss[3]):
                message['miss'] = "약간 부족"
            else:
                message['miss'] = "매우 부족"
            
    skill_rate_value = list(map(lambda x: round(x/sum(list(skill_rate.values())), 2)*100, list(skill_rate.values())))
    result = {
            "middle_lose_skill_rate": {'smash':smash[2], 'serve':serve[2], 'net':net[2], 'pushs':pushs[2], 'drops':drops[2], 'clears':clears[2]},
            "lose_skill_rate" : dict(zip(skill_rate.keys(), skill_rate_value)),
            "lose_skill_rate_text": message
            }
    return result

def checking_number3(df, user, match_df):
    # 득점 기술력
    my_skill_dict = my_skill(df, user, *total_skill(df, people_skill(match_df), user))
    skills = {
        "drops":"기술적인 플레이어에요! 드롭은 공을 짧고 부드럽게 떨어뜨려 상대방이 대응하기 어렵게 만드는 기술입니다. 상대방의 빈틈을 파고들어 경기 흐름을 제어하는 기술적이고 타이밍에 민감한 성향을 가집니다. 경기 속도를 조절하는 능력이 뛰어납니다.",
        "smash":"공격적인 파워 플레이어에요! 스매시는 상대방을 압박하고 빠르게 득점을 노리는 강한 공격 기술입니다. 스매시를 통해 상대방을 압박하고 빠르게 득점을 노리는 성향을 가집니다. 주로 강한 공격으로 경기를 주도합니다.",
        "clear":"안정적이고 수비적인 플레이어에요! 클리어는 상대방을 후방으로 밀어내면서 수비 위치를 잡는 기술입니다. 경기를 서두르지 않고, 상대방의 공격을 견디며 안정적이고 수비적인 성향을 가집니다.",
        "pushs":"빠르고 기민한 플레이어에요! 푸시는 네트 근처에서 빠르게 공을 밀어 상대방이 준비하지 못한 틈을 노리는 기술입니다. 기민하게 빠른 속도로 득점을 노리는 속공형 플레이를 즐기며, 상대의 타이밍을 빼앗는 능력이 뛰어납니다.",
        "net":"전략적이고 정교한 플레이어에요! 네트 플레이는 상대의 허점을 파고들어 짧고 정확한 샷으로 득점을 만드는 기술입니다. 빠르고 민첩한 움직임으로 상대방의 실수를 유도해 득점 기회를 만들어내는 능력이 뛰어납니다.",
        "serve":"---------------------흐음 얘는 뭐라고 해야 할까???"
        }
    worst, bad, best, better = [], [], [], []
    wo, ba, bes, bet = 0, 0, 0, 0
    for k, v in my_skill_dict['skill_rate_text'].items():
        if v == "매우 우수":
            best.append(k)
            bes+=1
        elif v == "우수":
            better.append(k)
            bet+=1
        elif v == " 약간 부족":
            bad.append(k)
            ba += 1
        elif v == "매우 부족":
            worst.append(k)
            wo += 1
    if bes >= 1:
        if bes == 1:
            my_skill_dict['message'] = skills[best[0]]
        else:
            print("!!")
            # for문 돌려서 제일 우수한거 찾기
    elif bet >= 1:
        if bet == 1:
            my_skill_dict['message'] = skills[better[0]]
        else:
            print("!!")
            # for문 돌려서 제일 우수한거 찾기
    else:
        my_skill_dict['message'] = "넌 왜 잘하는게 없니????????????"
            
    # 실점 기술력
    my_lose_skill_dict = my_lose_skill(df, user, *total_lose_skill(df, lose_people_skill(match_df), user))
    my_lose_skill_dict['message'] = "푸시에 대한 리시브가 취약해요. 상대가 푸시로 빠르게 공격을 전개할 때 반응이 느리거나 리턴이 부정확해 상대의 속공에 쉽게 실점을 허용하는 경향이 있습니다. 상대의 빠른 푸시 공격에 더욱 잘 대응할 수 있도록 네트 근처의 빠른 반응에 집중해서 실점율을 낮춰보세요!"
    
    result = {
        'score': my_skill_dict,
        'lose': my_lose_skill_dict
    }
    
    return result
import pandas as pd

def flow_function(df, i):
    
    earned_player = df['earned_player'][i]
    missed_player1 = df['missed_player1'][i]
    missed_player2 = df['missed_player2'][i]
    
    flag=False
    if (missed_player1 != 0 and missed_player2 != 0):
        flag = True

    if pd.isnull(earned_player):
        if flag:
            for ls in [missed_player1, missed_player2]:
                if i == 0:
                    df[f'{ls}_flow'][i] = -1
                elif df[f'{ls}_flow'][i-1] <= -1:
                    df[f'{ls}_flow'][i] = df[f'{ls}_flow'][i-1] -1
                else:
                    df[f'{ls}_flow'][i] = -1
            # flag = False
        else:
            if i == 0:
                df[f'{missed_player1}_flow'][i] = -1
            elif df[f'{missed_player1}_flow'][i-1] <= -1:
                df[f'{missed_player1}_flow'][i] = df[f'{missed_player1}_flow'][i-1] -1
            else:
                df[f'{missed_player1}_flow'][i] = -1
    else:
        if flag:
            if i == 0:
                df[f'{missed_player1}_flow'][i] = -1
                df[f'{missed_player2}_flow'][i] = -1
                df[f'{earned_player}_flow'][i] = 1
            else:
                for ls in [missed_player1, missed_player2]:
                    if df[f'{ls}_flow'][i-1] <= -1:
                        df[f'{ls}_flow'][i] = df[f'{ls}_flow'][i-1] -1
                    else:
                        df[f'{ls}_flow'][i] = -1
                if earned_player != 0:
                    if df[f'{earned_player}_flow'][i-1] >= 1:
                        df[f'{earned_player}_flow'][i] = df[f'{earned_player}_flow'][i-1] + 1
                    else:
                        df[f'{earned_player}_flow'][i] = 1
            flag = False
        else:
            if i == 0:
                df[f'{missed_player1}_flow'][i] = -1
                df[f'{earned_player}_flow'][i] = 1
            else:
                if df[f'{missed_player1}_flow'][i-1] <= -1:
                    df[f'{missed_player1}_flow'][i] = df[f'{missed_player1}_flow'][i-1] -1
                else:
                    df[f'{missed_player1}_flow'][i] = -1
                if earned_player != 0:
                    if df[f'{earned_player}_flow'][i-1] >= 1:
                        df[f'{earned_player}_flow'][i] = df[f'{earned_player}_flow'][i-1] + 1
                    else:
                        df[f'{earned_player}_flow'][i] = 1

def team_flow(df, i, score1, score2):
    if i == 0:
        if (df['missed_player1'][i])//10 == 1:
            df['team2'][i] = 1
            df['score2'][i] = score2 + 1
            score2 += 1
        else:
            df['team1'][i] = 1
            df['score1'][i] = score1 + 1
            score1 += 1
    else:
        if (df['missed_player1'][i])//10 == 1:
            df['team2'][i] = df['team2'][i-1] + 1
            df['score2'][i] = score2 + 1
            df['score1'][i] = score1
            score2 += 1
        else:
            df['team1'][i] = df['team1'][i-1] + 1
            df['score1'][i] = score1 + 1
            df['score2'][i] = score2
            score1 += 1
    return score1, score2

def change_df(df):
    df.loc[df['earned_player'].isna(), 'earned_player'] = 0
    df.loc[df['missed_player1'].isna(), 'missed_player1'] = 0
    df.loc[df['missed_player2'].isna(), 'missed_player2'] = 0
    df['earned_player'] = df['earned_player'].astype(int)
    df['missed_player1'] = df['missed_player1'].astype(int)
    df['missed_player2'] = df['missed_player2'].astype(int)
    
    df[['team1','team2',
        '11_flow','12_flow','21_flow','22_flow',
        'score1', 'score2']]= 0, 0, 0, 0, 0, 0, 0, 0

    matching = pd.DataFrame({})
    for set in df.set_id.unique():
        score1, score2 = 0, 0
        df_ = df.query(f"set_id == {set}").reset_index(drop=True)
        for i in range(len(df_)):
            flow_function(df_, i)
            score1, score2 = team_flow(df_, i, score1, score2)
        matching = pd.concat([matching, df_])
    return matching
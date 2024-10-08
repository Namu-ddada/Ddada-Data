import pandas as pd

def flow(df, user):
    lst = list(df[f'{user}_flow'])
    flow = []
    for i in range(len(lst)):
        if flow:
            result = flow[-1] + lst[i]
            flow.append(result)
        else:
            result = lst[i]
            flow.append(result)
            
    return flow
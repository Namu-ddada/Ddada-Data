import pandas as pd
from database import database
from racket_type import racket_type

async def recommend_racket(balance, weight, price, shaft, racket_id):
    check_bl = {'attack':'헤드헤비(공격형)', 'defense':"헤드라이트(수비형)", 'allround':"이븐밸런스(올라운드형)"}
    check_sh = {'stiff':'견고(Stiff)', 'medium':'중간(Medium)','flexible':'유연(Flexible)'}
    
    if weight == "heavy":
        weight_list = ['3U', '4U']
    elif weight == 'light':
        weight_list = ['5U', '6U']
    else:
        if balance == "attack":
            weight_list = ['5U', '6U']
        elif balance == "defense":
            weight_list = ['3U', '4U']
        else:
            weight_list = ['4U', '5U']
        
    if shaft == "":
        if balance == "attack":
            shaft = 'flexible'
        elif balance == "defense":
            shaft = 'stiff'
        else:
            shaft = 'medium'
            
            
    # 내가 보유한 라켓 입력 여부에 따른 추천
    if len(racket_id) > 0:
        where_sql = f"SELECT * FROM racket WHERE racket_id = {racket_id[0]}"
        for r in racket_id[1:]:
            where_sql += f" OR racket_id = {r}"
        already_my_racket = await database.fetch_all(where_sql)
        dict_rows = [dict(row) for row in already_my_racket]
        my_racket = pd.DataFrame(dict_rows)
        
        # 내가 입력한 내용과 유사한 라켓을 이미 보유하고 있는지 여부
        df = my_racket.query(f'"{check_bl[balance]}" in balance and ((weight == "{weight_list[0]}") or weight == "{weight_list[1]}")')
        if len(df) == 1:
            my_racket_cnt = 1
        elif len(df) > 1:
            first_next_df = df.query(f'shaft == "{check_sh[shaft]}"')
            if len(first_next_df) == 0:
                my_racket_cnt = len(df)
            else:
                df = first_next_df
                my_racket_cnt = len(df)
        else:
            my_racket_cnt = 0
    else:
        my_racket_cnt = 0


    ##### 질문에 대한 쿼리문
    query = "SELECT * FROM racket"
    # 밸런스 쿼리
    balance_query = f"balance LIKE '%{check_bl[balance]}%'"
    # 샤프트 쿼리
    shaft_query = f"shaft = '{check_sh[shaft]}'"
    # 무게 쿼리
    weight_query = f"(weight = '{weight_list[0]}' OR weight = '{weight_list[1]}')"
    # 가격 쿼리
    if price == 30:
        price_query = f"price >= {price*10000}"
    elif price != -1:
        price_query = f"price BETWEEN {price*10000} and {(price+10)*10000}"
    ## 최종 쿼리문
    if price != -1:
        full_query = query + " WHERE " + balance_query + " AND " + shaft_query + " AND " + weight_query + " AND " + price_query
    else:
        full_query = query + " WHERE " + balance_query + " AND " + shaft_query + " AND " + weight_query
    
    
    
    data = await database.fetch_all(full_query)
    
    while len(data) == 0:
        full_query = list(full_query.split(" AND "))[:-1]
        full_query = " AND ".join(full_query)
        data = await database.fetch_all(full_query)
    
    for i in range(len(data)):
        racket_dict = data[i]
        
        if not isinstance(racket_dict, dict):
            racket_dict = dict(racket_dict)
            data[i] = racket_dict
    if my_racket_cnt:
        df = df.reset_index(drop=True)
    
    if len(data) == 1:
        my_type = racket_type(balance, weight, shaft)
        if my_racket_cnt == 0:
            data[0]['type'] = "내가 보유한 라켓 종류와는 다른 새로운 라켓이에요.✨"
        elif my_racket_cnt == 1:
            data[0]['type'] = f'내가 보유한 라켓 "{df["name"][0]}"과 가장 유사해요.💫'
        else:
            df['cnt'] = 0
            max_cnt = 0
            max_i = 0
            for i in range(my_racket_cnt):
                print(df)
                if df.iloc[i,:]['manufacturer'] == data[0]['manufacturer']:
                    df.iloc[i,:]['cnt'] += 1
                if price*10000 <= df.iloc[i,:]['price'] <= (price+10)*10000:
                    df.iloc[i,:]['cnt'] += 1
                if df.iloc[i,:]['material'] == data[0]['material']:
                    df.iloc[i,:]['cnt'] += 1
                if df.iloc[i,:]['cnt'] > max_cnt:
                    max_cnt = df.iloc[i,:]['cnt']
                    max_i = i
            data[0]['type'] = f'내가 보유한 라켓 "{df.iloc[max_i, :]["name"]}"과 가장 유사해요.💫'
            
        racket = {
            'my_type':my_type,
            'racket':data
        }
        
    elif len(data) == 2:
        my_type = racket_type(balance, weight, shaft)
        if my_racket_cnt > 1:
            df[['cnt0','cnt1']] = 0, 0
            max_cnt0, max_cnt1 = 0, 0
            max_i0, max_i1 = 0, 0
            for i in range(my_racket_cnt):
                if df.iloc[i,:]['manufacturer'] == data[0]['manufacturer']:
                    df.iloc[i,:]['cnt0'] += 1
                if df.iloc[i,:]['manufacturer'] == data[1]['manufacturer']:
                    df.iloc[i,:]['cnt1'] += 1
                if df.iloc[i,:]['material'] == data[0]['material']:
                    df.iloc[i,:]['cnt0'] += 1
                if df.iloc[i,:]['material'] == data[1]['material']:
                    df.iloc[i,:]['cnt1'] += 1
                if df.iloc[i,:]['cnt0'] > max_cnt0:
                    max_cnt0 = df.iloc[i,:]['cnt0']
                    max_i0 = i
                if df.iloc[i,:]['cnt1'] > max_cnt1:
                    max_cnt1 = df.iloc[i,:]['cnt1']
                    max_i1 = i
            if max_i0 >= max_i1:
                data[0]['type'] = f'내가 보유한 라켓 "{df.iloc[max_i0, :]["name"]}"과 가장 유사해요.💫'
                if data[0]['price'] > data[1]['price']:
                    data[1]['type'] = '검색 조건에 부합한 라켓 중 가장 저렴해요.😁'
                elif data[1]['color'] != None:
                    if len(list(data[1]['color'].split())) > 1:
                        data[1]['type'] = '색상이 다양해서 취향에 따라 고를 수 있어요.🌈'
                    else:
                        if max_i0 != max_i1:
                            data[1]['type'] = f'내가 보유한 라켓 "{df.iloc[max_i1, :]["name"]}"과 가장 유사해요.💫'
                        else:
                            max_cnt1 = 0
                            max_i1 = 0
                            for i in range(my_racket_cnt):
                                if (i != max_i0) and (df.iloc[i,:]['cnt1'] >= max_cnt1):
                                    max_i1 = i
                                    max_cnt1 = df.iloc[i,:]['cnt1']
                            data[1]['type'] = f'내가 보유한 라켓 "{df.iloc[max_i1, :]["name"]}"과 가장 유사해요.💫'
                else:
                    if max_i0 != max_i1:
                        data[1]['type'] = f'내가 보유한 라켓 "{df.iloc[max_i1, :]["name"]}"과 가장 유사해요.💫'
                    else:
                        max_cnt1 = 0
                        max_i1 = 0
                        for i in range(my_racket_cnt):
                            if (i != max_i0) and (df.iloc[i,:]['cnt1'] >= max_cnt1):
                                max_i1 = i
                                max_cnt1 = df.iloc[i,:]['cnt1']
                        data[1]['type'] = f'내가 보유한 라켓 "{df.iloc[max_i1, :]["name"]}"과 가장 유사해요.💫'
            else:
                data[1]['type'] = f'내가 보유한 라켓 "{df.iloc[max_i1, :]["name"]}"과 가장 유사해요.💫'
                if data[1]['price'] > data[0]['price']:
                    data[0]['type'] = '검색 조건에 부합한 라켓 중 가장 저렴해요.😁'
                elif data[0]['color'] != None:
                    if len(list(data[0]['color'].split())) > 1:
                        data[0]['type'] = f'색상이 다양해서 취향에 따라 고를 수 있어요.🌈'
                    else:
                        if max_i0 != max_i1:
                            data[0]['type'] = f'내가 보유한 라켓 "{df.iloc[max_i0, :]["name"]}"과 가장 유사해요.💫'
                        else:
                            max_cnt0 = 0
                            max_i0 = 0
                            for i in range(my_racket_cnt):
                                if (i != max_i1) and (df.iloc[i,:]['cnt0'] >= max_cnt0):
                                    max_i0 = i
                                    max_cnt0 = df.iloc[i,:]['cnt0']
                            data[0]['type'] = f'내가 보유한 라켓 "{df.iloc[max_i0, :]["name"]}"과 가장 유사해요.💫'
                else:
                    if max_i0 != max_i1:
                        data[0]['type'] = f'내가 보유한 라켓 "{df.iloc[max_i0, :]["name"]}"과 가장 유사해요.💫'
                    else:
                        max_cnt0 = 0
                        max_i0 = 0
                        for i in range(my_racket_cnt):
                            if (i != max_i1) and (df.iloc[i,:]['cnt0'] >= max_cnt0):
                                max_i0 = i
                                max_cnt0 = df.iloc[i,:]['cnt0']
                        data[0]['type'] = f'내가 보유한 라켓 "{df.iloc[max_i0, :]["name"]}"과 가장 유사해요.💫'
        elif my_racket_cnt == 1:
            max_cnt0, max_cnt1 = 0, 0
            max_i0, max_i1 = 0, 0
            if df['manufacturer'][0] == data[0]['manufacturer']:
                max_i0 += 1
            if df['manufacturer'][0] == data[1]['manufacturer']:
                max_i1 += 1
            if df['material'][0] == data[0]['material']:
                max_i0 += 1
            if df['material'][0] == data[1]['material']:
                max_i1 += 1
            if max_i0 > max_i1:
                data[0]['type'] = f'내가 보유한 라켓 "{df["name"][0]}"과 가장 유사해요.💫'
                if data[0]['price'] > data[1]['price']:
                    data[1]['type'] = '검색 조건에 부합한 라켓 중 가장 저렴해요.😁'
                elif data[1]['color'] != None:
                    if len(list(data[1]['color'].split())) > 1:
                        data[1]['type'] = '색상이 다양해서 취향에 따라 고를 수 있어요.🌈'
                    else:
                        data[1]['type'] = '검색 조건에 부합한 라켓이에요.🤗'
            else:
                data[1]['type'] = f'내가 보유한 라켓 "{df["name"][1]}"과 가장 유사해요.💫'
                if data[1]['price'] > data[0]['price']:
                    data[0]['type'] = '검색 조건에 부합한 라켓 중 가장 저렴해요.😁'
                elif data[0]['color'] != None:
                    if len(list(data[0]['color'].split())) > 1:
                        data[0]['type'] = '색상이 다양해서 취향에 따라 고를 수 있어요.🌈'
                    else:
                        data[0]['type'] = '검색 조건에 부합한 라켓이에요.🤗'
        else:
            if data[0]['price'] > data[1]['price']:
                data[1]['type'] = '검색 조건에 부합한 라켓 중 가장 저렴해요.😁'
                if data[0]['color'] != None:
                    if len(list(data[0]['color'].split())) > 1:
                        data[0]['type'] = '색상이 다양해서 취향에 따라 고를 수 있어요.🌈'
                    else:
                        data[0]['type'] = f'검색 조건에 부합한 {data[0]["manufacturer"]} 라켓이에요.🤗'
                else:
                    data[0]['type'] = f'검색 조건에 부합한 {data[0]["manufacturer"]} 라켓이에요.🤗'
            elif data[0]['price'] < data[1]['price']:
                data[0]['type'] = '검색 조건에 부합한 라켓 중 가장 저렴해요.😁'
                if data[1]['color'] != None:
                    if len(list(data[1]['color'].split())) > 1:
                        data[1]['type'] = f'색상이 다양해서 취향에 따라 고를 수 있어요.🌈'
                    else:
                        data[1]['type'] = f'검색 조건에 부합한 {data[1]["manufacturer"]} 라켓이에요.🤗'
                else:
                    data[1]['type'] = f'검색 조건에 부합한 {data[1]["manufacturer"]} 라켓이에요.🤗'
            else:
                if data[0]['color'] != None:
                    color0 = len(list(data[0]['color'].split()))
                else:
                    color0 = 0
                if data[1]['color'] != None:
                    color1 = len(list(data[1]['color'].split()))
                else:
                    color1 = 0
                if color0 > color1:
                    data[0]['type'] = '색상이 다양해서 취향에 따라 고를 수 있어요.🌈'
                    data[1]['type'] = f'검색 조건에 부합한 {data[1]["manufacturer"]} 라켓이에요.🤗'
                elif color0 < color1:
                    data[1]['type'] = '색상이 다양해서 취향에 따라 고를 수 있어요.🌈'
                    data[0]['type'] = f'검색 조건에 부합한 {data[0]["manufacturer"]} 라켓이에요.🤗'
                else:
                    data[0]['type'] = f'검색 조건에 부합한 {data[0]["manufacturer"]} 라켓이에요.🤗'
                    data[1]['type'] = f'검색 조건에 부합한 {data[1]["manufacturer"]} 라켓이에요.🤗'
        
        racket = {
            'my_type':my_type,
            'racket':data
        }
        
    elif len(data) == 3:
        my_type = racket_type(balance, weight, shaft)
        if my_racket_cnt == 1:
            left_i = [0, 1, 2]
            color_cnt = 1
            color_i = 0
            for i in left_i:
                if data[i]['color'] != None:
                    if len(list(data[i]['color'].split())) > color_cnt:
                        color_i = i
                        color_cnt = len(list(data[i]['color'].split()))
            if color_cnt != 1:
                data[color_i]['type'] = '색상이 다양해서 취향에 따라 고를 수 있어요.🌈'
                left_i.remove(color_i)
                if (data[left_i[0]]['manufacturer'] == df['manufacturer'][0]) and (data[left_i[1]]['manufacturer'] != df['manufacturer'][0]):
                    data[left_i[0]]['type'] = f'내가 보유한 라켓 "{df["name"][0]}"과 가장 유사해요.💫'
                    if (data[color_i]['price'] > data[left_i[1]]['price']) and (data[left_i[0]]['price'] > data[left_i[1]]['price']):
                        data[left_i[1]]['type'] = '검색 조건에 부합한 라켓 중 가장 저렴해요.😁'
                    else:
                        data[left_i[1]]['type'] = f'검색 조건에 부합한 {data[left_i[1]]["manufacturer"]} 라켓이에요.🤗'
                elif (data[left_i[0]]['manufacturer'] != df['manufacturer'][0]) and (data[left_i[1]]['manufacturer'] == df['manufacturer'][0]):
                    data[left_i[1]]['type'] = f'내가 보유한 라켓 "{df["name"][0]}"과 가장 유사해요.💫'
                    if (data[color_i]['price'] > data[left_i[0]]['price']) and (data[left_i[1]]['price'] > data[left_i[0]]['price']):
                        data[left_i[0]]['type'] = '검색 조건에 부합한 라켓 중 가장 저렴해요.😁'
                    else:
                        data[left_i[0]]['type'] = f'검색 조건에 부합한 {data[left_i[0]]["manufacturer"]} 라켓이에요.🤗'
                else:
                    if abs(data[left_i[0]]['price'] - df['price'][0]) < abs(data[left_i[1]]['price'] - df['price'][0]):
                        data[left_i[0]]['type'] = f'내가 보유한 라켓 "{df["name"][0]}"과 가장 유사해요.💫'
                        if (data[color_i]['price'] > data[left_i[1]]['price']) and (data[left_i[0]]['price'] > data[left_i[1]]['price']):
                            data[left_i[1]]['type'] = '검색 조건에 부합한 라켓 중 가장 저렴해요.😁'
                        else:
                            data[left_i[1]]['type'] = f'검색 조건에 부합한 {data[left_i[1]]["manufacturer"]} 라켓이에요.🤗'
                    elif abs(data[left_i[0]]['price'] - df['price'][0]) > abs(data[left_i[1]]['price'] - df['price'][0]):
                        data[left_i[1]]['type'] = f'내가 보유한 라켓 "{df["name"][0]}"과 가장 유사해요.💫'
                        if (data[color_i]['price'] > data[left_i[0]]['price']) and (data[left_i[1]]['price'] > data[left_i[0]]['price']):
                            data[left_i[0]]['type'] = '검색 조건에 부합한 라켓 중 가장 저렴해요.😁'
                        else:
                            data[left_i[0]]['type'] = f'검색 조건에 부합한 {data[left_i[0]]["manufacturer"]} 라켓이에요.🤗'
                    else:
                        if (data[color_i]['price'] > data[left_i[0]]['price']) and (data[left_i[1]]['price'] > data[left_i[0]]['price']):
                            data[left_i[0]]['type'] = '검색 조건에 부합한 라켓 중 가장 저렴해요.😁'
                            data[left_i[1]]['type'] = f'검색 조건에 부합한 {data[left_i[1]]["manufacturer"]} 라켓이에요.🤗'
                        elif (data[color_i]['price'] > data[left_i[1]]['price']) and (data[left_i[0]]['price'] > data[left_i[1]]['price']):
                            data[left_i[1]]['type'] = '검색 조건에 부합한 라켓 중 가장 저렴해요.😁'
                            data[left_i[0]]['type'] = f'검색 조건에 부합한 {data[left_i[0]]["manufacturer"]} 라켓이에요.🤗'
                        else:
                            data[left_i[0]]['type'] = f'검색 조건에 부합한 {data[left_i[0]]["manufacturer"]} 라켓이에요.🤗'
                            data[left_i[1]]['type'] = f'검색 조건에 부합한 {data[left_i[1]]["manufacturer"]} 라켓이에요.🤗'
            else:
                check_ma = []
                for i in left_i:
                    if data[i]['manufacturer'] == df['manufacturer'][0]:
                        check_ma.append(i)
                if len(check_ma) == 1:
                    left_i.remove(check_ma[0])
                    data[check_ma[0]]['type'] = f'내가 보유한 라켓 "{df["name"][0]}"과 가장 유사해요.💫'
                    if (data[check_ma[0]]['price'] > data[left_i[0]]['price']) and (data[left_i[1]]['price'] > data[left_i[0]]['price']):
                        data[left_i[0]]['type'] = '검색 조건에 부합한 라켓 중 가장 저렴해요.😁'
                        data[left_i[1]]['type'] = f'검색 조건에 부합한 {data[left_i[1]]["manufacturer"]} 라켓이에요.🤗'
                    elif (data[check_ma[0]]['price'] > data[left_i[1]]['price']) and (data[left_i[0]]['price'] > data[left_i[1]]['price']):
                        data[left_i[1]]['type'] = '검색 조건에 부합한 라켓 중 가장 저렴해요.😁'
                        data[left_i[0]]['type'] = f'검색 조건에 부합한 {data[left_i[0]]["manufacturer"]} 라켓이에요.🤗'
                    else:
                        data[left_i[0]]['type'] = f'검색 조건에 부합한 {data[left_i[0]]["manufacturer"]} 라켓이에요.🤗'
                        data[left_i[1]]['type'] = f'검색 조건에 부합한 {data[left_i[1]]["manufacturer"]} 라켓이에요.🤗'
                elif (len(check_ma) == 0) or (len(check_ma) == 3):
                    price_list = [abs(data[0]['price'] - df['price'][0]), abs(data[1]['price'] - df['price'][0]), abs(data[2]['price'] - df['price'][0])]
                    i = price_list.index(min(price_list))
                    left_i.remove(i)
                    data[i]['type'] = f'내가 보유한 라켓 "{df["name"][0]}"과 가장 유사해요.💫'
                    if (data[check_ma[0]]['price'] > data[left_i[0]]['price']) and (data[left_i[1]]['price'] > data[left_i[0]]['price']):
                        data[left_i[0]]['type'] = '검색 조건에 부합한 라켓 중 가장 저렴해요.😁'
                        data[left_i[1]]['type'] = f'검색 조건에 부합한 {data[left_i[1]]["manufacturer"]} 라켓이에요.🤗'
                    elif (data[check_ma[0]]['price'] > data[left_i[1]]['price']) and (data[left_i[0]]['price'] > data[left_i[1]]['price']):
                        data[left_i[1]]['type'] = '검색 조건에 부합한 라켓 중 가장 저렴해요.😁'
                        data[left_i[0]]['type'] = f'검색 조건에 부합한 {data[left_i[0]]["manufacturer"]} 라켓이에요.🤗'
                    else:
                        data[left_i[0]]['type'] = f'검색 조건에 부합한 {data[left_i[0]]["manufacturer"]} 라켓이에요.🤗'
                        data[left_i[1]]['type'] = f'검색 조건에 부합한 {data[left_i[1]]["manufacturer"]} 라켓이에요.🤗'
                else:
                    price_list = [abs(data[check_ma[0]]['price'] - df['price'][0]), abs(data[check_ma[1]]['price'] - df['price'][0])]
                    i = check_ma[price_list.index(min(price_list))]
                    left_i.remove(i)
                    data[i]['type'] = f'내가 보유한 라켓 "{df["name"][0]}"과 가장 유사해요.💫'
                    if (data[i]['price'] > data[left_i[0]]['price']) and (data[left_i[1]]['price'] > data[left_i[0]]['price']):
                        data[left_i[0]]['type'] = '검색 조건에 부합한 라켓 중 가장 저렴해요.😁'
                        data[left_i[1]]['type'] = f'검색 조건에 부합한 {data[left_i[1]]["manufacturer"]} 라켓이에요.🤗'
                    elif (data[i]['price'] > data[left_i[1]]['price']) and (data[left_i[0]]['price'] > data[left_i[1]]['price']):
                        data[left_i[1]]['type'] = '검색 조건에 부합한 라켓 중 가장 저렴해요.😁'
                        data[left_i[0]]['type'] = f'검색 조건에 부합한 {data[left_i[0]]["manufacturer"]} 라켓이에요.🤗'
                    else:
                        data[left_i[0]]['type'] = f'검색 조건에 부합한 {data[left_i[0]]["manufacturer"]} 라켓이에요.🤗'
                        data[left_i[1]]['type'] = f'검색 조건에 부합한 {data[left_i[1]]["manufacturer"]} 라켓이에요.🤗'
        elif my_racket_cnt > 1:
            left_i = [0, 1, 2]
            color_cnt = 1
            color_i = 0
            for i in left_i:
                if data[i]['color'] != None:
                    if len(list(data[i]['color'].split())) > color_cnt:
                        color_i = i
                        color_cnt = len(list(data[i]['color'].split()))
            if color_cnt != 1:
                data[color_i]['type'] = '색상이 다양해서 취향에 따라 고를 수 있어요.🌈'
                left_i.remove(color_i)
                if (data[color_i]['price'] > data[left_i[0]]['price']) and (data[left_i[1]]['price'] > data[left_i[0]]['price']):
                    data[left_i[0]]['type'] = '검색 조건에 부합한 라켓 중 가장 저렴해요.😁'
                    df['price'] = abs(df['price']-data[left_i[1]]['price'])
                    imsi_df = df.query(f"manufacturer == {data[left_i[1]]['manufacturer']}").sort_values(by='price', ascending=True)
                    if len(imsi_df):
                        data[left_i[1]]['type'] = f'내가 보유한 라켓 "{imsi_df.iloc[0,:]["name"]}"과 가장 유사해요.💫'
                    else:
                        df = df.sort_values(by='price', ascending=True)
                        data[left_i[1]]['type'] = f'내가 보유한 라켓 "{df.iloc[0,:]["name"]}"과 가장 유사해요.💫'
                elif (data[color_i]['price'] > data[left_i[1]]['price']) and (data[left_i[0]]['price'] > data[left_i[1]]['price']):
                    data[left_i[1]]['type'] = '검색 조건에 부합한 라켓 중 가장 저렴해요.😁'
                    df['price'] = abs(df['price']-data[left_i[0]]['price'])
                    imsi_df = df.query(f"manufacturer == {data[left_i[0]]['manufacturer']}").sort_values(by='price', ascending=True)
                    if len(imsi_df):
                        data[left_i[0]]['type'] = f'내가 보유한 라켓 "{imsi_df.iloc[0,:]["name"]}"과 가장 유사해요.💫'
                    else:
                        df = df.sort_values(by='price', ascending=True)
                        data[left_i[0]]['type'] = f'내가 보유한 라켓 "{df.iloc[0,:]["name"]}"과 가장 유사해요.💫'
                else:
                    df0 = df
                    df0['price'] = abs(df0['price']-data[left_i[0]]['price'])
                    imsi_df0 = df0.query(f"manufacturer == {data[left_i[0]]['manufacturer']}").sort_values(by='price', ascending=True)
                    if len(imsi_df0):
                        data[left_i[0]]['type'] = f'내가 보유한 라켓 "{imsi_df0.iloc[0,:]["name"]}"과 가장 유사해요.💫'
                    else:
                        df0 = df0.sort_values(by='price', ascending=True)
                        data[left_i[0]]['type'] = f'내가 보유한 라켓 "{df0.iloc[0,:]["name"]}"과 가장 유사해요.💫'
                    
                    df['price'] = abs(df['price']-data[left_i[1]]['price'])
                    imsi_df = df.query(f"manufacturer == {data[left_i[1]]['manufacturer']}").sort_values(by='price', ascending=True)
                    if len(imsi_df) == 1:
                        if len(imsi_df0) and (imsi_df0.iloc[0,:]['name'] != imsi_df.iloc[0,:]['name']):
                            data[left_i[1]]['type'] = f'내가 보유한 라켓 "{imsi_df.iloc[0,:]["name"]}"과 가장 유사해요.💫'
                        elif (df0.iloc[0,:]['name'] != imsi_df.iloc[0,:]['name']):
                            data[left_i[1]]['type'] = f'내가 보유한 라켓 "{imsi_df.iloc[0,:]["name"]}"과 가장 유사해요.💫'
                        else:
                            data[left_i[1]]['type'] = f'검색 조건에 부합한 {data[left_i[1]]["manufacturer"]} 라켓이에요.🤗'
                    elif len(imsi_df) > 1:
                        if len(imsi_df0) and (imsi_df0.iloc[0,:]['name'] != imsi_df.iloc[0,:]['name']):
                            data[left_i[1]]['type'] = f'내가 보유한 라켓 "{imsi_df.iloc[0,:]["name"]}"과 가장 유사해요.💫'
                        elif (df0.iloc[0,:]['name'] != imsi_df.iloc[0,:]['name']):
                            data[left_i[1]]['type'] = f'내가 보유한 라켓 "{imsi_df.iloc[0,:]["name"]}"과 가장 유사해요.💫'
                        else:
                            data[left_i[1]]['type'] = f'내가 보유한 라켓 "{imsi_df.iloc[1,:]["name"]}"과 가장 유사해요.💫'
                    else:
                        df = df.sort_values(by='price', ascending=True)
                        if len(imsi_df0) and (imsi_df0.iloc[0,:]['name'] != df.iloc[0,:]['name']):
                            data[left_i[1]]['type'] = f'내가 보유한 라켓 "{df.iloc[0,:]["name"]}"과 가장 유사해요.💫'
                        elif (df0.iloc[0,:]['name'] != df.iloc[0,:]['name']):
                            data[left_i[1]]['type'] = f'내가 보유한 라켓 "{df.iloc[0,:]["name"]}"과 가장 유사해요.💫'
                        else:
                            data[left_i[1]]['type'] = f'내가 보유한 라켓 "{df.iloc[1,:]["name"]}"과 가장 유사해요.💫'
            else:
                price_list = [data[0]['price'], data[1]['price'], data[2]['price']]
                i = price_list.index(min(price_list))
                left_i.remove(i)
                data[i]['type'] = '검색 조건에 부합한 라켓 중 가장 저렴해요.😁'
                df0 = df
                df0['price'] = abs(df0['price']-data[left_i[0]]['price'])
                imsi_df0 = df0.query(f"manufacturer == {data[left_i[0]]['manufacturer']}").sort_values(by='price', ascending=True)
                if len(imsi_df0):
                    data[left_i[0]]['type'] = f'내가 보유한 라켓 "{imsi_df0.iloc[0,:]["name"]}"과 가장 유사해요.💫'
                else:
                    df0 = df0.sort_values(by='price', ascending=True)
                    data[left_i[0]]['type'] = f'내가 보유한 라켓 "{df0.iloc[0,:]["name"]}"과 가장 유사해요.💫'
                
                df['price'] = abs(df['price']-data[left_i[1]]['price'])
                imsi_df = df.query(f"manufacturer == {data[left_i[1]]['manufacturer']}").sort_values(by='price', ascending=True)
                if len(imsi_df) == 1:
                    if len(imsi_df0) and (imsi_df0.iloc[0,:]['name'] != imsi_df.iloc[0,:]['name']):
                        data[left_i[1]]['type'] = f'내가 보유한 라켓 "{imsi_df.iloc[0,:]["name"]}"과 가장 유사해요.💫'
                    elif (df0.iloc[0,:]['name'] != imsi_df.iloc[0,:]['name']):
                        data[left_i[1]]['type'] = f'내가 보유한 라켓 "{imsi_df.iloc[0,:]["name"]}"과 가장 유사해요.💫'
                    else:
                        data[left_i[1]]['type'] = f'검색 조건에 부합한 {data[left_i[1]]["manufacturer"]} 라켓이에요.🤗'
                elif len(imsi_df) > 1:
                    if len(imsi_df0) and (imsi_df0.iloc[0,:]['name'] != imsi_df.iloc[0,:]['name']):
                        data[left_i[1]]['type'] = f'내가 보유한 라켓 "{imsi_df.iloc[0,:]["name"]}"과 가장 유사해요.💫'
                    elif (df0.iloc[0,:]['name'] != imsi_df.iloc[0,:]['name']):
                        data[left_i[1]]['type'] = f'내가 보유한 라켓 "{imsi_df.iloc[0,:]["name"]}"과 가장 유사해요.💫'
                    else:
                        data[left_i[1]]['type'] = f'내가 보유한 라켓 "{imsi_df.iloc[1,:]["name"]}"과 가장 유사해요.💫'
                else:
                    df = df.sort_values(by='price', ascending=True)
                    if len(imsi_df0) and (imsi_df0.iloc[0,:]['name'] != df.iloc[0,:]['name']):
                        data[left_i[1]]['type'] = f'내가 보유한 라켓 "{df.iloc[0,:]["name"]}"과 가장 유사해요.💫'
                    elif (df0.iloc[0,:]['name'] != df.iloc[0,:]['name']):
                        data[left_i[1]]['type'] = f'내가 보유한 라켓 "{df.iloc[0,:]["name"]}"과 가장 유사해요.💫'
                    else:
                        data[left_i[1]]['type'] = f'내가 보유한 라켓 "{df.iloc[1,:]["name"]}"과 가장 유사해요.💫'
        else:
            left_i = [0, 1, 2]
            color_cnt = 1
            color_i = 0
            for i in left_i:
                if data[i]['color'] != None:
                    if len(list(data[i]['color'].split())) > color_cnt:
                        color_i = i
                        color_cnt = len(list(data[i]['color'].split()))
            if color_cnt != 1:
                data[color_i]['type'] = '색상이 다양해서 취향에 따라 고를 수 있어요.🌈'
                left_i.remove(color_i)
                if (data[color_i]['price'] > data[left_i[0]]['price']) and (data[left_i[1]]['price'] > data[left_i[0]]['price']):
                    data[left_i[0]]['type'] = '검색 조건에 부합한 라켓 중 가장 저렴해요.😁'
                    data[left_i[1]]['type'] = f'검색 조건에 부합한 {data[left_i[1]]["manufacturer"]} 라켓이에요.🤗'
                elif (data[color_i]['price'] > data[left_i[1]]['price']) and (data[left_i[0]]['price'] > data[left_i[1]]['price']):
                    data[left_i[1]]['type'] = '검색 조건에 부합한 라켓 중 가장 저렴해요.😁'
                    data[left_i[0]]['type'] = f'검색 조건에 부합한 {data[left_i[1]]["manufacturer"]} 라켓이에요.🤗'
                else:
                    data[left_i[0]]['type'] = f'검색 조건에 부합한 {data[left_i[0]]["manufacturer"]} 라켓이에요.🤗'
                    data[left_i[1]]['type'] = f'검색 조건에 부합한 {data[left_i[1]]["manufacturer"]} 라켓이에요.🤗'
            else:
                price_list = [data[0]['price'], data[1]['price'], data[2]['price']]
                i = price_list.index(min(price_list))
                left_i.remove(i)
                data[i]['type'] = '검색 조건에 부합한 라켓 중 가장 저렴해요.😁'
                data[left_i[0]]['type'] = f'검색 조건에 부합한 {data[left_i[0]]["manufacturer"]} 라켓이에요.🤗'
                data[left_i[1]]['type'] = f'검색 조건에 부합한 {data[left_i[1]]["manufacturer"]} 라켓이에요.🤗'
                
        racket = {
            'my_type':my_type,
            'racket':data
        }
    
    elif len(data) > 3:
        my_type = racket_type(balance, weight, shaft)
        my_data = []
        # 1개
        min_price_racket = min(data, key=lambda x: x['price'])
        data.remove(min_price_racket)
        min_price_racket['type'] = '검색 조건에 부합한 라켓 중 가장 저렴해요.😁'
        my_data.append(min_price_racket)
        # 2개
        max_color_racket = max(data, key=lambda x: len(list(x['color'].split(','))) if x['color'] != None else 0)
        data.remove(max_color_racket)
        max_color_racket['type'] = '색상이 다양해서 취향에 따라 고를 수 있어요.🌈'
        my_data.append(max_color_racket)
        # 3개
        if my_racket_cnt > 1:
            same_price_racket = min(data, key=lambda x: abs(x['price']-df.iloc[0,:]['price']))
            same_price_racket['type'] = f'내가 보유한 라켓 "{df.iloc[0,:]["name"]}"과 가장 유사해요.💫'
            my_data.append(same_price_racket)
        elif my_racket_cnt == 1:
            same_price_racket = min(data, key=lambda x: abs(x['price']-df['price'][0]))
            same_price_racket['type'] = f'내가 보유한 라켓 "{df["name"][0]}"과 가장 유사해요.💫'
            my_data.append(same_price_racket)
        else:
            final_racket = data[0]
            final_racket['type'] = f'검색 조건에 부합한 {final_racket["manufacturer"]} 라켓이에요.🤗'
            my_data.append(final_racket)
        
        racket = {
            'my_type':my_type,
            'racket':my_data
        }
    
    return racket
import pandas as pd
from database import database

async def recommend_racket(balance, weight, price, shaft, racket_id = []):
    if weight == "무거운":
        weight_list = ['3U', '4U']
    elif weight == '가벼운':
        weight_list = ['5U', '6U']
    else:
        if balance == "수비":
            weight_list = ['5U', '6U']
        elif balance == "공격":
            weight_list = ['3U', '4U']
        else:
            weight_list = ['4U', '5U']
        
    if shaft == "상관 없음":
        if balance == "수비":
            shaft = '유연'
        elif balance == "공격":
            shaft = '견고'
        else:
            shaft = '중간'
    

    # 질문에 대한 쿼리문
    query = "SELECT * FROM racket"
    balance_query = f"balance LIKE '%{balance}%'"
    shaft_query = f"shaft LIKE '{shaft}%'"
    weight_query = f"(weight = '{weight_list[0]}' OR weight = '{weight_list[1]}')"
    
    if price == 30:
        price_query = f"price >= {price*10000}"
    elif price != -1:
        price_query = f"price BETWEEN {price*10000} AND {(price+10)*10000}"

    full_query = query + " WHERE " + balance_query + " AND " + shaft_query + " AND " + weight_query + " AND " + price_query
    data = await database.fetch_all(full_query)
    if len(data) == 1:
        pass
    
    
    
    # 내가 보유한 라켓 입력 여부에 따른 추천
    if len(racket_id) > 0:
        pass
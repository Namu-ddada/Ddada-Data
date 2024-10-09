# -*- coding: utf-8 -*-
import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part, SafetySetting
from config import GOOGLE_APPLICATION_CREDENTIALS
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_APPLICATION_CREDENTIALS

def generate(score, lose, skill, strategy, mental):
    vertexai.init(project="ultra-hologram-438113-u3", location="us-central1")
    model = GenerativeModel(
        "gemini-1.0-pro-002",
    )

    text1 = """득점율, 1-실점율(실점하는 비율이 낮으면 낮을수록 높은 값), 기술력(다양한 기술에 대한 습득력, 활용력이 얼마나 좋은지), 
            전략적(상대 선수를 잘 파악해서 약점 공략을 잘 하는지), 멘탈(멘탈적인 부분으로 10점 이상인 상황에서 1,2점 차이로 접점일때 얼마나 득점을 많이 하는지, 
            연속적인 실점 후 다시 득점을 하기까지 얼마나 걸리는지, 15점 이상일 때의 득점율과 실점율이 얼마나 되는지 등을 전반적으로 평가) 이렇게 5가지의 지표에 따라 
            배드민턴 선수 유형을 나눌려고 해. 이 5가지 지표는 100점 만점으로 되어있는 지표이고, 각 지표별로 0~30점, 30~65점, 65~100점을 부족, 평균, 우수로 나눌거야.
            이 5가지 지표와 부족, 평균, 우수로 나올 수 있는 조합에 따라 배드민턴 선수 유형을 나누고 싶어. 내가 다음과 같이 정보를 주면 유형을 알려줄 수 있을까? 
            득점율: 70, 1-실점율: 20, 기술력: 40, 전략적: 80, 멘탈: 30 이런식으로 정보를 줄게. 그러면 너는 배드민턴 전문가가 되어서 무조건 다음과 같은 딕셔너리 형식으로만 반환값을 줘. 
            {type: ~~ 플레이어, type_message: ~~~} type에는 선수의 유형, type_message에는 그 유형과 내가 준 정보에 의한 각 지표의 점수를 반영해서 해당 플레이어의 성향을 설명해주고,
            혹시나 훌륭한 점이 있다면 그 부분에 대한 칭찬, 부족한 점이 있다면 그 부분에 대한 보완이 필요하다는 식의 조언을 남겨주면 돼. 너의 대답 예시를 알려줄게. 
            {type: 공격형 플레이어, 
            type_message: 공격적으로 경기를 주도하며, 약점을 빠르게 파악해 상대를 압박하는 데에 능숙하네요! 다만, 경기 중 멘탈이 흔들리고, 실점을 허용할 때가 많습니다. 
            실점율은 줄이고, 위기 상황에서도 득점을 이어가기 위해 수비를 강화하고, 집중력을 꾸준히 유지하는 연습을 해보는건 어떨까요?} 
            type과 type_message는 이러한 형식으로 주면 돼. type과 type_message 말고는 무조건 한글로만 작성해서 다음 정보에 대해 답을 줘.
            주의할건 무조건 저 딕셔너리 형식으로만 답을 줘야한다는거야.""" + f"득점율: {score}, 1-실점율: {lose}, 기술력: {skill}, 전략적: {strategy}, 멘탈: {mental}"

    generation_config = {
        "max_output_tokens": 2048,
        "temperature": 1,
        "top_p": 1,
    }

    safety_settings = [
        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
            threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
        ),
        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
            threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
        ),
        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
            threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
        ),
        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
            threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
        ),
    ]
    responses = model.generate_content(
        [text1],
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=True,
    )
    
    result = ""
    for response in responses:
        result += response.text
    
    return result

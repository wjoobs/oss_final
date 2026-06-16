import os

import pandas as pd
import requests
import streamlit as st


TEAMS = [
    "KIA 타이거즈",
    "LG 트윈스",
    "두산 베어스",
    "롯데 자이언츠",
    "삼성 라이온즈",
    "한화 이글스",
    "SSG 랜더스",
    "KT 위즈",
    "NC 다이노스",
    "키움 히어로즈",
]

PLAYERS = [
    "김도영",
    "나성범",
    "양현종",
    "오스틴 딘",
    "홍창기",
    "임찬규",
    "양의지",
    "정수빈",
    "곽빈",
    "전준우",
    "손호영",
    "나균안",
    "구자욱",
    "원태인",
    "강민호",
    "류현진",
    "노시환",
    "문동주",
    "최정",
    "김광현",
    "최지훈",
    "강백호",
    "고영표",
    "박영현",
    "박건우",
    "김주원",
    "신민혁",
    "송성문",
    "이주형",
    "김건희",
]


API_URL = os.getenv("API_URL", "http://back:8000").rstrip("/")

st.set_page_config(page_title="KBO 입문자를 위한 MZ식 응원팀 추천기", page_icon="⚾")
st.title("KBO 입문자를 위한 MZ식 응원팀 추천기")
st.subheader("도파민, 직관, 멘탈로 고르는 나의 KBO 팀")

with st.sidebar:
    st.caption("FastAPI 연결 상태")
    try:
        health_response = requests.get(f"{API_URL}/", timeout=3)
        if health_response.ok:
            st.success("FastAPI 연결 성공")
            st.info(f"API 서버: {API_URL}")
        else:
            st.warning(f"FastAPI 응답 오류: {health_response.status_code}")
    except requests.RequestException as exc:
        st.error("FastAPI 연결 실패")
        st.caption(str(exc))

st.divider()

family_fan = st.radio("질문 0. 부모님 또는 가족이 응원하는 KBO 팀이 있나요?", ["아니오", "예"])
family_team = ""
if family_fan == "예":
    family_team = st.selectbox("가족이 응원하는 팀은 어디인가요?", TEAMS)

favorite_player_exists = st.radio("질문 1. 좋아하는 KBO 선수가 있나요?", ["아니오", "예"])
favorite_player = ""
if favorite_player_exists == "예":
    favorite_player = st.selectbox("좋아하는 선수를 선택해주세요.", PLAYERS)

dopamine_style = st.radio(
    "질문 2. 도파민에 절여졌습니까?",
    [
        "네. 매 경기 감정기복 원합니다.",
        "적당히요. 재밌으면 좋지만 너무 힘든 건 싫어요.",
        "아니요. 편안하게 보고 싶습니다.",
    ],
)

baseball_style = st.radio(
    "질문 3. 어떤 야구가 더 끌립니까?",
    ["화끈한 공격야구", "나름 실리적인 야구", "투수전과 수비 안정감", "밈과 서사가 많은 야구"],
)

operation_style = st.radio(
    "질문 4. 팀 운영 스타일은 어떤 게 좋습니까?",
    [
        "원하는 선수 잘 사오는 팀이 좋다",
        "이상한 행보를 화끈하게 보여주는 팀도 재밌다",
        "육성으로 키워내는 팀이 좋다",
        "전통과 안정감이 있는 팀이 좋다",
    ],
)

live_game_preference = st.radio(
    "질문 5. 직관 좋아하십니까?",
    ["네. 야구장은 직접 가야죠.", "가끔 가고 싶습니다.", "아니요. 집에서 편하게 볼래요."],
)
residence = ""
if live_game_preference in ["네. 야구장은 직접 가야죠.", "가끔 가고 싶습니다."]:
    residence = st.selectbox(
        "질문 5-1. 직관 기준 거주지는 어디에 가깝습니까?",
        [
            "광주/전라",
            "서울",
            "대구/경북",
            "부산",
            "경남",
            "강원",
            "대전/충청",
            "인천/경기 서부",
            "제주",
            "수원/경기 동남부",
            "상관없음",
        ],
    )

fan_life_style = st.radio(
    "질문 6. 나는 어떤 팬 생활이 좋습니까?",
    [
        "응원하는 사람이 많은 팀이 좋다",
        "남들이랑 많이 안 겹치는 팀이 좋다",
        "멘탈이 강해서 고통도 콘텐츠다",
        "스포츠로 스트레스 받고 싶지 않다",
    ],
)

payload = {
    "family_fan": family_fan,
    "family_team": family_team,
    "favorite_player_exists": favorite_player_exists,
    "favorite_player": favorite_player,
    "dopamine_style": dopamine_style,
    "baseball_style": baseball_style,
    "operation_style": operation_style,
    "live_game_preference": live_game_preference,
    "residence": residence,
    "fan_life_style": fan_life_style,
}

st.divider()

if st.button("응원팀 추천받기", type="primary"):
    try:
        response = requests.post(f"{API_URL}/recommend", json=payload, timeout=5)
        response.raise_for_status()
        result = response.json()
        st.success("FastAPI에서 추천 결과를 받았습니다.")

        st.header(result["recommended_team"])
        st.write(f"**추천 이유**: {result['reason']}")
        st.write(f"**입문 포인트**: {result['beginner_point']}")
        st.write(f"**주의사항**: {result['warning']}")

        sub_candidates = result.get("sub_candidates", [])
        if sub_candidates:
            st.write(f"**다른 후보 팀 2개**: {', '.join(sub_candidates)}")
        else:
            st.write("**다른 후보 팀 2개**: 없음")

        score_df = (
            pd.DataFrame(
                [{"팀": team, "점수": score} for team, score in result["scores"].items()]
            )
            .sort_values("점수", ascending=False)
            .set_index("팀")
        )
        st.subheader("팀별 점수")
        st.bar_chart(score_df)
        st.dataframe(score_df, use_container_width=True)
    except requests.RequestException as exc:
        st.error("추천 요청 중 FastAPI 연결 문제가 발생했습니다.")
        st.caption(str(exc))

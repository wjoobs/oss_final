from typing import Dict, List, Optional

from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(title="KBO Team Recommender API")

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

PLAYER_TEAM_MAP = {
    "김도영": "KIA 타이거즈",
    "나성범": "KIA 타이거즈",
    "양현종": "KIA 타이거즈",
    "오스틴 딘": "LG 트윈스",
    "홍창기": "LG 트윈스",
    "임찬규": "LG 트윈스",
    "양의지": "두산 베어스",
    "정수빈": "두산 베어스",
    "곽빈": "두산 베어스",
    "전준우": "롯데 자이언츠",
    "손호영": "롯데 자이언츠",
    "나균안": "롯데 자이언츠",
    "구자욱": "삼성 라이온즈",
    "원태인": "삼성 라이온즈",
    "강민호": "삼성 라이온즈",
    "류현진": "한화 이글스",
    "노시환": "한화 이글스",
    "문동주": "한화 이글스",
    "최정": "SSG 랜더스",
    "김광현": "SSG 랜더스",
    "최지훈": "SSG 랜더스",
    "강백호": "KT 위즈",
    "고영표": "KT 위즈",
    "박영현": "KT 위즈",
    "박건우": "NC 다이노스",
    "김주원": "NC 다이노스",
    "신민혁": "NC 다이노스",
    "송성문": "키움 히어로즈",
    "이주형": "키움 히어로즈",
    "김건희": "키움 히어로즈",
}

TEAM_DESCRIPTIONS = {
    "KIA 타이거즈": "전통, 우승 역사, 강한 팬덤, 화끈한 경기 흐름을 함께 즐기고 싶은 입문자에게 잘 맞는 팀입니다.",
    "LG 트윈스": "비교적 안정적인 전력과 큰 팬덤, 직관 접근성을 함께 원하는 입문자에게 잘 맞는 팀입니다.",
    "두산 베어스": "잠실 야구장 직관 환경과 탄탄한 팀 이미지를 선호하는 입문자에게 잘 맞는 팀입니다.",
    "롯데 자이언츠": "야구의 낭만, 응원 문화, 감정 기복까지 함께 즐기고 싶은 입문자에게 잘 맞는 팀입니다.",
    "삼성 라이온즈": "전통 명문 이미지와 오랜 팬덤, 안정적인 야구 문화를 선호하는 입문자에게 잘 맞는 팀입니다.",
    "한화 이글스": "서사, 낭만, 팬덤의 열정, 그리고 원하는 선수를 데려오는 적극적인 운영을 즐기고 싶은 입문자에게 잘 맞는 팀입니다.",
    "SSG 랜더스": "수도권 기반의 실속 있는 팀 이미지와 적당한 팬덤 규모를 원하는 입문자에게 잘 맞는 팀입니다.",
    "KT 위즈": "편하게 야구를 보고 싶고, 비교적 안정적인 팀을 원하는 입문자에게 잘 맞는 팀입니다.",
    "NC 다이노스": "남들과 많이 겹치지 않으면서도 신흥 강팀 이미지를 즐기고 싶은 입문자에게 잘 맞는 팀입니다.",
    "키움 히어로즈": "홍대병 성향, 선수 성장 스토리, 예측하기 어려운 운영 스타일을 좋아하는 입문자에게 잘 맞는 팀입니다.",
}

DOPAMINE_SCORES = {
    "네. 매 경기 감정기복 원합니다.": {
        "롯데 자이언츠": 3,
        "한화 이글스": 3,
        "KIA 타이거즈": 2,
        "키움 히어로즈": 2,
    },
    "적당히요. 재밌으면 좋지만 너무 힘든 건 싫어요.": {
        "LG 트윈스": 2,
        "삼성 라이온즈": 2,
        "SSG 랜더스": 2,
        "두산 베어스": 1,
    },
    "아니요. 편안하게 보고 싶습니다.": {
        "KT 위즈": 3,
        "LG 트윈스": 2,
        "두산 베어스": 2,
        "NC 다이노스": 1,
    },
}

BASEBALL_STYLE_SCORES = {
    "화끈한 공격야구": {
        "KIA 타이거즈": 3,
        "롯데 자이언츠": 2,
        "삼성 라이온즈": 2,
        "한화 이글스": 1,
    },
    "나름 실리적인 야구": {
        "KT 위즈": 3,
        "LG 트윈스": 2,
        "두산 베어스": 2,
        "SSG 랜더스": 2,
    },
    "투수전과 수비 안정감": {
        "LG 트윈스": 2,
        "두산 베어스": 2,
        "KT 위즈": 2,
        "NC 다이노스": 1,
    },
    "밈과 서사가 많은 야구": {
        "한화 이글스": 3,
        "롯데 자이언츠": 3,
        "키움 히어로즈": 2,
        "KIA 타이거즈": 2,
    },
}

OPERATION_SCORES = {
    "원하는 선수 잘 사오는 팀이 좋다": {
        "한화 이글스": 4,
        "LG 트윈스": 2,
        "SSG 랜더스": 2,
        "KIA 타이거즈": 1,
    },
    "이상한 행보를 화끈하게 보여주는 팀도 재밌다": {
        "키움 히어로즈": 3,
        "KIA 타이거즈": 2,
        "롯데 자이언츠": 2,
        "한화 이글스": 1,
    },
    "육성으로 키워내는 팀이 좋다": {
        "키움 히어로즈": 3,
        "NC 다이노스": 2,
        "KT 위즈": 2,
        "삼성 라이온즈": 1,
    },
    "전통과 안정감이 있는 팀이 좋다": {
        "KIA 타이거즈": 3,
        "삼성 라이온즈": 3,
        "LG 트윈스": 2,
        "두산 베어스": 2,
    },
}

RESIDENCE_SCORES = {
    "광주/전라": {"KIA 타이거즈": 5},
    "서울": {"LG 트윈스": 3, "두산 베어스": 3, "키움 히어로즈": 3},
    "대구/경북": {"삼성 라이온즈": 5},
    "부산": {"롯데 자이언츠": 5},
    "경남": {"NC 다이노스": 5},
    "강원": {"키움 히어로즈": 4},
    "대전/충청": {"한화 이글스": 5},
    "인천/경기 서부": {"SSG 랜더스": 5},
    "제주": {"SSG 랜더스": 4},
    "수원/경기 동남부": {"KT 위즈": 5},
    "상관없음": {},
}

FAN_LIFE_SCORES = {
    "응원하는 사람이 많은 팀이 좋다": {
        "KIA 타이거즈": 3,
        "롯데 자이언츠": 3,
        "삼성 라이온즈": 2,
        "한화 이글스": 2,
        "LG 트윈스": 2,
    },
    "남들이랑 많이 안 겹치는 팀이 좋다": {
        "KT 위즈": 3,
        "NC 다이노스": 3,
        "키움 히어로즈": 3,
        "SSG 랜더스": 1,
    },
    "멘탈이 강해서 고통도 콘텐츠다": {
        "롯데 자이언츠": 3,
        "한화 이글스": 2,
        "키움 히어로즈": 2,
        "KIA 타이거즈": 1,
    },
    "스포츠로 스트레스 받고 싶지 않다": {
        "KT 위즈": 3,
        "LG 트윈스": 2,
        "두산 베어스": 2,
        "롯데 자이언츠": -3,
        "한화 이글스": -2,
    },
}


class RecommendRequest(BaseModel):
    family_fan: str
    family_team: Optional[str] = ""
    favorite_player_exists: str
    favorite_player: Optional[str] = ""
    dopamine_style: str
    baseball_style: str
    operation_style: str
    live_game_preference: str
    residence: Optional[str] = ""
    fan_life_style: str


class RecommendResponse(BaseModel):
    recommended_team: str
    reason: str
    beginner_point: str
    warning: str
    sub_candidates: List[str]
    scores: Dict[str, float]


def empty_scores() -> Dict[str, float]:
    return {team: 0 for team in TEAMS}


def scores_for_selected_team(team: str) -> Dict[str, float]:
    scores = empty_scores()
    scores[team] = 10
    return scores


def get_sub_candidates(scores: Dict[str, float], recommended_team: str) -> List[str]:
    return [
        team
        for team, _ in sorted(scores.items(), key=lambda item: item[1], reverse=True)
        if team != recommended_team
    ][:2]


def add_scores(scores: Dict[str, float], additions: Dict[str, float], multiplier: float = 1) -> None:
    for team, point in additions.items():
        scores[team] += point * multiplier


def recommend_family_team(family_team: str) -> RecommendResponse:
    scores = scores_for_selected_team(family_team)
    return RecommendResponse(
        recommended_team=family_team,
        reason=f"가족이 이미 {family_team}을 응원하고 있기 때문에, 함께 경기를 보며 자연스럽게 KBO에 입문하기 좋은 팀입니다.",
        beginner_point="처음에는 가족과 함께 경기를 보면서 선수, 응원가, 팀 분위기를 익히는 것을 추천합니다.",
        warning="가족 응원팀으로 입문하면 편하지만, 나중에 본인 취향에 따라 다른 팀을 좋아하게 되어도 괜찮습니다.",
        sub_candidates=get_sub_candidates(scores, family_team),
        scores=scores,
    )


def recommend_player_team(player_name: str) -> RecommendResponse:
    team = PLAYER_TEAM_MAP.get(player_name)
    if not team:
        scores = empty_scores()
        return recommend_by_score(scores)

    scores = scores_for_selected_team(team)
    return RecommendResponse(
        recommended_team=team,
        reason=f"선택한 선수 {player_name}이 {team} 소속이므로, 해당 선수를 중심으로 KBO에 입문하기 좋은 팀입니다.",
        beginner_point="처음에는 좋아하는 선수의 경기, 하이라이트, 인터뷰를 보면서 팀 분위기를 익히는 것을 추천합니다.",
        warning="선수 이적이나 은퇴로 소속이 바뀔 수 있으므로, 이후에는 팀의 응원 문화와 경기 스타일도 함께 살펴보는 것이 좋습니다.",
        sub_candidates=get_sub_candidates(scores, team),
        scores=scores,
    )


def calculate_scores(request: RecommendRequest) -> Dict[str, float]:
    scores = empty_scores()
    add_scores(scores, DOPAMINE_SCORES.get(request.dopamine_style, {}))
    add_scores(scores, BASEBALL_STYLE_SCORES.get(request.baseball_style, {}))
    add_scores(scores, OPERATION_SCORES.get(request.operation_style, {}))

    if request.live_game_preference == "네. 야구장은 직접 가야죠.":
        add_scores(scores, RESIDENCE_SCORES.get(request.residence or "", {}))
    elif request.live_game_preference == "가끔 가고 싶습니다.":
        add_scores(scores, RESIDENCE_SCORES.get(request.residence or "", {}), multiplier=0.7)

    add_scores(scores, FAN_LIFE_SCORES.get(request.fan_life_style, {}))
    return {team: round(score, 1) for team, score in scores.items()}


def recommend_by_score(scores: Dict[str, float], request: Optional[RecommendRequest] = None) -> RecommendResponse:
    recommended_team = max(scores, key=scores.get)
    return RecommendResponse(
        recommended_team=recommended_team,
        reason=TEAM_DESCRIPTIONS[recommended_team],
        beginner_point="처음에는 추천 팀의 최근 경기 하이라이트와 대표 선수, 응원가를 가볍게 보면서 입문해보세요.",
        warning="이 추천은 입문용 성향 매칭이므로 실제 시즌 성적, 선수 이적, 감독 교체에 따라 체감이 달라질 수 있습니다.",
        sub_candidates=get_sub_candidates(scores, recommended_team),
        scores=scores,
    )


@app.get("/")
def root():
    return {"message": "KBO team recommender API is running"}


@app.post("/recommend", response_model=RecommendResponse)
def recommend(request: RecommendRequest):
    if request.family_fan == "예" and request.family_team:
        return recommend_family_team(request.family_team)

    if request.favorite_player_exists == "예" and request.favorite_player:
        return recommend_player_team(request.favorite_player)

    scores = calculate_scores(request)
    return recommend_by_score(scores, request)

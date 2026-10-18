from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Any, Dict

app = FastAPI(title="Binary Search Step Visualizer API")

# ==========================================
# CORS(Cross-Origin Resource Sharing) 설정
# ==========================================
# Google Apps Script 및 외부 도메인에서의 API 요청을 허용하기 위한 설정입니다.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # 모든 오리진 허용 (필요시 특정 도메인으로 제한 가능)
    allow_credentials=True,
    allow_methods=["*"],        # 모든 HTTP 메서드(GET, POST 등) 허용
    allow_headers=["*"],        # 모든 HTTP 헤더 허용
)

# 클라이언트 요청 데이터 구조 정의
class SearchRequest(BaseModel):
    array: List[int]  # 검색 대상 정수 배열
    target: int      # 찾고자 하는 목표 값

@app.get("/")
def read_root():
    """서버 상태 확인용 헬스체크 엔드포인트"""
    return {"status": "online", "message": "Binary Search Server is running"}

@app.post("/search/binary")
def binary_search(data: SearchRequest) -> Dict[str, Any]:
    """
    이진 검색(Binary Search)을 수행하고,
    각 단계별(Step-by-step) 포인터(left, mid, right) 정보와 복잡도를 반환합니다.
    """
    # 1. 이진 검색은 반드시 정렬된 배열에서만 작동하므로 오름차순 정렬을 수행합니다.
    original_array = data.array
    sorted_array = sorted(original_array)
    target = data.target

    steps = []
    left = 0
    right = len(sorted_array) - 1
    found = False
    found_index = -1
    step_count = 0

    # 2. 이진 검색 알고리즘 수행
    while left <= right:
        step_count += 1
        mid = (left + right) // 2
        mid_val = sorted_array[mid]

        is_match = (mid_val == target)

        # 현재 단계의 포인터 및 상태 기록
        step_info = {
            "step": step_count,
            "left": left,               # 탐색 범위의 왼쪽 끝 인덱스
            "right": right,             # 탐색 범위의 오른쪽 끝 인덱스
            "mid": mid,                 # 현재 비교 중인 중간 인덱스
            "mid_value": mid_val,       # 중간 인덱스의 값
            "is_match": is_match,       # 일치 여부
            # 현재 단계의 탐색 대상 인덱스 목록
            "active_indices": list(range(left, right + 1))
        }
        steps.append(step_info)

        if is_match:
            found = True
            found_index = mid
            break
        elif mid_val < target:
            # 중앙값이 목표값보다 작으면 오른쪽 절반 탐색
            left = mid + 1
        else:
            # 중앙값이 목표값보다 크면 왼쪽 절반 탐색
            right = mid - 1

    # 알고리즘 시간 및 공간 복잡도 정의
    complexity = {
        "time_best": "O(1)",          # 최선의 경우: 첫 번째 mid에서 바로 찾은 경우
        "time_worst": "O(log N)",     # 최악의 경우: 탐색 범위를 절반씩 줄여나가는 경우
        "time_average": "O(log N)",   # 평균적인 경우
        "space": "O(1)"               # 반복문 기반 제자리 검색으로 추가 메모리 최소화
    }

    return {
        "success": True,
        "target": target,
        "sorted_array": sorted_array,  # 정렬된 배열 전달
        "found": found,
        "found_index": found_index,
        "total_steps": len(steps),
        "steps": steps,
        "complexity": complexity
    }

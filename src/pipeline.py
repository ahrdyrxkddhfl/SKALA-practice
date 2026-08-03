"""
Day1 종합실습: 데이터 수집 미니 파이프라인
작성자: 황도희
작성일: 2026-08-03
설명: Open-Meteo(날씨), Countries.dev(국가정보), ip-api(IP정보) 3개 API를
      asyncio.gather()로 동시에 수집하고, Pydantic으로 타입·범위 검증한 뒤
      CSV/Parquet으로 저장하며 성능을 비교하는 파이프라인
변경내역:
- 2026-08-03: 최초 작성 (비동기 수집 + 검증 + 저장 + 테스트)
- 2026-08-03: Pydantic 범위 검증(Field ge/le) 추가, country/ip 저장 로직 추가,
              API 타임아웃 및 부분실패 방어 추가, 검증 실패 테스트 케이스 추가
- 2026-08-03: raw.get() 방어(KeyError 방지), weather 빈 데이터 방어,
              country/ip도 CSV/Parquet 저장, 응답 상태코드 로그 추가
"""

import asyncio
import time

import httpx
import pandas as pd
from pydantic import BaseModel, Field, ValidationError

# 3개 API 주소를 딕셔너리로 관리 → 나중에 API가 늘어나면 여기에 추가할것~!
URLS = {
    "weather": "https://api.open-meteo.com/v1/forecast?latitude=37.5665&longitude=126.9780&hourly=temperature_2m,precipitation_probability&forecast_days=3&timezone=Asia/Seoul",
    "country": "https://countries.dev/alpha/KOR",
    "ip": "http://ip-api.com/json/8.8.8.8",
}


# =================================================================
# Pydantic 스키마 정의 (타입 + 범위 검증)
# BaseModel 상속 + Field로 조건 지정
# =================================================================
class WeatherRecord(BaseModel):
    """시간대별 날씨 한 건(row)을 표현하는 모델"""
    time: str                                                # ISO 8601 형식 시간 문자열 (예: "2026-08-03T00:00")
    temperature: float = Field(ge=-50, le=60)                # 지구상 기온이 이 범위를 벗어나면 센서/파싱 오류로 간주
    precipitation_probability: int = Field(ge=0, le=100)     # 확률(%)이므로 논리적으로 0~100을 벗어날 수 없음


class CountryRecord(BaseModel):
    """국가 정보 한 건을 표현하는 모델"""
    name: str
    capital: str | None = None                                # 수도가 없는 나라도 있을 수 있어 Optional 처리
    population: int = Field(gt=0)                              # 인구는 논리적으로 0 이하일 수 없음 (0 초과)


class IPRecord(BaseModel):
    """IP 기반 위치 정보 한 건을 표현하는 모델"""
    country: str
    city: str
    lat: float = Field(ge=-90, le=90)                           # 위도의 물리적 한계값
    lon: float = Field(ge=-180, le=180)                         # 경도의 물리적 한계값


# ==========================
# 비동기 수집 (asyncio + httpx)
# ==========================
async def fetch(client, name, url):
    """
    API 하나를 호출하는 단일 요청 함수.
    이 함수 자체는 "1개짜리 요청"만 담당하고, 여러 개를 동시에 돌리는 건
    아래 fetch_all()의 asyncio.gather()가 담당한다 (역할 분리).
    """
    resp = await client.get(url)          # await: 응답 올 때까지 이 코루틴만 대기, 다른 코루틴은 그동안 실행됨
    resp.raise_for_status()               # 상태코드가 4xx/5xx면 여기서 예외를 던짐 (200번대만 통과)
    print(f"[응답 확인] {name}: status={resp.status_code}")  # 응답 정상 확인: 요구사항의 증거를 로그로 남김
    return name, resp.json()              # (API이름, JSON데이터) 튜플로 반환 → 나중에 dict로 합치기 위함


async def fetch_all():
    """
    3개 API를 동시에 호출하는 함수.
    - timeout=10.0: API 응답이 10초 넘게 안 오면 자동으로 실패 처리 (무한 대기 방지)
    - return_exceptions=True: 3개 중 하나가 실패해도 나머지 2개는 정상적으로 결과를 받음
      (이게 없으면 하나만 실패해도 gather() 자체가 예외를 던지며 전체가 중단됨)
    """
    async with httpx.AsyncClient(timeout=10.0) as client:
        # 3개의 fetch() 코루틴을 리스트로 준비만 해둠 (아직 실행 안 됨)
        tasks = [fetch(client, name, url) for name, url in URLS.items()]
        # 여기서 3개를 동시에 실행 → 순차 호출이었다면 걸릴 시간의 합이 아니라
        # 가장 느린 API 하나의 응답 시간 정도로 전체가 끝남 (동시 수집의 핵심 이점)
        results = await asyncio.gather(*tasks, return_exceptions=True)

    output = {}
    # zip으로 URLS의 키(API이름)와 results(응답 또는 예외)를 한 쌍씩 순회
    for name, result in zip(URLS.keys(), results):
        if isinstance(result, BaseException):
            # 이 API만 실패한 것 — 프로그램을 멈추지 않고 경고만 출력하고 넘어감
            print(f"[경고] {name} API 호출 실패: {result}")
        else:
            _, content = result           # (이름, JSON) 튜플에서 JSON 부분만 꺼냄 (이름은 이미 알고 있으므로 버림)
            output[name] = content
    return output


# ====================================================================
# 스키마 검증 (raw dict -> Pydantic 모델)
# 모든 필드 접근을 raw.get()으로 하는 이유:
#   raw.get("key")는 키가 없으면 그냥 None을 반환하고, 그 None이 Pydantic에 전달되면
#   이 필드는 str이어야 하는데 None이 왔다-라는 식으로 ValidationError로
#   통일되어 처리
# =====================================================================
def parse_weather(raw):
    """weather API의 hourly 리스트 구조(시간 배열 3개)를 한 시간대씩 레코드로 풀어서 검증"""
    hourly = raw.get("hourly", {})                # hourly 키 자체가 없을 수도 있으니 기본값 {}
    times = hourly.get("time", [])
    temps = hourly.get("temperature_2m", [])
    precips = hourly.get("precipitation_probability", [])

    records = []
    # zip으로 세 리스트를 동시에 순회: 같은 인덱스의 time/temp/precip이 한 시간대의 데이터
    for t, temp, precip in zip(times, temps, precips):
        try:
            record = WeatherRecord(time=t, temperature=temp, precipitation_probability=precip)
            records.append(record)        # 검증 통과한 것만 결과 리스트에 추가
        except ValidationError as e:
            # 한 시간대 데이터가 이상해도 전체를 멈추지 않고, 그 건만 건너뛰고 계속 진행
            print("weather 검증 실패:", e)
    return records


def parse_country(raw):
    """country API 응답에서 필요한 필드만 추출해 CountryRecord로 검증"""
    try:
        return CountryRecord(
            name=raw.get("name"),
            capital=raw.get("capital"),
            population=raw.get("population"),
        )
    except ValidationError as e:
        print("country 검증 실패:", e)
        return None                       # 실패 시 None 반환 → 검증 실패 판단 가능


def parse_ip(raw):
    """ip API 응답에서 필요한 필드만 추출해 IPRecord로 검증"""
    try:
        return IPRecord(
            country=raw.get("country"),
            city=raw.get("city"),
            lat=raw.get("lat"),
            lon=raw.get("lon"),
        )
    except ValidationError as e:
        print("ip 검증 실패:", e)
        return None


def save_csv_parquet(df, prefix):
    """
    DataFrame 하나를 CSV와 Parquet 두 형식으로 각각 저장하고 다시 읽어보면서
    쓰기/읽기에 걸린 시간을 측정해서 4개 숫자로 반환하는 공용 함수.
    weather/country/ip 저장 로직이 거의 똑같아서 중복을 줄이려고 함수로 뺌.
    """
    t0 = time.time()
    df.to_csv(f"{prefix}.csv", index=False)     # index=False: 불필요한 행 번호 컬럼 저장 안 함
    csv_write_time = time.time() - t0

    t0 = time.time()
    pd.read_csv(f"{prefix}.csv")                 # 저장한 파일을 다시 읽어서 읽기 시간도 같이 측정
    csv_read_time = time.time() - t0

    t0 = time.time()
    df.to_parquet(f"{prefix}.parquet")           # Parquet: 컬럼 지향 이진 포맷, pyarrow 필요
    parquet_write_time = time.time() - t0

    t0 = time.time()
    pd.read_parquet(f"{prefix}.parquet")
    parquet_read_time = time.time() - t0

    return csv_write_time, csv_read_time, parquet_write_time, parquet_read_time


if __name__ == "__main__":
    # 1) 3개 API 동시 수집 (asyncio.run이 이벤트 루프를 새로 만들어서 fetch_all()을 실행)
    data = asyncio.run(fetch_all())

    # 2) 수집한 raw 데이터를 각각의 Pydantic 모델로 검증
    #    in data 체크: 해당 API가 fetch_all()에서 실패해서 아예 없을 수도 있으므로 방어
    weather_records = parse_weather(data["weather"]) if "weather" in data else []
    country_record = parse_country(data["country"]) if "country" in data else None
    ip_record = parse_ip(data["ip"]) if "ip" in data else None

    print(f"[검증] weather 레코드 수: {len(weather_records)}")
    if weather_records:
        print(f"[검증] weather 샘플: {weather_records[0]}")
    print(f"[검증] country: {country_record}")
    print(f"[검증] ip: {ip_record}")

    # ================================================================
    # weather: CSV vs Parquet 저장 + 성능 비교
    # weather만 성능 비교의 대표로 삼은 이유: 72건이라 표본이 있어서 포맷 간 속도
    # 차이를 재는 게 의미 있음. country/ip는 1건뿐이라 시간차가 사실상 노이즈 수준.
    # ================================================================
    if weather_records:
        # model_dump(): Pydantic 객체를 순수 dict로 변환 (DataFrame이 dict 리스트를 받을 수 있어서)
        weather_df = pd.DataFrame([r.model_dump() for r in weather_records])
        cw, cr, pw, pr = save_csv_parquet(weather_df, "output")
        print(f"[성능] weather CSV     - 쓰기: {cw:.6f}s / 읽기: {cr:.6f}s")
        print(f"[성능] weather Parquet - 쓰기: {pw:.6f}s / 읽기: {pr:.6f}s")
    else:
        # weather API가 실패해서 records가 비어있으면, 빈 DataFrame으로 저장을 시도하다
        # pd.read_csv()에서 EmptyDataError가 나는 걸 방지하기 위해 아예 건너뜀
        print("[경고] weather 데이터가 없어 CSV/Parquet 저장을 건너뜁니다")

    # =============================================================
    # country/ip: 검증 통과 데이터도 CSV·Parquet로 저장
    # ==============================================================
    if country_record:
        country_df = pd.DataFrame([country_record.model_dump()])   # 1행짜리 DataFrame
        country_df.to_csv("country_output.csv", index=False)
        country_df.to_parquet("country_output.parquet")
        print("[저장] country -> country_output.csv / country_output.parquet")

    if ip_record:
        ip_df = pd.DataFrame([ip_record.model_dump()])
        ip_df.to_csv("ip_output.csv", index=False)
        ip_df.to_parquet("ip_output.parquet")
        print("[저장] ip -> ip_output.csv / ip_output.parquet")
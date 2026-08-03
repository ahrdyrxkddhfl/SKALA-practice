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
"""

import asyncio
import json
import time

import httpx
import pandas as pd
from pydantic import BaseModel, Field, ValidationError

URLS = {
    "weather": "https://api.open-meteo.com/v1/forecast?latitude=37.5665&longitude=126.9780&hourly=temperature_2m,precipitation_probability&forecast_days=3&timezone=Asia/Seoul",
    "country": "https://countries.dev/alpha/KOR",
    "ip": "http://ip-api.com/json/8.8.8.8",
}


# ===============
# Pydantic 스키마 정의 (타입 + 범위 검증)
# ===============
class WeatherRecord(BaseModel):
    time: str
    temperature: float = Field(ge=-50, le=60)              # 현실적인 기온 범위(°C)
    precipitation_probability: int = Field(ge=0, le=100)    # 확률(%)이므로 0~100


class CountryRecord(BaseModel):
    name: str
    capital: str | None = None
    population: int = Field(gt=0)                            # 인구는 0보다 커야 함


class IPRecord(BaseModel):
    country: str
    city: str
    lat: float = Field(ge=-90, le=90)                         # 위도 범위
    lon: float = Field(ge=-180, le=180)                       # 경도 범위


# ===============
# 비동기 수집 (asyncio + httpx)
# ===============
async def fetch(client, name, url):
    """단일 API 요청. 실패하면 예외를 그대로 위로 전달(gather에서 처리)"""
    resp = await client.get(url)
    resp.raise_for_status()      # 상태코드가 4xx/5xx면 예외 발생
    return name, resp.json()


async def fetch_all():
    """3개 API를 동시에 호출. 타임아웃 지정 + 일부 실패해도 나머지는 살림"""
    async with httpx.AsyncClient(timeout=10.0) as client:
        tasks = [fetch(client, name, url) for name, url in URLS.items()]
        results = await asyncio.gather(*tasks, return_exceptions=True)

    output = {}
    for name, result in zip(URLS.keys(), results):
        if isinstance(result, BaseException):
            print(f"[경고] {name} API 호출 실패: {result}")
        else:
            _, content = result
            output[name] = content
    return output


# ===============
# 스키마 검증 (raw dict -> Pydantic 모델)
# ===============
def parse_weather(raw):
    """weather API의 hourly 리스트 구조를 시간대별 레코드로 풀어서 검증"""
    hourly = raw["hourly"]
    records = []
    for t, temp, precip in zip(
        hourly["time"], hourly["temperature_2m"], hourly["precipitation_probability"]
    ):
        try:
            record = WeatherRecord(time=t, temperature=temp, precipitation_probability=precip)
            records.append(record)
        except ValidationError as e:
            print("weather 검증 실패:", e)
    return records


def parse_country(raw):
    """country API 응답에서 필요한 필드만 추출해 CountryRecord로 검증"""
    try:
        return CountryRecord(name=raw["name"], capital=raw.get("capital"), population=raw["population"])
    except ValidationError as e:
        print("country 검증 실패:", e)
        return None


def parse_ip(raw):
    """ip API 응답에서 필요한 필드만 추출해 IPRecord로 검증"""
    try:
        return IPRecord(country=raw["country"], city=raw["city"], lat=raw["lat"], lon=raw["lon"])
    except ValidationError as e:
        print("ip 검증 실패:", e)
        return None


if __name__ == "__main__":
    data = asyncio.run(fetch_all())

    weather_records = parse_weather(data["weather"]) if "weather" in data else []
    country_record = parse_country(data["country"]) if "country" in data else None
    ip_record = parse_ip(data["ip"]) if "ip" in data else None

    print(f"[검증] weather 레코드 수: {len(weather_records)}")
    if weather_records:
        print(f"[검증] weather 샘플: {weather_records[0]}")
    print(f"[검증] country: {country_record}")
    print(f"[검증] ip: {ip_record}")

    # ===============
    # weather: CSV vs Parquet 저장 + 성능 비교 (여러 건이라 포맷 비교에 적합)
    # ===============
    df = pd.DataFrame([record.model_dump() for record in weather_records])

    t0 = time.time()
    df.to_csv("output.csv", index=False)
    csv_write_time = time.time() - t0

    t0 = time.time()
    pd.read_csv("output.csv")
    csv_read_time = time.time() - t0

    t0 = time.time()
    df.to_parquet("output.parquet")
    parquet_write_time = time.time() - t0

    t0 = time.time()
    pd.read_parquet("output.parquet")
    parquet_read_time = time.time() - t0

    print(f"[성능] CSV     - 쓰기: {csv_write_time:.6f}s / 읽기: {csv_read_time:.6f}s")
    print(f"[성능] Parquet - 쓰기: {parquet_write_time:.6f}s / 읽기: {parquet_read_time:.6f}s")

    # ===============
    # country/ip: 검증 통과 데이터도 별도 저장 (요구사항: 검증 통과 데이터 저장)
    # ===============
    with open("validated_summary.json", "w", encoding="utf-8") as f:
        json.dump(
            {
                "country": country_record.model_dump() if country_record else None,
                "ip": ip_record.model_dump() if ip_record else None,
            },
            f,
            ensure_ascii=False,
            indent=2,
        )
    print("[저장] country/ip 검증 결과 -> validated_summary.json")
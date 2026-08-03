"""
Day1 종합실습: 데이터 수집 미니 파이프라인
작성자: 황도희
작성일: 2026-08-03
설명: Open-Meteo(날씨), Countries.dev(국가정보), ip-api(IP정보) 3개 API를
      asyncio.gather()로 동시에 수집하는 파이프라인
변경내역: (나중에 수정하면 여기에 한 줄씩 추가)
"""

import asyncio
import time

import httpx
import pandas as pd

URLS = {
    "weather": "https://api.open-meteo.com/v1/forecast?latitude=37.5665&longitude=126.9780&hourly=temperature_2m,precipitation_probability&forecast_days=3&timezone=Asia/Seoul",
    "country": "https://countries.dev/alpha/KOR",
    "ip": "http://ip-api.com/json/8.8.8.8",
}


async def fetch(client, name, url):
    resp = await client.get(url)          # 해당 API에 요청 보내고 응답 기다림
    resp.raise_for_status()               # 상태코드가 에러(4xx, 5xx)면 예외 발생
    return name, resp.json()              # (이름, JSON데이터) 튜플로 반환


async def fetch_all():
    async with httpx.AsyncClient() as client:
        tasks = [fetch(client, name, url) for name, url in URLS.items()]  # 3개 요청을 준비만 해둠
        results = await asyncio.gather(*tasks)   # 여기서 3개를 동시에 실행
    return dict(results)                          # {"weather": {...}, "country": {...}, "ip": {...}}


# ================
# pydantic 모델+검증
# ================
from pydantic import BaseModel, ValidationError


class WeatherRecord(BaseModel):
    time: str
    temperature: float
    precipitation_probability: int


class CountryRecord(BaseModel):
    name: str
    capital: str | None = None
    population: int


class IPRecord(BaseModel):
    country: str
    city: str
    lat: float
    lon: float


def parse_weather(raw):
    """weather API의 리스트 구조를 시간대별 레코드 리스트로 변환 후 검증"""
    hourly = raw["hourly"]
    records = []
    for t, temp, precip in zip(hourly["time"], hourly["temperature_2m"], hourly["precipitation_probability"]):
        try:
            record = WeatherRecord(time=t, temperature=temp, precipitation_probability=precip)
            records.append(record)
        except ValidationError as e:
            print("weather 검증 실패:", e)
    return records


def parse_country(raw):
    try:
        return CountryRecord(name=raw["name"], capital=raw.get("capital"), population=raw["population"])
    except ValidationError as e:
        print("country 검증 실패:", e)
        return None


def parse_ip(raw):
    try:
        return IPRecord(country=raw["country"], city=raw["city"], lat=raw["lat"], lon=raw["lon"])
    except ValidationError as e:
        print("ip 검증 실패:", e)
        return None
    

if __name__ == "__main__":
    data = asyncio.run(fetch_all())

    weather_records = parse_weather(data["weather"])
    country_record = parse_country(data["country"])
    ip_record = parse_ip(data["ip"])

    print(f"[검증] weather 레코드 수: {len(weather_records)}")
    print(f"[검증] weather 샘플: {weather_records[0]}")
    print(f"[검증] country: {country_record}")
    print(f"[검증] ip: {ip_record}")

    # weather 레코드들을 DataFrame으로 변환 (여러 건이라 저장 비교용으로 적합)
    df = pd.DataFrame([record.model_dump() for record in weather_records])

    # CSV 저장/읽기 시간 측정
    t0 = time.time()
    df.to_csv("output.csv", index=False)
    csv_write_time = time.time() - t0

    t0 = time.time()
    pd.read_csv("output.csv")
    csv_read_time = time.time() - t0

    # Parquet 저장/읽기 시간 측정
    t0 = time.time()
    df.to_parquet("output.parquet")
    parquet_write_time = time.time() - t0

    t0 = time.time()
    pd.read_parquet("output.parquet")
    parquet_read_time = time.time() - t0

    print(f"[성능] CSV     - 쓰기: {csv_write_time:.6f}s / 읽기: {csv_read_time:.6f}s")
    print(f"[성능] Parquet - 쓰기: {parquet_write_time:.6f}s / 읽기: {parquet_read_time:.6f}s")
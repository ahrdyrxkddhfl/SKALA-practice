"""
Day1 종합실습 테스트 코드
작성자: 황도희
작성일: 2026-08-03
설명: pipeline.py의 Pydantic 모델 검증 로직 테스트
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from pipeline import CountryRecord, IPRecord, WeatherRecord


def test_weather_record_valid():
    record = WeatherRecord(time="2026-08-03T00:00", temperature=25.3, precipitation_probability=0)
    assert record.temperature == 25.3
    assert record.precipitation_probability == 0


def test_country_record_valid():
    record = CountryRecord(name="Korea (Republic of)", capital="Seoul", population=51780579)
    assert record.capital == "Seoul"


def test_ip_record_valid():
    record = IPRecord(country="United States", city="Ashburn", lat=39.03, lon=-77.5)
    assert record.city == "Ashburn"
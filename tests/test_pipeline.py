"""
Day1 종합실습 테스트 코드
작성자: 황도희
작성일: 2026-08-03
설명: pipeline.py의 Pydantic 모델 검증 로직 테스트
      1) 정상 데이터가 통과하는지 확인
      2) 범위를 벗어난 비정상 데이터가 실제로 걸러지는지 확인
변경내역:
- 2026-08-03: 최초 작성 (정상 케이스 테스트)
- 2026-08-03: 범위 검증 실패 케이스 테스트 추가
"""

import os
import sys

import pytest
from pydantic import ValidationError

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from pipeline import CountryRecord, IPRecord, WeatherRecord


# ===============
# 정상 케이스 - 통과해야 함
# ===============
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


# ===============
# 비정상 케이스 - 반드시 검증에 걸려서 예외가 발생해야 함
# ===============
def test_weather_precipitation_out_of_range():
    """강수확률은 0~100이어야 하는데 150을 넣으면 실패해야 함"""
    with pytest.raises(ValidationError):
        WeatherRecord(time="2026-08-03T00:00", temperature=25.0, precipitation_probability=150)


def test_weather_temperature_out_of_range():
    """비현실적인 기온(200도)은 실패해야 함"""
    with pytest.raises(ValidationError):
        WeatherRecord(time="2026-08-03T00:00", temperature=200.0, precipitation_probability=10)


def test_ip_lat_out_of_range():
    """위도는 -90~90이어야 하는데 999를 넣으면 실패해야 함"""
    with pytest.raises(ValidationError):
        IPRecord(country="Test", city="Test", lat=999, lon=0)


def test_country_population_must_be_positive():
    """인구는 0보다 커야 하는데 음수를 넣으면 실패해야 함"""
    with pytest.raises(ValidationError):
        CountryRecord(name="Test", capital="Test", population=-5)
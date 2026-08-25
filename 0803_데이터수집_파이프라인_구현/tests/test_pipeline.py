"""
Day1 종합실습 테스트 코드
작성자: 황도희
작성일: 2026-08-03
설명: pipeline.py의 Pydantic 모델 검증 로직 테스트
      1) 정상 데이터가 통과하는지 확인
      2) 범위를 벗어난 비정상 데이터가 실제로 걸러지는지 확인 (범위 오류)
      3) 값 자체가 타입에 안 맞는 경우가 걸러지는지 확인 (타입 오류)
      4) 필드가 아예 없을 때(None)도 안전하게 걸러지는지 확인
변경내역:
- 2026-08-03: 최초 작성 (정상 케이스 테스트)
- 2026-08-03: 범위 검증 실패 케이스 테스트 추가
- 2026-08-03: 타입 오류 테스트, 필드 누락 테스트 추가
"""

import os
import sys

import pytest
from pydantic import ValidationError

# tests/ 폴더와 src/ 폴더가 형제 관계라, 파이썬이 기본적으로 src 안의 모듈을 찾지 못한다. 
# sys.path에 src 경로를 직접 추가해서 import가 가능하게 만듦.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from pipeline import CountryRecord, IPRecord, WeatherRecord


# =======================================
# 정상 케이스 - 조건을 모두 만족하는 값을 넣었을 때, 
# 예외 없이 정상 생성되는지 확인
# =======================================
def test_weather_record_valid():
    """정상 범위의 기온/확률 값이면 문제없이 객체가 만들어지고 값이 그대로 저장되는지"""
    record = WeatherRecord(time="2026-08-03T00:00", temperature=25.3, precipitation_probability=0)
    assert record.temperature == 25.3
    assert record.precipitation_probability == 0


def test_country_record_valid():
    """정상적인 국가 정보가 그대로 저장되는지"""
    record = CountryRecord(name="Korea (Republic of)", capital="Seoul", population=51780579)
    assert record.capital == "Seoul"


def test_ip_record_valid():
    """정상적인 IP 위치 정보가 그대로 저장되는지"""
    record = IPRecord(country="United States", city="Ashburn", lat=39.03, lon=-77.5)
    assert record.city == "Ashburn"


# ====================================================================
# 범위 오류 케이스 - 타입은 맞지만 값의 범위가 논리적으로 말이 안 되는 경우
# pytest.raises(ValidationError): 이 블록 안에서 ValidationError가 발생해야
# 테스트 통과-라는 뜻. 즉 예외가 없다면 외려 테스트 실패가 되는 구조.
# ====================================================================
def test_weather_precipitation_out_of_range():
    """강수확률은 0~100(%)이어야 하는데 150을 넣으면 Field(le=100)에 걸려 실패해야 함"""
    with pytest.raises(ValidationError):
        WeatherRecord(time="2026-08-03T00:00", temperature=25.0, precipitation_probability=150)


def test_weather_temperature_out_of_range():
    """비현실적인 기온(200도)은 Field(le=60)에 걸려 실패해야 함"""
    with pytest.raises(ValidationError):
        WeatherRecord(time="2026-08-03T00:00", temperature=200.0, precipitation_probability=10)


def test_ip_lat_out_of_range():
    """위도는 물리적으로 -90~90이어야 하는데 999를 넣으면 Field(le=90)에 걸려 실패해야 함"""
    with pytest.raises(ValidationError):
        IPRecord(country="Test", city="Test", lat=999, lon=0)


def test_country_population_must_be_positive():
    """인구는 Field(gt=0)이므로 음수를 넣으면 실패해야 함"""
    with pytest.raises(ValidationError):
        CountryRecord(name="Test", capital="Test", population=-5)


# ================================================================
# 타입 오류 케이스 - 범위가 아니라 값 자체가 그 타입으로 변환조차 안 되는 경우
# 위의 범위 오류들과 구분되는 지점: 
# 150은 int로는 유효하지만 범위를 벗어난 것,
# 맑음은 애초에 float으로 변환할 방법이 없는 진짜 타입 불일치.
# ================================================================
def test_weather_temperature_type_error():
    """temperature 자리에 숫자로 변환 불가능한 문자열이 오면 타입 오류로 실패해야 함"""
    with pytest.raises(ValidationError):
        WeatherRecord(time="2026-08-03T00:00", temperature="맑음", precipitation_probability=10)


# ====================================================================
# 필드 누락 케이스 - pipeline.py의 raw.get() 방어 로직과 짝이 되는 테스트
# raw.get()이 없는 키에 대해 None을 반환하면, 그 None이 Pydantic 필드에 들어갔을 때
# 실제로 ValidationError로 이어지는지(=KeyError가 아니라 안전하게 처리되는지) 확인
# =====================================================================
def test_country_missing_population_field():
    """population 필드 자체가 없어서 None이 들어오면 검증 실패해야 함"""
    with pytest.raises(ValidationError):
        CountryRecord(name="Test", capital="Test", population=None)
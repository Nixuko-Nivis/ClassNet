from pydantic import BaseModel
from typing import List, Optional


class AirQuality(BaseModel):
    """空气质量"""
    aqi: str
    level: str
    category: str


class HourlyForecast(BaseModel):
    """小时预报"""
    time: str
    temperature: str
    weather: str
    weatherIcon: str
    wind: str
    precipitation: str


class DailyForecast(BaseModel):
    """每日预报"""
    date: str
    dayWeather: str
    nightWeather: str
    dayTemp: str
    nightTemp: str
    dayWind: str
    nightWind: str
    sunrise: str
    sunset: str


class WeatherResponse(BaseModel):
    """天气响应"""
    code: int
    message: str
    data: dict

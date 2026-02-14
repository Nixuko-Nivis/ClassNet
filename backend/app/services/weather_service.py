from typing import Dict, Any, Optional
import requests
import redis
import json
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# Redis连接
try:
    redis_client = redis.from_url(settings.redis_url, decode_responses=True)
except Exception as e:
    logger.warning(f"Redis连接失败: {e}，将不使用缓存")
    redis_client = None


def get_weather() -> Dict[str, Any]:
    """获取天气信息"""
    # 先尝试从缓存获取
    cached_data = _get_cached_weather()
    if cached_data:
        return cached_data
    
    # 调用API获取天气数据
    try:
        weather_data = fetch_weather_data()
        # 缓存天气数据（30分钟）
        _cache_weather(weather_data)
        return weather_data
    except Exception as e:
        logger.error(f"获取天气信息失败: {e}")
        # 返回模拟数据作为 fallback
        return _get_mock_weather()


def fetch_weather_data(city: str = "北京") -> Dict[str, Any]:
    """从API获取天气数据"""
    # 这里使用 OpenWeatherMap API 作为示例
    # 实际使用时需要替换为真实的API密钥
    api_key = "your_openweathermap_api_key"
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    forecast_url = "http://api.openweathermap.org/data/2.5/forecast"
    
    # 构建请求参数
    params = {
        "q": city,
        "appid": api_key,
        "lang": "zh_cn",
        "units": "metric"
    }
    
    # 获取当前天气
    current_response = requests.get(base_url, params=params, timeout=10)
    current_data = current_response.json()
    
    # 获取预报数据
    forecast_response = requests.get(forecast_url, params=params, timeout=10)
    forecast_data = forecast_response.json()
    
    # 转换为统一格式
    return _transform_weather_data(current_data, forecast_data, city)


def _transform_weather_data(current_data: Dict[str, Any], forecast_data: Dict[str, Any], city: str) -> Dict[str, Any]:
    """转换天气数据格式"""
    # 构建当前天气数据
    weather_data = {
        "city": city,
        "temperature": f"{current_data['main']['temp']:.1f}°C",
        "feelsLike": f"{current_data['main']['feels_like']:.1f}°C",
        "weather": current_data['weather'][0]['description'],
        "weatherIcon": current_data['weather'][0]['icon'],
        "humidity": f"{current_data['main']['humidity']}%",
        "wind": f"{current_data['wind']['deg']}° {current_data['wind']['speed']}m/s",
        "pressure": f"{current_data['main']['pressure']}hPa",
        "visibility": f"{current_data.get('visibility', 10000) / 1000}km",
        "uvIndex": "中等",  # OpenWeatherMap需要单独的API调用来获取UV指数
        "airQuality": {
            "aqi": "85",
            "level": "良",
            "category": "轻度污染"
        },
        "hourlyForecast": [],
        "dailyForecast": []
    }
    
    # 构建小时预报
    hourly_data = forecast_data['list'][:8]  # 取前8个小时
    for item in hourly_data:
        hour_forecast = {
            "time": item['dt_txt'].split(' ')[1],
            "temperature": f"{item['main']['temp']:.1f}°C",
            "weather": item['weather'][0]['description'],
            "weatherIcon": item['weather'][0]['icon'],
            "wind": f"{item['wind']['deg']}° {item['wind']['speed']}m/s",
            "precipitation": f"{item.get('pop', 0) * 100:.0f}%"
        }
        weather_data['hourlyForecast'].append(hour_forecast)
    
    # 构建每日预报（简化版）
    daily_data = forecast_data['list'][::8][:3]  # 每8小时取一个，取前3天
    for item in daily_data:
        day_forecast = {
            "date": item['dt_txt'].split(' ')[0],
            "dayWeather": item['weather'][0]['description'],
            "nightWeather": item['weather'][0]['description'],
            "dayTemp": f"{item['main']['temp_max']:.1f}°C",
            "nightTemp": f"{item['main']['temp_min']:.1f}°C",
            "dayWind": f"{item['wind']['deg']}° {item['wind']['speed']}m/s",
            "nightWind": f"{item['wind']['deg']}° {item['wind']['speed']}m/s",
            "sunrise": "06:45",  # 需要单独API获取
            "sunset": "17:30"  # 需要单独API获取
        }
        weather_data['dailyForecast'].append(day_forecast)
    
    return weather_data


def _get_mock_weather() -> Dict[str, Any]:
    """获取模拟天气数据"""
    return {
        "city": "北京",
        "temperature": "25°C",
        "feelsLike": "26°C",
        "weather": "晴",
        "weatherIcon": "sunny",
        "humidity": "45%",
        "wind": "西北风 3级",
        "pressure": "1013hPa",
        "visibility": "10km",
        "uvIndex": "中等",
        "airQuality": {
            "aqi": "85",
            "level": "良",
            "category": "轻度污染"
        },
        "hourlyForecast": [
            {
                "time": "08:00",
                "temperature": "20°C",
                "weather": "晴",
                "weatherIcon": "sunny",
                "wind": "西北风 2级",
                "precipitation": "0%"
            },
            {
                "time": "12:00",
                "temperature": "25°C",
                "weather": "晴",
                "weatherIcon": "sunny",
                "wind": "西北风 3级",
                "precipitation": "0%"
            },
            {
                "time": "16:00",
                "temperature": "26°C",
                "weather": "多云",
                "weatherIcon": "cloudy",
                "wind": "西北风 2级",
                "precipitation": "0%"
            },
            {
                "time": "20:00",
                "temperature": "22°C",
                "weather": "晴",
                "weatherIcon": "clear-night",
                "wind": "西北风 1级",
                "precipitation": "0%"
            }
        ],
        "dailyForecast": [
            {
                "date": "2026-02-07",
                "dayWeather": "晴",
                "nightWeather": "晴",
                "dayTemp": "25°C",
                "nightTemp": "15°C",
                "dayWind": "西北风 3级",
                "nightWind": "西北风 1级",
                "sunrise": "06:45",
                "sunset": "17:30"
            },
            {
                "date": "2026-02-08",
                "dayWeather": "多云",
                "nightWeather": "晴",
                "dayTemp": "24°C",
                "nightTemp": "14°C",
                "dayWind": "西北风 2级",
                "nightWind": "西北风 1级",
                "sunrise": "06:46",
                "sunset": "17:31"
            },
            {
                "date": "2026-02-09",
                "dayWeather": "晴",
                "nightWeather": "多云",
                "dayTemp": "26°C",
                "nightTemp": "16°C",
                "dayWind": "东风 2级",
                "nightWind": "东风 1级",
                "sunrise": "06:47",
                "sunset": "17:32"
            }
        ]
    }


def _get_cached_weather() -> Optional[Dict[str, Any]]:
    """从缓存获取天气数据"""
    if not redis_client:
        return None
    
    try:
        cached_data = redis_client.get("weather:current")
        if cached_data and isinstance(cached_data, (str, bytes, bytearray)):
            return json.loads(cached_data)
    except Exception as e:
        logger.warning(f"从缓存获取天气数据失败: {e}")
    
    return None


def _cache_weather(weather_data: Dict[str, Any]) -> None:
    """缓存天气数据"""
    if not redis_client:
        return
    
    try:
        redis_client.setex(
            "weather:current",
            1800,  # 30分钟过期
            json.dumps(weather_data, ensure_ascii=False)
        )
    except Exception as e:
        logger.warning(f"缓存天气数据失败: {e}")

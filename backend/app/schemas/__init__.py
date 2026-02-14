from app.schemas.auth import RegisterRequest, RegisterResponse, LoginResponse, ChangePasswordRequest, ChangePasswordResponse
from app.schemas.user import UserProfileUpdate, UserProfileResponse, PasswordUpdate, PasswordUpdateResponse
from app.schemas.chat import Message, MessageCreate, MessageList
from app.schemas.media import MediaFile, MediaFileCreate, MediaFileUpdate, MediaFileList
from app.schemas.system import SystemStatusResponse
from app.schemas.weather import AirQuality, HourlyForecast, DailyForecast, WeatherResponse

__all__ = [
    "RegisterRequest", "RegisterResponse", "LoginResponse", "ChangePasswordRequest", "ChangePasswordResponse",
    "UserProfileUpdate", "UserProfileResponse", "PasswordUpdate", "PasswordUpdateResponse",
    "Message", "MessageCreate", "MessageList",
    "MediaFile", "MediaFileCreate", "MediaFileUpdate", "MediaFileList",
    "SystemStatusResponse",
    "AirQuality", "HourlyForecast", "DailyForecast", "WeatherResponse"
]

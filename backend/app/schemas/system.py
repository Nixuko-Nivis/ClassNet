from pydantic import BaseModel
from typing import Optional


class SystemStatusResponse(BaseModel):
    """系统状态响应"""
    code: int
    message: str
    data: dict

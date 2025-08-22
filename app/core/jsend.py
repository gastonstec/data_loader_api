# imports
from pydantic import BaseModel
from typing import Any, Optional


# JSend responses
class JSendSuccessResponse(BaseModel):
    status: str = "success"
    data: Any


class JSendFailResponse(BaseModel):
    status: str = "fail"
    data: Any


class JSendErrorResponse(BaseModel):
    status: str = "error"
    message: str
    code: Optional[int] = None
    data: Optional[Any] = None


def success(data: Any):
    return JSendSuccessResponse(data=data)


def fail(data: Any):
    return JSendFailResponse(data=data)


def error(message: str, code: int = None, data: Any = None):
    return JSendErrorResponse(message=message, code=code, data=data)
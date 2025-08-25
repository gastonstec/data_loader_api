# imports
from pydantic import BaseModel
from typing import Any, Optional


# JSendSuccess response
class JSendSuccessResponse(BaseModel):
    status: str = "success"
    data: Any


# JSendFail response
class JSendFailResponse(BaseModel):
    status: str = "fail"
    data: Any


# JSendError response
class JSendErrorResponse(BaseModel):
    status: str = "error"
    message: str
    code: Optional[int] = None
    data: Optional[Any] = None


# JSend success factory function
def jsend_success(data: Any):
    return JSendSuccessResponse(data=data)


# JSend fail factory function
def jsend_fail(data: Any):
    return JSendFailResponse(data=data)


# JSend error factory function
def jsend_error(
        message: str, code: Optional[int] = None, data: Any = None):
    return JSendErrorResponse(message=message, code=code, data=data)

from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse


# 全局捕获HTTP错误
async def http_error_handler(_: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse({"errors": [exc.detail]}, status_code=exc.status_code)


# 自定义404错误
class NotFound404Error(HTTPException):
    def __init__(self, detail="资源未找到"):
        super().__init__(status_code=404, detail=detail)

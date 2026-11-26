"""侧车入口：只监听 127.0.0.1，由 Go 主后端拉起并代理调用，不直接对浏览器开放。

路由按业务分文件（app/api/v1/<业务>.py），与 Go 的 api/<业务>/v1 对应；统一挂在 /py/v1 下。
"""
from fastapi import FastAPI

from app.api.v1 import demo, health

app = FastAPI(title="__SIDECAR_NAME__")

app.include_router(health.router, prefix="/py/v1")
app.include_router(demo.router, prefix="/py/v1")

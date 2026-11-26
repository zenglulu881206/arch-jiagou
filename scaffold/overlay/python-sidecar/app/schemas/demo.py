"""示例业务的请求/响应模型，与 Go 侧 api/aidemo/v1 的字段一一对应。"""
from pydantic import BaseModel, Field


class SummarizeReq(BaseModel):
    text: str = Field(min_length=1, max_length=10000)


class SummarizeRes(BaseModel):
    chars: int
    lines: int
    preview: str

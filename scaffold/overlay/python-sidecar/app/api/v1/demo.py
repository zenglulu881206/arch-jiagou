"""示例业务路由：只做参数接收与返回，计算放 app/services/demo/<场景>.py。首个真实能力落地后删除 demo。"""
from fastapi import APIRouter

from app.schemas.demo import SummarizeReq, SummarizeRes
from app.services.demo.summarize import summarize

router = APIRouter(prefix="/demo", tags=["示例"])


@router.post("/summarize", response_model=SummarizeRes)
def summarize_api(req: SummarizeReq) -> SummarizeRes:
    """场景「摘要」：转调 services，同名对应。"""
    return summarize(req)

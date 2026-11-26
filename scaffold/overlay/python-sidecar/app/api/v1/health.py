from fastapi import APIRouter

router = APIRouter(tags=["系统"])


@router.get("/health")
def health() -> dict:
    """存活探针：Go 主后端启动侧车后轮询本接口，返回 healthy=true 才算就绪。"""
    return {"healthy": True}

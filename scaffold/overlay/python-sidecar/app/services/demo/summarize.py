"""场景「摘要」：示例用纯计算，便于离线验收；真实场景在这里调用模型、向量库或 OCR。"""
from app.schemas.demo import SummarizeReq, SummarizeRes

PREVIEW_LEN = 20


def summarize(req: SummarizeReq) -> SummarizeRes:
    """统计字数、行数，截取前 20 个字作为预览；首尾空白不计。"""
    text = req.text.strip()
    return SummarizeRes(
        chars=len(text),
        lines=len(text.splitlines()) if text else 0,
        preview=text[:PREVIEW_LEN],
    )

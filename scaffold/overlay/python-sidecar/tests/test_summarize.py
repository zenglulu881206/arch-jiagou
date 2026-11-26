from fastapi.testclient import TestClient

from app.main import app
from app.schemas.demo import SummarizeReq
from app.services.demo.summarize import summarize

client = TestClient(app)


def test_summarize_service():
    res = summarize(SummarizeReq(text=" 第一行\n第二行 "))
    assert res.chars == 7
    assert res.lines == 2
    assert res.preview == "第一行\n第二行"


def test_health():
    assert client.get("/py/v1/health").json() == {"healthy": True}


def test_summarize_rejects_empty():
    assert client.post("/py/v1/demo/summarize", json={"text": ""}).status_code == 422

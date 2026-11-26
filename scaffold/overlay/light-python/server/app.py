"""
轻后端：只做存取，业务逻辑在前端单页 web/index.html。只用 Python 标准库，零第三方依赖。

接口：
- GET  /api/health          存活探针
- GET  /api/store/<key>     读一个 key 的 JSON 值；没有时返回 null
- PUT  /api/store/<key>     整体覆盖一个 key 的 JSON 值
其余路径托管 web/ 下的静态文件，页面与接口同源（双击 file:// 打开连不上接口）。

数据：data/<库名>.db，单表 kv(k, v)。每个请求单独开连接（多线程共用一个连接会报错）。
注意：PUT 是整 key 覆盖，多人同时编辑同一 key 会互相覆盖；用户变多时改标准分离。
"""
import json
import os
import re
import sqlite3
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB_DIR = ROOT / "web"
DATA_DIR = Path(os.environ.get("APP_DATA_DIR", ROOT / "data"))
DB_PATH = DATA_DIR / "__LIGHT_DB__.db"
PORT = int(os.environ.get("APP_PORT", "__LIGHT_PORT__"))
KEY_PATTERN = re.compile(r"^[a-z][a-z0-9_]{0,63}$")
MAX_BODY = 10 * 1024 * 1024


def connect() -> sqlite3.Connection:
    """打开库连接；首次运行时建目录与表。"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("CREATE TABLE IF NOT EXISTS kv (k TEXT PRIMARY KEY, v TEXT NOT NULL)")
    return conn


class Handler(SimpleHTTPRequestHandler):
    """静态文件 + /api 存取。错误统一回 {"error": 面向操作者的文案}。"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEB_DIR), **kwargs)

    def send_json(self, status: int, payload) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def store_key(self):
        """从 /api/store/<key> 取 key；不合法返回 None。"""
        key = self.path.split("?")[0].removeprefix("/api/store/")
        return key if KEY_PATTERN.match(key) else None

    def do_GET(self):
        if self.path == "/api/health":
            return self.send_json(200, {"status": "ok"})
        if self.path.startswith("/api/store/"):
            key = self.store_key()
            if key is None:
                return self.send_json(400, {"error": "数据名称不合法"})
            with connect() as conn:
                row = conn.execute("SELECT v FROM kv WHERE k = ?", (key,)).fetchone()
            return self.send_json(200, {"value": json.loads(row[0]) if row else None})
        return super().do_GET()

    def do_PUT(self):
        if not self.path.startswith("/api/store/"):
            return self.send_json(404, {"error": "地址不存在"})
        key = self.store_key()
        if key is None:
            return self.send_json(400, {"error": "数据名称不合法"})
        length = int(self.headers.get("Content-Length") or 0)
        if length > MAX_BODY:
            return self.send_json(413, {"error": "内容过大，请拆分后再保存"})
        try:
            value = json.loads(self.rfile.read(length) or b"null")
        except ValueError:
            return self.send_json(400, {"error": "内容格式不正确"})
        with connect() as conn:
            conn.execute(
                "INSERT INTO kv (k, v) VALUES (?, ?) ON CONFLICT(k) DO UPDATE SET v = excluded.v",
                (key, json.dumps(value, ensure_ascii=False)),
            )
        return self.send_json(200, {"value": value})


def main():
    server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print(f"服务已启动：http://127.0.0.1:{PORT}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()

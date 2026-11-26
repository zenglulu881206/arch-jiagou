"""标准库 unittest：起一个临时端口的服务，测健康检查、存取与非法 key。"""
import json
import os
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer

os.environ["APP_DATA_DIR"] = tempfile.mkdtemp()

from server import app  # noqa: E402


class AppTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), app.Handler)
        cls.base = f"http://127.0.0.1:{cls.server.server_address[1]}"
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()

    def call(self, method, path, body=None):
        data = None if body is None else json.dumps(body).encode()
        req = urllib.request.Request(self.base + path, data=data, method=method)
        try:
            with urllib.request.urlopen(req) as resp:
                return resp.status, json.loads(resp.read())
        except urllib.error.HTTPError as err:
            return err.code, json.loads(err.read())

    def test_health(self):
        self.assertEqual(self.call("GET", "/api/health"), (200, {"status": "ok"}))

    def test_store_roundtrip(self):
        self.assertEqual(self.call("GET", "/api/store/memo"), (200, {"value": None}))
        self.call("PUT", "/api/store/memo", {"text": "你好"})
        self.assertEqual(self.call("GET", "/api/store/memo"), (200, {"value": {"text": "你好"}}))

    def test_bad_key(self):
        status, body = self.call("GET", "/api/store/Bad-Key")
        self.assertEqual(status, 400)
        self.assertIn("不合法", body["error"])


if __name__ == "__main__":
    unittest.main()

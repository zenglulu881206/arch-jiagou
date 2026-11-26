#!/usr/bin/env python3
"""
脚手架验收：证明 init.py 生成的项目「真实可用」。按 SELECTION.json 里有哪几端就验哪几端。

用法：python3 verify.py --selection SELECTION.json --target <项目根目录> [--headless]

通过标准（全部满足才退出码 0）：
- 前端（frontend）：类型检查 + 构建；浏览器输入名字看到问候语，名字为空看到后端错误提示。
- 后端（backend）：go vet / test / build；起服后 GET /api/health 返回 code=0、status=ok。
- 侧车（backend.sidecar）：pytest；Go 起服时拉起侧车，经 Go 调 /api/aidemo/summarize 结果正确，空文字被拦下；
  Go 退出后侧车端口释放。
- 轻后端（light）：unittest；起服后健康检查；浏览器保存备忘、刷新后仍在；非法数据名返回 400。

约定端口已被占用时直接失败，不另换端口起第二份（端口在 SELECTION.json 里改）。
本脚本只关闭自己启动的进程。
"""
import argparse
import json
import os
import shutil
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path


def run(cmd, cwd):
    """执行构建/测试命令；失败即判验收不通过。"""
    print(f"$ {' '.join(cmd)}  (cwd={cwd})", flush=True)
    if subprocess.run(cmd, cwd=cwd).returncode != 0:
        sys.exit(f"验收失败：{' '.join(cmd)}")


def port_in_use(port: int) -> bool:
    """端口是否已有进程在听。"""
    with socket.socket() as sock:
        return sock.connect_ex(("127.0.0.1", port)) == 0


def wait_http(url: str, timeout=60):
    """轮询直到 url 返回 200，返回响应体；超时判失败。"""
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=2) as resp:
                return resp.read().decode("utf-8")
        except OSError:
            time.sleep(0.5)
    sys.exit(f"验收失败：{url} 在 {timeout} 秒内未就绪")


def call_json(method: str, url: str, body=None):
    """发 JSON 请求，返回 (HTTP 状态码, 解析后的响应体)。"""
    data = None if body is None else json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, method=method, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as err:
        return err.code, json.loads(err.read())


def open_page_factory(sel: dict, target: Path):
    """取项目统一浏览器入口 e2e_launch.open_page（目录规则同 init.py e2e_dir）。"""
    sys.dont_write_bytecode = True
    e2e = "admin/scripts" if sel.get("admin_zone", True) else "scripts/e2e"
    sys.path.insert(0, str(target / e2e))
    from e2e_launch import open_page
    return open_page


def greet_smoke(open_page, fe_url: str, headless: bool):
    """前端：正常问候 + 空名字反例。"""
    from playwright.sync_api import expect

    with open_page(fe_url + "/demo/greet", headless=headless) as page:
        page.get_by_placeholder("请输入名字").fill("张三")
        page.locator("[data-test=greet-submit]").click()
        expect(page.locator("[data-test=greet-message]")).to_have_text("你好，张三")

        page.get_by_placeholder("请输入名字").fill("")
        page.locator("[data-test=greet-submit]").click()
        expect(page.locator(".el-message--error")).to_contain_text("请填写名字")
    print("浏览器冒烟：正常问候 / 空名字反例 均通过")


def memo_smoke(open_page, url: str, headless: bool):
    """轻后端：保存备忘 → 刷新页面仍在。"""
    from playwright.sync_api import expect

    text = "验收备忘 " + time.strftime("%H%M%S")
    with open_page(url, headless=headless) as page:
        page.locator("[data-test=memo-text]").fill(text)
        page.locator("[data-test=memo-save]").click()
        expect(page.locator("[data-test=memo-status]")).to_have_text("已保存")
        page.reload()
        expect(page.locator("[data-test=memo-text]")).to_have_value(text)
    print("浏览器冒烟：保存备忘 / 刷新后仍在 均通过")


def verify_sidecar_api(be_port: int):
    """经 Go 调侧车：正例结果正确，空文字被 Go 校验拦下。"""
    status, body = call_json("POST", f"http://127.0.0.1:{be_port}/api/aidemo/summarize", {"text": " 第一行\n第二行 "})
    data = body.get("data") or {}
    if status != 200 or body.get("code") != 0 or data.get("chars") != 7 or data.get("lines") != 2:
        sys.exit(f"验收失败：经 Go 调侧车返回 {status} {body}")
    status, body = call_json("POST", f"http://127.0.0.1:{be_port}/api/aidemo/summarize", {"text": ""})
    if body.get("code") == 0:
        sys.exit(f"验收失败：空文字未被拦下 {body}")
    print("侧车调用：正例 / 空文字反例 均通过")


def stop(procs):
    """关闭本脚本启动的进程（逆序：先前端后后端）。"""
    for proc in reversed(procs):
        proc.terminate()
        try:
            proc.wait(timeout=15)
        except subprocess.TimeoutExpired:
            proc.kill()


def main():
    parser = argparse.ArgumentParser(description="脚手架真实可用验收")
    parser.add_argument("--selection", required=True)
    parser.add_argument("--target", required=True)
    parser.add_argument("--headless", action="store_true", help="无头运行（默认有头）")
    args = parser.parse_args()

    sel = json.loads(Path(args.selection).read_text(encoding="utf-8"))
    target = Path(args.target).resolve()
    fe = sel.get("frontend")
    be = sel.get("backend")
    sidecar = (be or {}).get("sidecar")
    light = sel.get("light")

    # 1. 构建与单测
    if fe:
        run(["npm", "run", "build"], cwd=target / fe["dir"])
    if be:
        be_root = target / be["dir"]
        run(["go", "vet", "./..."], cwd=be_root)
        run(["go", "test", "./..."], cwd=be_root)
        run(["go", "build", "-o", "bin/server", "."], cwd=be_root)
    if sidecar:
        venv = target / sidecar["dir"] / ".venv"
        python = venv / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
        run([str(python), "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider"], cwd=target / sidecar["dir"])
    if light:
        run([sys.executable, "-B", "-m", "unittest", "discover", "-s", "tests", "-t", "."], cwd=target / light["dir"])

    ports = [p for p in (fe and not (be and sel.get("deploy", {}).get("shape") == "single-binary") and fe["port"], be and be["port"], sidecar and sidecar["port"], light and light["port"]) if p]
    for port in ports:
        if port_in_use(port):
            sys.exit(f"端口 {port} 已被占用：不另起第二份，请在 SELECTION.json 改端口或先停掉占用进程")

    # 单 exe 交付：前端产物复制到后端托管目录，浏览器直接访问后端端口
    single_binary = bool(fe and be and sel.get("deploy", {}).get("shape") == "single-binary")
    if single_binary:
        web_root = target / be["dir"] / "resource/public/html"
        shutil.copytree(target / fe["dir"] / "dist", web_root, dirs_exist_ok=True)
        print(f"前端产物已复制到 {web_root}")

    # 2. 起服与浏览器冒烟
    open_page = open_page_factory(sel, target)
    procs = []
    try:
        if be:
            procs.append(subprocess.Popen([str(be_root / "bin/server")], cwd=be_root))
            health = json.loads(wait_http(f"http://127.0.0.1:{be['port']}/api/health", timeout=120))
            if health.get("code") != 0 or health["data"]["status"] != "ok":
                sys.exit(f"验收失败：健康检查返回 {health}")
            print(f"后端健康检查通过：{health}")
            if sidecar:
                verify_sidecar_api(be["port"])
        if single_binary:
            greet_smoke(open_page, f"http://127.0.0.1:{be['port']}", args.headless)
            try:
                with urllib.request.urlopen(f"http://127.0.0.1:{be['port']}/api/not-exist", timeout=5) as resp:
                    leaked = '<div id="app">' in resp.read().decode("utf-8", "ignore")
            except urllib.error.HTTPError:
                leaked = False
            if leaked:
                sys.exit("验收失败：不存在的接口被当成页面返回")
            print("后端托管前端：页面刷新回 index.html、接口 404 不被吞")
        elif fe:
            fe_root = target / fe["dir"]
            procs.append(subprocess.Popen(
                [str(fe_root / "node_modules/.bin/vite"), "preview", "--host", "127.0.0.1"], cwd=fe_root))
            fe_url = f"http://127.0.0.1:{fe['port']}"
            wait_http(fe_url)
            greet_smoke(open_page, fe_url, args.headless)
        if light:
            env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
            procs.append(subprocess.Popen([sys.executable, "server/app.py"], cwd=target / light["dir"], env=env))
            url = f"http://127.0.0.1:{light['port']}"
            health = json.loads(wait_http(url + "/api/health"))
            if health != {"status": "ok"}:
                sys.exit(f"验收失败：健康检查返回 {health}")
            status, body = call_json("GET", url + "/api/store/Bad-Key")
            if status != 400:
                sys.exit(f"验收失败：非法数据名应返回 400，实际 {status} {body}")
            print("轻后端健康检查 / 非法数据名反例 均通过")
            memo_smoke(open_page, url, args.headless)
    finally:
        stop(procs)

    if sidecar:
        time.sleep(1)
        if port_in_use(sidecar["port"]):
            sys.exit(f"验收失败：Go 退出后侧车端口 {sidecar['port']} 仍被占用")
        print("Go 退出后侧车已关闭")

    print("脚手架验收通过")


if __name__ == "__main__":
    main()

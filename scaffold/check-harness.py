#!/usr/bin/env python3
"""
harness 机器自检：把 SKILL.md 第 7 步能机器判定的项变成脚本，失败即退出码 1。

用法：python3 check-harness.py --target <项目根目录> [--selection SELECTION.json]

检查项：
1. 必备根级骨架目录、文件齐全（按 SELECTION 判断前端/后端/架构图九幅）。
2. 文档无残留占位符 {{…}} / __XXX__。
3. 根 AGENTS.md 第一章是「0. 按需加载」，链到架构图；必须存在 agent/AGENTS-继承准则.md（§2/§3/§4 全文）并在根登记。
4. 分层 AGENT 含对应模板的全部二级标题（模板是唯一标准，禁止缩成摘要）。
5. 脚手架增量目录：overlay 里的每个目录在项目里真实存在，且在对应 AGENT 里有登记。
6. 架构图：Mermaid 围栏首行是合法图类型；索引每幅图有状态（测试骨架/骨架/与现状一致/过期/N/A）。
   加 --render 时用真实 mermaid（12.3.0，首次从 npmmirror 下载到 ~/.cache）在浏览器里逐块渲染，语法错误逐条报出。
7. Markdown 相对链接可达。
"""
import argparse
import json
import re
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
TEMPLATES = SKILL / "templates"
OVERLAY = SKILL / "scaffold" / "overlay"

LAYER_AGENTS = {
    # 继承准则用 check_root 做全文锚点检查（含 {{USER_ADDRESS}} 替换后标题会变，不走进分层标题全等）
    "agent/AGENTS-前端.md": "AGENTS.frontend.md",
    "agent/AGENTS-后端.md": "AGENTS.backend.md",
    "agent/AGENTS-数据.md": "AGENTS.data.md",
    "agent/AGENTS-测试.md": "AGENTS.test.md",
    "agent/AGENTS-研发流程.md": "AGENTS.workflow.md",
    "agent/AGENTS-侧车.md": "AGENTS.sidecar.md",
    "agent/AGENTS-轻后端.md": "AGENTS.light.md",
}
DIAGRAMS = [
    "01-system-context.md", "02-containers.md", "03-backend-layers.md",
    "04-frontend-shell.md", "05-data-domains.md", "06-authz.md",
    "07-license-crypto.md", "08-deploy.md", "09-business-flow.md",
]
STATUSES = ("测试骨架", "骨架", "与现状一致", "过期", "N/A")
MERMAID_TYPES = (
    "flowchart", "graph", "sequenceDiagram", "classDiagram", "stateDiagram",
    "erDiagram", "journey", "gantt", "pie", "C4", "mindmap", "timeline",
)
PLACEHOLDER = re.compile(r"\{\{[^}]*\}\}|__(APP|FE|DB|SIDECAR|LIGHT)_[A-Z_]*[A-Z]__")
SKIP_DIR_PARTS = {"demo", "health", "aidemo"}

MERMAID_VERSION = "12.3.0"
MERMAID_CACHE = Path.home() / ".cache/arch-jiagou" / f"mermaid-{MERMAID_VERSION}.min.js"
NPM_MIRROR = "https://registry.npmmirror.com"

failures = []


def fail(msg: str):
    failures.append(msg)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def headings(text: str):
    """取二级标题文本（去掉序号差异以外原样比较）。"""
    return [line[3:].strip() for line in text.splitlines() if line.startswith("## ")]


def harness_docs(root: Path):
    """本脚本负责检查的文档集合：AGENT、架构图、项目特化、选型表。"""
    docs = [root / "AGENTS.md", root / "SELECTION.md", root / "admin/AGENTS.md"]
    docs += sorted((root / "agent").glob("*.md"))
    docs += sorted((root / "docs/架构图").glob("*.md"))
    docs += sorted((root / "docs/项目特化").glob("*.md"))
    return [p for p in docs if p.exists()]


def check_required(root: Path, sel: dict):
    required = ["AGENTS.md", "SELECTION.md", "docs/项目特化/README.md", "docs/架构图/README.md",
                "admin/scripts/e2e_launch.py",
                "agent/AGENTS-继承准则.md", "admin/AGENTS.md",
                "agent/AGENTS-数据.md", "agent/AGENTS-测试.md", "agent/AGENTS-研发流程.md"]
    if sel.get("frontend"):
        required.append("agent/AGENTS-前端.md")
    if sel.get("backend"):
        required.append("agent/AGENTS-后端.md")
    if (sel.get("backend") or {}).get("sidecar"):
        required.append("agent/AGENTS-侧车.md")
    if sel.get("light"):
        required.append("agent/AGENTS-轻后端.md")
    if sel.get("archetype", "erp-go-vue-pg") == "erp-go-vue-pg":
        required += [f"docs/架构图/{name}" for name in DIAGRAMS]
    for rel in required:
        if not (root / rel).exists():
            fail(f"[必备文件] 缺 {rel}")
    directories = [
        "admin/scripts", "admin/release", "docs/架构图", "docs/PRD及测试用例",
        "docs/项目特化", "docs/旧低代码系统调研记录", "agent", "log", "scripts", "tests",
    ]
    for rel in directories:
        if not (root / rel).is_dir():
            fail(f"[根目录骨架] 缺目录 {rel}/")


def check_placeholders(root: Path):
    for path in harness_docs(root):
        for no, line in enumerate(read(path).splitlines(), 1):
            if PLACEHOLDER.search(line):
                fail(f"[占位符] {path.relative_to(root)}:{no} {line.strip()[:80]}")


def check_root(root: Path):
    text = read(root / "AGENTS.md")
    heads = headings(text)
    if not heads or "按需加载" not in heads[0]:
        fail("[根 AGENTS] 第一章不是「0. 按需加载」")
    if "docs/架构图/README.md" not in text:
        fail("[根 AGENTS] 未链到 docs/架构图/README.md")
    # §2/§3/§4 完整继承：必须落盘全文文件，禁止摘要冒充
    inherited = root / "agent/AGENTS-继承准则.md"
    if not inherited.exists():
        fail("[完整继承] 缺 agent/AGENTS-继承准则.md（§2/§3/§4 全文）")
    else:
        it = read(inherited)
        for needle, label in [
            ("多 Agent 工作流", "§2 多 Agent"),
            ("全局行为准则", "§3 行为铁律"),
            ("通用编码准则", "§4 编码准则"),
            ("小闭环", "§3.15 小闭环"),
            ("外科手术式改动", "§4.3 手术刀"),
        ]:
            if needle not in it:
                fail(f"[完整继承] AGENTS-继承准则.md 缺少{label}（疑似被缩成摘要）")
    if "AGENTS-继承准则.md" not in text:
        fail("[根 AGENTS] 按需加载/正文未登记 agent/AGENTS-继承准则.md")
    if "0.2" not in text and "完整继承" not in text:
        fail("[根 AGENTS] 缺 §0.2 经验准则完整继承说明")


def check_layer_depth(root: Path):
    for rel, template in LAYER_AGENTS.items():
        path = root / rel
        if not path.exists():
            continue
        have = set(headings(read(path)))
        for head in headings(read(TEMPLATES / template)):
            if head not in have:
                fail(f"[分层深度] {rel} 缺模板章节「{head}」")


def scaffold_pairs(sel: dict):
    """(项目内代码目录, overlay 名, 登记该目录的 AGENT) 列表，按 SELECTION 开启的端生成。"""
    pairs = []
    if sel.get("frontend"):
        pairs.append((sel["frontend"]["dir"], "vue3", "agent/AGENTS-前端.md"))
    if sel.get("backend"):
        pairs.append((sel["backend"]["dir"], "goframe", "agent/AGENTS-后端.md"))
        sidecar = sel["backend"].get("sidecar")
        if sidecar:
            pairs.append((sidecar["dir"], "python-sidecar", "agent/AGENTS-侧车.md"))
            pairs.append((sel["backend"]["dir"], "goframe-sidecar", "agent/AGENTS-侧车.md"))
    if sel.get("light"):
        pairs.append((sel["light"]["dir"], "light-python", "agent/AGENTS-轻后端.md"))
    return pairs


def check_scaffold_dirs(root: Path, sel: dict):
    for code_dir, stack, agent in scaffold_pairs(sel):
        code_root = root / code_dir
        if not code_root.exists():
            fail(f"[脚手架] {code_dir}/ 不存在：先跑 scaffold/init.py")
            continue
        agent_text = read(root / agent)
        for src in sorted((OVERLAY / stack).rglob("*")):
            rel = src.relative_to(OVERLAY / stack)
            if not src.is_dir() or SKIP_DIR_PARTS & set(rel.parts):
                continue
            if not (code_root / rel).is_dir():
                fail(f"[脚手架] 增量目录 {code_dir}/{rel}/ 在项目中不存在")
            if f"{rel.name}/" not in agent_text:
                fail(f"[脚手架] 增量目录 {rel}/ 未在 {agent} 登记")


def check_diagrams(root: Path):
    diagram_dir = root / "docs/架构图"
    for path in sorted(diagram_dir.glob("*.md")):
        lines = read(path).splitlines()
        for i, line in enumerate(lines):
            if line.strip() == "```mermaid":
                first = lines[i + 1].strip() if i + 1 < len(lines) else ""
                if not first.startswith(MERMAID_TYPES):
                    fail(f"[架构图] {path.name}:{i + 2} Mermaid 首行不是合法图类型：{first[:40]}")
    index = read(diagram_dir / "README.md")
    for name in DIAGRAMS:
        rows = [line for line in index.splitlines() if name in line and line.startswith("|")]
        if rows and not any(status in rows[0] for status in STATUSES):
            fail(f"[架构图] 索引中 {name} 未标状态（{' / '.join(STATUSES)}）")


def mermaid_blocks(root: Path):
    """收集架构图目录下所有 Mermaid 围栏：(文件名, 起始行号, 代码)。"""
    blocks = []
    for path in sorted((root / "docs/架构图").glob("*.md")):
        lines = read(path).splitlines()
        i = 0
        while i < len(lines):
            if lines[i].strip() == "```mermaid":
                start = i + 2
                body = []
                i += 1
                while i < len(lines) and lines[i].strip() != "```":
                    body.append(lines[i])
                    i += 1
                blocks.append((path.name, start, "\n".join(body)))
            i += 1
    return blocks


def ensure_mermaid() -> Path:
    """确保本机缓存有 mermaid.min.js；没有就 npm pack 下载，只取 dist/mermaid.min.js 一个文件。"""
    if MERMAID_CACHE.exists():
        return MERMAID_CACHE
    MERMAID_CACHE.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        result = subprocess.run(["npm", "pack", f"mermaid@{MERMAID_VERSION}", "--registry", NPM_MIRROR, "--silent"],
                                cwd=tmp, capture_output=True, text=True)
        if result.returncode != 0:
            sys.exit(f"下载 mermaid 失败：{result.stderr.strip()}")
        with tarfile.open(Path(tmp) / f"mermaid-{MERMAID_VERSION}.tgz") as tar:
            member = tar.extractfile("package/dist/mermaid.min.js")
            MERMAID_CACHE.write_bytes(member.read())
    return MERMAID_CACHE


def check_mermaid_render(root: Path):
    """在无头浏览器里用真实 mermaid 逐块渲染；渲染失败即判该图不合格。"""
    from playwright.sync_api import sync_playwright

    blocks = mermaid_blocks(root)
    if not blocks:
        return
    script = ensure_mermaid()
    with sync_playwright() as pw:
        browser = pw.chromium.launch(channel="chrome", headless=True)
        page = browser.new_page()
        page.set_content("<html><body></body></html>")
        page.add_script_tag(path=str(script))
        page.evaluate("mermaid.initialize({ startOnLoad: false })")
        for no, (name, line, code) in enumerate(blocks):
            error = page.evaluate("""async ([id, code]) => {
                try { await mermaid.render(id, code); return null }
                catch (e) { return String(e && e.message || e).split('\\n').slice(0, 3).join(' ') }
            }""", [f"m{no}", code])
            if error:
                fail(f"[架构图渲染] {name}:{line} {error[:160]}")
        browser.close()
    print(f"Mermaid 渲染检查：{len(blocks)} 块")


def check_links(root: Path):
    link = re.compile(r"\]\(([^)#\s]+)(?:#[^)]*)?\)")
    for path in harness_docs(root):
        for target in link.findall(read(path)):
            if re.match(r"^[a-z]+:", target):
                continue
            if not (path.parent / target).exists():
                fail(f"[链接] {path.relative_to(root)} → {target} 不存在")


def main():
    parser = argparse.ArgumentParser(description="harness 机器自检")
    parser.add_argument("--target", required=True)
    parser.add_argument("--selection", help="默认读 <target>/SELECTION.json")
    parser.add_argument("--docs-only", action="store_true", help="只查文档，不查代码目录（如 skill 内的 dry-run 样例）")
    parser.add_argument("--render", action="store_true", help="用真实 mermaid 渲染架构图（需 npm 与本机 Chrome）")
    args = parser.parse_args()

    root = Path(args.target).resolve()
    sel_path = Path(args.selection) if args.selection else root / "SELECTION.json"
    sel = json.loads(read(sel_path) or "{}")

    check_required(root, sel)
    check_placeholders(root)
    check_root(root)
    check_layer_depth(root)
    if not args.docs_only:
        check_scaffold_dirs(root, sel)
    check_diagrams(root)
    if args.render:
        check_mermaid_render(root)
    check_links(root)

    if failures:
        print(f"harness 自检不通过（{len(failures)} 项）：")
        print("\n".join(f"- {msg}" for msg in failures))
        sys.exit(1)
    print("harness 自检通过")


if __name__ == "__main__":
    main()

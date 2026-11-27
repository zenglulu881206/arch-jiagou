#!/usr/bin/env python3
"""
脚手架生成：官方 init 基线 + 经验增量（overlay）。

用法：python3 init.py --selection SELECTION.json --target <项目根目录>

步骤：
1. 创建统一根目录和通用入口。
2. 跑选中技术栈的官方 init，版本取 SELECTION.json。
3. 按栈说明删改官方示例，拷贝 overlay 并替换 __XXX__ 占位符。
4. 走国内镜像装依赖，跑格式化和静态检查。

不覆盖：目标前端/后端目录已存在时直接退出，由人先确认。
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OVERLAY = HERE / "overlay"
PLACEHOLDER = re.compile(r"__(APP|FE|DB|SIDECAR|LIGHT)_[A-Z_]*[A-Z]__")
TEXT_SUFFIXES = {".go", ".ts", ".vue", ".css", ".yaml", ".sql", ".md", ".json", ".npmrc", ".py", ".toml", ".html", ""}
PIP_MIRROR = "https://pypi.tuna.tsinghua.edu.cn/simple"


def run(cmd, cwd, env=None):
    """执行外部命令并回显；失败即退出，避免半截脚手架被当成可用。"""
    print(f"$ {' '.join(cmd)}  (cwd={cwd})", flush=True)
    result = subprocess.run(cmd, cwd=cwd, env=env)
    if result.returncode != 0:
        sys.exit(f"命令失败（退出码 {result.returncode}）：{' '.join(cmd)}")


def copy_overlay(src: Path, dst: Path, values: dict):
    """把 overlay 拷进目标目录（同名覆盖官方文件），并替换文本文件里的占位符。"""
    for path in src.rglob("*"):
        if path.is_dir():
            continue
        target = dst / path.relative_to(src)
        target.parent.mkdir(parents=True, exist_ok=True)
        if path.suffix in TEXT_SUFFIXES:
            text = path.read_text(encoding="utf-8")
            for key, value in values.items():
                text = text.replace(key, str(value))
            target.write_text(text, encoding="utf-8")
        else:
            shutil.copy2(path, target)


def assert_no_placeholder(root: Path):
    """生成后不得残留 __XXX__ 占位符；node_modules 不查。"""
    left = []
    for path in root.rglob("*"):
        if "node_modules" in path.parts or not path.is_file():
            continue
        if path.suffix not in TEXT_SUFFIXES:
            continue
        if PLACEHOLDER.search(path.read_text(encoding="utf-8", errors="ignore")):
            left.append(str(path))
    if left:
        sys.exit("占位符未替换：\n" + "\n".join(left))


def remove(root: Path, rel_paths):
    """按删改表删除官方示例；不存在则跳过（官方模板版本差异）。"""
    for rel in rel_paths:
        path = root / rel
        if path.is_dir():
            shutil.rmtree(path)
        elif path.exists():
            path.unlink()


LEGACY_WINDOWS = {"7", "8", "8.1", "2008", "2008r2", "2012", "2012r2"}
LEGACY_GOFRAME_MAX = (2, 7)
# Win7 / Server 2008 线：照 Win7 内网项目在客户 Win7 实机跑通的组合钉版本。
# 钉 x/sys v0.15.0、otel v1.21.0 后，GoFrame 只能停在 v2.7.x（v2.8 依赖更高版本会被强制降级）。
LEGACY_PINS = [
    "golang.org/x/sys@v0.15.0",
    "go.opentelemetry.io/otel@v1.21.0",
    "go.opentelemetry.io/otel/metric@v1.21.0",
    "go.opentelemetry.io/otel/sdk@v1.21.0",
    "go.opentelemetry.io/otel/trace@v1.21.0",
]
WEB_ROOT = "resource/public/html"


def goframe_minor(version: str):
    """v2.10.5 → (2, 10)，用于和 Win7 可用上限比较。"""
    major, minor = version.lstrip("v").split(".")[:2]
    return int(major), int(minor)


def is_legacy_windows(sel: dict) -> bool:
    """目标机是否 Windows 7/8、Server 2008/2012（Go 1.21 起不再支持）。"""
    deploy = sel.get("deploy", {})
    os_version = str(deploy.get("os_version", "")).lower().replace(" ", "")
    return deploy.get("os") == "windows" and os_version in LEGACY_WINDOWS


def build_target(sel: dict) -> str:
    """前端构建目标：选型给了浏览器下限（如 chrome-109）就按它，否则用 Vite 默认。"""
    floor = str(sel.get("clients", {}).get("browser_min", ""))
    m = re.fullmatch(r"chrome-(\d+)", floor)
    if m:
        return f"['chrome{m.group(1)}', 'edge{m.group(1)}']"
    return "'baseline-widely-available'"


def check_selection(sel: dict):
    """动手前校验选型组合；冲突直接退出，避免生成一个在目标机上跑不起来的项目。"""
    deploy = sel.get("deploy", {})
    be = sel.get("backend")
    if be and is_legacy_windows(sel):
        # Go 1.21 起不再支持 Windows 7/8、Server 2008/2012；GoFrame v2.9 起要求 Go 1.22+。
        if goframe_minor(be["goframe"]) > LEGACY_GOFRAME_MAX:
            sys.exit(f"目标机是 Windows {deploy['os_version']}：后端须用 Go 1.20.x + GoFrame v2.7.x"
                     f"（Win7 内网项目实机组合），当前选型是 {be['goframe']}，请改 SELECTION.json")
        print("提示：发布包必须用 Go 1.20.x 编译（GOOS=windows），本机新版 Go 只能用于开发调试。", flush=True)
    if deploy.get("shape") == "single-binary" and not sel.get("frontend"):
        print("提示：deploy.shape=single-binary 但没有前端，web.root 将指向空目录。", flush=True)
    engine = sel.get("database", {}).get("engine", "pgsql")
    if engine not in ("pgsql", "sqlite"):
        sys.exit(f"database.engine 只支持 pgsql / sqlite，当前为 {engine}")


def db_link(db: dict) -> str:
    """按数据库引擎生成 GoFrame 连接串；密码一律占位 CHANGE_ME，不写真实凭据。"""
    if db.get("engine", "pgsql") == "sqlite":
        return f"sqlite::@file(./data/{db['name']}.db)"
    return f"pgsql:{db['user']}:CHANGE_ME@tcp(127.0.0.1:5432)/{db['name']}"


def init_frontend(sel: dict, target: Path):
    """create-vue 基线 + vue3 overlay + Element Plus。"""
    fe = sel["frontend"]
    flags = ["--" + f for f in fe["features"]]
    run(["npx", "-y", f"create-vue@{fe['create_vue']}", *flags, "--bare", fe["dir"]], cwd=target)

    root = target / fe["dir"]
    copy_overlay(OVERLAY / "vue3", root, {
        "__APP_PORT__": sel["backend"]["port"],
        "__FE_PORT__": fe["port"],
        "__FE_BUILD_TARGET__": build_target(sel),
        "__APP_TITLE__": sel["project"]["title"],
    })
    assert_no_placeholder(root)

    run(["npm", "install"], cwd=root)
    run(["npm", "install", f"element-plus@{fe['element_plus']}"], cwd=root)
    run(["npm", "run", "format"], cwd=root)
    run(["npm", "run", "lint"], cwd=root)


def init_backend(sel: dict, target: Path):
    """gf init 基线 + goframe overlay + PostgreSQL 驱动。"""
    be = sel["backend"]
    run(["gf", "init", be["dir"], "-g", be["module"]], cwd=target)

    root = target / be["dir"]
    drops = ["api/hello", "internal/controller/hello", "utility", "manifest/config/config.yaml"]
    if not be.get("keep_docker"):
        drops.append("manifest/docker")
    if not be.get("keep_kustomize"):
        drops.append("manifest/deploy")
    remove(root, drops)

    db = sel["database"]
    engine = db.get("engine", "pgsql")
    values = {
        "__APP_MODULE__": be["module"],
        "__APP_PORT__": be["port"],
        "__DB_DRIVER__": engine,
        "__DB_LINK__": db_link(db),
        "__APP_WEBROOT__": WEB_ROOT if sel.get("deploy", {}).get("shape") == "single-binary" else "",
    }
    copy_overlay(OVERLAY / "goframe", root, values)
    if engine == "sqlite":
        # SQLite 没有 schema 概念：初始迁移只留说明；库文件目录不入库。
        (root / "migrations/0001_init_schema.sql").write_text(
            "-- SQLite 无 schema；首张业务表在后续迁移中创建。\n", encoding="utf-8")
        (root / "data").mkdir(exist_ok=True)
    config_dir = root / "manifest/config"
    shutil.copy2(config_dir / "config.example.yaml", config_dir / "config.yaml")
    with open(root / ".gitignore", "a", encoding="utf-8") as fh:
        fh.write("\n# 本机/现场真实配置，含凭据，不入库\nmanifest/config/config.yaml\n")
        if engine == "sqlite":
            fh.write("# SQLite 库文件\ndata/\n")
        if sel.get("deploy", {}).get("shape") == "single-binary":
            fh.write(f"# 前端构建产物（打包时从前端 dist 复制）\n{WEB_ROOT}/*\n!{WEB_ROOT}/.gitkeep\n")
    assert_no_placeholder(root)

    env = dict(os.environ)
    env.setdefault("GOPROXY", "https://goproxy.cn,direct")
    # gf init 内置模板的框架版本随 CLI 走（CLI v2.10 仍给 v2.7.1），这里统一钉到选型表版本。
    gf_version = be["goframe"]
    run(["go", "get", f"github.com/gogf/gf/v2@{gf_version}"], cwd=root, env=env)
    run(["go", "get", f"github.com/gogf/gf/contrib/drivers/{engine}/v2@{gf_version}"], cwd=root, env=env)
    if is_legacy_windows(sel):
        run(["go", "mod", "edit", "-go=1.20"], cwd=root, env=env)
        run(["go", "get", *LEGACY_PINS], cwd=root, env=env)
    run(["go", "mod", "tidy"], cwd=root, env=env)
    run(["gofmt", "-w", "."], cwd=root)


def venv_python(venv: Path) -> Path:
    """虚拟环境里的 python 路径（Windows 与类 Unix 不同）。"""
    return venv / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def require_python(python: str, minimum: tuple):
    """检查本机 Python 版本不低于 minimum；侧车依赖 FastAPI 需 3.11+。"""
    out = subprocess.run([python, "-c", "import sys;print(*sys.version_info[:2])"],
                         capture_output=True, text=True)
    if out.returncode != 0:
        sys.exit(f"找不到 {python}，请先安装 Python {'.'.join(map(str, minimum))}+")
    have = tuple(int(x) for x in out.stdout.split())
    if have < minimum:
        sys.exit(f"{python} 版本 {'.'.join(map(str, have))} 低于要求 {'.'.join(map(str, minimum))}")


def init_sidecar(sel: dict, target: Path):
    """Python 侧车：venv 基线 + python-sidecar overlay；Go 侧追加 sidecar 管理包、示例业务与启动挂载。"""
    be = sel["backend"]
    sc = be["sidecar"]
    python = sc.get("python", "python3")
    require_python(python, (3, 11))

    root = target / sc["dir"]
    copy_overlay(OVERLAY / "python-sidecar", root, {
        "__SIDECAR_NAME__": f"{sel['project']['name']}-sidecar",
        "__SIDECAR_PORT__": sc["port"],
    })
    assert_no_placeholder(root)
    run([python, "-m", "venv", ".venv"], cwd=root)
    env = dict(os.environ, PIP_DISABLE_PIP_VERSION_CHECK="1")
    run([str(venv_python(root / ".venv")), "-m", "pip", "install", "-i", PIP_MIRROR, "-e", ".[dev]"], cwd=root, env=env)

    be_root = target / be["dir"]
    copy_overlay(OVERLAY / "goframe-sidecar", be_root, {
        "__APP_MODULE__": be["module"],
        "__SIDECAR_DIR__": sc["dir"],
        "__SIDECAR_PORT__": sc["port"],
    })
    with open(be_root / "manifest/config/config.example.yaml", "a", encoding="utf-8") as fh:
        fh.write(f"""
# Python 侧车：由本进程拉起，只监听 127.0.0.1；模型加载慢时调大 startTimeoutSec。
sidecar:
  dir: "../{sc['dir']}"
  port: {sc['port']}
  startTimeoutSec: 60
""")
    shutil.copy2(be_root / "manifest/config/config.example.yaml", be_root / "manifest/config/config.yaml")
    assert_no_placeholder(be_root)
    run(["gofmt", "-w", "."], cwd=be_root)


def init_light(sel: dict, target: Path):
    """轻后端：Python 标准库 + SQLite + 单 HTML，没有官方 init，整份来自 light-python overlay。"""
    light = sel["light"]
    require_python(light.get("python", "python3"), (3, 9))
    root = target / light["dir"]
    copy_overlay(OVERLAY / "light-python", root, {
        "__LIGHT_DB__": sel["database"]["name"],
        "__LIGHT_PORT__": light["port"],
        "__LIGHT_TITLE__": sel["project"]["title"],
    })
    assert_no_placeholder(root)


def init_root(target: Path):
    """生成所有项目共用的根目录骨架；已存在文件一律不覆盖。"""
    directories = [
        "admin/scripts", "admin/release", "docs/架构图",
        "docs/PRD及测试用例", "docs/项目特化", "docs/旧低代码系统调研记录",
        "agent", "log", "scripts", "tests",
    ]
    for rel in directories:
        path = target / rel
        path.mkdir(parents=True, exist_ok=True)
        marker = path / ".gitkeep"
        if not marker.exists():
            marker.touch()

    admin_agents = target / "admin/AGENTS.md"
    if not admin_agents.exists():
        shutil.copy2(HERE / "templates/AGENTS.admin.md", admin_agents)

    src_root = OVERLAY / "root"
    for path in src_root.rglob("*"):
        rel = path.relative_to(src_root)
        dst = target / rel
        if path.is_dir() or dst.exists():
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dst)
    claude = target / "CLAUDE.md"
    if not claude.exists() and not claude.is_symlink():
        claude.symlink_to("AGENTS.md")


def main():
    parser = argparse.ArgumentParser(description="统一根目录骨架 + 技术栈官方 init + 经验增量")
    parser.add_argument("--selection", required=True, help="选型结果 SELECTION.json")
    parser.add_argument("--target", required=True, help="项目根目录（可已存在，但前后端子目录不得存在）")
    args = parser.parse_args()

    sel = json.loads(Path(args.selection).read_text(encoding="utf-8"))
    target = Path(args.target).resolve()
    target.mkdir(parents=True, exist_ok=True)

    sidecar = (sel.get("backend") or {}).get("sidecar")
    dirs = [sel[k]["dir"] for k in ("frontend", "backend", "light") if sel.get(k)]
    if sidecar:
        dirs.append(sidecar["dir"])
    for rel in dirs:
        if (target / rel).exists():
            sys.exit(f"{target / rel} 已存在：本脚本不覆盖已有代码，请先确认后再处理。")

    check_selection(sel)

    tools = []
    if sel.get("frontend"):
        tools += ["node", "npm", "npx"]
    if sel.get("backend"):
        tools += ["go", "gofmt", "gf"]
    for tool in tools:
        if not shutil.which(tool):
            sys.exit(f"缺少命令 {tool}，请先安装（版本见 scaffold/*.md 基线表）")

    init_root(target)
    if sel.get("frontend"):
        init_frontend(sel, target)
    if sel.get("backend"):
        init_backend(sel, target)
    if sidecar:
        init_sidecar(sel, target)
    if sel.get("light"):
        init_light(sel, target)
    print("脚手架生成完成；下一步运行 verify.py 验收。")


if __name__ == "__main__":
    main()

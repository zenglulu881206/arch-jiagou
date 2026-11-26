"""侧车配置：一律从环境变量读取，由 Go 主后端启动时注入；密钥不写进代码和日志。"""
import os
from pathlib import Path

# 侧车代码根目录
BASE_DIR = Path(__file__).resolve().parents[2]
# 安装根目录：生产由 Go 注入 APP_INSTALL_ROOT，源码环境回退到侧车目录的上一级
INSTALL_ROOT = Path(os.environ.get("APP_INSTALL_ROOT", str(BASE_DIR.parent))).resolve()
# 数据目录（模型缓存、向量库等运行时文件），不入库
DATA_DIR = INSTALL_ROOT / "data"

APP_HOST = "127.0.0.1"
APP_PORT = int(os.environ.get("APP_SIDECAR_PORT", "__SIDECAR_PORT__"))

# 模型调用按 OpenAI 兼容协议写，换供应商只改这三项；本地模型（Ollama）同样适用
LLM_BASE_URL = os.environ.get("APP_LLM_BASE_URL", "")
LLM_MODEL = os.environ.get("APP_LLM_MODEL", "")
LLM_API_KEY = os.environ.get("APP_LLM_API_KEY", "")

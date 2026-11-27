import importlib.util
import tempfile
import unittest
from pathlib import Path


INIT_PATH = Path(__file__).with_name("init.py")
SPEC = importlib.util.spec_from_file_location("arch_jiagou_init", INIT_PATH)
INIT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(INIT)


class InitRootTests(unittest.TestCase):
    def test_creates_common_skeleton_and_preserves_existing_admin_rules(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            admin_agents = target / "admin/AGENTS.md"
            admin_agents.parent.mkdir(parents=True)
            admin_agents.write_text("user-owned rules", encoding="utf-8")

            INIT.init_root(target)

            expected = [
                "admin/scripts", "admin/release", "docs/架构图",
                "docs/PRD及测试用例", "docs/项目特化", "docs/旧低代码系统调研记录",
                "agent", "log", "scripts", "tests",
            ]
            for rel in expected:
                self.assertTrue((target / rel).is_dir(), rel)
            self.assertTrue((target / "admin/scripts/e2e_launch.py").is_file())
            self.assertEqual(admin_agents.read_text(encoding="utf-8"), "user-owned rules")
            self.assertTrue((target / "CLAUDE.md").is_symlink())


if __name__ == "__main__":
    unittest.main()

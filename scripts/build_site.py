#!/usr/bin/env python3
"""把演示页打成可挂在 /项目名/ 下的静态站点。

用法:
    python scripts/build_site.py

产物（写入 dist/site/，随 dist/ 被 .gitignore 忽略）:
    dist/site/interactive-questionnaire/index.html
    dist/site/interactive-questionnaire/assets/demo.html

两份都是 `assets/demo.html` 的拷贝：目录访问走 index.html，
/assets/demo.html 深链也可用。仅依赖 Python 3 标准库。
"""

import shutil
import sys
from pathlib import Path

SKILL_NAME = "interactive-questionnaire"
REPO_ROOT = Path(__file__).resolve().parent.parent
DEMO_SRC = REPO_ROOT / SKILL_NAME / "assets" / "demo.html"
SITE_DIR = REPO_ROOT / "dist" / "site" / SKILL_NAME


def fail(msg: str) -> None:
    print(f"[站点构建失败] {msg}")
    sys.exit(1)


def build() -> Path:
    if not DEMO_SRC.is_file():
        fail(f"找不到演示页: {DEMO_SRC}")

    assets = SITE_DIR / "assets"
    assets.mkdir(parents=True, exist_ok=True)

    index_path = SITE_DIR / "index.html"
    demo_path = assets / "demo.html"
    shutil.copyfile(DEMO_SRC, index_path)
    shutil.copyfile(DEMO_SRC, demo_path)

    size_kb = DEMO_SRC.stat().st_size / 1024
    print(f"[完成] {index_path.relative_to(REPO_ROOT)}")
    print(f"[完成] {demo_path.relative_to(REPO_ROOT)}")
    print(f"[完成] 同源 {DEMO_SRC.relative_to(REPO_ROOT)}（{size_kb:.0f} KB）")
    return SITE_DIR


if __name__ == "__main__":
    build()

#!/usr/bin/env python3
"""把技能文件夹打包成可分发的 .skill 包（本质是 zip，压缩包根即技能文件夹）。

用法:
    python scripts/package.py            # 版本号取 CHANGELOG.md 最新一条
    python scripts/package.py 1.2.0      # 显式指定版本号

产物（写入 dist/，该目录已被 .gitignore 忽略）:
    dist/interactive-questionnaire-v<版本>.skill
    dist/interactive-questionnaire-v<版本>.zip   # 同一份内容的 .zip 后缀副本，
                                                 # 供只认 .zip 的上传入口使用

仅依赖 Python 3 标准库，Windows / macOS / Linux 通用。
"""

import re
import shutil
import sys
import zipfile
from pathlib import Path

SKILL_NAME = "interactive-questionnaire"
REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = REPO_ROOT / SKILL_NAME
DIST_DIR = REPO_ROOT / "dist"

# 打包时排除的杂项（与 Agent Skills skill-creator 的打包脚本口径一致）
EXCLUDE_DIR_NAMES = {"__pycache__", "node_modules", ".git"}
EXCLUDE_FILE_NAMES = {".DS_Store", "Thumbs.db"}
EXCLUDE_SUFFIXES = {".pyc"}


def fail(msg: str) -> None:
    print(f"[打包失败] {msg}")
    sys.exit(1)


def resolve_version() -> str:
    """版本号来源：命令行参数 > CHANGELOG.md 最新一条 `## [x.y.z]`。"""
    if len(sys.argv) > 1:
        return sys.argv[1].lstrip("v")
    changelog = REPO_ROOT / "CHANGELOG.md"
    if changelog.exists():
        m = re.search(
            r"^##\s*\[(\d+\.\d+\.\d+[^\]]*)\]",
            changelog.read_text(encoding="utf-8"),
            re.MULTILINE,
        )
        if m:
            return m.group(1)
    return "0.0.0-dev"


def validate_skill() -> None:
    """轻量校验：SKILL.md 存在，且 YAML frontmatter 含 name 与 description。"""
    skill_md = SKILL_DIR / "SKILL.md"
    if not SKILL_DIR.is_dir():
        fail(f"找不到 skill 目录: {SKILL_DIR}")
    if not skill_md.is_file():
        fail(f"找不到 {skill_md}（每个 skill 必须有 SKILL.md）")
    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---"):
        fail("SKILL.md 必须以 YAML frontmatter（--- 开头）起始")
    end = text.find("---", 3)
    if end == -1:
        fail("SKILL.md 的 frontmatter 没有闭合的 ---")
    frontmatter = text[3:end]
    for field in ("name:", "description:"):
        if field not in frontmatter:
            fail(f"SKILL.md frontmatter 缺少必填字段 {field.rstrip(':')}")
    print(f"[校验通过] {skill_md.relative_to(REPO_ROOT)}")


def should_exclude(path: Path) -> bool:
    rel = path.relative_to(SKILL_DIR)
    if any(part in EXCLUDE_DIR_NAMES for part in rel.parts):
        return True
    if path.name in EXCLUDE_FILE_NAMES:
        return True
    return path.suffix in EXCLUDE_SUFFIXES


def build(version: str) -> Path:
    DIST_DIR.mkdir(exist_ok=True)
    skill_path = DIST_DIR / f"{SKILL_NAME}-v{version}.skill"
    zip_path = skill_path.with_suffix(".zip")

    files = sorted(
        p for p in SKILL_DIR.rglob("*") if p.is_file() and not should_exclude(p)
    )
    if not files:
        fail("技能目录里没有可打包的文件")

    with zipfile.ZipFile(skill_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in files:
            # 压缩包内路径以技能文件夹名开头，如
            # interactive-questionnaire/SKILL.md —— 与 Agent Skills 的 .skill 包结构一致
            arcname = f"{SKILL_NAME}/{f.relative_to(SKILL_DIR).as_posix()}"
            zf.write(f, arcname)
            print(f"  + {arcname}")

    shutil.copyfile(skill_path, zip_path)
    size_kb = skill_path.stat().st_size / 1024
    print(f"[完成] {skill_path.relative_to(REPO_ROOT)}（{size_kb:.0f} KB，共 {len(files)} 个文件）")
    print(f"[完成] {zip_path.relative_to(REPO_ROOT)}（同内容 .zip 副本）")
    return skill_path


if __name__ == "__main__":
    validate_skill()
    build(resolve_version())

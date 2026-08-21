#!/usr/bin/env python3
"""写出 GitHub Release 正文：该版本国内 / 海外下载地址 + 一条 Changelog 链接。

环境变量:
    TAG                 如 v1.0.0
    PROJECT_SLUG        如 interactive-questionnaire
    GITHUB_REPOSITORY   如 duskykitecn/interactive-questionnaire

用法:
    python scripts/write_release_body.py /tmp/release-body.md
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from textwrap import dedent


def previous_tag(current: str) -> str:
    tags = subprocess.check_output(
        ["git", "tag", "--list", "v*", "--sort=-version:refname"],
        text=True,
    ).split()
    try:
        idx = tags.index(current)
    except ValueError:
        return ""
    if idx + 1 < len(tags):
        return tags[idx + 1]
    return ""


def build_body() -> str:
    tag = os.environ["TAG"]
    slug = os.environ["PROJECT_SLUG"]
    repo = os.environ["GITHUB_REPOSITORY"]
    pkg = f"{slug}-{tag}"
    cn = f"https://static.duskykite.com.cn/{slug}/releases/{tag}"
    xyz = f"https://static.duskykite.xyz/{slug}/releases/{tag}"
    prev = previous_tag(tag)
    changelog = (
        f"https://github.com/{repo}/compare/{prev}...{tag}"
        if prev
        else f"https://github.com/{repo}/commits/{tag}"
    )
    return dedent(
        f"""\
        ## Downloads

        ### 国内
        - [{pkg}.skill]({cn}/{pkg}.skill)
        - [{pkg}.zip]({cn}/{pkg}.zip)

        ### 海外
        - [{pkg}.skill]({xyz}/{pkg}.skill)
        - [{pkg}.zip]({xyz}/{pkg}.zip)

        GitHub Release 附件与上面是同一份文件。

        **Full Changelog**: {changelog}
        """
    )


def main() -> None:
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/release-body.md")
    out.write_text(build_body(), encoding="utf-8")


if __name__ == "__main__":
    main()

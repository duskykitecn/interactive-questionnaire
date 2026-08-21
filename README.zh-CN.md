# interactive-questionnaire

[English](README.md) | 简体中文

> 一份智能体技能：把智能体对你的零散追问，变成结构化的问卷。

![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)
![Release](https://img.shields.io/github/v/release/duskykitecn/interactive-questionnaire)
![Agent Skills](https://img.shields.io/badge/Agent_Skills-compatible-4B57D6)

## 这是什么

与智能体协作时，它常常需要向你收集偏好、需求或决策。默认行为是想到哪问到哪：问题散落在多轮对话里，答案是一段段散文，既费你的心力，也难被稳定解析。

本技能让智能体的**每一次提问**都走两条规范路线之一：

- **简单提问 → 文字版**：编号列出问题（题号 `1.` `2.`、选项号 `a.` `b.`），每题附一段「为什么问、要解决什么、推荐怎么选」的描述，你用 `1: a,c` 这样的方式作答即可。
- **复杂提问 → HTML 交互问卷**：智能体用内置模板与 12 种组件（单选、多选、开关追问、滑杆、区间、计数、文本、排序等）装配出一份可交互问卷，你逐题填写后点「复制结果」，把结构化 JSON 回贴给智能体解析。

配套约束：**一经调用，对整个会话持续生效**——不会问完一份问卷就退回随口散问；每轮回复结尾有一次静默自检，发现散问会当场按规范补上。

## 效果预览

没有这份技能时，智能体把问题塞进一段分析里；你也只能写一段话回去。

<p align="center">
  <img src="docs/preview/without.zh-CN.svg" alt="没有这份技能时：八个问题夹在智能体的一段话里，你也只能写一段话回去" width="800">
</p>

启用之后，复杂的提问会变成一份能点的问卷。**在线演示**（三处同一份 `demo.html`）：

- 国内：https://static.duskykite.com.cn/interactive-questionnaire/
- 海外：https://static.duskykite.xyz/interactive-questionnaire/
- GitHub Pages：https://duskykitecn.github.io/interactive-questionnaire/

12 种组件都在：明暗主题、异议、「改用文字填写」、结果 JSON。第一次打开会弹出引导，不想看可以跳过，浏览器会记下；顶栏问号能再打开。push 到 `main` 后本仓库 GitHub Pages 会自己更新；自定义域名走组织 `static` 总仓的 `/interactive-questionnaire/`，第一次接入见 [PUBLISHING.md](PUBLISHING.md)「静态托管」。也可以克隆后直接打开 [`interactive-questionnaire/assets/demo.html`](interactive-questionnaire/assets/demo.html)。

## 安装

这是一份符合 [Agent Skills](https://agentskills.io) 规范的**智能体技能**：本质是一个含 `SKILL.md` 的文件夹。安装就是把这个文件夹放到智能体应用会扫描的技能目录（路径中一般为 `skills`），或通过该应用提供的技能上传入口导入。

复制的必须是**仓库根目录下的同名子文件夹**（即含 `SKILL.md` 的那层），不是整个仓库。

### 放入技能目录

个人级（对当前用户的所有项目生效），以常见智能体应用为例：

```bash
git clone https://github.com/duskykitecn/interactive-questionnaire.git

# Cursor
mkdir -p ~/.cursor/skills
cp -r interactive-questionnaire/interactive-questionnaire ~/.cursor/skills/

# Claude Code
mkdir -p ~/.claude/skills
cp -r interactive-questionnaire/interactive-questionnaire ~/.claude/skills/
```

项目级（随仓库共享给团队）：复制到项目根下该应用约定的目录，例如 `.cursor/skills/`、`.claude/skills/`。其他兼容 Agent Skills 的智能体应用，目录名以各自文档为准，做法相同。

Windows 将 `~` 换成 `%USERPROFILE%`。

### 以压缩包上传

部分智能体应用只接受压缩包。压缩包以技能文件夹为根（`interactive-questionnaire/SKILL.md`）。上传入口若只认 `.zip` 就用后者。

国内（不经过 GitHub）：

- `.skill`：https://static.duskykite.com.cn/interactive-questionnaire/releases/latest/interactive-questionnaire.skill
- `.zip`：https://static.duskykite.com.cn/interactive-questionnaire/releases/latest/interactive-questionnaire.zip

海外：

- `.skill`：https://static.duskykite.xyz/interactive-questionnaire/releases/latest/interactive-questionnaire.skill
- `.zip`：https://static.duskykite.xyz/interactive-questionnaire/releases/latest/interactive-questionnaire.zip

GitHub Releases 仍有同名附件：https://github.com/duskykitecn/interactive-questionnaire/releases/latest

本地打包：

```bash
python scripts/package.py
```

例如 claude.ai 在 **设置 → 功能（Settings → Capabilities）** 的 Skills 区域上传（需相应套餐并开启代码执行；自定义技能通常仅对当前账号生效）；Claude API 则通过 `/v1/skills` 上传后再引用返回的 `skill_id`。

## 用法

- **触发**：对话中点名 `interactive-questionnaire`（或在支持的应用里用斜杠命令 `/interactive-questionnaire`）显式启用；启用后凡智能体需要向你提问的场合都会按本技能组织。
- **文字版作答**：选择题按选项字母回答（多选给多个字母，如 `1: a,c`），自由题直接写文字。
- **HTML 问卷作答**：逐题填写（每题都可点「＋ 改用文字填写」换成自由文字，或提出异议），完成后点「复制结果」，把 JSON 粘贴回对话。
- **结果 JSON**：每题一个条目，三种形态——`answer`（按控件作答，带 `dirty` 标记区分是否改过默认值）、`custom`（自由文字）、`objection`（异议）；另有 `system` 元信息（主题、展示 / 折叠模式）。字段契约详见 [`interactive-questionnaire/SKILL.md`](interactive-questionnaire/SKILL.md)。
- **停止**：明确告诉智能体停用即可。

## 目录结构

```
interactive-questionnaire/            ← 仓库根
├── README.md                         ← 英文说明
├── README.zh-CN.md                   ← 本文件
├── LICENSE
├── CHANGELOG.md                      ← 版本记录（Keep a Changelog）
├── PUBLISHING.md                     ← 维护者手册：发版流程、GitHub/Gitee/CNB 多平台同步
├── scripts/
│   ├── package.py                    ← 本地打包脚本（仅需 Python 3 标准库）
│   ├── build_site.py                 ← 把 demo.html 打成 /项目名/ 静态站点
│   └── write_release_body.py         ← GitHub Release 说明（国内 / 海外下载地址）
├── .github/workflows/
│   ├── release.yml                   ← 推送 v* 标签 → 自动打包并发布 GitHub Release
│   ├── deploy-site.yml               ← 可选：把演示站推到 duskykitecn/static（默认关闭）
│   └── sync-mirrors.yml              ← Gitee 开 GITEE_SYNC_ENABLED；不要开 CNB_SYNC_ENABLED（CNB 用 .cnb.yml 拉）
├── .cnb.yml                          ← CNB 镜像：定时 git-sync 从 GitHub 拉取
├── docs/preview/                     ← README 痛点静图（中 / 英 SVG）
└── interactive-questionnaire/        ← 技能实体（安装/打包的对象就是这一层）
    ├── SKILL.md                      ← 入口：路由规则、文字版约定、装配流程、JSON 契约
    ├── assets/
    │   ├── template.html             ← HTML 问卷外壳模板
    │   └── demo.html                 ← 全组件演示页
    └── references/
        ├── components.md             ← 组件登记表与装配细则
        └── snippets/                 ← 12 种组件片段（每种一个 .html）
```

## 本地打包

```bash
python scripts/package.py          # 版本号自动取 CHANGELOG.md 最新一条
python scripts/package.py 1.2.0    # 或显式指定
```

产物在 `dist/` 下：`interactive-questionnaire-vX.Y.Z.skill` 与同内容的 `.zip`。

## 版本与发布

版本号遵循 SemVer，变更记录在 [CHANGELOG.md](CHANGELOG.md)。维护者推送 `vX.Y.Z` 标签后，GitHub Actions 会自动打包：GitHub Release 附上 `.skill` / `.zip`，并推到 `static` 总仓。完整发版流程见 [PUBLISHING.md](PUBLISHING.md)。

仓库地址：

- GitHub（主库）：https://github.com/duskykitecn/interactive-questionnaire
- Gitee（镜像）：https://gitee.com/duskykite/interactive-questionnaire
- CNB（镜像）：https://cnb.cool/DuskyKite/interactive-questionnaire

## 许可证

本项目采用 [CC BY-NC 4.0](LICENSE)（署名-非商业性使用）许可：允许复制、修改与再分发，须署名并注明改动，**禁止商业用途**；商业授权请联系作者。协议原文见[知识共享官网](https://creativecommons.org/licenses/by-nc/4.0/deed.zh-hans)。

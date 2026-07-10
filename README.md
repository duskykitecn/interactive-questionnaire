# interactive-questionnaire

> 一个 Claude Agent Skill：把 Claude 对你的零散追问，变成结构化的问卷。
> A Claude Agent Skill that turns Claude's scattered follow-up questions into structured questionnaires (plain-text or interactive HTML) with machine-parsable JSON answers.

![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)
![Release](https://img.shields.io/github/v/release/duskykitecn/interactive-questionnaire)
![Platform](https://img.shields.io/badge/Platform-Claude-d97757)

## 这是什么

与 Claude 协作时，它常常需要向你收集偏好、需求或决策。默认行为是想到哪问到哪：问题散落在多轮对话里，答案是一段段散文，既费你的心力，也难被稳定解析。

本 skill 让 Claude 的**每一次提问**都走两条规范路线之一：

- **简单提问 → 文字版**：编号列出问题（题号 `1.` `2.`、选项号 `a.` `b.`），每题附一段「为什么问、要解决什么、推荐怎么选」的描述，你用 `1: a,c` 这样的方式作答即可。
- **复杂提问 → HTML 交互问卷**：Claude 用内置模板与 12 种组件（单选、多选、开关追问、滑杆、区间、计数、文本、排序等）装配出一份可交互问卷，你逐题填写后点「复制结果」，把结构化 JSON 回贴给 Claude 解析。

配套约束：**一经调用，对整个会话持续生效**——不会问完一份问卷就退回随口散问；每轮回复结尾有一次静默自检，发现散问会当场按规范补上。

## 效果预览

**在线演示**：https://duskykitecn.github.io/interactive-questionnaire/ —— 全部 12 种组件的交互演示（含明暗主题、异议与「改用文字填写」入口、结果 JSON 生成），打开即用。也可以克隆仓库后用浏览器直接打开 [`interactive-questionnaire/assets/demo.html`](interactive-questionnaire/assets/demo.html) 在本地查看。

## 安装

Skill 的本质是一个含 `SKILL.md` 的文件夹；安装就是把这个文件夹交给对应的 Claude 产品。三个入口任选：

### 1. claude.ai（网页版 / 客户端）

1. 从 [Releases](https://github.com/duskykitecn/interactive-questionnaire/releases) 下载最新的 `interactive-questionnaire-vX.Y.Z.zip`（`.skill` 与 `.zip` 内容相同，上传入口若只认 `.zip` 就用后者）。
2. 打开 claude.ai 的 **设置 → 功能（Settings → Capabilities）**，在 Skills 区域上传该压缩包。
3. 需要 Pro / Max / Team / Enterprise 套餐并开启代码执行；上传的自定义 skill 属于个人，不在组织内共享。详见[官方 Agent Skills 文档](https://platform.claude.com/docs/zh-CN/agents-and-tools/agent-skills/overview)。

### 2. Claude Code

把 skill 文件夹放进 Claude Code 扫描的目录即可：

```bash
# 个人级（对所有项目生效）
git clone https://github.com/duskykitecn/interactive-questionnaire.git
mkdir -p ~/.claude/skills
cp -r interactive-questionnaire/interactive-questionnaire ~/.claude/skills/

# 或项目级（随仓库共享给团队）：复制到项目根的 .claude/skills/ 下
```

Windows 对应目录为 `%USERPROFILE%\.claude\skills\`。注意复制的是**仓库根目录下的同名子文件夹**（即含 `SKILL.md` 的那层）。

### 3. Claude API（Skills API）

通过 `/v1/skills` 端点把打包好的 zip 上传到工作区，再在请求中引用返回的 `skill_id`。详见[官方 Skills API 文档](https://platform.claude.com/docs/zh-CN/agents-and-tools/agent-skills/overview)。

## 用法

- **触发**：对话中点名 `interactive-questionnaire`（或在支持的产品里用斜杠命令 `/interactive-questionnaire`）显式启用；启用后凡 Claude 需要向你提问的场合都会按本 skill 组织。
- **文字版作答**：选择题按选项字母回答（多选给多个字母，如 `1: a,c`），自由题直接写文字。
- **HTML 问卷作答**：逐题填写（每题都可点「＋ 改用文字填写」换成自由文字，或提出异议），完成后点「复制结果」，把 JSON 粘贴回对话。
- **结果 JSON**：每题一个条目，三种形态——`answer`（按控件作答，带 `dirty` 标记区分是否改过默认值）、`custom`（自由文字）、`objection`(异议)；另有 `system` 元信息（主题、展示 / 折叠模式）。字段契约详见 [`interactive-questionnaire/SKILL.md`](interactive-questionnaire/SKILL.md)。
- **停止**：明确告诉 Claude 停用即可。

## 目录结构

```
interactive-questionnaire/            ← 仓库根
├── README.md                         ← 本文件
├── LICENSE
├── CHANGELOG.md                      ← 版本记录（Keep a Changelog）
├── PUBLISHING.md                     ← 维护者手册：发版流程、GitHub/Gitee/CNB 多平台同步
├── scripts/
│   └── package.py                    ← 本地打包脚本（仅需 Python 3 标准库）
├── .github/workflows/
│   ├── release.yml                   ← 推送 v* 标签 → 自动打包并发布 GitHub Release
│   └── sync-mirrors.yml              ← 可选：自动镜像到 Gitee / CNB（默认关闭）
└── interactive-questionnaire/        ← skill 实体（安装/打包的对象就是这一层）
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

产物在 `dist/` 下：`interactive-questionnaire-vX.Y.Z.skill` 与同内容的 `.zip`。压缩包以 skill 文件夹为根（`interactive-questionnaire/SKILL.md`），与官方 `.skill` 包结构一致，可直接上传 claude.ai 或 Skills API。

## 版本与发布

版本号遵循 SemVer，变更记录在 [CHANGELOG.md](CHANGELOG.md)。维护者推送 `vX.Y.Z` 标签后，GitHub Actions 会自动打包并创建附带 `.skill` / `.zip` 的 Release；完整发版流程与 GitHub / Gitee / CNB 多平台同步方案见 [PUBLISHING.md](PUBLISHING.md)。

仓库地址：

- GitHub（主库）：https://github.com/duskykitecn/interactive-questionnaire
- Gitee（镜像）：https://gitee.com/duskykite/interactive-questionnaire
- CNB（镜像）：https://cnb.cool/DuskyKite/interactive-questionnaire

## 许可证

本项目采用 [CC BY-NC 4.0](LICENSE)（署名-非商业性使用）许可：允许复制、修改与再分发，须署名并注明改动，**禁止商业用途**；商业授权请联系作者。协议原文见[知识共享官网](https://creativecommons.org/licenses/by-nc/4.0/deed.zh-hans)。

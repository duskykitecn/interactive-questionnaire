# 更新日志

本文件记录本项目所有值得注意的变更。

格式遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，
版本号遵循[语义化版本 SemVer](https://semver.org/lang/zh-CN/)。
针对本 skill 的版本号判据见 [PUBLISHING.md](PUBLISHING.md)。

## [未发布]

（暂无）

## [1.0.0] - 2026-07-10

首个公开版本。

### 新增

- 提问路由规则：简单提问走文字版（题号 / 选项号约定，每题附「为什么问、推荐怎么选」的描述），复杂提问走 HTML 交互问卷；一经调用对整个会话持续生效，且每轮结尾静默自检、发现散问当场补救。
- HTML 问卷引擎：`assets/template.html` 外壳 + `references/snippets/` 12 种组件片段（13 类用法，slider 含档位 / 数值两种模式），覆盖单选、多选、开关追问、滑杆、区间、计数、文本、排序等；`assets/demo.html` 提供全组件演示。
- 组件三条硬规则：每个可选组件带「改用文字填写」入口；必须预选最可能的默认项；能用直观控件就不用下拉。
- 结果 JSON 契约：用户点「复制结果」得到结构化 JSON，每题三态（`answer` 控件作答 / `custom` 自由文字 / `objection` 异议），含 `dirty` 默认值标记与 `system`（主题、展示 / 折叠模式）元信息；支持明暗主题自动探测与手动切换。
- 组件登记完备性自检：`references/components.md` 登记表、`references/snippets/` 文件数、`demo.html` 内 `COMPONENTS` 条目三处数量必须一致（当前均为 12）。

[未发布]: https://github.com/duskykitecn/interactive-questionnaire/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/duskykitecn/interactive-questionnaire/releases/tag/v1.0.0

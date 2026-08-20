---
name: interactive-questionnaire
description: >-
  When you (the agent) would ask the user anything at all — one quick
  question or a full intake of preferences, requirements, or structured input —
  use this skill instead of asking loosely in chat. It routes by complexity:
  simple asks become a numbered plain-text list (题号/选项号 convention); complex
  asks become an interactive HTML questionnaire assembled from a template plus
  component snippets, which the user fills in and copies back as JSON. Once
  invoked in a conversation it stays in effect for the whole conversation: every
  later question, even a single simple one, must go through the questionnaire or
  the text-version — never a casual free-form ask. Enforced by a mandatory
  silent end-of-turn self-check: each turn, verify no ask bypassed the
  questionnaire/text-version; stay silent when clean, else surface it and
  remediate on the spot. Covers the routing rule, the text convention, HTML
  assembly, component selection, the result-JSON contract, and the self-check.
---

# Interactive Questionnaire

当你要向用户提问时（哪怕只有一个问题），用本技能组织提问，而不是在聊天里零散追问。**一经在对话中启用，就对整个对话持续生效**（见下方「生效范围」）。

## 何时用

- 你需要向用户提问、或收集偏好/需求/结构化输入时——**哪怕只有一个问题**。
- 需要把用户回答变成**可解析的结构化结果**，而非一段散文。

## 生效范围：一经调用，全会话生效

本技能一旦在某次对话中被调用，就对该对话的**所有后续回合持续生效**，直到用户明确要求停止。**不要**问完一份问卷，就在下一回合把它忘掉、退回随口提问或散在聊天里问——那会导致「上一份问完、下一回合就不遵守、还退回没有约定的散问」，正是要杜绝的。

**任何时候你要向用户提问——无论问题多少、无论多简单——只能走以下两条之一，不存在第三条「随口简单问」的路线：**

- 复杂 → HTML 问卷；
- 简单 → 文字版（题号/选项号约定 + 每题描述），**即使只有一个问题也照此办理**。

即：普通自由散问被禁用；每一次提问，要么是问卷，要么是符合约定的文字版。

## 每轮结尾自检（强制）

本技能生效期间，**每一轮回复的结尾**都必须执行一次自检：逐条核对本轮输出中「面向用户、期待其回答的提问」是否全部走了问卷或文字版。修辞性反问、不期待用户回答的语句不在核对范围内。

- **静默执行**：自检通过时不输出任何标注，不打扰用户。
- **发现散问 → 当场补救**：在本轮结尾简要标注自检结果，并立即把该散问按路由规则（复杂 → HTML 问卷；简单 → 文字版）重新组织补上——是补救，不是只报告违规。
- 本自检是「生效范围」的强制执行机制：防止问完一份问卷后，回合一多就退化回随口散问。

## 用法：先正常输出，末尾再把问题总结成问卷/文字版

**本技能不改变你自身的输出行为。** 先按你的惯例正常展开分析、给出思路与建议——该怎么写就怎么写。等这一轮正常输出结束后，再做一次「总结性提问」：把其中真正需要用户拍板的问题，用最小心智负担、精确而完整地概括成「标题 + 描述 + 选项（如有）」，据此生成问卷（复杂）或文字版（简单），呈现给用户作答。

每个问题都带一段**描述**（见下）：讲清这个问题**为什么会出现**、**要解决什么**、**推荐哪种做法、为什么**。用意是——用户若能仅凭问卷/文字版就做决定，就直接决定；否则可对照你上面的原始输出理解、或就原始输出向你追问，从而以最快、最省心的方式与你的思路对齐。

## 路由：按复杂度二选一

技能触发后**不默认走问卷**，先判复杂度：

- **简单**（问题少、每题选项少、无排序/区间/多层嵌套）→ **文字版**：编号列出问题，用下面的题号/选项号约定。
- **复杂**（问题多，或含多选长列表、排序、数值区间、条件追问等）→ **HTML 问卷**：装配交给用户填。
- 用户可显式指定走哪一种，以用户要求为准。

## 文字版约定（题号 / 选项号）

只用于文字版；HTML 问卷不带题号/选项号（可视化已区分各题）。

**题号（强制）**：每题以阿拉伯数字 + `.` + 空格 + 问题正文开头，如 `1. 出行人数`、`2. 出发城市`。每份问卷从 `1.` 重新编号；第 10 题及以后用多位数 `10.`、`11.`。

**选项号**：
- **选择类问题**（有预设选项供选）→ 每个选项以小写字母 + `.` + 空格 + 选项正文给出，如 `a. 美食`、`b. 自然风光`；用户靠字母作答。
- **自由回答类问题**（让用户自己写文字，无预设选项）→ **不加**选项号。
- 选项超过 26 个（超出 `z`）时，把**最后一个选项固定为「其他」**，请用户用自己的话补充。

**问题描述**：在题号与选项之间放一段该问题的描述（**不带编号**），讲清为什么问、要解决什么、推荐怎么选——与 HTML 问卷里的描述区同义。

**用户回复与解析**：选择题按字母作答（多选给多个字母，如 `1: a,c`）、自由题写文字，按题号定位。解析这些回复填回你的流程；不要另造固定回传语法，自然作答即可。

示例：

```
1. 出行人数？
   同行人数决定房型与整体节奏，填你确定的人数即可；带老人小孩可在备注说明。
   a. 1 人   b. 2 人   c. 3–4 人   d. 5 人以上
2. 兴趣（可多选）？
   决定我优先推荐哪类目的地与活动，选你真正想要的即可。
   a. 美食   b. 自然风光   c. 历史人文
3. 怎么称呼你？（直接写）
   只是方便称呼你，随意填，不影响推荐。
```

## HTML 问卷：装配流程

引擎已封装为 `assets/template.html`（外壳）+ `references/snippets/`（每种组件一个片段）。装配步骤（详见 `references/components.md`）：

1. 复制 `assets/template.html`。
2. 替换顶部 `<QUESTIONNAIRE_TITLE>`（标题）与 `<QUESTIONNAIRE_SUBTITLE>`（一句副标题，**不写填写说明**）。
3. 每个问题选一种组件 → 从 `snippets/` 取片段 → 替换其中 `<大写下划线>` 占位（片段末尾有注释指引）→ 删掉注释行。
4. 所有填好的片段按顺序拼接，整体替换模板里那行 `<!-- QUESTION_FIELDS -->`。
5. 把完成的 HTML 交给用户打开填写。用户填完点「复制结果」得到 JSON，回贴给你解析。

要点：`data-field` 全问卷唯一、snake_case（= 结果 JSON 的 key）；每题预选最可能的默认项。每题标题下、预设区之上有一段**描述区**（填 `<QUESTION_DESC>`），承载该问题的「为什么 / 解决什么 / 推荐什么」——它只帮助用户理解，**不出现在结果 JSON 里**。完整 13 组件范例见 `assets/demo.html`。

## 组件选择

| 需求 | 用 | data-type |
| --- | --- | --- |
| 单选 · 选项少且短 | segmented | `segmented` |
| 单选 · 选项多 | select | `select` |
| 单选 · 每项需一句说明 | radio-cards | `radiocards` |
| 多选 · 选项少且短 | chips | `chips` |
| 多选 · 选项多或较长 | multi-select | `multiselect` |
| 是/否（可开启后追问） | toggle-reveal | `toggle` |
| 有序档位（悠闲/适中/紧凑） | slider（label 模式） | `slider` |
| 单个数值（预算等） | slider（number 模式） | `slider` |
| 数值区间（上下限） | range | `range` |
| 小整数计数（住几晚） | stepper | `stepper` |
| 单行短文本 | text | `text` |
| 多行长文本 | textarea | `textarea` |
| 优先级排序 | rank | `rank` |

**三条硬规则**：
1. 每个可选组件都带「＋ 改用文字填写」入口（用户随时可改为自由文字，值可能是字符串）——`text`/`textarea` 本身即文字，无此入口。
2. 必**预选最可能项**：单选选一项、多选选一或多个、数值/区间/计数给默认值、排序给合理初始次序。
3. 能用直观控件就不用下拉：选项少优先 segmented 而非 select；是/否用 toggle 而非两个选项。

## 结果 JSON 契约

用户点「复制结果」得到（与 `assets/demo.html` 引擎一致，**只含可见字段**——隐藏的条件子字段不出现）：

```json
{
  "title": "问卷标题",
  "responses": {
    "party_size": { "type": "answer",    "answer":    { "value": "2 人", "dirty": false } },
    "budget":     { "type": "custom",    "custom":    { "value": "看行程再定" } },
    "need_hotel": { "type": "objection", "objection": { "text": "这题不适用" } }
  },
  "system": {
    "theme": null,
    "display_mode": "preview",
    "fold_mode": "collapsed"
  }
}
```

- `responses` 的 key = 组件 `data-field`。每题一个条目，形如 `{ "type": ..., "<type>": {...} }`，只带当前 `type` 对应的那个对象：
  - `type: "answer"` → `answer: { value, dirty }`：用户按控件作答。`dirty=false` 表示仍是预选默认值（未改动），`true` 表示用户改过。
  - `type: "custom"` → `custom: { value }`：用户点了「改用文字填写」，`value` 是其自由文字。
  - `type: "objection"` → `objection: { text }`：用户对该题有异议/认为不适用，`text` 是其说明（可空）。
- `answer.value` 的形态随组件：单选/档位为字符串，多选为字符串数组，区间为 `[下限, 上限]`，排序为有序数组，计数/数值为数字。以引擎实际输出为准。
- `system`：`theme`、`display_mode`（`preview`/`raw`）、`fold_mode`（`collapsed`/`expanded`）。`theme` 取值 `null` | `"light"` | `"dark"` 且**恒出现**：首次问卷为 `null`（页面据环境 `prefers-color-scheme` 探测——探到则回填 `light`/`dark`，探不到保持 `null`；`null` 按 light 渲染但值不写成 light），用户手动切换后落为 `"light"`/`"dark"`；一旦非 `null` 便不再被探测覆盖。若要在同一会话的后续问卷里保持用户上次的选择，把新问卷 `template.html` 中的 `var themeState={value:null}` 改为上一份结果的 `system.theme`。解析结果时通常只关心 `responses`。

## 完备性自检

**三份清单必须行数相等**：`references/components.md` 登记表的行数 == `references/snippets/` 的文件数 == `assets/demo.html` 里 `COMPONENTS` 的条目数（当前均为 **12**）。

**加一种组件**只需三处小改：`assets/demo.html`（及 `template.html`）里 `COMPONENTS` 加一条 `{def, wire, collect, ...}` 条目 + `components.md` 登记表加一行 + `snippets/` 加一个片段文件。共享逻辑（折叠、异议、自定义、dirty、JSON 组装）已在引擎核心，无需触碰。

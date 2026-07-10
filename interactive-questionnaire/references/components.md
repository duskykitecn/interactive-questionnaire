# 组件库（HTML 问卷）

配合 `assets/template.html`。模板是引擎外壳，本目录每个片段是一种「字段」。装配一份问卷 = 选若干组件 → 复制对应片段 → 填占位 → 依次塞进模板的 `<!-- QUESTION_FIELDS -->` 处。引擎逻辑、交互、结果 JSON 全部内置，无需改动。

## 装配步骤

1. 复制 `assets/template.html`。
2. 替换顶部两个占位：`<QUESTIONNAIRE_TITLE>`（问卷标题）、`<QUESTIONNAIRE_SUBTITLE>`（一句副标题；不要写填写说明）。
3. 每个要问的问题：从 `snippets/` 取对应组件片段，替换其中 `<大写下划线>` 占位（见下表与片段末尾注释），删掉片段末尾的 `<!-- ... -->` 注释行。
4. 把填好的片段按提问顺序拼接，整体替换模板里那一行 `<!-- QUESTION_FIELDS -->`。
5. 完成的 HTML 作为 artifact 交给用户；用户填完点「复制结果」得到 JSON 回贴。

> `data-field` 必须**全问卷唯一**、用 **snake_case**——它就是结果 JSON 里该题的 key。`<QUESTION_LABEL>` 要**同时**填进 `data-label` 和 `.name`（两处一致）。

## 术语属性（data-*）

这些是稳定的「术语属性」，驱动引擎行为；不要新增或改名。

| 属性 | 用于 | 含义 |
| --- | --- | --- |
| `data-field` | 全部 | 该题唯一 key（snake_case），= 结果 JSON 的键 |
| `data-label` | 全部 | 问题标题（与 `.name` 文本一致） |
| `data-type` | 全部 | 组件类型，驱动全部逻辑（值无连字符：`multiselect`/`radiocards`/`toggle`） |
| `data-default` | text / textarea | 默认值（可空 `""`） |
| `data-mode` `data-labels` | slider | `label` 档位模式用 `data-labels`；`number` 数值模式 |
| `data-prefix` `data-suffix` | number-slider / range / stepper | 数值前后缀（如 `¥`、` 晚`） |
| `data-min` `data-max` | stepper | 计数夹取范围 |
| `data-items` | rank | 待排序项，逗号分隔 |
| `min` `max` `step` `value`（在 `<input>` 上） | slider / range | 滑块真实取值范围与预选值 |

> 标题里的 `.ctype`（如 `segmented`、`multi-select`）**仅供显示**，不影响逻辑，原样保留即可。

## 共用描述区（qdesc）

**每个**片段的 `.fbody` 第一个子元素都是描述区（在标题之下、预设区之上）：

```html
<div class="qdesc"><QUESTION_DESC></div>
```

`<QUESTION_DESC>` 填该问题的一段描述——为什么问、要解决什么、推荐怎么选，帮助用户看清问题全貌。折叠或标记异议时它随 `.fbody` 一起隐藏；它**仅用于显示，不出现在结果 JSON 里**。（文字版对应：题号与选项之间那段不带编号的描述。）

## 共用「改用文字填写」块

除 `text` / `textarea` 外，每个片段结尾都带这一段（原样保留）：

```html
<div class="cust"><button class="cust-toggle">＋ 改用文字填写</button><div class="reveal cust-reveal"><input type="text" class="cust-input" placeholder="<CUSTOM_PLACEHOLDER>"></div></div>
```

用户点它 → 该题改为自由文字作答（结果 `type` 变 `custom`）。`<CUSTOM_PLACEHOLDER>` 可留 `用你自己的话填写`，或按该题语境改（如 `填写城市名`）。

## 组件登记表

| 组件 | `data-type` | 何时选用 | 关键占位 | 片段 |
| --- | --- | --- | --- | --- |
| segmented | `segmented` | 单选 · 选项少且短 | `OPTION_*` | `snippets/segmented.html` |
| select | `select` | 单选 · 选项多（滚动圆选） | `OPTION_*` | `snippets/select.html` |
| radio-cards | `radiocards` | 单选 · 每项需一句说明 | `OPTION_VALUE/TITLE/DESC_*` | `snippets/radiocards.html` |
| chips | `chips` | 多选 · 选项少且短 | `OPTION_*` | `snippets/chips.html` |
| multi-select | `multiselect` | 多选 · 选项多或较长 | `OPTION_*` | `snippets/multiselect.html` |
| toggle-reveal | `toggle` | 是/否（可开启后追问） | `TOGGLE_HINT` `REVEAL_*` | `snippets/toggle.html` |
| slider | `slider` | 档位(label)或数值(number) | `LABEL_*` / `PREFIX` `SUFFIX` `MIN` `MAX` | `snippets/slider.html` |
| range | `range` | 数值区间（上下限） | `MIN` `MAX` `STEP` `VALUE_*` `PREFIX` | `snippets/range.html` |
| stepper | `stepper` | 小整数计数 | `MIN` `MAX` `VALUE` `SUFFIX` | `snippets/stepper.html` |
| text | `text` | 单行自由填写 | `DEFAULT` `PLACEHOLDER` | `snippets/text.html` |
| textarea | `textarea` | 多行自由填写 | `DEFAULT` `PLACEHOLDER` | `snippets/textarea.html` |
| rank | `rank` | 优先级排序 | `ITEM_*` | `snippets/rank.html` |

> **完备性 = 三份清单对齐**：本表 **12 行** == `snippets/` **12 个文件** == 引擎 `assets/demo.html` 里 `COMPONENTS` 的 **12 条目**。加一种组件 = 引擎加一条 `COMPONENTS` 条目 + 本表加一行 + `snippets/` 加一个文件，三处齐了就完备。

## 占位符速查

- `<FIELD_ID>`：题的唯一 key（snake_case）
- `<QUESTION_LABEL>`：问题标题（填进 `data-label` 与 `.name`）
- `<QUESTION_DESC>`：该问题的一段描述（标题下、预设上；帮助用户理解，不进结果 JSON）
- `<OPTION_1>` `<OPTION_2>`…：选项文本（按需增减；单选恰好一个 `aria-pressed="true"`，多选零或多个）
- `<OPTION_VALUE_*>` `<OPTION_TITLE_*>` `<OPTION_DESC_*>`：radio-cards 的值 / 标题 / 说明
- `<LABEL_1>…`：slider 档位标签（与 `.ticks` 的 `span` 一一对应）
- `<PREFIX>` `<SUFFIX>`：数值前后缀
- `<MIN>` `<MAX>` `<STEP>` `<VALUE>` `<VALUE_MIN>` `<VALUE_MAX>`：数值/区间/计数的范围与预选
- `<ITEM_1>…`：rank 待排序项
- `<TOGGLE_HINT>`：开关旁提示；`<REVEAL_FIELD_ID>` `<REVEAL_LABEL>` `<REVEAL_PLACEHOLDER>`：追问子字段
- `<DEFAULT>`：text/textarea 默认值；`<PLACEHOLDER>`：输入框提示
- `<CUSTOM_PLACEHOLDER>`：共用「改用文字填写」输入提示

## 装配示例（2 题）

模板里 `<!-- QUESTION_FIELDS -->` 替换为：

```html
<div class="field" data-field="party_size" data-type="segmented" data-label="出行人数">
  <div class="fhead"><span class="htitle"><span class="name">出行人数</span><span class="ctype">segmented</span></span></div>
  <div class="fbody">
    <div class="qdesc">同行人数决定房型与整体节奏，填你确定的人数即可；带老人小孩可在备注说明。</div>
    <div class="primary"><div class="seg" role="group" aria-label="出行人数"><button aria-pressed="false">1 人</button><button aria-pressed="true">2 人</button><button aria-pressed="false">3 人以上</button></div></div>
    <div class="cust"><button class="cust-toggle">＋ 改用文字填写</button><div class="reveal cust-reveal"><input type="text" class="cust-input" placeholder="用你自己的话填写"></div></div>
  </div>
</div>

<div class="field" data-field="name" data-type="text" data-label="称呼" data-default="小王">
  <div class="fhead"><span class="htitle"><span class="name">怎么称呼你</span><span class="ctype">text</span></span></div>
  <div class="fbody">
    <div class="qdesc">只是方便我在建议里称呼你，随意填或用默认都行，不影响推荐。</div>
    <div class="primary"><input type="text" placeholder="小王（默认）"></div>
  </div>
</div>
```

顶部 `<QUESTIONNAIRE_TITLE>` → `出行偏好`，`<QUESTIONNAIRE_SUBTITLE>` → `帮我了解你的出行偏好，以便给出更合适的建议。`

完整 13 组件范例见 `assets/demo.html`。

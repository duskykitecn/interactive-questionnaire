# 维护者手册：发版与多平台同步

面向仓库维护者。使用者看 [README.md](README.md)（英文）或 [README.zh-CN.md](README.zh-CN.md)（简体中文）。

## 总体分工

- **主库 GitHub**：https://github.com/duskykitecn/interactive-questionnaire ——唯一的开发源头，承担 CI（自动打包）、Releases（分发 `.skill` / `.zip`）、Issue 与 PR。
- **镜像 Gitee**：https://gitee.com/duskykite/interactive-questionnaire
- **镜像 CNB**：https://cnb.cool/DuskyKite/interactive-questionnaire
- 同步策略：Gitee 由 GitHub Actions 推送（`GITEE_SYNC_ENABLED`）；CNB 由 `.cnb.yml` git-sync 定时拉取。同一镜像不要推、拉两套同时开。**不在镜像仓库上直接提交**，镜像更新以覆盖为准。

> 若日后想改以 CNB 为主库开发：把「打标签自动发版」从 GitHub Actions 迁到 `.cnb.yml`（tag 触发流水线执行 `scripts/package.py`），同步方向反转即可，其余流程不变。

## 首次建仓（GitHub 主库）

```bash
cd interactive-questionnaire   # 仓库根目录
git init -b main
git add .
git commit -m "feat: v1.0.0 首个公开版本"

# 先在 GitHub 网页上新建空仓库 interactive-questionnaire（不要初始化 README），然后：
git remote add origin git@github.com:duskykitecn/interactive-questionnaire.git
git push -u origin main

# 打首个版本标签（触发 CI 自动出 Release）
git tag v1.0.0
git push origin v1.0.0
```

## 镜像初始化与日常同步

### Gitee

Gitee 官方「仓库镜像管理」选不到 GitHub **组织仓**（只能选个人仓），所以日常同步走主库 GitHub Actions 推送，不要靠 Gitee 网页从 GitHub 拉。

- **首次**：网页右上角「+ → 从 GitHub / GitLab 导入仓库」，源填 `https://github.com/duskykitecn/interactive-questionnaire`，路径落在 `duskykite/interactive-questionnaire`。（若已手动建了空仓库，也可本地 `git push --mirror git@gitee.com:duskykite/interactive-questionnaire.git` 灌一次。）
- **打开推送**：主库 Secrets 加 `GITEE_SSH_PRIVATE_KEY`（对应公钥加到 Gitee **个人 SSH 公钥**，标题如 `github-actions-gitee`；部署公钥只读，推不上去）。Variables 加 `GITEE_SYNC_ENABLED=true`。之后每次 push `main` 或 `v*` 标签，`sync-mirrors.yml` 强制推到 Gitee。
- 仓库页「同步」只留作备用。不要再打开 Gitee 自带的 GitHub 定时拉取，两套会对打。
- 镜像上关掉 Issue / PR / Wiki；简介写明请到 GitHub。

### CNB

GitHub 主库 → CNB 镜像，用官方 [git-sync](https://cnb.cool/cnb/plugins/tencentcom/git-sync) **拉取模式**（配置已在本仓库 `.cnb.yml`）。不要再打开 GitHub Actions 的 `CNB_SYNC_ENABLED`，两套会对着推。

**首次把代码灌进 CNB**（仓必须建在组织下，例如 `DuskyKite/interactive-questionnaire`）：

```bash
# 在 CNB 网页建空仓后，本机推一次完整镜像。用户名固定 cnb，密码用 CNB 访问令牌（只在终端输入，不要贴进对话）。
git push --mirror https://cnb.cool/DuskyKite/interactive-questionnaire.git
```

**打开定时同步**：

1. 建一个 GitHub fine-grained PAT，只授本仓库 Contents **只读**（公开仓也建议带令牌，避免匿名限额）。
2. 在 CNB 镜像仓的流水线 / 环境变量里加 `GIT_USERNAME`（GitHub 用户名）、`GIT_ACCESS_TOKEN`（上一步 PAT）。更稳妥是放进 CNB 密钥库再 `imports`，不要写进 YAML。
3. `.cnb.yml` 随主库同步到 CNB 后，crontab 每 2 小时（UTC）从 GitHub pull，含标签、允许强制覆盖。可在 CNB 流水线页点「立即运行」等不及定时。

**日常**：主库 `git push` 之后最多等一个 crontab 周期；发版打了 `v*` 标签也会被 `push_tags` 拉过去。GitHub Release 附件不会出现在 CNB。国内下载走 `static.duskykite.com.cn`，见下文「静态托管」。

密钥不写进 `.cnb.yml`，放在组织密钥仓 `DuskyKite/secrets`。密钥文件若声明了 `allow_images`，`imports` 必须写在 `tencentcom/git-sync` 插件任务上，不能写在流水线层，否则会报「只能在插件任务引用」。`allow_events` 必须写成完整事件名（如 `"crontab: 0 */2 * * *"`），只写 `crontab` 对不上。CNB 没有关闭 Issue / PR 的开关，简介写明镜像即可。

### 镜像平台的发行版

GitHub Release 及其附件**不会**随 git 同步到镜像（同步的只有提交与标签）。国内下载以 `static` 总仓为准，不必在 Gitee / CNB 再传一遍附件。

## 静态托管（多项目共用 static 子域，不走 COS）

演示页和发版包都是静态文件，挂在同一对 **static 子域** 的 `/项目名/` 下。本项目地址：

- GitHub Pages：https://duskykitecn.github.io/interactive-questionnaire/
- 国内演示：https://static.duskykite.com.cn/interactive-questionnaire/
- 海外演示：https://static.duskykite.xyz/interactive-questionnaire/
- 国内下载（最新）：https://static.duskykite.com.cn/interactive-questionnaire/releases/latest/interactive-questionnaire.skill
- 海外下载（最新）：https://static.duskykite.xyz/interactive-questionnaire/releases/latest/interactive-questionnaire.skill

命名统一用 **static**：子域名是 `static`，总仓是 `duskykitecn/static`。不要用 `artifacts`（那是 CI 产物，不含演示 HTML）。根域 `duskykite.com.cn` / `duskykite.xyz` 留给以后的官网。

**不要用 COS。** 静态 HTML 和很小的 `.skill` / `.zip` 用免费托管即可。

**也不要把每个项目仓库单独接成 EdgeOne Pages。** 一个 Git 项目占整个主机名的 `/`，项目之间会抢。正确做法是单独一个 **static 总仓**，根目录按项目名分文件夹；`static.*` 两个主机名都发布这个总仓。

```
duskykitecn/static            ← 总仓，只放拍扁后的静态文件
├── .nojekyll
├── index.html                ← 可选：项目目录索引
├── interactive-questionnaire/
│   ├── index.html
│   ├── assets/demo.html
│   └── releases/
│       ├── latest/
│       │   ├── interactive-questionnaire.skill
│       │   └── interactive-questionnaire.zip
│       └── v1.0.0/
│           ├── interactive-questionnaire-v1.0.0.skill
│           └── interactive-questionnaire-v1.0.0.zip
└── <下一个项目>/
```

不要在总仓放 GitHub Pages 的 `CNAME`：两个 `static.` 都走 EdgeOne，再写 `CNAME` 会把 xyz 抢回 GitHub。

发布链路（EdgeOne Makers 免费版，两个项目）：

```
各项目仓库
    ├─ push main
    │    ├─ 该仓库自己的 GitHub Pages → github.io/<项目名>/
    │    └─ Actions 只更新总仓里的 /<项目名>/ 演示页（不动 releases/）
    └─ 推送 v* 标签
         ├─ GitHub Release 附件
         └─ Actions 写入总仓 /<项目名>/releases/vX.Y.Z/ 与 releases/latest/
                ├─ EdgeOne 项目 A（中国大陆）
                │    static.duskykite.com.cn/<项目名>/
                └─ EdgeOne 项目 B（全球不含大陆）
                     static.duskykite.xyz/<项目名>/
```

原理：DNS 把 `static.duskykite.*` 指到 **EdgeOne**，不是 GitHub。加速区域是项目级，所以国内、海外各建一个 Makers 项目，都导入同一个 `duskykitecn/static`。文件夹名仍是 URL 路径。

免费：Makers 免费版约 40 个项目、200 个自定义域名、免费证书；静态文件几乎用不完。免费版不承诺 SLA，日后商业化可能收紧配额。`.com.cn` 已备案所以能走国内节点；`.xyz` 选「不含大陆」故不必备案，访问也不经过 GitHub。

本项目日常：改 `interactive-questionnaire/assets/demo.html` 并 push `main`。本仓库 GitHub Pages 自动更新；打开了总仓同步后，两个 `static.` 地址一起更新。其它项目复制 `scripts/build_site.py` + `deploy-site.yml`，把目录名改成自己的项目名即可。

本地预览构建产物：

```bash
python scripts/build_site.py
# 用浏览器打开 dist/site/interactive-questionnaire/index.html
```

### 首次接入（组织级，只做一次）

仓库侧不会登录你的腾讯云或 GitHub 账号。PAT 只进 GitHub Secrets，不要贴进对话。

若总仓仍叫 `duskykitecn/pages`、子域仍是 `pages.`，在 GitHub 网页把仓库改名为 `static`，DNS 把主机记录 `pages` 改成 `static`，EdgeOne 两个项目的自定义域名同步改绑。GitHub 会重定向旧仓地址。

1. **建总仓**（新环境；已有仓则改名即可）：

```bash
gh repo create duskykitecn/static --public --add-readme --description "DuskyKite static hosting"
```

总仓根保留 `.nojekyll`。若已误加 GitHub 用的 `CNAME`，删掉并推送。可选再放一个简单的 `index.html` 作目录。总仓 **不必** 开 GitHub Pages 自定义域名。

2. **EdgeOne 项目 A（国内）**：开通 Makers 免费版 → 导入 `duskykitecn/static` → 分支 `main`，无构建、输出 `.`。加速区域 **中国大陆可用区**。绑定 `static.duskykite.com.cn`，免费证书。DNS（com.cn）：CNAME 主机记录 `static` → 该项目控制台给出的地址。

3. **EdgeOne 项目 B（海外）**：再新建一个 Makers 项目，导入 **同一个** GitHub 仓。加速区域 **全球可用区（不含中国大陆）**（不必备案）。绑定 `static.duskykite.xyz`，免费证书。DNS（xyz）：CNAME 主机记录 `static` → **这个**项目控制台给出的地址（与国内那条不是同一个 CNAME 目标）。两个项目不要交叉绑定域名。

4. **本仓库打开同步**：建一个**只对 `duskykitecn/static` 有 Contents 写权限**的 fine-grained PAT。在本仓库 Settings → Secrets 加 `STATIC_DEPLOY_TOKEN`（在 GitHub 网页粘贴）。Settings → Variables 加 `STATIC_DEPLOY_ENABLED=true`、`STATIC_REPO=duskykitecn/static`。删掉旧的 `PAGES_*`。Actions 里手动跑一次 **Deploy demo site**；已有版本用 **Release** 的 `workflow_dispatch`、version 填 `1.0.0` 补推发版包。

5. **以后新项目**：同一套脚本，把 `PROJECT_SLUG` / 构建输出目录改成新项目名；PAT 可复用。总仓和两个 EdgeOne 项目都不用再建。

常见坑：把某个项目的整仓原样挂到 `/项目名/` 会双重路径。必须用 `build_site.py` 的拍扁产物。演示同步只覆盖 `index.html` 与 `assets/demo.html`，**不要** `rm -rf` 整个项目目录，否则会删掉 `releases/`。

## 日常发版流程

1. 修改技能内容（`interactive-questionnaire/` 子目录）。
2. 在 `CHANGELOG.md` 的「未发布」区记录变更；发版时把它落成新版本号小节（含日期），并更新文件底部的对比链接。
3. 本地验证打包：`python scripts/package.py`，抽查 `dist/` 产物能正常解压、`SKILL.md` 在压缩包根级文件夹内。
4. 提交并推送：`git add . && git commit -m "..." && git push`。
5. 打标签并推送：`git tag vX.Y.Z && git push origin vX.Y.Z`。
6. GitHub Actions（`release.yml`）自动打包：先把 `.skill` / `.zip` 写入 `static` 总仓 `releases/`，再创建或更新 GitHub Release（正文含该版本国内 / 海外下载地址，并覆盖旧说明）。检查 Release 正文链接与 `static.duskykite.com.cn/.../releases/latest/` 都能打开。补跑已有标签时从 **main** 触发 `workflow_dispatch`（不要用旧标签上的 workflow）；工作流会检出该标签打包，再从触发提交取回写说明脚本。
7. 若改过 `demo.html`：push 到 `main` 后本仓库 GitHub Pages 自动更新；打开了 `STATIC_DEPLOY_ENABLED` 则 `static.` 子域随总仓一起更新（见上文「静态托管」）。
8. 同步镜像：Gitee 由 `sync-mirrors.yml` 随 push 自动推（需 `GITEE_SYNC_ENABLED`）；CNB 由 `.cnb.yml` 的 git-sync crontab 拉取（见上文「CNB」）。等不及定时可在 CNB 流水线点「立即运行」。

## 版本号判据（针对本技能的 SemVer 语义）

- **MAJOR（不兼容变更）**：改动会让老用户的既有用法失效——如结果 JSON 契约字段改名 / 结构变化、文字版题号选项号约定变更、组件 `data-field` 语义变化。
- **MINOR（向下兼容的新能力）**：新增组件、新增可选字段、新增路由能力、demo / 模板的功能性增强。
- **PATCH（向下兼容的修复）**：文案修订、样式修补、示例修正、打包脚本修复。

判断口径：**以「已装旧版的用户升级后是否需要改变用法」为准**。

## 主库与镜像核对清单

只在 GitHub 开发。Gitee / CNB 当只读镜像。

**GitHub 主库**

- About：Description 与 Topics（如 `agent-skills`）；Website 填本仓 GitHub Pages `https://duskykitecn.github.io/interactive-questionnaire/`（国内演示写在 README，不要改成 `static.`）。
- Issues / PR 开在这里；Releases 由 `v*` 标签 + `release.yml` 生成。
- Settings → Pages：源 `main` 根目录（本仓演示已有 `index.html`）。
- 打开 `GITEE_SYNC_ENABLED`（Gitee 网页拉不到组织仓）。不要打开 `CNB_SYNC_ENABLED`（与 CNB git-sync 对推）。

**Gitee 镜像**

- 用「从 GitHub 导入」或一次 `git push --mirror` 灌入；之后靠 `GITEE_SYNC_ENABLED` + `GITEE_SSH_PRIVATE_KEY` 推送。
- 简介写明镜像、Issue 请到 GitHub。关掉 Issue / PR / Wiki。
- 仓库页「同步」只留备用；不要再开 Gitee 自带的 GitHub 定时拉取。
- 不必上传发行版附件，国内下载走 `static.` 子域。

**CNB 镜像**

- 仓在组织下；首次 `--mirror` 灌入后走 `.cnb.yml` git-sync。
- 密钥在 `DuskyKite/secrets`，由 `.cnb.yml` 的 `imports` 注入；简介标明镜像。
- CNB 关不掉 Issue / PR，简介写明即可。

**不必做**

- 镜像上再配一套 GitHub Actions / 再打一遍 Release。
- 每个项目单独接 EdgeOne Pages 或 COS。
- 在 Gitee / CNB 直接 commit（下次同步会被覆盖）。

## 备选同步方案（一般不用）

### 方案 A：一次 push 同推三个远程（零依赖）

```bash
git remote set-url --add --push origin git@github.com:duskykitecn/interactive-questionnaire.git
git remote set-url --add --push origin git@gitee.com:duskykite/interactive-questionnaire.git
git remote set-url --add --push origin https://cnb.cool/DuskyKite/interactive-questionnaire.git
git push && git push origin --tags
```

注意：`--add --push` 第一次执行会清掉默认 push 地址，所以 GitHub 地址也要显式加一遍（如上）。

### 方案 B 的 CNB 推送（不要与 crontab 同时开）

`.github/workflows/sync-mirrors.yml` 的 **Gitee job 已是当前方案**（`GITEE_SYNC_ENABLED=true`）。CNB job 保持关闭：不要设 `CNB_SYNC_ENABLED`，否则会与 `.cnb.yml` git-sync 对推。若以后改成主库推 CNB，再加 `CNB_TOKEN` 并关掉 crontab。

## 常见坑

- **标签漏推**：Release 由标签触发，`git push` 默认不推标签，务必 `git push origin vX.Y.Z`。
- **在镜像上直接改动**：无论哪种同步方式，镜像更新都是覆盖式的，Gitee / CNB 上的直接提交会丢；统一只在 GitHub 主库开发。
- **CNB 仓库归属与认证**：CNB 仓库必须建在组织（根组织）下；git 地址即仓库页面地址（带不带 `.git` 均可）；HTTPS 认证的用户名固定为 `cnb`、密码为访问令牌——令牌等同密码，切勿提交进仓库。
- **压缩包结构**：给智能体应用上传的 `.skill` / `.zip` 必须以技能文件夹为根（`interactive-questionnaire/SKILL.md`），不要把 `SKILL.md` 直接放在压缩包顶层，也不要把整个仓库（含 README 等）打进去——用 `scripts/package.py` 即可保证。
- **静态托管双重路径**：`static.` 主机名必须用 `build_site.py` 的拍扁产物挂到总仓 `/项目名/`，不要把整仓原样上传，也不要为每个项目单独接 EdgeOne Pages。
- **不要用 COS**：演示页和发版包都走 GitHub Pages + EdgeOne Makers 免费版。
- **改了组件记得三处对齐**：`references/components.md` 登记表行数、`references/snippets/` 文件数、`assets/demo.html` 里 `COMPONENTS` 条目数必须一致（SKILL.md「完备性自检」）。

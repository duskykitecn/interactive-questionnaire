# 维护者手册：发版与多平台同步

面向仓库维护者。使用者只需看 [README.md](README.md)。

## 总体分工

- **主库 GitHub**：https://github.com/duskykitecn/interactive-questionnaire ——唯一的开发源头，承担 CI（自动打包）、Releases（分发 `.skill` / `.zip`）、Issue 与 PR。
- **镜像 Gitee**：https://gitee.com/duskykite/interactive-questionnaire
- **镜像 CNB**：https://cnb.cool/DuskyKite/interactive-questionnaire
- 同步策略：当前采用**平台自带工具**（下文「当前同步方案」）；**不在镜像仓库上直接提交**，镜像更新以覆盖为准。

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

## 镜像初始化与日常同步（当前方案：平台自带工具）

### Gitee

- **首次**：网页右上角「+ → 从 GitHub / GitLab 导入仓库」，源填 `https://github.com/duskykitecn/interactive-questionnaire`，路径落在 `duskykite/interactive-questionnaire`。（若已手动建了空仓库，也可本地 `git push --mirror git@gitee.com:duskykite/interactive-questionnaire.git` 一次灌入。）
- **日常**：每次 GitHub 发版后，到 Gitee 仓库页点「同步」按钮更新镜像。

### CNB

- **首次**（两选一）：
  1. 官方批量迁移工具 [code-import](https://cnb.cool/cnb/plugins/cnbcool/code-import)（需源平台令牌 + CNB 访问令牌）；
  2. 本地一次镜像推送：`git push --mirror https://cnb.cool/DuskyKite/interactive-questionnaire.git`（HTTPS 认证：用户名固定为 `cnb`，密码填访问令牌）。
- **日常**（两选一）：
  1. 官方跨平台同步插件 [git-sync](https://cnb.cool/cnb/plugins/tencentcom/git-sync)，在 CNB 侧配成定时任务，自动从 GitHub 拉取并推送到 CNB 镜像，一次配置长期有效；
  2. 更新频率低就更省事：每次发版后本地重复上面那条 `git push --mirror ...` 即可（凭据管理器记住令牌后无感）。

### 镜像平台的发行版

GitHub Release 及其附件**不会**随 git 同步到镜像（同步的只有提交与标签）。Gitee 与 CNB 侧若需要本地下载入口：发版后在各自的「发行版」页手动创建同名发行版，把 `dist/` 里的 `.skill` / `.zip` 作为附件上传；或直接在镜像 README 里引导到 GitHub Releases 下载。

## 日常发版流程

1. 修改 skill 内容（`interactive-questionnaire/` 子目录）。
2. 在 `CHANGELOG.md` 的「未发布」区记录变更；发版时把它落成新版本号小节（含日期），并更新文件底部的对比链接。
3. 本地验证打包：`python scripts/package.py`，抽查 `dist/` 产物能正常解压、`SKILL.md` 在压缩包根级文件夹内。
4. 提交并推送：`git add . && git commit -m "..." && git push`。
5. 打标签并推送：`git tag vX.Y.Z && git push origin vX.Y.Z`。
6. GitHub Actions（`release.yml`）自动打包并创建 Release，附上 `.skill` 与 `.zip`。检查 Release 页面产物无误。
7. 同步镜像：Gitee 点「同步」；CNB 由 git-sync 定时任务自动跟上（或手动 mirror push 一次）。

## 版本号判据（针对本 skill 的 SemVer 语义）

- **MAJOR（不兼容变更）**：改动会让老用户的既有用法失效——如结果 JSON 契约字段改名 / 结构变化、文字版题号选项号约定变更、组件 `data-field` 语义变化。
- **MINOR（向下兼容的新能力）**：新增组件、新增可选字段、新增路由能力、demo / 模板的功能性增强。
- **PATCH（向下兼容的修复）**：文案修订、样式修补、示例修正、打包脚本修复。

判断口径：**以「已装旧版的用户升级后是否需要改变用法」为准**。

## 备选同步方案（暂未采用，备查）

### 方案 A：一次 push 同推三个远程（零依赖）

```bash
git remote set-url --add --push origin git@github.com:duskykitecn/interactive-questionnaire.git
git remote set-url --add --push origin git@gitee.com:duskykite/interactive-questionnaire.git
git remote set-url --add --push origin https://cnb.cool/DuskyKite/interactive-questionnaire.git
git push && git push origin --tags
```

注意：`--add --push` 第一次执行会清掉默认 push 地址，所以 GitHub 地址也要显式加一遍（如上）。

### 方案 B：GitHub Actions 自动镜像

`.github/workflows/sync-mirrors.yml` 已按上述三个地址写好，默认关闭。启用 Gitee 侧：Secrets 加 `GITEE_SSH_PRIVATE_KEY`（对应公钥加到 Gitee）+ Variables 加 `GITEE_SYNC_ENABLED=true`；启用 CNB 侧：Secrets 加 `CNB_TOKEN` + Variables 加 `CNB_SYNC_ENABLED=true`。此后每次 push 到 `main` 或推送 `v*` 标签自动强制镜像。

## 常见坑

- **标签漏推**：Release 由标签触发，`git push` 默认不推标签，务必 `git push origin vX.Y.Z`。
- **在镜像上直接改动**：无论哪种同步方式，镜像更新都是覆盖式的，Gitee / CNB 上的直接提交会丢；统一只在 GitHub 主库开发。
- **CNB 仓库归属与认证**：CNB 仓库必须建在组织（根组织）下；git 地址即仓库页面地址（带不带 `.git` 均可）；HTTPS 认证的用户名固定为 `cnb`、密码为访问令牌——令牌等同密码，切勿提交进仓库。
- **压缩包结构**：上传 claude.ai / Skills API 的包必须以 skill 文件夹为根（`interactive-questionnaire/SKILL.md`），不要把 `SKILL.md` 直接放在压缩包顶层，也不要把整个仓库（含 README 等）打进去——用 `scripts/package.py` 即可保证。
- **改了组件记得三处对齐**：`references/components.md` 登记表行数、`references/snippets/` 文件数、`assets/demo.html` 里 `COMPONENTS` 条目数必须一致（SKILL.md「完备性自检」）。

# GH Account Router

用于在多个 GitHub 账号之间安全地路由 `gh` CLI 命令的 Skill 包。

## 功能概览

- 按账号别名选择对应 Token 执行 `gh` 命令
- 仅对子进程注入 `GH_TOKEN`，不污染当前 shell
- 自动脱敏输出中的 Token 字符串
- 支持私有账号文件（不入库）

## 快速开始

从 `gh-account-router/` 路径安装 Skill：

```powershell
python scripts/install-skill-from-github.py --repo Harzva/gh-account-router --path gh-account-router
```

安装后重启 Codex，使新 Skill 被发现。

## 仓库结构

```text
gh-account-router/
  SKILL.md
  agents/openai.yaml
  scripts/gh_account_router.py
  references/accounts.md
```

说明：仓库根目录主要是打包与说明文件，Skill 主体位于 `gh-account-router/` 目录。

## 账号文件（私有）

不要提交 Token。请将账号文件存放在仓库外，例如：

```text
<github token for account A>
harzva
Harzva

<github token for account B>
saihao
3873225350
```

配置环境变量：

```powershell
$env:GH_ACCOUNT_ROUTER_ACCESS_FILE = "D:\private\github-accounts.txt"
```

或在命令中显式传入：

```powershell
python .\gh-account-router\scripts\gh_account_router.py --access-file D:\private\github-accounts.txt --account harzva -- api user --jq .login
```

## 常用命令

以下示例使用 `saihao` 账号，你也可以替换为 `harzva`。

列出已配置账号别名：

```powershell
python .\gh-account-router\scripts\gh_account_router.py --list
```

用指定账号查询当前登录信息：

```powershell
python .\gh-account-router\scripts\gh_account_router.py --account saihao -- api user --jq .login
```

用指定账号查看仓库：

```powershell
python .\gh-account-router\scripts\gh_account_router.py --account saihao -- repo view saihao/<repository-name>
```

## 安全说明

- 不要在 README、提交记录、日志、Issue 或对话中粘贴 Token
- 不要提交账号文件、`.env`、凭据转储、日志或缓存
- 仅在确实需要鉴权时读取私有账号文件

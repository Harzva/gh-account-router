# GH Account Router Skill

Codex Skill package for routing GitHub CLI work across multiple GitHub accounts.

## Skill Package

Install this repo as a skill from the `gh-account-router/` path:

```powershell
python scripts/install-skill-from-github.py --repo Harzva/gh-account-router --path gh-account-router
```

After installing, restart Codex so the new skill is discovered.

## Repository Layout

```text
gh-account-router/
  SKILL.md
  agents/openai.yaml
  scripts/gh_account_router.py
  references/accounts.md
```

The root of this repository only contains packaging documentation and repository metadata. The actual skill is the `gh-account-router/` folder.

## Private Access File

Do not commit tokens. Store account tokens outside this repository:

```text
<github token for account A>
harzva
Harzva

<github token for account B>
saihao
3873225350
```

Set the path:

```powershell
$env:GH_ACCOUNT_ROUTER_ACCESS_FILE = "D:\private\github-accounts.txt"
```

Or pass it directly:

```powershell
python .\gh-account-router\scripts\gh_account_router.py --access-file D:\private\github-accounts.txt --account harzva -- api user --jq .login
```

## Safety

This repository intentionally excludes `githubacess.txt`, `.env` files, token dumps, logs, and caches.

# GH Account Router

Route GitHub CLI work between multiple GitHub accounts without changing the global `gh` login.

This repository publishes the `gh-account-router` Codex skill plus its helper script. It is designed for users who keep separate GitHub tokens for personal, organization, client, or lab accounts and want each `gh` command to run with the correct identity.

## What It Does

- Reads a private local token file.
- Finds the requested account by alias.
- Runs `gh` with `GH_TOKEN` set only for that child process.
- Removes conflicting `GITHUB_TOKEN` from the child environment.
- Redacts token-like strings from command output.

## Files

```text
SKILL.md                     Codex skill instructions
scripts/gh_account_router.py CLI wrapper for GitHub account routing
references/accounts.md       Account-file format reference
agents/openai.yaml           Optional UI metadata
```

## Private Access File

Do not commit this file. Store it outside the repository, for example:

```text
<github token for account A>
harzva
Harzva

<github token for account B>
saihao
3873225350
```

Then configure the path:

```powershell
$env:GH_ACCOUNT_ROUTER_ACCESS_FILE = "D:\private\github-accounts.txt"
```

Or pass it per command:

```powershell
python .\scripts\gh_account_router.py --access-file D:\private\github-accounts.txt --account harzva -- api user --jq .login
```

## Examples

```powershell
python .\scripts\gh_account_router.py --list
python .\scripts\gh_account_router.py --account harzva -- repo view Harzva/example
python .\scripts\gh_account_router.py --account saihao -- api user --jq .login
```

Everything after `--` is passed directly to `gh`:

```powershell
python .\scripts\gh_account_router.py --account harzva -- repo create Harzva/new-repo --public
```

## Safety

Never commit tokens, `.env` files, credential dumps, or generated logs. This repository intentionally contains only the router code and documentation.

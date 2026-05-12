---
name: gh-account-router
description: Route GitHub and gh CLI work between the user's two managed GitHub accounts, Harzva and saiHao/saihao. Use when creating repositories, pushing code, setting remotes, selecting the correct GitHub token, publishing to Harzva or saihao, or diagnosing account/permission mismatches. Never expose or commit tokens.
---

# GH Account Router

Use this skill to choose and operate the correct GitHub account for repository work.

## Accounts

Managed accounts:

- `Harzva`: default/current personal account.
- `saihao`: user-facing alias whose token currently resolves to GitHub login `3873225350`.

Private token source:

- A private access file passed with `--access-file` or configured through `GH_ACCOUNT_ROUTER_ACCESS_FILE`.

Do not copy token values into prompts, skill files, commits, logs, README files, or final answers. Read this file only when a GitHub operation needs authentication.

## Routing Rules

- If the user says `harzva`, `Harzva`, or asks for the Harzva profile/account, use `Harzva`.
- If the user says `saihao`, `saiHao`, or asks to publish under saihao, use the `saihao` alias and verify the canonical login before creating the repo.
- If the repository owner is explicit in a URL such as `saihao/repo` or `Harzva/repo`, follow the owner.
- If owner intent is unclear, inspect existing remotes and nearby docs before asking.
- Before creating a repository, verify the active account can create under the requested owner. If not, use the token-routed script below or explain the permission issue.

## Preferred Workflow

1. Determine the target owner: `Harzva` or the `saihao` alias.
2. Check current state:

```powershell
gh auth status
git remote -v
git status --short --branch
```

3. For account-specific `gh` commands, prefer the helper script:

```powershell
python scripts/gh_account_router.py --account saihao -- repo view saihao/REPO
```

Everything after `--` is passed to `gh`.

4. For repository creation:

```powershell
python scripts/gh_account_router.py --account saihao -- repo create saihao/REPO --public --description "..." --source . --remote origin --push
```

5. If using plain git remotes, use HTTPS remotes and let `gh`/credential manager handle auth:

```powershell
git remote add origin https://github.com/saihao/REPO.git
git push -u origin main
```

6. After publishing, verify with:

```powershell
python scripts/gh_account_router.py --account saihao -- repo view saihao/REPO --json nameWithOwner,url,visibility
```

## Helper Script

Use `scripts/gh_account_router.py` when account identity matters. It reads the private access file, selects the token block matching the requested account or alias, sets `GH_TOKEN` only for the child `gh` process, and redacts token-like strings from output.

Useful commands:

```powershell
python scripts/gh_account_router.py --list
python scripts/gh_account_router.py --account harzva -- api user --jq .login
python scripts/gh_account_router.py --account saihao -- api user --jq .login
```

If this returns `3873225350`, publish repositories under `3873225350/<repo>` unless the user explicitly confirms that `saiHao/<repo>` is required and provides a token with permission for that owner.

## Safety

- Never print raw access file contents.
- Never commit `githubacess.txt`, tokens, `.env`, credential dumps, or generated logs containing secrets.
- When final-answering, mention only account names, repository URLs, commands run, and status.
- If GitHub returns permission errors, report the owner mismatch plainly and avoid retry loops.

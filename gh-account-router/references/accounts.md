# Managed GitHub Accounts

This skill manages two GitHub identities:

| Canonical owner | Aliases | Typical use |
| --- | --- | --- |
| `Harzva` | `harzva` | Default personal repositories and profile projects. |
| `3873225350` | `saihao`, `saiHao` | Repositories the user refers to as saihao-owned, when the token resolves to `3873225350`. |

Private access file: pass `--access-file` or set `GH_ACCOUNT_ROUTER_ACCESS_FILE`.

Expected file pattern:

```text
<github token for account A>
<alias/login for account A>

<github token for account B>
<alias/login for account B>
<optional extra alias>
```

Token values must stay only in the private access file.

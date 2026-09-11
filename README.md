# Snippet Vault

Two independent apps in one repo: a React front end in `web/` and a NestJS API in `api/`.

## Start the front end

```sh
cd web && npm install && npm run dev
```

## Start the API

```sh
cd api && npm install && npm run start:dev
```

## Quality gates

Run inside `api/` (the `web/` app has `npm run lint` only):

| Command | What it catches |
| --- | --- |
| `npm run lint` | Bugs and bad patterns oxlint can spot statically (unused vars, unreachable code, suspicious comparisons). |
| `npm run format` | Inconsistent formatting; rewrites files with prettier. `npm run format:check` reports instead of rewriting. |
| `npm run test` | Broken behaviour in unit tests. `npm run test:e2e` does the same for HTTP routes end to end. |
| `npm audit` | Dependencies with known security vulnerabilities. |

`npm run gate` runs lint, format:check, test and test:e2e in that order and stops at the first failure.

To run the gate automatically before every commit (api gate plus web lint), enable the repo hooks once:

```sh
git config core.hooksPath .githooks
```

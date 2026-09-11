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

### API configuration

The API reads its settings from environment variables (see `api/src/config.ts`). The start scripts load `api/.env` if it exists via `node --env-file-if-exists`, so copy the example and edit it; the file is gitignored. You can also export the variables in your shell instead.

```sh
cp api/.env.example api/.env
```

| Variable | Default | Meaning |
| --- | --- | --- |
| `PORT` | `3000` | TCP port the API listens on. |
| `CORS_ORIGIN` | `http://localhost:5173` | The single browser origin allowed to call the API (the Vite dev server by default). `*` is rejected at startup. |

## Run with Docker

Builds both apps and starts them together. The API loads `api/.env` (copy it from the example first, see above).

```sh
docker compose up --build
```

The app is at http://localhost:5173 (nginx serves the front end and proxies `/snippets` to the API). The API is also published directly at http://localhost:3000.

```sh
docker compose down
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

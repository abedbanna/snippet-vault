# Snippet Vault

[![CI](https://github.com/abedbanna/snippet-vault/actions/workflows/ci.yml/badge.svg)](https://github.com/abedbanna/snippet-vault/actions/workflows/ci.yml)

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

## Production

The host needs Docker (with the compose plugin), a clone of this repo, and a `.env` at the repo root holding the API settings from the table above (set `CORS_ORIGIN` to the site's public origin, e.g. `http://vault.example.com`). The file is gitignored; create it on the server.

```sh
docker compose -f docker-compose.prod.yml up -d --build
```

This builds the `snippet-vault-api` and `snippet-vault-web` images on the host and serves the app on port 80. Only the web service is published: nginx proxies `/snippets` to the API inside the compose network, so the API is not reachable from the internet. Both containers restart automatically unless stopped.

### Deploy to DigitalOcean

`terraform/` creates one droplet (`s-1vcpu-2gb`, Ubuntu 24.04, `fra1`) with your SSH key and a firewall that only allows inbound TCP 22, 80 and 443. `ansible/` installs Docker on it, clones this repo into `/opt/snippet-vault`, writes the `.env` and starts the production stack. Three commands:

```sh
# 1. Create the droplet. The token comes from the environment only: never from a file,
#    and not from your shell history either (read -s prompts for it without echo).
read -rs DIGITALOCEAN_TOKEN && export DIGITALOCEAN_TOKEN
terraform -chdir=terraform init
terraform -chdir=terraform apply -var ssh_public_key_path=~/.ssh/id_ed25519.pub

# 2. Write the Ansible inventory from the droplet's public IP.
printf '[vault]\n%s\n' "$(terraform -chdir=terraform output -raw droplet_ipv4)" > ansible/inventory.ini

# 3. Provision the host and start the app. port and cors_origin end up in /opt/snippet-vault/.env.
export ANSIBLE_PRIVATE_KEY_FILE=~/.ssh/id_ed25519   # or pass --private-key ~/.ssh/id_ed25519
ansible-playbook -e port=3000 -e cors_origin=http://$(terraform -chdir=terraform output -raw droplet_ipv4) ansible/playbook.yml
```

Run the `ansible-playbook` command from inside `ansible/` so its `ansible.cfg` is picked up, or set `ANSIBLE_CONFIG=ansible/ansible.cfg`. The playbook is idempotent: rerun it to pull the latest `main` and rebuild. `terraform destroy` removes the droplet, key and firewall. Terraform state, `*.tfvars` and `ansible/inventory.ini` are gitignored.

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

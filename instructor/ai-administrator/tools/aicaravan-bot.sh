#!/usr/bin/env bash
# aicaravan-bot: choose which Hermes profile answers on @aicaravan_bot.
#   aicaravan-bot status      which profile holds the bot now
#   aicaravan-bot mapreview   Day 2 Session 3: the bot becomes the map reviewer (no tools, no memory)
#   aicaravan-bot riskreview  Day 2 Session 4: the bot becomes the risk challenger (no tools, no memory)
#   aicaravan-bot default     back to the Day 1 classroom agent / Session 2 test bench
# Moves the TELEGRAM_BOT_TOKEN and TELEGRAM_ALLOW_ALL_USERS lines between profile .env files (values never printed),
# then restarts the multiplexed gateway. Two profiles must never hold the same token at once.
set -euo pipefail
H="$HOME/.hermes"
declare -A ENV=( [default]="$H/.env" [mapreview]="$H/profiles/mapreview/.env" [riskreview]="$H/profiles/riskreview/.env" )
holder() { for p in default mapreview riskreview; do grep -qE '^TELEGRAM_BOT_TOKEN=.+' "${ENV[$p]}" && { echo "$p"; return; }; done; echo none; }
cmd="${1:-status}"
cur="$(holder)"
if [[ "$cmd" == status ]]; then echo "@aicaravan_bot is answered by profile: $cur"; exit 0; fi
[[ -n "${ENV[$cmd]:-}" ]] || { echo "usage: aicaravan-bot status|mapreview|riskreview|default"; exit 2; }
if [[ "$cur" == "$cmd" ]]; then echo "already on $cmd"; exit 0; fi
[[ "$cur" == none ]] && { echo "no profile holds the token; fix by hand"; exit 1; }
src="${ENV[$cur]}"; dst="${ENV[$cmd]}"
cp -p "$src" "$src.bak"; cp -p "$dst" "$dst.bak"
grep -E '^TELEGRAM_(BOT_TOKEN|ALLOW_ALL_USERS)=' "$src" >> "$dst"
sed -i -E '/^TELEGRAM_(BOT_TOKEN|ALLOW_ALL_USERS)=/d' "$src"
chmod 600 "$src" "$dst"
hermes gateway restart >/dev/null 2>&1 || hermes gateway start >/dev/null 2>&1
sleep 3
echo "@aicaravan_bot now answered by profile: $(holder)"

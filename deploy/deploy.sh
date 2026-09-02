#!/usr/bin/env bash
# Deploy dist/ to the server. Usage: deploy/deploy.sh [--dry-run]
# Makes a timestamped tarball backup on the server first, then rsyncs dist/ -> /var/www/html (no --delete: never removes unknown live files).
set -euo pipefail
HERE="$(cd "$(dirname "$0")/.." && pwd)"
HOST="${DEPLOY_HOST:-root@albanna-tutorials.com}"
DOCROOT="${DEPLOY_DOCROOT:-/var/www/html}"
STAMP="$(date +%Y%m%d-%H%M%S)"
DRY=""; [[ "${1:-}" == "--dry-run" ]] && DRY="--dry-run"
[[ -d "$HERE/dist" ]] || { echo "dist/ missing — run: python3 tools/build.py"; exit 1; }
echo "==> backup on server: /root/html-backup-$STAMP.tar.gz"
[[ -n "$DRY" ]] || ssh "$HOST" "tar -czf /root/html-backup-$STAMP.tar.gz -C $(dirname $DOCROOT) $(basename $DOCROOT)"
echo "==> rsync dist/ -> $HOST:$DOCROOT $DRY"
rsync -avz --checksum $DRY --exclude '.DS_Store' "$HERE/dist/" "$HOST:$DOCROOT/"
if [[ -z "$DRY" ]]; then
  echo "==> apache conf + permissions"
  scp "$HERE/deploy/zz-albanna-portal.conf" "$HOST:/etc/httpd/conf.d/zz-albanna-portal.conf"
  ssh "$HOST" "restorecon -R $DOCROOT; find $DOCROOT -type f -exec chmod 644 {} +; find $DOCROOT -type d -exec chmod 755 {} +; apachectl configtest && systemctl reload httpd && echo reloaded"
fi
echo "done"

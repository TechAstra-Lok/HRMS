#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

if [ -z "${1-}" ]; then
  echo "Usage: $0 <new-hex-32>"
  exit 1
fi

cat > encryption_key_template.txt <<EOF
encryption_key: $1
EOF

echo "Encryption key rotated in encryption_key_template.txt"

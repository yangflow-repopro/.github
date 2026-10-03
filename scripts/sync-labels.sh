#!/bin/bash
# Create or update the shared labels from labels.yml in one or more repositories.
#
#   scripts/sync-labels.sh <owner/repo> [<owner/repo> ...]
#
# Existing labels with the same name are updated (color, description); other labels in the repository
# are left alone, so per-repository scope labels survive. Needs gh with repo scope and python3.
set -euo pipefail

cd "$(dirname "$0")/.."
[ $# -ge 1 ] || { sed -n '2,8p' "$0" | sed 's/^# \{0,1\}//'; exit 1; }

# labels.yml is a flat list; parse it without PyYAML so the script runs anywhere.
labels=$(python3 - <<'PY'
import re, json
items, cur = [], None
for line in open("labels.yml", encoding="utf-8"):
    if line.lstrip().startswith("#") or not line.strip():
        continue
    m = re.match(r"^- name: (.+)$", line)
    if m:
        cur = {"name": m.group(1).strip()}; items.append(cur); continue
    m = re.match(r"^\s+(color|description): (.+)$", line)
    if m and cur is not None:
        cur[m.group(1)] = m.group(2).strip().strip('"')
print(json.dumps(items))
PY
)

for repo in "$@"; do
  echo "==> $repo"
  echo "$labels" | python3 -c 'import json,sys; [print(l["name"], l["color"], l["description"], sep="\t") for l in json.load(sys.stdin)]' |
  while IFS=$'\t' read -r name color desc; do
    if gh label create "$name" --repo "$repo" --color "$color" --description "$desc" --force >/dev/null 2>&1; then
      echo "    $name"
    else
      echo "    FAILED: $name" >&2
    fi
  done
done

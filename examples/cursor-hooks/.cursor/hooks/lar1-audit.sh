#!/usr/bin/env bash
# LAR-1 audit hook — logs suggested semantic tags after tool use (fail-open)
set -euo pipefail

INPUT=$(cat)

TOOL=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_name','unknown'))" 2>/dev/null || echo "unknown")

case "$TOOL" in
  *read*|*get*|*list*|*search*) C=obs; E=direct; L=0.85 ;;
  *write*|*delete*|*update*)     C=det; E=direct; L=0.7  ;;
  *)                              C=inf; E=derived; L=0.6 ;;
esac

echo "[lar-1 audit] tool=$TOOL suggested: C=$C E=$E L=$L V=unverified" >&2
echo '{}'

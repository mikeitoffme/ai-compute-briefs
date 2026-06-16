#!/usr/bin/env bash
# Reproduce every number behind the two slides (standard library only).
set -euo pipefail
cd "$(dirname "$0")"

echo "==> Printing all figures (GPU fleets, Atlas/DeepSeek margin, bottom-up TCO) ..."
python3 model.py

# Optional: re-run the notebook with outputs (first: pip install -r requirements.txt)
# jupyter nbconvert --to notebook --execute --inplace notebook.ipynb

echo "==> Done. Sources & per-number provenance: sources.md"

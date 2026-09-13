#!/usr/bin/env bash
# Demo Week: sandbox the Herp & Rodent Haven save so an instructor can freely
# explore any week (play turns, open --admin, trigger assessments) without
# ever touching the real student save. Restores the original game_state.json
# and artifacts/ automatically on exit, including Ctrl+C or a crash.

set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

STATE_FILE="data/game_state.json"
ARTIFACTS_DIR="artifacts"
BACKUP_DIR="$(mktemp -d)"

restore() {
    echo
    echo "Tearing down sandbox -- restoring your real save and artifacts..."
    if [[ -f "$BACKUP_DIR/game_state.json" ]]; then
        cp "$BACKUP_DIR/game_state.json" "$STATE_FILE"
    else
        rm -f "$STATE_FILE"
    fi
    rm -rf "$ARTIFACTS_DIR"
    mv "$BACKUP_DIR/artifacts" "$ARTIFACTS_DIR"
    rm -rf "$BACKUP_DIR"
    echo "Done. Nothing from this sandbox session was kept."
}
trap restore EXIT INT TERM

[[ -f "$STATE_FILE" ]] && cp "$STATE_FILE" "$BACKUP_DIR/game_state.json"
mkdir -p "$ARTIFACTS_DIR"
cp -r "$ARTIFACTS_DIR" "$BACKUP_DIR/artifacts"

python3 - <<'PY'
from pathlib import Path
from engine.admin import load_demo_state
from engine.state import save_state

state_path = Path("data/game_state.json")
state = load_demo_state(state_path)
save_state(state, state_path)
PY

echo "Sandbox ready: all modules unlocked, difficulty bumped for demoing."
echo "Play freely: python main.py | python main.py --admin | python main.py --create-assessment"
echo "Type 'exit' or press Ctrl+D when you're done -- everything rolls back automatically."
echo

"${SHELL:-bash}" -i

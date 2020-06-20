#!/usr/bin/env bash
set -eu

root="$(dirname -- $0)"

if ! [[ -e "$root/.venv/bin/activate" ]]; then
    python3 -mvenv "$root/.venv"
fi

. "$root/.venv/bin/activate"

"$@"

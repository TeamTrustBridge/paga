#!/usr/bin/env bash
#
# Build the three documentation sites and publish them into their repos.
#
#   tools/publish-docs.sh            build and sync every site
#   tools/publish-docs.sh python     build and sync one site
#
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

REPO_python="paga-python-docs"
REPO_typescript="paga-ts-docs"
REPO_rust="paga-rs-docs"

targets=("python" "typescript" "rust")
if [ $# -gt 0 ]; then
  targets=("$@")
fi

repo_for() {
  case "$1" in
    python) echo "$REPO_python" ;;
    typescript) echo "$REPO_typescript" ;;
    rust) echo "$REPO_rust" ;;
    *) echo "" ;;
  esac
}

label_for() {
  case "$1" in
    python) echo "Python" ;;
    typescript) echo "TypeScript" ;;
    rust) echo "Rust" ;;
    *) echo "" ;;
  esac
}

for language in "${targets[@]}"; do
  repo="$(repo_for "$language")"
  label="$(label_for "$language")"
  target="$ROOT/$repo/docs"

  echo "=== building the $label site -> $target"
  rm -rf "$target"
  node tools/build-docs.mjs --language "$language" --out "$target"

  echo "--- syncing into $repo"
  cd "$ROOT/$repo"

  # The generated site is committed, so the repository is the fallback and the
  # deploy workflow can publish it without a build step.
  git add -A
  if git diff --cached --quiet; then
    echo "    no changes"
  else
    git -c user.name="${GIT_AUTHOR_NAME:-Righteousness Ude}" \
        -c user.email="${GIT_AUTHOR_EMAIL:-righteousnessude@gmail.com}" \
        commit -q -m "docs: regenerate the $label site"
    echo "    committed"
  fi

  cd "$ROOT"
done

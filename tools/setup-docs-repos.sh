#!/usr/bin/env bash
#
# Set up the three documentation repositories: README, licence, workflow.
#
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

set_repo() {
  local repo="$1" language="$2" package="$3" sdk_repo="$4"

  echo "=== setting up $repo"
  cd "$ROOT/$repo"

  mkdir -p .github/workflows

  # The workflow is the same for all three, apart from the language. The
  # template lives in the monorepo so it is never the file being written.
  sed "s/__LANGUAGE__/$language/" \
    "$ROOT/tools/docs-workflow.yml" \
    > ".github/workflows/docs.yml"

  cp "$ROOT/paga-python/LICENSE" LICENSE

  cat > README.md <<EOF
# ${repo}

Unofficial documentation website for the [\`${package}\`](${sdk_repo}) SDK for the
[Paga Engine API](https://developer-docs.paga.com/).

> **This is unofficial documentation.** It is not built, endorsed, supported or
> published by Paga. It is community-maintained and follows Paga's published API
> reference. Paga's own documentation is the source of truth — if these pages
> and Paga's disagree, Paga's is right.

## Site

<https://teamtrustbridge.github.io/${repo}/>

## Deployment

The site is published by GitHub Pages from \`docs/\` on \`main\`, by
\`.github/workflows/docs.yml\`. The workflow fetches the dataset and generator
from [TeamTrustBridge/paga](https://github.com/TeamTrustBridge/paga), so the
site always reflects the canonical data.

GitHub Pages has to be enabled for the organisation first: **Settings → Pages
→ Build and deployment → Source → GitHub Actions**. The workflow enables it
per repository; the organisation-level switch is what it needs.

Until that is set, the site can be read straight from the repository, or
through a CDN that serves the HTML with the right content type:

\`\`\`
https://raw.githack.com/TeamTrustBridge/${repo}/main/docs/index.html
\`\`\`

## How it is built

The site is plain HTML, CSS and JavaScript — no framework, no build step and
no runtime dependencies. Every page is fully readable with JavaScript
disabled; the script only adds a theme toggle, the mobile navigation, a filter
over the operation reference, and copy-to-clipboard buttons.

The content comes from a shared dataset in
[TeamTrustBridge/paga](https://github.com/TeamTrustBridge/paga), so this site
and the other two always describe the same operations.

- \`docs/\` — the generated site, committed so the repository is the fallback
- \`docs/operations.json\` — the dataset, machine-readable
- \`docs/llms.txt\` — a plain-text outline of the whole site
- \`docs/sitemap.xml\` — the page list

## Local preview

\`\`\`bash
python3 -m http.server --directory docs 8000
\`\`\`

## License

GPL-3.0 — see [LICENSE](LICENSE).
EOF

  cd "$ROOT"
}

set_repo "paga-python-docs" "python" "paga-python" "https://github.com/TeamTrustBridge/paga-python"
set_repo "paga-ts-docs" "typescript" "paga-ts" "https://github.com/TeamTrustBridge/paga-ts"
set_repo "paga-rs-docs" "rust" "paga-rs" "https://github.com/TeamTrustBridge/paga-rs"

echo "done"

/**
 * Build the Paga Engine SDK documentation site.
 *
 * Reads the shared dataset and emits a complete static site: plain HTML,
 * CSS and JS, with no build step and no runtime dependencies. Every page is
 * fully readable with JavaScript disabled.
 *
 *   node tools/build-docs.mjs --language python --out ../paga-python-docs/docs
 *
 * Options:
 *   --language <python|typescript|rust>   which SDK's site to build
 *   --out <dir>                            output directory
 *   --base-url <url>                       canonical URL prefix
 *   --data <file>                          the dataset (defaults to data/operations.json)
 */

import { mkdirSync, readFileSync, writeFileSync, copyFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(HERE, "..");

/* -------------------------------------------------------------------------- */
/* Languages                                                                   */
/* -------------------------------------------------------------------------- */

const LANGUAGES = {
  python: {
    id: "python",
    name: "Python",
    package: "paga-python",
    install: "pip install paga-python",
    importLine: "from paga import PagaClient",
    repo: "https://github.com/TeamTrustBridge/paga-python",
    docsRepo: "https://github.com/TeamTrustBridge/paga-python-docs",
    site: "https://teamtrustbridge.github.io/paga-python-docs/",
    fence: "python",
    label: "Python",
  },
  typescript: {
    id: "typescript",
    name: "TypeScript",
    package: "paga-ts",
    install: "npm install paga-ts",
    importLine: 'import { PagaClient } from "paga";',
    repo: "https://github.com/TeamTrustBridge/paga-ts",
    docsRepo: "https://github.com/TeamTrustBridge/paga-ts-docs",
    site: "https://teamtrustbridge.github.io/paga-ts-docs/",
    fence: "typescript",
    label: "TypeScript",
  },
  rust: {
    id: "rust",
    name: "Rust",
    package: "paga-rs",
    install: "cargo add paga-rs",
    importLine: "use paga::{CreatePayment, PagaClient};",
    repo: "https://github.com/TeamTrustBridge/paga-rs",
    docsRepo: "https://github.com/TeamTrustBridge/paga-rs-docs",
    site: "https://teamtrustbridge.github.io/paga-rs-docs/",
    fence: "rust",
    label: "Rust",
  },
};

/* -------------------------------------------------------------------------- */
/* Helpers                                                                     */
/* -------------------------------------------------------------------------- */

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function escapeAttr(value) {
  return escapeHtml(value).replace(/'/g, "&#39;");
}

/**
 * Escape prose, then turn `backticked` spans into inline code.
 */
function prose(value) {
  return escapeHtml(value).replace(/`([^`]+)`/g, "<code>$1</code>");
}

/**
 * Render a code block with a stable id so the copy button can target it.
 */
function codeBlockStable(language, code, key) {
  const id = `code-${language.id}-${key}`;
  return [
    `<div class="code-block">`,
    `<button class="button" data-copy="#${id}" type="button">Copy</button>`,
    `<pre><code id="${id}" class="language-${escapeAttr(language.fence)}">${escapeHtml(code)}</code></pre>`,
    `</div>`,
  ].join("");
}

function tag(text, className) {
  return `<span class="tag ${className ?? ""}">${escapeHtml(text)}</span>`;
}

function apiTag(operation) {
  if (operation.api === "collect") return tag("Collect API", "tag-collect");
  return tag("Business API");
}

function authLabel(auth) {
  return auth === "basic" ? "HTTP Basic" : "principal / credentials headers";
}

/* -------------------------------------------------------------------------- */
/* Page shell                                                                  */
/* -------------------------------------------------------------------------- */

function nav(sections, groups, current) {
  const items = [];
  items.push(`<li><a href="index.html"${current === "index" ? ' aria-current="page"' : ""}>Getting started</a></li>`);

  for (const group of groups) {
    items.push(`<div class="nav-group"><p class="nav-heading">${escapeHtml(group.title)}</p><ul class="nav-list">`);
    for (const section of sections.filter((entry) => entry.group === group.id)) {
      items.push(
        `<li><a href="${section.id}.html"${current === section.id ? ' aria-current="page"' : ""}>${escapeHtml(section.navTitle)}</a></li>`,
      );
    }
    items.push(`</ul></div>`);
  }

  items.push(`<div class="nav-group"><p class="nav-heading">Reference</p><ul class="nav-list">`);
  items.push(`<li><a href="reference.html"${current === "reference" ? ' aria-current="page"' : ""}>All operations</a></li>`);
  items.push(`<li><a href="webhooks.html"${current === "webhooks" ? ' aria-current="page"' : ""}>Webhooks</a></li>`);
  items.push(`</ul></div>`);

  return items.join("\n");
}

function page({ language, dataset, title, description, current, body, extraHead = "" }) {
  const sections = dataset.sections;
  const groups = dataset.groups;

  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${escapeHtml(title)}</title>
<meta name="description" content="${escapeAttr(description)}">
<link rel="canonical" href="${escapeAttr(language.site + current + ".html")}">
<meta property="og:title" content="${escapeAttr(title)}">
<meta property="og:description" content="${escapeAttr(description)}">
<meta property="og:type" content="website">
<meta property="og:url" content="${escapeAttr(language.site + current + ".html")}">
<meta name="generator" content="paga-docs-builder">
<link rel="stylesheet" href="assets/style.css">
${extraHead}
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<div class="layout">
<nav class="sidebar" aria-label="Documentation">
  <a class="brand" href="index.html">
    <span class="brand-name">Paga Engine</span>
    <span class="brand-language">${escapeHtml(language.label)}</span>
  </a>
  ${nav(sections, groups, current)}
</nav>
<div class="main">
  <div class="topbar">
    <button class="button menu-toggle" data-menu-toggle type="button" aria-expanded="false" aria-label="Toggle navigation">Menu</button>
    <span class="topbar-spacer"></span>
    <button class="button" data-theme-toggle type="button" aria-label="Toggle the colour theme">☾</button>
  </div>
  <main class="content" id="main">
${body}
  </main>
  <footer class="footer">
    <span>Unofficial community documentation. Not built, endorsed or supported by Paga.</span>
    <nav aria-label="Footer">
      <a href="${escapeAttr(language.repo)}">${escapeHtml(language.package)} on GitHub</a>
      <a href="operations.json">operations.json</a>
      <a href="llms.txt">llms.txt</a>
      <a href="https://github.com/TeamTrustBridge/paga">All Paga SDKs</a>
    </nav>
  </footer>
</div>
</div>
<script src="assets/script.js" defer></script>
</body>
</html>
`;
}

/* -------------------------------------------------------------------------- */
/* Operation rendering                                                         */
/* -------------------------------------------------------------------------- */

function operationBlock(operation, language) {
  const lang = operation.languages[language.id];
  const notes = (operation.notes ?? [])
    .map((note) => `<li>${prose(note)}</li>`)
    .join("\n");

  const hash = operation.hashFields.length
    ? tag(operation.hashFields.join(" + "), "tag-endpoint")
    : "";

  return `<article class="op" id="op-${escapeAttr(operation.id)}" data-operation="${escapeAttr(operation.id)}">
  <div class="op-header">
    <h3 class="op-name">${escapeHtml(operation.name)}</h3>
    <a class="op-anchor" href="#op-${escapeAttr(operation.id)}" aria-label="Link to ${escapeAttr(operation.name)}">#</a>
  </div>
  <div class="meta">
    ${apiTag(operation)}
    ${tag(operation.endpoint, "tag-endpoint")}
    ${tag(authLabel(operation.auth))}
    ${hash}
  </div>
  <p>${prose(operation.description)}</p>
  ${notes ? `<ul>${notes}</ul>` : ""}
  <h4>${escapeHtml(language.label)}</h4>
  <p><code>${escapeHtml(lang.method)}</code></p>
  ${codeBlockStable(language, lang.example, operation.id)}
</article>`;
}

function operationRow(operation, language, sectionTitle) {
  const lang = operation.languages[language.id];
  return `<tr data-filter-item data-section="${escapeAttr(operation.section)}" data-search="${escapeAttr(
    [
      operation.name,
      operation.operation,
      operation.endpoint,
      sectionTitle,
      lang.method,
    ].join(" ").toLowerCase(),
  )}">
  <td><a href="#op-${escapeAttr(operation.id)}">${escapeHtml(operation.name)}</a></td>
  <td><code>${escapeHtml(operation.endpoint)}</code></td>
  <td>${escapeHtml(sectionTitle)}</td>
  <td><code>${escapeHtml(lang.method)}</code></td>
</tr>`;
}

/* -------------------------------------------------------------------------- */
/* Pages                                                                       */
/* -------------------------------------------------------------------------- */

function indexPage(language, dataset) {
  const quickStart = {
    python: `async def main() -> None:
    async with PagaClient(
        public_id="YOUR_PUBLIC_KEY",
        credentials="YOUR_SECRET_KEY",
        hash_key="YOUR_HASH_KEY",
        environment="test",
    ) as client:
        payment = await client.create_payment(
            reference_number="ORD-2026-0187",
            amount=50,
            payer_name="Bello Ramon",
            payer_phone_number="08064343187",
            payee_name="Your business name",
            call_back_url="https://yourstore.com/webhooks/paga",
        )
        status = await client.get_payment_status(reference_number="ORD-2026-0187")`,
    typescript: `const client = new PagaClient(
  process.env.PAGA_PUBLIC_KEY!,
  process.env.PAGA_SECRET_KEY!,
  process.env.PAGA_HASH_KEY!,
  { environment: "test" },
);

const payment = await client.createPayment({
  referenceNumber: "ORD-2026-0187",
  amount: 50,
  payerName: "Bello Ramon",
  payerPhoneNumber: "08064343187",
  payeeName: "Your business name",
  callBackUrl: "https://yourstore.com/webhooks/paga",
});

const status = await client.getPaymentStatus({
  referenceNumber: "ORD-2026-0187",
});`,
    rust: `let client = PagaClient::new(
    "YOUR_PUBLIC_KEY",
    "YOUR_SECRET_KEY",
    "YOUR_HASH_KEY",
    "test",
)?;

let payment = client
    .create_payment(CreatePayment::new(
        "ORD-2026-0187",
        50.0,
        "Bello Ramon",
        "08064343187",
        "Your business name",
    ))
    .await?;

let status = client.get_payment_status("ORD-2026-0187").await?;`,
  }[language.id];

  const aliasNote =
    language.id === "typescript"
      ? `<div class="callout">
  <p class="callout-title">Importing as <code>paga</code></p>
  <p>The package is published as <code>paga-ts</code>. To import it under the short name, alias it in your <code>package.json</code>:</p>
  ${codeBlockStable(language, `{
  "dependencies": {
    "paga": "npm:paga-ts@^0.1.0"
  }
}`, "alias")}
</div>`
      : "";

  const importNote =
    language.id === "rust"
      ? `<p>The crate is published as <code>paga-rs</code>, but the library is imported as <code>paga</code>.</p>`
      : `<p>Import it as <code>paga</code>.</p>`;

  const body = `<h1>${escapeHtml(language.package)}</h1>
<p class="lead">Unofficial async ${escapeHtml(language.label)} SDK for the <a href="https://developer-docs.paga.com/">Paga Engine API</a>.</p>

<div class="callout">
  <p class="callout-title">This is an unofficial SDK</p>
  <p>It is not built, endorsed, supported or published by Paga. It is community-maintained and follows Paga's published API reference. Paga's own documentation is the source of truth — if these pages and Paga's disagree, Paga's is right.</p>
</div>

<h2 id="install">Install</h2>
${codeBlockStable(language, language.install, "install")}
${importNote}
${aliasNote}
${codeBlockStable(language, language.importLine, "import")}

<h2 id="quick-start">Quick start</h2>
${codeBlockStable(language, quickStart, "quick-start")}

<h2 id="what-is-covered">What is covered</h2>
<p>The SDK wraps ${dataset.operations.length} documented operations and ${dataset.webhooks.length} callbacks, organised by the sections of Paga's own documentation.</p>
<div class="card-grid">
${dataset.groups
  .map((group) => {
    const count = dataset.operations.filter((operation) => {
      const section = dataset.sections.find((entry) => entry.id === operation.section);
      return section && section.group === group.id;
    }).length;
    return `  <div class="card">
    <h3>${escapeHtml(group.title)}</h3>
    <p>${escapeHtml(group.description)} ${count} operations.</p>
  </div>`;
  })
  .join("\n")}
</div>

<h2 id="conventions">Conventions</h2>
<h3>Two APIs, two auth styles</h3>
<div class="table-wrap">
<table>
<caption>How Paga's APIs authenticate</caption>
<thead><tr><th scope="col">API</th><th scope="col">Auth</th><th scope="col">Success field</th></tr></thead>
<tbody>
<tr><td>Collect</td><td>HTTP Basic plus a <code>hash</code> header</td><td><code>statusCode</code> (the string <code>"0"</code>)</td></tr>
<tr><td>Business</td><td><code>principal</code> and <code>credentials</code> headers plus a <code>hash</code> header</td><td><code>responseCode</code> (the integer <code>0</code>)</td></tr>
</tbody>
</table>
</div>

<h3>Hashing</h3>
<p>Every request that carries a body is signed: <code>SHA-512(concat(hash fields in order) + hashKey)</code>, lowercase hex, sent as the <code>hash</code> header. The hash key is never transmitted. A missing field signs as an empty string, and a string value signs verbatim.</p>

<h3>Outcomes</h3>
<p>A <code>200</code> response does not mean the money moved. The SDK exposes Paga's code vocabularies and an outcome classifier, so you can tell a definite failure from an undetermined one. Paga's <code>-1</code>, <code>105</code> and <code>135</code> mean <strong>unknown</strong>: check the transaction status with the original reference number, never resend.</p>

<h3>Retries</h3>
<p>Only HTTP <code>429</code> is retried, and only when you opt in. A server error or a timeout leaves the outcome unknown, so it is never retried automatically.</p>

<div class="callout">
  <p class="callout-title">Your IP must be whitelisted</p>
  <p>Paga rejects requests from an IP that is not on your allow-list, with a <code>403</code>. Allow-list your server's addresses before you integrate.</p>
</div>

<h2 id="next">Next</h2>
<ul>
  <li><a href="accept-payments.html">Accept payments</a> &mdash; collect money from a customer</li>
  <li><a href="make-payments.html">Make payments</a> &mdash; send money out</li>
  <li><a href="manage-accounts.html">Manage accounts</a> &mdash; your account and your customers'</li>
  <li><a href="reference.html">All operations</a> &mdash; the complete reference</li>
  <li><a href="webhooks.html">Webhooks</a> &mdash; verifying Paga's callbacks</li>
</ul>`;

  return page({
    language,
    dataset,
    title: `${language.package} — unofficial ${language.label} SDK for the Paga Engine API`,
    description: `Unofficial async ${language.label} SDK for the Paga Engine API: ${dataset.operations.length} operations, ${dataset.webhooks.length} webhook verifiers.`,
    current: "index",
    body,
  });
}

function groupPage(language, dataset, group) {
  const groupSections = dataset.sections.filter((section) => section.group === group.id);
  const sectionIds = new Set(groupSections.map((section) => section.id));
  const operations = dataset.operations.filter((operation) => sectionIds.has(operation.section));

  const body = `<h1>${escapeHtml(group.title)}</h1>
<p class="lead">${prose(group.description)}</p>

<div class="card-grid">
${groupSections
  .map(
    (section) => `  <div class="card">
    <h3><a href="${section.id}.html">${escapeHtml(section.title)}</a></h3>
    <p>${prose(section.description)}</p>
  </div>`,
  )
  .join("\n")}
</div>

<h2 id="operations">Operations in this section</h2>
<div class="table-wrap">
<table>
<caption>${groupSections.length} sections, ${operations.length} operations</caption>
<thead><tr><th scope="col">Operation</th><th scope="col">Endpoint</th><th scope="col">Section</th><th scope="col">Method</th></tr></thead>
<tbody>
${operations
  .map((operation) =>
    operationRow(
      operation,
      language,
      dataset.sections.find((section) => section.id === operation.section).navTitle,
    ),
  )
  .join("\n")}
</tbody>
</table>
</div>`;

  return page({
    language,
    dataset,
    title: `${group.title} — ${language.package}`,
    description: `${group.description} ${operations.length} operations in the ${language.label} SDK for the Paga Engine API.`,
    current: group.id,
    body,
  });
}

function sectionPage(language, dataset, section) {
  const operations = dataset.operations.filter((operation) => operation.section === section.id);

  const body = `<h1>${escapeHtml(section.title)}</h1>
<p class="lead">${prose(section.description)}</p>

<p>${escapeHtml(section.intro)}</p>

<h2 id="operations">Operations</h2>
${operations.map((operation) => operationBlock(operation, language)).join("\n\n")}

<h2 id="next">Next</h2>
<ul>
${dataset.groups
  .flatMap((group) =>
    dataset.sections
      .filter((entry) => entry.group === group.id && entry.id !== section.id)
      .slice(0, 4)
      .map((entry) => `<li><a href="${entry.id}.html">${escapeHtml(entry.title)}</a></li>`),
  )
  .join("\n")}
  <li><a href="reference.html">All operations</a></li>
</ul>`;

  return page({
    language,
    dataset,
    title: `${section.title} — ${language.package}`,
    description: `${section.description} ${operations.length} operations in the ${language.label} SDK for the Paga Engine API.`,
    current: section.id,
    body,
  });
}

function referencePage(language, dataset) {
  const sectionById = Object.fromEntries(dataset.sections.map((entry) => [entry.id, entry]));

  const body = `<h1>All operations</h1>
<p class="lead">Every documented Paga Engine operation, in one place.</p>

<div data-filter-root>
  <div class="filter-group">
    <input class="search" type="search" placeholder="Filter operations&hellip;  (press /)" data-filter-search aria-label="Filter operations">
  </div>
  <div class="filter-group">
    <button class="filter" data-filter-section="all" type="button" aria-pressed="true">All</button>
${dataset.sections
  .map(
    (section) =>
      `    <button class="filter" data-filter-section="${escapeAttr(section.id)}" type="button" aria-pressed="false">${escapeHtml(section.navTitle)}</button>`,
  )
  .join("\n")}
  </div>
  <p class="no-results" data-filter-empty hidden>No operation matches that filter.</p>

${dataset.operations
  .map((operation) => {
    const section = sectionById[operation.section];
    const lang = operation.languages[language.id];
    return `<article class="op" id="op-${escapeAttr(operation.id)}" data-operation="${escapeAttr(operation.id)}" data-filter-item data-section="${escapeAttr(operation.section)}" data-search="${escapeAttr(
      [operation.name, operation.operation, operation.endpoint, section.navTitle, lang.method]
        .join(" ")
        .toLowerCase(),
    )}">
  <div class="op-header">
    <h3 class="op-name">${escapeHtml(operation.name)}</h3>
    <a class="op-anchor" href="#op-${escapeAttr(operation.id)}" aria-label="Link to ${escapeAttr(operation.name)}">#</a>
  </div>
  <div class="meta">
    ${apiTag(operation)}
    ${tag(operation.endpoint, "tag-endpoint")}
    ${tag(authLabel(operation.auth))}
    ${tag(section.navTitle)}
    ${operation.hashFields.length ? tag(operation.hashFields.join(" + "), "tag-endpoint") : ""}
  </div>
  <p>${prose(operation.description)}</p>
  ${(operation.notes ?? []).length ? `<ul>${operation.notes.map((note) => `<li>${prose(note)}</li>`).join("\n")}</ul>` : ""}
  <h4>${escapeHtml(language.label)}</h4>
  <p><code>${escapeHtml(lang.method)}</code></p>
  ${codeBlockStable(language, lang.example, operation.id)}
</article>`;
  })
  .join("\n\n")}
</div>`;

  return page({
    language,
    dataset,
    title: `All operations — ${language.package}`,
    description: `All ${dataset.operations.length} documented Paga Engine operations, with endpoints, auth styles, hash fields and ${language.label} examples.`,
    current: "reference",
    body,
  });
}

function webhooksPage(language, dataset) {
  const body = `<h1>Webhooks</h1>
<p class="lead">Paga's callbacks, and how to verify them.</p>

<div class="callout">
  <p class="callout-title">Always verify the hash first</p>
  <p>Verify the signature before you act on a callback. Then de-duplicate: Paga retries until you answer, so the same callback will arrive more than once.</p>
</div>

<h2 id="callbacks">Callbacks</h2>
${dataset.webhooks
  .map((hook) => {
    const lang = hook.languages[language.id];
    const signed = hook.signedFields.length
      ? `<p class="tag tag-endpoint">${escapeHtml(hook.signedFields.join(" + "))}</p>`
      : `<p class="tag">no signature</p>`;
    return `<article class="op" id="op-${escapeAttr(hook.id)}" data-operation="${escapeAttr(hook.id)}">
  <div class="op-header">
    <h3 class="op-name">${escapeHtml(hook.name)}</h3>
    <a class="op-anchor" href="#op-${escapeAttr(hook.id)}" aria-label="Link to ${escapeAttr(hook.name)}">#</a>
  </div>
  <div class="meta">
    ${tag(hook.operation)}
    ${signed}
  </div>
  <p>${prose(hook.description)}</p>
  <p><strong>Delivery:</strong> ${escapeHtml(hook.delivery)}</p>
  ${(hook.notes ?? []).length ? `<ul>${hook.notes.map((note) => `<li>${prose(note)}</li>`).join("\n")}</ul>` : ""}
  <h4>${escapeHtml(language.label)}</h4>
  <p><code>${escapeHtml(lang.method)}</code></p>
  ${codeBlockStable(language, lang.example, hook.id)}
</article>`;
  })
  .join("\n\n")}

<h2 id="next">Next</h2>
<ul>
  <li><a href="reference.html">All operations</a></li>
  <li><a href="index.html">Getting started</a></li>
</ul>`;

  return page({
    language,
    dataset,
    title: `Webhooks — ${language.package}`,
    description: `How to verify Paga's ${dataset.webhooks.length} callbacks in ${language.label}.`,
    current: "webhooks",
    body,
  });
}

/* -------------------------------------------------------------------------- */
/* Sidecars                                                                    */
/* -------------------------------------------------------------------------- */

function llmsTxt(language, dataset) {
  const lines = [];
  lines.push(`# ${language.package}`);
  lines.push("");
  lines.push(
    `> Unofficial async ${language.label} SDK for the Paga Engine API. Not built, endorsed or supported by Paga.`,
  );
  lines.push("");
  lines.push(`Source: ${language.repo}`);
  lines.push(`Install: ${language.install}`);
  lines.push("");

  lines.push("## Pages");
  lines.push("");
  lines.push(
    `- [Getting started](${language.site}index.html): Install, quick start, and the SDK's conventions.`,
  );
  for (const group of dataset.groups) {
    lines.push(
      `- [${group.title}](${language.site}${group.id}.html): ${group.description}`,
    );
    for (const section of dataset.sections.filter((entry) => entry.group === group.id)) {
      const count = dataset.operations.filter((operation) => operation.section === section.id).length;
      lines.push(
        `  - [${section.title}](${language.site}${section.id}.html): ${section.description} (${count} operations)`,
      );
    }
  }
  lines.push(
    `- [All operations](${language.site}reference.html): Every documented operation, with endpoints and hash fields.`,
  );
  lines.push(
    `- [Webhooks](${language.site}webhooks.html): Every callback, and how to verify it.`,
  );
  lines.push("");

  lines.push("## Operations");
  lines.push("");
  for (const operation of dataset.operations) {
    const lang = operation.languages[language.id];
    const hash = operation.hashFields.length ? ` Hash: ${operation.hashFields.join(" + ")}.` : "";
    lines.push(
      `- \`${lang.method}\` — ${operation.name} (\`${operation.endpoint}\`). ${operation.description}${hash}`,
    );
  }
  lines.push("");

  lines.push("## Webhooks");
  lines.push("");
  for (const hook of dataset.webhooks) {
    const lang = hook.languages[language.id];
    const hash = hook.signedFields.length
      ? ` Hash: ${hook.signedFields.join(" + ")}.`
      : " No signature.";
    lines.push(`- \`${lang.method}\` — ${hook.name}.${hash}`);
  }
  lines.push("");

  return lines.join("\n");
}

function sitemapXml(language, dataset) {
  const urls = ["index.html"];
  for (const group of dataset.groups) urls.push(`${group.id}.html`);
  for (const section of dataset.sections) urls.push(`${section.id}.html`);
  urls.push("reference.html", "webhooks.html");

  const entries = urls
    .map((url) => {
      const priority = url === "index.html" ? "1.0" : url === "reference.html" ? "0.9" : "0.8";
      return `  <url>
    <loc>${escapeHtml(language.site + url)}</loc>
    <changefreq>weekly</changefreq>
    <priority>${priority}</priority>
  </url>`;
    })
    .join("\n");

  return `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${entries}
</urlset>
`;
}

function robotsTxt(language) {
  return `User-agent: *
Allow: /

Sitemap: ${language.site}sitemap.xml
`;
}

/* -------------------------------------------------------------------------- */
/* Build                                                                       */
/* -------------------------------------------------------------------------- */

function parseArgs(argv) {
  const args = { language: null, out: null, baseUrl: null, data: join(ROOT, "data", "operations.json") };
  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === "--language") args.language = argv[++index];
    else if (arg === "--out") args.out = argv[++index];
    else if (arg === "--base-url") args.baseUrl = argv[++index];
    else if (arg === "--data") args.data = argv[++index];
  }
  return args;
}

function main() {
  const args = parseArgs(process.argv.slice(2));

  if (!args.language || !LANGUAGES[args.language]) {
    console.error("usage: build-docs.mjs --language <python|typescript|rust> --out <dir>");
    process.exit(1);
  }
  if (!args.out) {
    console.error("--out is required");
    process.exit(1);
  }

  const language = LANGUAGES[args.language];
  if (args.baseUrl) language.site = args.baseUrl.endsWith("/") ? args.baseUrl : `${args.baseUrl}/`;

  const dataset = JSON.parse(readFileSync(resolve(args.data), "utf8"));
  const out = resolve(args.out);

  mkdirSync(join(out, "assets"), { recursive: true });

  const pages = new Map();
  pages.set("index.html", indexPage(language, dataset));
  for (const group of dataset.groups) {
    pages.set(`${group.id}.html`, groupPage(language, dataset, group));
  }
  for (const section of dataset.sections) {
    pages.set(`${section.id}.html`, sectionPage(language, dataset, section));
  }
  pages.set("reference.html", referencePage(language, dataset));
  pages.set("webhooks.html", webhooksPage(language, dataset));

  for (const [name, html] of pages) {
    writeFileSync(join(out, name), html, "utf8");
  }

  copyFileSync(join(HERE, "assets", "style.css"), join(out, "assets", "style.css"));
  copyFileSync(join(HERE, "assets", "script.js"), join(out, "assets", "script.js"));

  writeFileSync(join(out, "operations.json"), JSON.stringify(dataset, null, 2) + "\n", "utf8");
  writeFileSync(join(out, "llms.txt"), llmsTxt(language, dataset), "utf8");
  writeFileSync(join(out, "sitemap.xml"), sitemapXml(language, dataset), "utf8");
  writeFileSync(join(out, "robots.txt"), robotsTxt(language), "utf8");

  console.log(`built ${pages.size} pages for ${language.package} in ${out}`);
}

main();

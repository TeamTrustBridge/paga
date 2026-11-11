# Paga Engine SDKs

Unofficial community SDKs for the [Paga Engine API](https://developer-docs.paga.com/),
one per language, all tracking the same operation set.

> **These are unofficial SDKs.** They are not built, endorsed, supported or
> published by Paga. They are community-maintained and follow Paga's published
> API reference. Paga's own documentation is the source of truth — if this
> documentation and Paga's disagree, Paga's is right.
>
> Use at your own risk, and report issues here rather than to Paga.

| SDK | Package | Import | Docs | Repository |
|---|---|---|---|---|
| Python | [`paga-python`](https://pypi.org/project/paga-python/) | `import paga` | [paga-python-docs](https://teamtrustbridge.github.io/paga-python-docs/) | [TeamTrustBridge/paga-python](https://github.com/TeamTrustBridge/paga-python) |
| TypeScript | `paga-ts` | `import ... from "paga"` | [paga-ts-docs](https://teamtrustbridge.github.io/paga-ts-docs/) | [TeamTrustBridge/paga-ts](https://github.com/TeamTrustBridge/paga-ts) |
| Rust | [`paga-rs`](https://crates.io/crates/paga-rs) | `use paga::` | [paga-rs-docs](https://teamtrustbridge.github.io/paga-rs-docs/) | [TeamTrustBridge/paga-rs](https://github.com/TeamTrustBridge/paga-rs) |

Each package is named after its language, so the three can be published side
by side on the same registry. The import path is the same short name in all
three: `paga`.

## Install

```bash
pip install paga-python     # Python
npm install paga-ts          # TypeScript
cargo add paga-rs            # Rust
```

All three are imported as `paga`. In TypeScript, alias the package in your
`package.json` to get the short import name:

```json
{
  "dependencies": {
    "paga": "npm:paga-ts@^0.1.0"
  }
}
```

## What is covered

All three SDKs cover the documented Paga Engine API surface:

- **Checkout** — verify a charge
- **Refunds** — refund or cancel, check refund status
- **Dynamic virtual account**, **Bank USSD**, **Paga wallet** and **USD bank
  transfer** — create a payment request, check payment status, list the
  customer's banks, check USD payment status
- **Direct Debit (Open Banking)** — hosted set-up session, mandate by API,
  mandate status, charge the mandate, charge status, disable a mandate
- **Money Transfer** — list institutions, validate the account, send to a bank
  account, send to a Paga wallet, validate a Paga wallet transfer, bulk
  transfer, transaction status
- **Airtime and data** — list operators, list data bundles, buy airtime or data
- **Bill payment (VAS)** — list billers, list a biller's services, validate the
  customer, pay the bill
- **Your business account** — balance, transaction history, recent transactions,
  operation status, onboard a merchant, dispense cash
- **Subsidiary accounts** — create, charge, top up, transfer, retrieve, update,
  balance, history
- **Persistent payment accounts** — register, update, get, delete
- **Customers** — register, register with KYC, upload account photo, upload
  identification

Plus webhook verification for every callback Paga documents.

See [PARITY.md](PARITY.md) for the full matrix: operation, endpoint, auth
style, hash fields and the method name in each SDK.

## The operations are organised like the documentation

Each SDK splits its operations into one module (or mixin) per section of
Paga's reference — checkout, collection, refunds, direct debit, money
transfer, airtime, bill payment, status, business, subsidiary, persistent and
customer. The SDKs read in the same order as the documentation they wrap.

## Shared conventions

**Two APIs, two auth styles.**

| API | Base URL | Auth | Success field |
|---|---|---|---|
| Collect | `https://beta-collect.paga.com` / `https://collect.paga.com` | HTTP Basic + `hash` header | `statusCode` (string `"0"`) |
| Business | `https://beta.mypaga.com/paga-webservices/business-rest/secured` / `https://www.mypaga.com/paga-webservices/business-rest/secured` | `principal` + `credentials` headers + `hash` header | `responseCode` (integer `0`) |

**Hashing.** `SHA-512( concat(hash fields in order) + hashKey )`, lowercase
hex, sent as the `hash` header. The hash key is never transmitted. A missing
field signs as an empty string; a string value signs verbatim.

**Outcomes.** A 200 response does not mean the money moved. Each SDK exposes
the Collect and Business code vocabularies and a `classify()` helper that
turns a response into `SUCCESS` / `PENDING` / `PARTIAL` / `FAILED` /
`UNKNOWN`. Three Business codes — `-1`, `105` and `135` — mean the outcome is
**unknown**, not failed: check the transaction status with the *original*
reference number, never resend.

**Retries.** Only HTTP 429 is retried, and only when you opt in. A 5xx or a
timeout leaves the outcome unknown, so it is never retried automatically.

**IP allow-listing.** Paga requires your server's IP to be whitelisted. A 403
usually means it is not.

## Hash vectors

`fixtures/hash_vectors.json` holds the vectors all three SDKs are tested
against. The digests are generated outside the SDKs, so they pin byte-level
behaviour rather than merely confirming each SDK agrees with itself.

Each SDK repository carries a copy under `tests/fixtures/`; this file is the
canonical one. When it changes, copy it to all three:

```bash
for sdk in paga-python paga-ts paga-rs; do
  cp fixtures/hash_vectors.json "$sdk/tests/fixtures/hash_vectors.json"
done
```

## Documentation

Each SDK has its own documentation website, published with GitHub Pages and
generated from the shared dataset in this repository:

- [paga-python-docs](https://teamtrustbridge.github.io/paga-python-docs/)
- [paga-ts-docs](https://teamtrustbridge.github.io/paga-ts-docs/)
- [paga-rs-docs](https://teamtrustbridge.github.io/paga-rs-docs/)

The sites are plain HTML, CSS and JavaScript — no framework and no build
step. Every page is readable with JavaScript disabled, and each one carries
machine-readable sidecars: `operations.json`, `llms.txt` and `sitemap.xml`.

This repository owns the pipeline that produces them:

- `data/operations.json` — the 50 documented operations and the 9 callbacks,
  each with the endpoint, the auth style, the hash field order, and an
  example in all three languages
- `tools/build-docs.mjs` — the generator
- `tools/assets/` — the shared stylesheet and script
- `tools/publish-docs.sh` — builds a site and commits it into its repo

Because one dataset produces all three, the sites can never disagree with
each other or with the SDKs.

## License

GPL-3.0

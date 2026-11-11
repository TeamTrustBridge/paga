# Documentation site

This directory is the home of the documentation website for the Paga Engine
SDKs.

It is built and published with GitHub Pages, so the documentation lives in the
repository next to the code it describes.

## Structure

- `index.md` — the landing page, generated from this README.
- `guides/` — longer, task-shaped guides (accepting payments, paying out,
  managing accounts).
- `reference/` — the API reference, generated from the SDK sources.

## Building

The site is published automatically from `main` by GitHub Actions. To preview
it locally, serve this directory with any static file server:

```bash
python3 -m http.server --directory docs 8000
```

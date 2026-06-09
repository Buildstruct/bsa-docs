# BSA - Docs

Documentation for Buildstruct Admen (BSA), built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/).

The live site is hosted at [docs.buildstruct.net/bsa/](https://docs.buildstruct.net/bsa/).

---

## Running locally

This is only needed if you are modifying BSA itself and want to maintain your own fork of the documentation.\
If you are just writing a plugin, you do not need this.

### Requirements

- Python 3.x
- pip

### Install dependencies

```bash
pip install mkdocs-material mkdocs-macros-plugin
```

### Serve with live preview

```bash
mkdocs serve
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000).\
The server reloads automatically when you save a file.

### Build the static site

```bash
mkdocs build
```

Output goes to `site/`.\
This directory is in `.gitignore` and is not tracked.

---

## Deploying

### GitHub Pages (CI)

Pushes to `develop` automatically trigger the CI workflow in `.github/workflows/ci.yml`, which runs `mkdocs gh-deploy` and publishes to the repo's GitHub Pages endpoint.

No manual deploy step is needed unless you are hosting outside of GitHub Pages.

### Self-hosted static

After `mkdocs build`, serve the `site/` directory from any static file host or web server.\
The output is plain HTML/CSS/JS with no server-side requirements.

Example with Python's built-in server for a quick local check:

```bash
cd site
python -m http.server 8080
```

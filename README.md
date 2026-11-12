# CI/CD demo: Field Reader

A very small Python project used to demonstrate a **CI/CD pipeline with GitHub Actions**.

The code reads a value by its label (for example `Account Number: 100000000123`),
so it still works when the line moves. Sample data only.

## The pipeline (`.github/workflows/pipeline.yml`)

```
push / pull request
        │
        ▼
Test (Python 3.11) ─┐
Test (Python 3.12) ─┴─► Build website ─► Deploy to GitHub Pages
   lint + pytest          site/ folder      only on the main branch
```

* **CI** runs on every push and pull request: lint (`ruff`), tests (`pytest`), build the site.
* **CD** runs only when code reaches `main`: the site is deployed to GitHub Pages.
* A failing test stops the pipeline, so broken code is never deployed.

## Run it on your PC (Windows PowerShell)

```powershell
py -m pip install -r requirements.txt
py -m ruff check .
py -m pytest -v
py scripts/build_site.py      # then open site\index.html
```

## Files

| File | What it is |
|---|---|
| `src/fieldreader/reader.py` | The code |
| `tests/test_reader.py` | The tests the pipeline runs |
| `scripts/build_site.py` | Builds the website that gets deployed |
| `VERSION` | Version shown on the website |
| `.github/workflows/pipeline.yml` | The CI/CD pipeline |

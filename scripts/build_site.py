"""Build the small website that the pipeline deploys (the "CD" part).

Writes site/index.html with the version, the build number, the commit and
the list of labels the reader understands. Run it with:  python scripts/build_site.py
"""

import html
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from fieldreader import LABELS  # noqa: E402  (import after the path is set)

IST = timezone(timedelta(hours=5, minutes=30))


def main() -> None:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    run_number = os.environ.get("GITHUB_RUN_NUMBER", "local")
    commit = os.environ.get("GITHUB_SHA", "local")[:7]
    built_by = "GitHub Actions" if "GITHUB_ACTIONS" in os.environ else "my laptop"
    built_at = datetime.now(IST).strftime("%d %b %Y, %H:%M IST")

    rows = "\n".join(
        f"<tr><td>{html.escape(field)}</td><td>{html.escape(', '.join(labels))}</td></tr>"
        for field, labels in LABELS.items()
    )

    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Field Reader v{html.escape(version)}</title>
<style>
  body {{ font-family: Arial, sans-serif; margin: 0; background: #F4F7F8; color: #1B2433; }}
  main {{ max-width: 720px; margin: 0 auto; padding: 32px 16px; }}
  h1 {{ margin: 0 0 4px; font-size: 28px; }}
  .version {{ display: inline-block; background: #0E7C86; color: #fff; border-radius: 999px;
             padding: 4px 14px; font-weight: 700; font-size: 18px; margin: 8px 0 20px; }}
  .card {{ background: #fff; border-radius: 10px; padding: 16px 20px; margin-bottom: 16px;
          box-shadow: 0 1px 3px rgba(0,0,0,.08); }}
  .card h2 {{ margin: 0 0 12px; font-size: 20px; }}
  table {{ width: 100%; border-collapse: collapse; }}
  th, td {{ text-align: left; padding: 8px; border-bottom: 1px solid #E1E8EA; }}
  th {{ background: #EAF2F4; }}
  .meta td:first-child {{ color: #5B6C7D; width: 40%; }}
</style>
</head>
<body>
<main>
  <h1>Field Reader</h1>
  <div>This page is built and deployed automatically by the CI/CD pipeline.</div>
  <div class="version">Version {html.escape(version)}</div>
  <div class="card">
    <table class="meta">
      <tr><td>Build number</td><td>#{html.escape(run_number)}</td></tr>
      <tr><td>Commit</td><td>{html.escape(commit)}</td></tr>
      <tr><td>Built by</td><td>{html.escape(built_by)}</td></tr>
      <tr><td>Built at</td><td>{html.escape(built_at)}</td></tr>
    </table>
  </div>
  <div class="card">
    <h2>Labels the reader understands</h2>
    <table>
      <tr><th>Field</th><th>Label names</th></tr>
      {rows}
    </table>
  </div>
</main>
</body>
</html>
"""
    out = ROOT / "site"
    out.mkdir(exist_ok=True)
    (out / "index.html").write_text(page, encoding="utf-8")
    print(f"Built site/index.html for version {version}")


if __name__ == "__main__":
    main()

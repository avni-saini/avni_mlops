"""Build the Lab 7 submission PDF from the screenshots and registry summary."""
import base64
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SHOTS = HERE / "screenshots"
OUT = HERE / "Lab7_S24CSEU1037_Avni_Saini.pdf"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

LAB_DATE = sys.argv[1] if len(sys.argv) > 1 else "27 October 2026"
summary = json.loads((HERE / "registry_summary.json").read_text())


def img(name):
    data = base64.b64encode((SHOTS / name).read_bytes()).decode()
    return f'<img src="data:image/png;base64,{data}">'


html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@page {{ size: A4; margin: 18mm 16mm; }}
body {{ font-family: -apple-system, Helvetica, Arial, sans-serif; font-size: 11pt; color: #111; }}
h1 {{ font-size: 17pt; margin: 0 0 4px; }}
h2 {{ font-size: 12.5pt; margin: 22px 0 8px; border-bottom: 1px solid #999; padding-bottom: 3px; }}
.sub {{ color: #444; margin-bottom: 14px; }}
table {{ border-collapse: collapse; width: 100%; }}
td {{ border: 1px solid #bbb; padding: 6px 9px; vertical-align: top; }}
td:first-child {{ width: 34%; font-weight: 600; background: #f3f3f3; }}
img {{ width: 100%; border: 1px solid #aaa; }}
.page {{ page-break-before: always; }}
code {{ font-family: Menlo, monospace; font-size: 9.5pt; }}
</style></head><body>
<h1>Lab 7: Model Registry and Serving with MLflow</h1>
<div class="sub">SCSE3040 Machine Learning Operations &middot; Bennett University</div>

<h2>1. Student details</h2>
<table>
<tr><td>Name</td><td>Avni Saini</td></tr>
<tr><td>Roll number</td><td>S24CSEU1037</td></tr>
<tr><td>Batch</td><td>12</td></tr>
<tr><td>Date of laboratory session</td><td>{LAB_DATE}</td></tr>
</table>

<h2>2. MLflow Model Registry: version in Production</h2>
{img("1_registry.png")}

<h2 class="page">3. Serving the model with <code>mlflow models serve</code></h2>
{img("2_serve.png")}

<h2>4. Test request and prediction</h2>
{img("3_request.png")}

<h2 class="page">5. Model details</h2>
<table>
<tr><td>Registered model name</td><td><code>{summary["model_name"]}</code></td></tr>
<tr><td>Version promoted</td><td>{summary["version"]} (stage: {summary["stage"]})</td></tr>
<tr><td>Run ID</td><td><code>{summary["run_id"]}</code></td></tr>
<tr><td>Port served on</td><td>{summary["port"]}</td></tr>
</table>
</body></html>"""

tmp = HERE / "screenshots" / "_submission.html"
tmp.write_text(html, encoding="utf-8")
subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                f"--print-to-pdf={OUT}", tmp.as_uri()], check=True,
               capture_output=True)
tmp.unlink()
print("wrote", OUT)

from pathlib import Path
from datetime import datetime
import json


def write_json(report: dict, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=2)



def write_markdown(report: dict, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    rows = report["summary"]["rows"]
    columns = report["columns"]

    with open(path, "w", encoding="utf-8") as f:
        f.write("# Data Profile Report\n\n")

        f.write("## Summary\n")
        f.write(f"- Rows: {rows}\n")
        f.write(f"- Columns: {len(columns)}\n\n")

        f.write("| Column | Type | Missing % | Unique |\n")
        f.write("|--------|------|-----------|--------|\n")

        for name, col in columns.items():
            missing = col["stats"].get("missing", col["stats"].get("Missing", 0))
            unique = col["stats"]["unique"]
            pct = (missing / rows) * 100 if rows else 0
            f.write(f"| {name} | {col['type']} | {pct:.1f}% | {unique} |\n")

        f.write("\n## Column Details\n")

        for name, col in columns.items():
            f.write(f"\n### {name}\n")
            f.write(f"- Type: {col['type']}\n")

            stats = col["stats"]

            if col["type"] == "Number":
                f.write(f"- Min: {stats['min']}\n")
                f.write(f"- Max: {stats['max']}\n")
                f.write(f"- Mean: {stats['mean']}\n")
            else:
                f.write("- Top values:\n")
                for v, c in stats["Top"]:
                    f.write(f"  - {v}: {c}\n")




def render_markdown(report: dict) -> str:
    lines: list[str] = []

    lines.append(f"# CSV Profiling Report\n")
    lines.append(f"Generated: {datetime.now().isoformat(timespec='seconds')}\n")

    lines.append("## Summary\n")
    lines.append(f"- Rows: **{report['n_rows']}**")
    lines.append(f"- Columns: **{report['n_cols']}**\n")

    lines.append("## Columns\n")
    lines.append("| name | type | missing | missing_pct | unique |")
    lines.append("|---|---:|---:|---:|---:|")
    for i in report['columns']:
        lines.append(f"{i['name']}|{i['type']}|{i['missing']}|{i['missing_pct']}|{i['unique']}")

    lines.append("\n## Notes\n")
    lines.append("- Missing values are: `''`, `na`, `n/a`, `null`, `none`, `nan` (case-insensitive)")

    return "\n".join(lines)


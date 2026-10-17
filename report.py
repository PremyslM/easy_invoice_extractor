import json
import statistics
from collections import defaultdict
from pathlib import Path

RESULTS_DIR = Path("results")
README = Path("README.md")
START, END = "<!-- RESULTS:START -->", "<!-- RESULTS:END -->"

# USD per 1M tokens – fill in current values from the provider's pricing page
PRICES = {
    "claude-haiku-5-5": {"in": 0.0, "out": 0.0},
}


def load_runs() -> dict:
    groups = defaultdict(list)
    for f in sorted(RESULTS_DIR.glob("*.json")):
        r = json.loads(f.read_text(encoding="utf-8"))
        groups[(r["prompt_version"], r["model"])].append(r)
    return groups


def fmt(values: list[float], pct: bool = True) -> str:
    mean = statistics.mean(values)
    spread = (max(values) - min(values)) / 2
    if pct:
        return f"{mean:.1%} ± {spread:.1%}" if len(values) > 1 else f"{mean:.1%}"
    return f"{mean:.1f} ± {spread:.1f}" if len(values) > 1 else f"{mean:.1f}"


def summary_table(groups: dict) -> str:
    lines = [
        "| Prompt | Model | Runs | Clean JSON | Field accuracy | Hallucinations | Cost / 1k invoices |",
        "|---|---|---|---|---|---|---|",
    ]
    for (version, model), runs in sorted(groups.items()):
        strict = [r["strict_json"] / r["n_invoices"] for r in runs]
        acc = [r["counts"]["correct"] / sum(r["counts"].values()) for r in runs]
        hall = [r["counts"]["hallucinated"] for r in runs]
        price = PRICES.get(model, {"in": 0, "out": 0})
        cost = statistics.mean(
            (r["tokens_in"] * price["in"] + r["tokens_out"] * price["out"]) / 1e6 / r["n_invoices"] * 1000
            for r in runs
        )
        lines.append(
            f"| {version} | {model} | {len(runs)} | {fmt(strict)} | {fmt(acc)} | {fmt(hall, pct=False)} | ${cost:.2f} |"
        )
    return "\n".join(lines)


def per_field_table(groups: dict) -> str:
    keys = sorted(groups)
    fields = list(next(iter(groups.values()))[0]["per_field"].keys())
    lines = [
        "| Field | " + " | ".join(v for v, _ in keys) + " |",
        "|---|" + "---|" * len(keys),
    ]
    for field in fields:
        cells = []
        for key in keys:
            vals = [r["per_field"][field]["correct"] / r["per_field"][field]["total"] for r in groups[key]]
            cells.append(f"{statistics.mean(vals):.0%}")
        lines.append(f"| `{field}` | " + " | ".join(cells) + " |")
    return "\n".join(lines)


def error_list(groups: dict) -> str:
    lines = []
    for (version, model), runs in sorted(groups.items()):
        latest = runs[-1]
        if not latest["errors"]:
            continue
        lines.append(f"\n**{version} / {model}** (latest run)\n")
        for e in latest["errors"]:
            lines.append(
                f"- `{e['invoice']}` · `{e['field']}` · {e['type']}: "
                f"expected `{e['expected']}`, got `{e['actual']}`"
            )
    return "\n".join(lines) or "_No errors._"


def build() -> str:
    groups = load_runs()
    return "\n\n".join([
        "### Summary",
        summary_table(groups),
        "### Accuracy per field",
        per_field_table(groups),
        "### Errors",
        error_list(groups),
    ])


if __name__ == "__main__":
    content = build()
    text = README.read_text(encoding="utf-8")
    before, rest = text.split(START)
    _, after = rest.split(END)
    README.write_text(f"{before}{START}\n{content}\n{END}{after}", encoding="utf-8")
    print("README updated")

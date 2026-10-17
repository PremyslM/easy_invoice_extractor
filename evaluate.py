import json
import re
import subprocess
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from extractor import extract
from validation import validate

INVOICES_DIR = Path("invoices")
LABELS_DIR = Path("labels")
RESULTS_DIR = Path("results")
FIELDS = ["document_type", "supplier", "ico", "amount_due", "vat", "currency", "due_date"]


def git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], text=True).strip()
    except Exception:
        return "unknown"


def parse_output(text: str) -> tuple[dict | None, bool]:
    """Returns (data, strict_ok). Strict = pure JSON with nothing around it."""
    try:
        return json.loads(text), True
    except json.JSONDecodeError:
        pass

    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group()), False
        except json.JSONDecodeError:
            pass
    return None, False


def values_equal(field: str, expected, actual) -> bool:
    if field in ("amount_due", "vat"):
        try:
            return abs(float(expected) - float(actual)) < 0.01
        except (TypeError, ValueError):
            return False
    return str(expected).strip().lower() == str(actual).strip().lower()


def compare_field(field: str, expected, actual) -> str:
    if expected is None and actual is None:
        return "correct"
    if expected is None:
        return "hallucinated"
    if actual is None:
        return "missed"
    return "correct" if values_equal(field, expected, actual) else "wrong"


def evaluate(prompt_version: str, model: str = "claude-haiku-5-5") -> dict:
    counts = {"correct": 0, "wrong": 0, "missed": 0, "hallucinated": 0}
    review = {"auto_ok": 0, "auto_with_errors": 0, "caught": 0, "false_alarm": 0}
    per_field = defaultdict(lambda: {"correct": 0, "total": 0})
    errors = []
    evaluated = strict_ok = parsed_ok = 0
    tokens_in = tokens_out = 0

    invoices = sorted(p for p in INVOICES_DIR.iterdir() if p.is_file())

    for invoice in invoices:
        label_path = LABELS_DIR / f"{invoice.stem}.json"
        if not label_path.exists():
            print(f"⚠️  {invoice.name}: missing label, skipping")
            continue

        evaluated += 1
        expected = json.loads(label_path.read_text(encoding="utf-8"))
        result = extract(str(invoice), prompt_version, model)
        tokens_in += result["input_tokens"]
        tokens_out += result["output_tokens"]

        data, is_strict = parse_output(result["raw_text"])
        strict_ok += is_strict

        if data is None:
            print(f"❌ {invoice.name}: unparseable output → review")
            errors.append({"invoice": invoice.name, "field": "*", "type": "unparseable",
                           "expected": None, "actual": result["raw_text"][:200]})
            review["caught"] += 1
            continue
        parsed_ok += 1

        invoice_has_error = False
        for field in FIELDS:
            exp, act = expected.get(field), data.get(field)
            outcome = compare_field(field, exp, act)
            counts[outcome] += 1
            per_field[field]["total"] += 1
            if outcome == "correct":
                per_field[field]["correct"] += 1
            else:
                invoice_has_error = True
                print(f"   {invoice.name}  {outcome:12} {field}: expected {exp!r}, got {act!r}")
                errors.append({"invoice": invoice.name, "field": field, "type": outcome,
                               "expected": exp, "actual": act})

        issues = validate(data)
        if issues:
            print(f"   🔎 {invoice.name} → review: {'; '.join(issues)}")
            if invoice_has_error:
                review["caught"] += 1          # validation correctly flagged a bad invoice
            else:
                review["false_alarm"] += 1     # flagged, but extraction was fine
        else:
            if invoice_has_error:
                review["auto_with_errors"] += 1  # error slipped through silently (worst case)
            else:
                review["auto_ok"] += 1

    total = sum(counts.values())
    auto = review["auto_ok"] + review["auto_with_errors"]

    print(f"\n===== {prompt_version} / {model} =====")
    print(f"Clean JSON:      {strict_ok}/{evaluated}")
    print(f"Parseable:       {parsed_ok}/{evaluated}")
    print(f"Field accuracy:  {counts['correct']}/{total} ({counts['correct'] / max(total, 1):.1%})")
    print(f"Wrong:           {counts['wrong']}")
    print(f"Missed:          {counts['missed']}")
    print(f"Hallucinated:    {counts['hallucinated']}")
    print(f"Tokens:          in {tokens_in}, out {tokens_out}")
    print("--- Validation ---")
    print(f"Auto-processed:  {auto}/{evaluated}")
    print(f"Silent errors:   {review['auto_with_errors']}")
    print(f"Caught:          {review['caught']}")
    print(f"False alarms:    {review['false_alarm']}")

    run = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "git_commit": git_commit(),
        "prompt_version": prompt_version,
        "model": model,
        "n_invoices": evaluated,
        "strict_json": strict_ok,
        "parsed": parsed_ok,
        "counts": counts,
        "per_field": dict(per_field),
        "review": review,
        "tokens_in": tokens_in,
        "tokens_out": tokens_out,
        "errors": errors,
    }

    RESULTS_DIR.mkdir(exist_ok=True)
    filename = f"{run['timestamp'].replace(':', '-')}_{prompt_version}_{model}.json"
    (RESULTS_DIR / filename).write_text(json.dumps(run, indent=2, ensure_ascii=False), encoding="utf-8")
    return run


if __name__ == "__main__":
    RUNS = 3
    for version in ["v1_zero_shot", "v2_rules"]:
        for i in range(RUNS):
            print(f"\n▶ {version}, run {i + 1}/{RUNS}")
            evaluate(version)

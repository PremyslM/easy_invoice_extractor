from cProfile import label
from email.policy import strict
import json
import math
import re
from pathlib import Path
from extractor import extract

INVOICES_DIR = Path("faktury")
LABELS_DIR = Path("labels")
FIELDS = ["document_type", "supplier", "ico", "amount_due", "vat", "currency", "due_date"]

def parse_output(text: str) -> tuple[dict | None, bool]:
    try:
        return json.loads(text), True
    except json.JSONDecodeError:
        pass

    match = re.search(r"\{.*}", text, re.DOTALL)

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

def compare_fields(field: str, expected, actual) -> str:
    if expected is None and actual is None:
        return "correct"
    if expected is None:
        return "hallucinated"
    if actual is None:
        return "missed"
    return "correct" if values_equal(field, expected, actual) else "wrong"

def evaluate(prompt_version: str, model: str = "claude-haiku-5-5"):
    counts = {"correct": 0, "wrong": 0, "missed": 0, "hallucinated": 0}
    strict_ok = 0
    parsed_ok = 0
    tokens_in = tokens_out = 0
    invoices = sorted(p for p in INVOICES_DIR.iterdir() if p.is_file())

    for invoice in invoices:
        label_path = LABELS_DIR / f"{invoice.stem}.json"

        if not label_path.exists():
            print(f"⚠️  {invoice.name}: Missing label")
            continue

        expected = json.loads(label_path.read_text(encoding="utf-8"))
        result = extract(str(invoice), prompt_version, model)
        tokens_in += result["output_tokens"]
        tokens_out += result["input_tokens"]

        data, strict = parse_output(result["raw_text"])
        strict_ok += strict

        if data is None:
            print(f"X {invoice.name}: Can't read")
            continue
        parsed_ok += 1

        print(f"\n📄 {invoice.name}")

        for field in FIELDS:
            outcome = compare_fields(field, expected.get(field), data.get(field))
            counts[outcome] += 1
            if outcome != "correct":
                print(f"    {outcome:12} {field}: čekal {expected.get(field)!r}, dostal {data.get(field)!r}")

    total = sum(counts.values())
    n = len(invoices)

    print(f"\n===== {prompt_version} / {model} =====")
    print(f"Clean JSON:        {strict_ok}/{n}")
    print(f"Readed correctly):     {parsed_ok}/{n}")
    print(f"Field Accuracy:     {counts['correct']}/{total} ({counts['correct']/max(total,1):.0%})")
    print(f"Wrong:            {counts['wrong']}")
    print(f"Founded:        {counts['missed']}")
    print(f"Hallucinated:        {counts['hallucinated']}")
    print(f"Tokens total:     in {tokens_in}, out {tokens_out}")

    if __name__ == "__main__":
        for version in ["v1_zero_shot", "v2_rules"]:
            evaluate(version)

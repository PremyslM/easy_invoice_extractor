from datetime import date

VALID_CURRENCIES = {"CZK", "EUR", "USD", "GBP", "PLN", "CHF"}


def ico_is_valid(ico: str) -> bool:
    if not ico or not ico.isdigit() or len(ico) != 8:
        return False
    weighted = sum(int(d) * w for d, w in zip(ico[:7], range(8, 1, -1)))
    check = (11 - weighted % 11) % 10
    return check == int(ico[7])


def validate(data: dict) -> list[str]:
    """Returns a list of problems. Empty list = data looks consistent."""
    issues = []

    ico = data.get("ico")
    if ico is not None and not ico_is_valid(str(ico)):
        issues.append(f"invalid IČO checksum: {ico}")

    amount, vat = data.get("amount_due"), data.get("vat")
    if amount is not None and vat is not None:
        try:
            if abs(float(vat)) > abs(float(amount)):
                issues.append(f"VAT {vat} is larger than amount {amount}")
        except (TypeError, ValueError):
            issues.append("amount or VAT is not a number")

    currency = data.get("currency")
    if currency not in VALID_CURRENCIES:
        issues.append(f"unknown currency: {currency}")

    due = data.get("due_date")
    if due is not None:
        try:
            date.fromisoformat(due)
        except (TypeError, ValueError):
            issues.append(f"due_date is not YYYY-MM-DD: {due}")

    for required in ("supplier", "amount_due"):
        if data.get(required) is None:
            issues.append(f"missing required field: {required}")

    return issues

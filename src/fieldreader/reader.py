"""A tiny field reader, used to demonstrate a CI/CD pipeline.

It finds a value by its LABEL (for example "Account Number: 100000000123"),
not by its position, so it still works when a line moves.
"""

# Every field and the label names it can appear under.
LABELS = {
    "account_number": ["account number", "account no", "billing account"],
    "order_number": ["order number", "order no", "order #"],
    "due_date": ["due date", "delivery date"],
}


def read_field(text: str, field: str) -> str | None:
    """Return the value written after the field's label, or None if missing."""
    aliases = LABELS.get(field)
    if aliases is None:
        raise KeyError(f"unknown field: {field}")

    for line in text.splitlines():
        if ":" not in line:
            continue
        label, _, value = line.partition(":")
        if label.strip().lower() in aliases:
            value = value.strip()
            return value or None
    return None


def read_all(text: str) -> dict[str, str | None]:
    """Read every known field from the text."""
    return {field: read_field(text, field) for field in LABELS}

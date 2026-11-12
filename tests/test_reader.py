import pytest

from fieldreader import read_all, read_field

EMAIL = """Order Number: ORD-48213
Account Number: 100000000123
Due Date: 2026-12-14
"""

# Same email, but the lines are in a different order (the field "moved").
EMAIL_MOVED = """Due Date: 2026-12-14
Customer: Example Retail LLC
Account Number: 100000000123
Order Number: ORD-48213
"""


def test_reads_account_number():
    assert read_field(EMAIL, "account_number") == "100000000123"


def test_still_works_when_the_line_moves():
    assert read_field(EMAIL_MOVED, "account_number") == "100000000123"


def test_label_is_not_case_sensitive():
    assert read_field("ACCOUNT NUMBER: 100000000123", "account_number") == "100000000123"


def test_other_label_name_works():
    assert read_field("Acct No: 100000000123", "account_number") == "100000000123"


def test_due_date_other_label():
    assert read_field("Delivery Date: 2026-12-14", "due_date") == "2026-12-14"


def test_extra_spaces_are_ignored():
    assert read_field("  Order Number :   ORD-48213  ", "order_number") == "ORD-48213"


def test_missing_field_returns_none():
    assert read_field("Hello, no fields here", "due_date") is None


def test_empty_value_returns_none():
    assert read_field("Due Date:", "due_date") is None


def test_unknown_field_raises_error():
    with pytest.raises(KeyError):
        read_field(EMAIL, "favourite_colour")


def test_read_all_fields():
    assert read_all(EMAIL) == {
        "account_number": "100000000123",
        "order_number": "ORD-48213",
        "due_date": "2026-12-14",
    }


def test_new_label_billing_account():
   assert read_field("Billing Account: 100000000123", "account_number") == "100000000123"
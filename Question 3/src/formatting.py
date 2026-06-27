"""
Formatting helpers for Question 3.

No third-party libraries are used, so the program can run in PyCharm,
VS Code, terminal, or any basic Python environment.
"""

from textwrap import wrap
from typing import Iterable, Sequence


def print_title(title: str) -> None:
    """Print a formatted title."""
    border = "=" * 92
    print(f"\n{border}")
    print(title.center(92))
    print(f"{border}")


def print_message(message: str, success: bool = True) -> None:
    """Print a consistent success or error message."""
    prefix = "[OK]" if success else "[ERROR]"
    print(f"{prefix} {message}")


def format_table(headers: Sequence[str], rows: Iterable[Sequence[str]]) -> str:
    """
    Return a formatted table as a string.
    """
    rows = list(rows)

    if not rows:
        rows = [["-" for _ in headers]]

    column_widths = [
        max(len(str(header)), *(len(str(row[index])) for row in rows))
        for index, header in enumerate(headers)
    ]

    def build_row(row: Sequence[str]) -> str:
        return " | ".join(
            str(value).ljust(column_widths[index])
            for index, value in enumerate(row)
        )

    header_line = build_row(headers)
    divider = "-+-".join("-" * width for width in column_widths)
    body = "\n".join(build_row(row) for row in rows)

    return f"{header_line}\n{divider}\n{body}"


def format_large_number(number: int, width: int = 92) -> str:
    """
    Format a large integer over multiple lines.

    Factorials such as 200! are very large, so this helper keeps the output
    readable while still showing the complete value.
    """
    number_text = str(number)
    return "\n".join(wrap(number_text, width=width))

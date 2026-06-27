"""
Output formatting helpers.

The program uses plain Python only, so it can run easily in PyCharm,
VS Code, terminal, or GitHub Codespaces without extra dependencies.
"""

from typing import Iterable, Sequence


def print_title(title: str) -> None:
    """Print a formatted section title."""
    border = "=" * 88
    print(f"\n{border}")
    print(title.center(88))
    print(f"{border}")


def print_message(message: str, success: bool = True) -> None:
    """Print a consistent success or error message."""
    prefix = "[OK]" if success else "[ERROR]"
    print(f"{prefix} {message}")


def format_table(headers: Sequence[str], rows: Iterable[Sequence[str]]) -> str:
    """
    Return a formatted text table.

    Args:
        headers: Column names.
        rows: Table row values.

    Returns:
        A string containing a neatly aligned table.
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

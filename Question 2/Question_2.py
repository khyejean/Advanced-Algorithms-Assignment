"""
Question 2: Divide and Conquer Algorithm

This program implements:
    1. Merge Sort for sorting customer transaction data
    2. Recursive Binary Search for searching transaction data
    3. Linear Search for comparison
    4. A menu-driven command-line transaction system

Run:
    python Question_2.py
"""

from pathlib import Path

from src.cli import TransactionCLI, create_transaction_system_from_file


DEFAULT_DATA_FILE = Path("data/sample_transactions.csv")


def main() -> None:
    """
    Program entry point.
    """
    if not DEFAULT_DATA_FILE.exists():
        raise FileNotFoundError(
            f"Sample data file not found: {DEFAULT_DATA_FILE}. "
            "Please run this program from the project root folder."
        )

    system = create_transaction_system_from_file(DEFAULT_DATA_FILE)
    app = TransactionCLI(system)
    app.run()


if __name__ == "__main__":
    main()

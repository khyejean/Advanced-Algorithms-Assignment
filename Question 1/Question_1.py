"""
Question 1: Hashing - Pharmacy Inventory System

Run this file:
    python pharmacy_hashing_q1.py

This entry file keeps the program easy to run, while the real implementation
is separated into reusable modules inside the src folder.
"""

from pathlib import Path

from src.cli import PharmacyInventoryCLI, create_inventory_from_file


DEFAULT_DATA_FILE = Path("data/sample_medicines.csv")


def main() -> None:
    """
    Program entry point.
    """
    if not DEFAULT_DATA_FILE.exists():
        raise FileNotFoundError(
            f"Sample data file not found: {DEFAULT_DATA_FILE}. "
            "Please run the program from the project root folder."
        )

    inventory = create_inventory_from_file(DEFAULT_DATA_FILE)
    app = PharmacyInventoryCLI(inventory)
    app.run()


if __name__ == "__main__":
    main()

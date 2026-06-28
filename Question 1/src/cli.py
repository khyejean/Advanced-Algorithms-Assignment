"""
Command-line interface for the Pharmacy Inventory System.
"""

from datetime import date
from pathlib import Path

from src.formatting import format_table, print_message, print_title
from src.inventory import PharmacyInventory
from src.models import Medicine
from src.performance import SearchPerformanceExperiment


class PharmacyInventoryCLI:
    """
    Handles all user interaction for the command-line program.
    """

    MENU_OPTIONS = {
        "1": "Display inventory records",
        "2": "Display hash table buckets",
        "3": "Insert new medicine",
        "4": "Search medicine by ID",
        "5": "Edit medicine stock or price",
        "6": "Delete medicine",
        "7": "View hash table statistics",
        "8": "Run performance comparison",
        "9": "Exit",
    }

    INVENTORY_HEADERS = [
        "Medicine ID",
        "Name",
        "Category",
        "Dosage",
        "Stock Quantity",
        "Price",
        "Expiry Date",
    ]

    BUCKET_HEADERS = ["Bucket", "Status", "Key", "Value"]
    RESULT_HEADERS = ["Description", "Value"]

    def __init__(self, inventory: PharmacyInventory) -> None:
        self._inventory = inventory

    def run(self) -> None:
        """
        Start the command-line menu loop.
        """
        while True:
            self._display_menu()
            choice = input("Enter your choice (1-9): ").strip()

            if choice == "1":
                self._display_inventory()
            elif choice == "2":
                self._display_buckets()
            elif choice == "3":
                self._insert_medicine()
            elif choice == "4":
                self._search_medicine()
            elif choice == "5":
                self._edit_medicine()
            elif choice == "6":
                self._delete_medicine()
            elif choice == "7":
                self._display_statistics()
            elif choice == "8":
                self._run_performance_comparison()
            elif choice == "9":
                print_message("Thank you for using the Pharmacy Inventory System.")
                break
            else:
                print_message("Invalid choice. Please enter a number from 1 to 9.", False)

    def _display_menu(self) -> None:
        """Display the main menu."""
        print_title("PHARMACY INVENTORY SYSTEM")
        for number, description in self.MENU_OPTIONS.items():
            print(f"{number}. {description}")
        print("-" * 72)

    def _display_inventory(self) -> None:
        """Display all medicine records."""
        print_title("MEDICINE INVENTORY RECORDS")
        print(format_table(self.INVENTORY_HEADERS, self._inventory.get_inventory_rows()))

    def _display_buckets(self) -> None:
        """Display hash table bucket structure."""
        print_title("HASH TABLE BUCKET STRUCTURE")
        print(format_table(self.BUCKET_HEADERS, self._inventory.get_bucket_rows()))

    def _display_statistics(self) -> None:
        """Display hash table statistics."""
        print_title("HASH TABLE STATISTICS")
        print(format_table(self.RESULT_HEADERS, self._inventory.get_statistics_rows()))

    def _insert_medicine(self) -> None:
        """Insert a new medicine record."""
        print_title("INSERT NEW MEDICINE")

        try:
            medicine = Medicine(
                medicine_id=self._read_required_text("Medicine ID").upper(),
                name=self._read_required_text("Medicine Name"),
                category=self._read_required_text("Category"),
                dosage=self._read_required_text("Dosage"),
                stock_quantity=self._read_non_negative_integer("Stock Quantity"),
                price=self._read_non_negative_float("Price in RM"),
                expiry_date=self._read_date("Expiry Date, format YYYY-MM-DD"),
            )

            self._inventory.insert_medicine(medicine)
            print_message("Medicine record inserted or updated successfully.")

        except ValueError as error:
            print_message(str(error), False)

    def _search_medicine(self) -> None:
        """Search for one medicine record by ID."""
        print_title("SEARCH MEDICINE")
        medicine_id = self._read_required_text("Medicine ID").upper()
        medicine = self._inventory.search_by_hash_table(medicine_id)

        if medicine is None:
            print_message(f"No medicine found with ID {medicine_id}.", False)
            return

        print(format_table(self.INVENTORY_HEADERS, [medicine.to_row()]))

    def _edit_medicine(self) -> None:
        """Edit stock stock_stock quantity and/or price."""
        print_title("EDIT MEDICINE")
        medicine_id = self._read_required_text("Medicine ID").upper()
        medicine = self._inventory.search_by_hash_table(medicine_id)

        if medicine is None:
            print_message(f"No medicine found with ID {medicine_id}.", False)
            return

        print("Current record:")
        print(format_table(self.INVENTORY_HEADERS, [medicine.to_row()]))

        stock_quantity = self._read_optional_non_negative_integer(
            "New stock_quantity, or press Enter to keep current"
        )
        price = self._read_optional_non_negative_float(
            "New price in RM, or press Enter to keep current"
        )

        updated = self._inventory.update_medicine(
            medicine_id=medicine_id,
            stock_quantity=stock_quantity,
            price=price,
        )

        if updated:
            print_message("Medicine record updated successfully.")
        else:
            print_message("Medicine record could not be updated.", False)

    def _delete_medicine(self) -> None:
        """Delete a medicine record."""
        print_title("DELETE MEDICINE")
        medicine_id = self._read_required_text("Medicine ID").upper()
        deleted = self._inventory.delete_medicine(medicine_id)

        if deleted:
            print_message("Medicine record deleted successfully.")
        else:
            print_message(f"No medicine found with ID {medicine_id}.", False)

    def _run_performance_comparison(self) -> None:
        """Run and display the search performance experiment."""
        print_title("SEARCH PERFORMANCE COMPARISON")
        experiment = SearchPerformanceExperiment(self._inventory)
        result = experiment.run()
        print(format_table(self.RESULT_HEADERS, result.to_rows()))

    @staticmethod
    def _read_required_text(label: str) -> str:
        """Read non-empty text input."""
        value = input(f"{label}: ").strip()

        if not value:
            raise ValueError(f"{label} cannot be empty.")

        return value

    @staticmethod
    def _read_non_negative_integer(label: str) -> int:
        """Read a required non-negative integer."""
        value = int(input(f"{label}: "))

        if value < 0:
            raise ValueError(f"{label} cannot be negative.")

        return value

    @staticmethod
    def _read_non_negative_float(label: str) -> float:
        """Read a required non-negative decimal value."""
        value = float(input(f"{label}: "))

        if value < 0:
            raise ValueError(f"{label} cannot be negative.")

        return value

    @staticmethod
    def _read_optional_non_negative_integer(label: str) -> int | None:
        """Read an optional non-negative integer."""
        raw_value = input(f"{label}: ").strip()

        if raw_value == "":
            return None

        value = int(raw_value)

        if value < 0:
            raise ValueError("Stock quantity cannot be negative.")

        return value

    @staticmethod
    def _read_optional_non_negative_float(label: str) -> float | None:
        """Read an optional non-negative decimal value."""
        raw_value = input(f"{label}: ").strip()

        if raw_value == "":
            return None

        value = float(raw_value)

        if value < 0:
            raise ValueError("Price cannot be negative.")

        return value

    @staticmethod
    def _read_date(label: str) -> date:
        """Read a valid date using YYYY-MM-DD format."""
        raw_value = input(f"{label}: ").strip()

        if not raw_value:
            raise ValueError(f"{label} cannot be empty.")

        return date.fromisoformat(raw_value)


def create_inventory_from_file(data_file: Path) -> PharmacyInventory:
    """
    Create the inventory and load predefined sample records from CSV.
    """
    inventory = PharmacyInventory(table_capacity=31)
    loaded_count = inventory.load_from_csv(data_file)
    print_message(f"{loaded_count} predefined medicine records loaded.")
    return inventory

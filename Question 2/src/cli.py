"""
Command-line interface for Question 2.
"""

from datetime import date
from pathlib import Path

from src.formatting import format_table, print_message, print_title
from src.merge_sort import MergeSorter
from src.models import Transaction
from src.performance import PerformanceExperiment, complexity_rows
from src.transaction_system import TransactionSystem


class TransactionCLI:
    """
    Menu-driven interface for the online shopping transaction system.
    """

    TRANSACTION_HEADERS = [
        "Transaction ID",
        "Customer Name",
        "Product Name",
        "Amount",
        "Transaction Date",
    ]

    RESULT_HEADERS = ["Description", "Value"]
    COMPLEXITY_HEADERS = ["Algorithm", "Best Case", "Average Case", "Worst Case", "Note"]

    SORT_ATTRIBUTE_OPTIONS = {
        "1": ("transaction_id", "Transaction ID"),
        "2": ("amount", "Amount"),
        "3": ("customer_name", "Customer Name"),
        "4": ("product_name", "Product Name"),
        "5": ("transaction_date", "Transaction Date"),
    }

    MENU_OPTIONS = {
        "1": "Display all transactions",
        "2": "Sort transactions by Transaction ID using Merge Sort",
        "3": "Search transaction using Binary Search",
        "4": "Search transaction using Linear Search",
        "5": "Insert transaction dynamically",
        "6": "Sort transactions by another attribute",
        "7": "Display last Merge Sort recursive calls",
        "8": "Run performance comparison",
        "9": "Display time complexity analysis",
        "10": "Exit",
    }

    def __init__(self, system: TransactionSystem) -> None:
        self._system = system

    def run(self) -> None:
        """
        Start the menu loop.
        """
        while True:
            self._display_menu()
            choice = input("Enter your choice (1-10): ").strip()

            if choice == "1":
                self._display_transactions()
            elif choice == "2":
                self._sort_by_transaction_id()
            elif choice == "3":
                self._binary_search()
            elif choice == "4":
                self._linear_search()
            elif choice == "5":
                self._insert_transaction()
            elif choice == "6":
                self._sort_by_custom_attribute()
            elif choice == "7":
                self._display_last_recursive_calls()
            elif choice == "8":
                self._run_performance_comparison()
            elif choice == "9":
                self._display_complexity_analysis()
            elif choice == "10":
                print_message("Thank you for using the Transaction Management System.")
                break
            else:
                print_message("Invalid choice. Please enter a number from 1 to 10.", False)

    def _display_menu(self) -> None:
        """Display the main menu."""
        print_title("ONLINE SHOPPING TRANSACTION SYSTEM")
        for number, description in self.MENU_OPTIONS.items():
            print(f"{number}. {description}")
        print("-" * 88)

    def _display_transactions(self) -> None:
        """Display all transaction records."""
        print_title("ALL TRANSACTION RECORDS")
        print(format_table(self.TRANSACTION_HEADERS, self._system.get_rows()))

    def _sort_by_transaction_id(self) -> None:
        """
        Mandatory feature:
        Sort transactions based on transaction ID using Merge Sort.
        """
        print_title("BEFORE SORTING")
        print(format_table(self.TRANSACTION_HEADERS, self._system.get_rows()))

        result = self._system.sort_transactions(
            sort_attribute="transaction_id",
            show_trace=True,
        )

        print_title("RECURSIVE CALL TRACE")
        for line in result.trace_lines:
            print(line)

        print_title("AFTER SORTING BY TRANSACTION ID")
        print(format_table(self.TRANSACTION_HEADERS, self._system.get_rows()))
        print_message(f"Merge Sort completed with {result.recursive_calls} recursive calls.")

    def _binary_search(self) -> None:
        """
        Mandatory feature:
        Search a transaction using recursive Binary Search.
        """
        print_title("BINARY SEARCH")
        transaction_id = self._read_required_text("Enter Transaction ID").upper()
        result = self._system.binary_search_transaction(transaction_id, show_trace=True)

        print_title("BINARY SEARCH TRACE")
        for line in result.trace_lines:
            print(line)

        if result.found:
            print_title("SEARCH RESULT")
            print(format_table(self.TRANSACTION_HEADERS, [result.transaction.to_row()]))
            print_message(f"Transaction found using {result.comparisons} comparison(s).")
        else:
            print_message(
                f"Transaction {transaction_id} was not found after "
                f"{result.comparisons} comparison(s).",
                False,
            )

    def _linear_search(self) -> None:
        """
        Mandatory comparison feature:
        Search a transaction using Linear Search.
        """
        print_title("LINEAR SEARCH")
        transaction_id = self._read_required_text("Enter Transaction ID").upper()
        result = self._system.linear_search_transaction(transaction_id)

        print_title("LINEAR SEARCH TRACE")
        for line in result.trace_lines:
            print(line)

        if result.found:
            print_title("SEARCH RESULT")
            print(format_table(self.TRANSACTION_HEADERS, [result.transaction.to_row()]))
            print_message(f"Transaction found using {result.comparisons} comparison(s).")
        else:
            print_message(
                f"Transaction {transaction_id} was not found after "
                f"{result.comparisons} comparison(s).",
                False,
            )

    def _insert_transaction(self) -> None:
        """
        Extra feature:
        Allow user to insert transaction dynamically.
        """
        print_title("INSERT NEW TRANSACTION")

        try:
            transaction = Transaction(
                transaction_id=self._read_required_text("Transaction ID").upper(),
                customer_name=self._read_required_text("Customer Name"),
                product_name=self._read_required_text("Product Name"),
                amount=self._read_non_negative_float("Amount in RM"),
                transaction_date=self._read_date("Transaction Date, format YYYY-MM-DD"),
            )

            self._system.insert_transaction(transaction)
            print_message("Transaction inserted or updated successfully.")

        except ValueError as error:
            print_message(str(error), False)

    def _sort_by_custom_attribute(self) -> None:
        """
        Extra feature:
        Allow sorting by different attributes.
        """
        print_title("SORT BY DIFFERENT ATTRIBUTE")
        for number, (_, label) in self.SORT_ATTRIBUTE_OPTIONS.items():
            print(f"{number}. {label}")

        choice = input("Choose sort attribute (1-5): ").strip()
        selected_option = self.SORT_ATTRIBUTE_OPTIONS.get(choice)

        if selected_option is None:
            print_message("Invalid sort attribute selected.", False)
            return

        sort_attribute, label = selected_option
        result = self._system.sort_transactions(sort_attribute=sort_attribute, show_trace=False)

        print_title(f"TRANSACTIONS SORTED BY {label.upper()}")
        print(format_table(self.TRANSACTION_HEADERS, self._system.get_rows()))
        print_message(f"Sorted by {label} with {result.recursive_calls} recursive calls.")

    def _display_last_recursive_calls(self) -> None:
        """
        Extra feature:
        Display number of recursive calls made during the last Merge Sort.
        """
        print_title("MERGE SORT RECURSIVE CALL COUNT")

        if self._system.last_sort_result is None:
            print_message("No Merge Sort has been performed yet.", False)
            return

        rows = [
            ["Last sort attribute", self._system.last_sort_attribute],
            ["Recursive calls", str(self._system.last_sort_result.recursive_calls)],
        ]

        print(format_table(self.RESULT_HEADERS, rows))

    def _run_performance_comparison(self) -> None:
        """
        Mandatory/analysis feature:
        Compare Merge Sort, Binary Search, and Linear Search performance.
        """
        print_title("PERFORMANCE COMPARISON")
        experiment = PerformanceExperiment(self._system.transactions)
        result = experiment.run()
        print(format_table(self.RESULT_HEADERS, result.to_rows()))

        print("\nAnalysis:")
        print(
            "Merge Sort sorts the full transaction list, so its average and worst-case "
            "time complexity is O(n log n). Binary Search only searches inside an "
            "already sorted list, so its time complexity is O(log n). Linear Search "
            "checks records one by one, so its average and worst-case time complexity "
            "is O(n). The measured time may be very small because the dataset contains "
            "20 records, but the comparison still shows the algorithmic difference."
        )

    def _display_complexity_analysis(self) -> None:
        """
        Extra feature:
        Display time complexity analysis in table format.
        """
        print_title("TIME COMPLEXITY ANALYSIS")
        print(format_table(self.COMPLEXITY_HEADERS, complexity_rows()))

    @staticmethod
    def _read_required_text(label: str) -> str:
        """Read non-empty text input."""
        value = input(f"{label}: ").strip()

        if not value:
            raise ValueError(f"{label} cannot be empty.")

        return value

    @staticmethod
    def _read_non_negative_float(label: str) -> float:
        """Read a non-negative float value."""
        value = float(input(f"{label}: "))

        if value < 0:
            raise ValueError(f"{label} cannot be negative.")

        return value

    @staticmethod
    def _read_date(label: str) -> date:
        """Read a date using ISO format."""
        raw_value = input(f"{label}: ").strip()
        return date.fromisoformat(raw_value)


def create_transaction_system_from_file(data_file: Path) -> TransactionSystem:
    """
    Create the transaction system and load predefined records from CSV.
    """
    system = TransactionSystem()
    loaded_count = system.load_from_csv(data_file)
    print_message(f"{loaded_count} predefined transaction records loaded.")
    return system

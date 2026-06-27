"""
Business logic for the online shopping transaction system.
"""

import csv
from datetime import date
from pathlib import Path
from typing import Optional

from src.merge_sort import MergeSorter, MergeSortResult
from src.models import Transaction
from src.search import BinarySearcher, LinearSearcher, SearchResult


class TransactionSystem:
    """
    Manages customer transactions and applies sorting/searching algorithms.
    """

    def __init__(self) -> None:
        self._transactions: list[Transaction] = []
        self._last_sort_result: Optional[MergeSortResult] = None
        self._last_sort_attribute: Optional[str] = None

    @property
    def transactions(self) -> list[Transaction]:
        """Return the current transaction list."""
        return self._transactions

    @property
    def last_sort_result(self) -> Optional[MergeSortResult]:
        """Return details of the most recent Merge Sort operation."""
        return self._last_sort_result

    @property
    def last_sort_attribute(self) -> Optional[str]:
        """Return the attribute used in the most recent sort."""
        return self._last_sort_attribute

    def load_from_csv(self, file_path: Path) -> int:
        """
        Load transaction records from a CSV file.

        Returns:
            Number of records loaded.
        """
        loaded_count = 0

        with file_path.open("r", encoding="utf-8", newline="") as csv_file:
            reader = csv.DictReader(csv_file)

            for row in reader:
                transaction = Transaction(
                    transaction_id=row["transaction_id"].strip().upper(),
                    customer_name=row["customer_name"].strip(),
                    product_name=row["product_name"].strip(),
                    amount=float(row["amount"]),
                    transaction_date=date.fromisoformat(row["transaction_date"]),
                )
                self.insert_transaction(transaction)
                loaded_count += 1

        return loaded_count

    def insert_transaction(self, transaction: Transaction) -> None:
        """
        Insert a new transaction dynamically.

        If the ID already exists, the existing transaction is updated.
        """
        transaction.transaction_id = transaction.transaction_id.strip().upper()
        existing_index = self._find_index(transaction.transaction_id)

        if existing_index is None:
            self._transactions.append(transaction)
        else:
            self._transactions[existing_index] = transaction

        # Any insertion/update may change the order.
        self._last_sort_result = None
        self._last_sort_attribute = None

    def sort_transactions(
        self,
        sort_attribute: str = "transaction_id",
        show_trace: bool = True,
    ) -> MergeSortResult:
        """
        Sort transactions using Merge Sort and update the current list.
        """
        sorter = MergeSorter(sort_attribute=sort_attribute, show_trace=show_trace)
        result = sorter.sort(self._transactions)

        self._transactions = result.sorted_transactions
        self._last_sort_result = result
        self._last_sort_attribute = sort_attribute

        return result

    def binary_search_transaction(
        self,
        transaction_id: str,
        show_trace: bool = True,
    ) -> SearchResult:
        """
        Search transaction by ID using Binary Search.

        Binary Search requires the data to be sorted by transaction_id. If the
        current data is not sorted by transaction_id, it is sorted automatically
        without trace to protect correctness.
        """
        if self._last_sort_attribute != "transaction_id":
            self.sort_transactions(sort_attribute="transaction_id", show_trace=False)

        searcher = BinarySearcher(show_trace=show_trace)
        return searcher.search(self._transactions, transaction_id)

    def linear_search_transaction(self, transaction_id: str) -> SearchResult:
        """
        Search transaction by ID using Linear Search.
        """
        searcher = LinearSearcher()
        return searcher.search(self._transactions, transaction_id)

    def get_rows(self) -> list[list[str]]:
        """
        Return transactions as table rows.
        """
        return [transaction.to_row() for transaction in self._transactions]

    def _find_index(self, transaction_id: str) -> Optional[int]:
        """
        Return the index of a transaction ID, or None if it does not exist.
        """
        for index, transaction in enumerate(self._transactions):
            if transaction.transaction_id == transaction_id:
                return index

        return None

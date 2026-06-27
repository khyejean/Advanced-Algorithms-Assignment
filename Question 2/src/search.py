"""
Search algorithms for Question 2.

This module provides:
    - Recursive Binary Search
    - Linear Search for comparison
"""

from dataclasses import dataclass
from typing import Optional

from src.models import Transaction


@dataclass
class SearchResult:
    """
    Stores the result of a search operation.

    Attributes:
        transaction: Found transaction, or None if not found.
        comparisons: Number of comparisons performed.
        trace_lines: Steps taken during the search.
    """

    transaction: Optional[Transaction]
    comparisons: int
    trace_lines: list[str]

    @property
    def found(self) -> bool:
        """Return True if a transaction was found."""
        return self.transaction is not None


class BinarySearcher:
    """
    Recursive Binary Search for sorted Transaction records.

    The transaction list must be sorted by transaction_id before using
    binary search.
    """

    def __init__(self, show_trace: bool = True) -> None:
        self._show_trace = show_trace
        self._comparisons = 0
        self._trace_lines: list[str] = []

    def search(self, transactions: list[Transaction], target_id: str) -> SearchResult:
        """
        Search for a transaction ID using recursive Binary Search.
        """
        self._comparisons = 0
        self._trace_lines = []

        target_id = target_id.strip().upper()
        found_transaction = self._binary_search_recursive(
            transactions=transactions,
            target_id=target_id,
            low=0,
            high=len(transactions) - 1,
            depth=0,
        )

        return SearchResult(
            transaction=found_transaction,
            comparisons=self._comparisons,
            trace_lines=self._trace_lines,
        )

    def _binary_search_recursive(
        self,
        transactions: list[Transaction],
        target_id: str,
        low: int,
        high: int,
        depth: int,
    ) -> Optional[Transaction]:
        """
        Recursive Binary Search.

        DIVIDE:
            Check the middle transaction.
        CONQUER:
            Continue searching only the left half or right half.
        COMBINE:
            No merging is required. The result is returned back through
            the recursive calls.
        """
        self._add_trace(depth, f"Search range index {low} to {high}")

        if low > high:
            self._add_trace(depth, "Base case: range is empty. Transaction not found.")
            return None

        middle = (low + high) // 2
        middle_transaction = transactions[middle]
        middle_id = middle_transaction.transaction_id
        self._comparisons += 1

        self._add_trace(
            depth,
            f"Compare target {target_id} with middle {middle_id} at index {middle}",
        )

        if middle_id == target_id:
            self._add_trace(depth, f"Transaction {target_id} found.")
            return middle_transaction

        if target_id < middle_id:
            self._add_trace(depth, "Target is smaller. Search left half.")
            return self._binary_search_recursive(
                transactions=transactions,
                target_id=target_id,
                low=low,
                high=middle - 1,
                depth=depth + 1,
            )

        self._add_trace(depth, "Target is larger. Search right half.")
        return self._binary_search_recursive(
            transactions=transactions,
            target_id=target_id,
            low=middle + 1,
            high=high,
            depth=depth + 1,
        )

    def _add_trace(self, depth: int, message: str) -> None:
        """Add an indented binary search trace line."""
        if self._show_trace:
            self._trace_lines.append(f"{'  ' * depth}{message}")


class LinearSearcher:
    """
    Linear Search for unsorted Transaction records.

    This is included for comparison with Binary Search.
    """

    def search(self, transactions: list[Transaction], target_id: str) -> SearchResult:
        """
        Search each transaction one by one from left to right.
        """
        target_id = target_id.strip().upper()
        trace_lines: list[str] = []
        comparisons = 0

        for index, transaction in enumerate(transactions):
            comparisons += 1
            trace_lines.append(
                f"Compare target {target_id} with {transaction.transaction_id} at index {index}"
            )

            if transaction.transaction_id == target_id:
                trace_lines.append(f"Transaction {target_id} found.")
                return SearchResult(transaction, comparisons, trace_lines)

        trace_lines.append(f"Transaction {target_id} not found after checking all records.")
        return SearchResult(None, comparisons, trace_lines)

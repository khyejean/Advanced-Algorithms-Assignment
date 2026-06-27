"""
Merge Sort implementation for Question 2.

This module clearly separates the Divide, Conquer, and Combine stages.
The implementation is recursive and can show recursive calls for reporting
and demonstration purposes.
"""

from dataclasses import dataclass
from typing import Any

from src.models import Transaction


@dataclass
class MergeSortResult:
    """
    Stores the output of Merge Sort.

    Attributes:
        sorted_transactions: New sorted list of Transaction objects.
        recursive_calls: Number of recursive merge sort calls made.
        trace_lines: Text log showing the recursive calls and stages.
    """

    sorted_transactions: list[Transaction]
    recursive_calls: int
    trace_lines: list[str]


class MergeSorter:
    """
    Recursive Merge Sort for Transaction records.

    The sorter can sort by different attributes:
        - transaction_id
        - customer_name
        - product_name
        - amount
        - transaction_date
    """

    VALID_SORT_ATTRIBUTES = {
        "transaction_id",
        "customer_name",
        "product_name",
        "amount",
        "transaction_date",
    }

    def __init__(self, sort_attribute: str = "transaction_id", show_trace: bool = True) -> None:
        if sort_attribute not in self.VALID_SORT_ATTRIBUTES:
            raise ValueError(f"Invalid sort attribute: {sort_attribute}")

        self._sort_attribute = sort_attribute
        self._show_trace = show_trace
        self._recursive_calls = 0
        self._trace_lines: list[str] = []

    def sort(self, transactions: list[Transaction]) -> MergeSortResult:
        """
        Sort transactions using recursive Merge Sort.

        Args:
            transactions: Original unsorted transaction list.

        Returns:
            MergeSortResult containing sorted records, recursive call count,
            and trace lines.
        """
        self._recursive_calls = 0
        self._trace_lines = []

        copied_transactions = transactions.copy()
        sorted_transactions = self._merge_sort(copied_transactions, depth=0)

        return MergeSortResult(
            sorted_transactions=sorted_transactions,
            recursive_calls=self._recursive_calls,
            trace_lines=self._trace_lines,
        )

    def _merge_sort(self, transactions: list[Transaction], depth: int) -> list[Transaction]:
        """
        Recursive Merge Sort function.

        This function controls the overall divide-and-conquer process.
        """
        self._recursive_calls += 1
        self._add_trace(depth, f"Call {self._recursive_calls}: merge_sort({self._ids(transactions)})")

        # Base case: a list with 0 or 1 item is already sorted.
        if len(transactions) <= 1:
            self._add_trace(depth, f"Base case reached: {self._ids(transactions)}")
            return transactions

        # DIVIDE: Split the list into two smaller sublists.
        left_half, right_half = self._divide(transactions, depth)

        # CONQUER: Recursively sort both halves.
        sorted_left = self._conquer(left_half, depth)
        sorted_right = self._conquer(right_half, depth)

        # COMBINE: Merge the two sorted halves into one sorted list.
        combined = self._combine(sorted_left, sorted_right, depth)
        return combined

    def _divide(
        self,
        transactions: list[Transaction],
        depth: int,
    ) -> tuple[list[Transaction], list[Transaction]]:
        """
        DIVIDE STEP:
        Split the transaction list into left and right halves.
        """
        middle_index = len(transactions) // 2
        left_half = transactions[:middle_index]
        right_half = transactions[middle_index:]

        self._add_trace(
            depth,
            f"Divide: {self._ids(transactions)} -> "
            f"Left {self._ids(left_half)}, Right {self._ids(right_half)}",
        )

        return left_half, right_half

    def _conquer(self, transactions: list[Transaction], depth: int) -> list[Transaction]:
        """
        CONQUER STEP:
        Recursively sort a smaller sublist.
        """
        self._add_trace(depth, f"Conquer: recursively sort {self._ids(transactions)}")
        return self._merge_sort(transactions, depth + 1)

    def _combine(
        self,
        left_half: list[Transaction],
        right_half: list[Transaction],
        depth: int,
    ) -> list[Transaction]:
        """
        COMBINE STEP:
        Merge two sorted lists into one sorted list.
        """
        merged_list: list[Transaction] = []
        left_index = 0
        right_index = 0

        while left_index < len(left_half) and right_index < len(right_half):
            if self._key(left_half[left_index]) <= self._key(right_half[right_index]):
                merged_list.append(left_half[left_index])
                left_index += 1
            else:
                merged_list.append(right_half[right_index])
                right_index += 1

        # Add any remaining records from either half.
        merged_list.extend(left_half[left_index:])
        merged_list.extend(right_half[right_index:])

        self._add_trace(
            depth,
            f"Combine: {self._ids(left_half)} + {self._ids(right_half)} -> "
            f"{self._ids(merged_list)}",
        )

        return merged_list

    def _key(self, transaction: Transaction) -> Any:
        """
        Return the value used for comparing two transactions.
        """
        return getattr(transaction, self._sort_attribute)

    @staticmethod
    def _ids(transactions: list[Transaction]) -> list[str]:
        """
        Return only transaction IDs for shorter recursive trace output.
        """
        return [transaction.transaction_id for transaction in transactions]

    def _add_trace(self, depth: int, message: str) -> None:
        """
        Add an indented trace line if tracing is enabled.
        """
        if self._show_trace:
            indentation = "  " * depth
            self._trace_lines.append(f"{indentation}{message}")

"""
Performance experiment for Question 2.

The experiment measures:
    - Merge Sort execution time
    - Binary Search execution time
    - Linear Search execution time

Merge Sort and Binary Search solve different tasks, so the analysis explains
that their execution times are not directly interchangeable.
"""

from dataclasses import dataclass
import time

from src.merge_sort import MergeSorter
from src.models import Transaction
from src.search import BinarySearcher, LinearSearcher


@dataclass
class PerformanceResult:
    """
    Stores performance measurement results.
    """

    merge_sort_time: float
    binary_search_time: float
    linear_search_time: float
    recursive_calls: int
    binary_comparisons: int
    linear_comparisons: int
    existing_key: str
    non_existing_key: str

    def to_rows(self) -> list[list[str]]:
        """Return experiment results as table rows."""
        return [
            ["Merge Sort time", f"{self.merge_sort_time:.8f} seconds"],
            ["Binary Search time", f"{self.binary_search_time:.8f} seconds"],
            ["Linear Search time", f"{self.linear_search_time:.8f} seconds"],
            ["Merge Sort recursive calls", str(self.recursive_calls)],
            ["Binary Search comparisons", str(self.binary_comparisons)],
            ["Linear Search comparisons", str(self.linear_comparisons)],
            ["Existing key tested", self.existing_key],
            ["Non-existing key tested", self.non_existing_key],
        ]


class PerformanceExperiment:
    """
    Runs the performance comparison for Question 2.
    """

    def __init__(
        self,
        transactions: list[Transaction],
        existing_key: str = "T1015",
        non_existing_key: str = "T9999",
    ) -> None:
        self._transactions = transactions
        self._existing_key = existing_key
        self._non_existing_key = non_existing_key

    def run(self) -> PerformanceResult:
        """
        Measure Merge Sort, Binary Search, and Linear Search execution time.
        """
        # Measure Merge Sort.
        merge_sorter = MergeSorter(sort_attribute="transaction_id", show_trace=False)

        start_time = time.perf_counter()
        sort_result = merge_sorter.sort(self._transactions)
        merge_sort_time = time.perf_counter() - start_time

        sorted_transactions = sort_result.sorted_transactions

        # Measure Binary Search using two keys: one existing and one non-existing.
        binary_searcher = BinarySearcher(show_trace=False)

        start_time = time.perf_counter()
        existing_binary_result = binary_searcher.search(sorted_transactions, self._existing_key)
        missing_binary_result = binary_searcher.search(sorted_transactions, self._non_existing_key)
        binary_search_time = time.perf_counter() - start_time

        total_binary_comparisons = (
            existing_binary_result.comparisons + missing_binary_result.comparisons
        )

        # Measure Linear Search using the same two keys.
        linear_searcher = LinearSearcher()

        start_time = time.perf_counter()
        existing_linear_result = linear_searcher.search(self._transactions, self._existing_key)
        missing_linear_result = linear_searcher.search(self._transactions, self._non_existing_key)
        linear_search_time = time.perf_counter() - start_time

        total_linear_comparisons = (
            existing_linear_result.comparisons + missing_linear_result.comparisons
        )

        return PerformanceResult(
            merge_sort_time=merge_sort_time,
            binary_search_time=binary_search_time,
            linear_search_time=linear_search_time,
            recursive_calls=sort_result.recursive_calls,
            binary_comparisons=total_binary_comparisons,
            linear_comparisons=total_linear_comparisons,
            existing_key=self._existing_key,
            non_existing_key=self._non_existing_key,
        )


def complexity_rows() -> list[list[str]]:
    """
    Return time complexity analysis in tabular form.
    """
    return [
        ["Merge Sort", "O(n log n)", "O(n log n)", "O(n log n)", "Sorts the full dataset"],
        ["Binary Search", "O(1)", "O(log n)", "O(log n)", "Requires sorted data"],
        ["Linear Search", "O(1)", "O(n)", "O(n)", "Works on unsorted data"],
    ]

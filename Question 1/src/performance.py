"""
Performance experiment for Question 1.

Compares Hash Table search with one-dimensional array sequential search.
"""

from dataclasses import dataclass
import time

from src.inventory import PharmacyInventory


@dataclass
class SearchExperimentResult:
    """
    Stores result values from the search performance experiment.
    """

    search_keys: list[str]
    repetitions: int
    hash_table_time: float
    array_time: float

    @property
    def faster_structure(self) -> str:
        """Return the faster data structure in this experiment."""
        if self.hash_table_time < self.array_time:
            return "Hash Table"
        return "One-Dimensional Array"

    @property
    def speed_difference(self) -> float:
        """Return how many times faster one structure is than the other."""
        slower_time = max(self.hash_table_time, self.array_time)
        faster_time = min(self.hash_table_time, self.array_time)

        if faster_time == 0:
            return 0

        return slower_time / faster_time

    def to_rows(self) -> list[list[str]]:
        """Return experiment results as formatted table rows."""
        return [
            ["Search keys tested", ", ".join(self.search_keys)],
            ["Repetitions per key", str(self.repetitions)],
            ["Hash table search time", f"{self.hash_table_time:.8f} seconds"],
            ["Array search time", f"{self.array_time:.8f} seconds"],
            ["Faster structure", self.faster_structure],
            ["Speed difference", f"{self.speed_difference:.2f} times"],
        ]


class SearchPerformanceExperiment:
    """
    Runs the search performance comparison.

    The same search keys are used for both data structures to ensure a fair
    comparison.
    """

    DEFAULT_SEARCH_KEYS = [
        "M001",
        "M003",
        "M006",
        "M009",
        "M012",
        "M013",
        "M020",
        "X001",
        "ABC",
        "M999",
    ]

    def __init__(
        self,
        inventory: PharmacyInventory,
        search_keys: list[str] | None = None,
        repetitions: int = 10000,
    ) -> None:
        self._inventory = inventory
        self._search_keys = search_keys or self.DEFAULT_SEARCH_KEYS
        self._repetitions = repetitions

    def run(self) -> SearchExperimentResult:
        """
        Run the comparison and return measured execution times.
        """
        hash_table_time = self._measure_hash_table_search()
        array_time = self._measure_array_search()

        return SearchExperimentResult(
            search_keys=self._search_keys,
            repetitions=self._repetitions,
            hash_table_time=hash_table_time,
            array_time=array_time,
        )

    def _measure_hash_table_search(self) -> float:
        """Measure total search time for the hash table."""
        start_time = time.perf_counter()

        for _ in range(self._repetitions):
            for key in self._search_keys:
                self._inventory.search_by_hash_table(key)

        return time.perf_counter() - start_time

    def _measure_array_search(self) -> float:
        """Measure total search time for the one-dimensional array."""
        start_time = time.perf_counter()

        for _ in range(self._repetitions):
            for key in self._search_keys:
                self._inventory.search_by_array(key)

        return time.perf_counter() - start_time

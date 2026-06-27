"""
Data models for Question 3 experiment results.
"""

from dataclasses import dataclass, field


@dataclass
class FactorialTaskResult:
    """
    Stores the result produced by one factorial task.
    """

    number: int
    factorial_value: int
    digit_count: int
    thread_name: str
    started_at_ns: int
    finished_at_ns: int

    @property
    def duration_ns(self) -> int:
        """Return the duration of this individual task in nanoseconds."""
        return self.finished_at_ns - self.started_at_ns


@dataclass
class ExperimentRoundResult:
    """
    Stores the timing and task results for one experiment round.
    """

    round_number: int
    total_time_ns: int
    task_results: list[FactorialTaskResult] = field(default_factory=list)

    def to_summary_row(self) -> list[str]:
        """Return a formatted row for the round summary table."""
        return [
            str(self.round_number),
            f"{self.total_time_ns:,}",
        ]


@dataclass
class ExperimentSummary:
    """
    Stores all rounds for either the threaded or non-threaded experiment.
    """

    experiment_name: str
    round_results: list[ExperimentRoundResult]

    @property
    def average_time_ns(self) -> float:
        """Return the average total time in nanoseconds."""
        if not self.round_results:
            return 0.0

        total_time = sum(round_result.total_time_ns for round_result in self.round_results)
        return total_time / len(self.round_results)

    @property
    def fastest_time_ns(self) -> int:
        """Return the fastest round time."""
        return min(round_result.total_time_ns for round_result in self.round_results)

    @property
    def slowest_time_ns(self) -> int:
        """Return the slowest round time."""
        return max(round_result.total_time_ns for round_result in self.round_results)

    def to_summary_rows(self) -> list[list[str]]:
        """Return each round as formatted rows."""
        return [round_result.to_summary_row() for round_result in self.round_results]

    def to_statistics_rows(self) -> list[list[str]]:
        """Return experiment statistics as formatted rows."""
        return [
            ["Experiment", self.experiment_name],
            ["Rounds", str(len(self.round_results))],
            ["Fastest time", f"{self.fastest_time_ns:,} ns"],
            ["Slowest time", f"{self.slowest_time_ns:,} ns"],
            ["Average time", f"{self.average_time_ns:,.2f} ns"],
        ]

"""
Command-line interface for Question 3.

This version focuses only on the practical experiment features required
inside the Python program:
    - Big-O derivation for the factorial function
    - Multithreading experiment
    - Non-multithreading experiment
    - Full comparison experiment
"""

from src.experiments import NonThreadedFactorialExperiment, ThreadedFactorialExperiment
from src.factorial import factorial_complexity_rows
from src.formatting import format_table, print_message, print_title
from src.models import ExperimentSummary


class ConcurrentProcessCLI:
    """
    Menu-driven interface for the concurrent process experiment.
    """

    DEFAULT_NUMBERS = [50, 100, 200]
    DEFAULT_ROUNDS = 10

    RESULT_HEADERS = ["Description", "Value"]
    ROUND_HEADERS = ["Round", "Total Time (ns)"]
    TASK_HEADERS = ["n", "Thread", "Digits in n!", "Task Time (ns)"]
    COMPLEXITY_HEADERS = ["Operation", "Frequency", "Explanation"]

    MENU_OPTIONS = {
        "1": "Show factorial Big-O derivation",
        "2": "Run multithreading experiment",
        "3": "Run non-multithreading experiment",
        "4": "Run full comparison experiment",
        "5": "Exit",
    }

    def __init__(self) -> None:
        self._last_threaded_summary: ExperimentSummary | None = None
        self._last_non_threaded_summary: ExperimentSummary | None = None

    def run(self) -> None:
        """
        Start the command-line menu loop.
        """
        while True:
            self._display_menu()
            choice = input("Enter your choice (1-5): ").strip()

            if choice == "1":
                self._display_big_o_derivation()
            elif choice == "2":
                self._run_threaded_experiment()
            elif choice == "3":
                self._run_non_threaded_experiment()
            elif choice == "4":
                self._run_full_comparison()
            elif choice == "5":
                print_message("Thank you for using the Concurrent Process System.")
                break
            else:
                print_message("Invalid choice. Please enter a number from 1 to 5.", False)

    def _display_menu(self) -> None:
        """
        Display the main menu.
        """
        print_title("QUESTION 3: CONCURRENT PROCESS EXPERIMENT")
        for number, description in self.MENU_OPTIONS.items():
            print(f"{number}. {description}")
        print("-" * 92)

    def _display_big_o_derivation(self) -> None:
        """
        Display primitive operation analysis and Big-O conclusion.
        """
        print_title("FACTORIAL BIG-O DERIVATION")
        print(format_table(self.COMPLEXITY_HEADERS, factorial_complexity_rows()))
        print(
            "\nConclusion: The factorial function has O(n) time complexity because "
            "the number of loop iterations increases linearly with the input number n. "
            "For n!, the function performs one multiplication for each value from 2 to n."
        )

    def _run_threaded_experiment(self) -> None:
        """
        Run only the multithreading experiment.
        """
        print_title("MULTITHREADING EXPERIMENT")
        experiment = ThreadedFactorialExperiment(
            numbers=self.DEFAULT_NUMBERS,
            rounds=self.DEFAULT_ROUNDS,
        )
        self._last_threaded_summary = experiment.run()
        self._display_experiment_summary(self._last_threaded_summary)

    def _run_non_threaded_experiment(self) -> None:
        """
        Run only the non-threaded experiment.
        """
        print_title("NON-MULTITHREADING EXPERIMENT")
        experiment = NonThreadedFactorialExperiment(
            numbers=self.DEFAULT_NUMBERS,
            rounds=self.DEFAULT_ROUNDS,
        )
        self._last_non_threaded_summary = experiment.run()
        self._display_experiment_summary(self._last_non_threaded_summary)

    def _run_full_comparison(self) -> None:
        """
        Run both experiments and compare the results.
        """
        print_title("FULL COMPARISON EXPERIMENT")

        threaded_experiment = ThreadedFactorialExperiment(
            numbers=self.DEFAULT_NUMBERS,
            rounds=self.DEFAULT_ROUNDS,
        )
        non_threaded_experiment = NonThreadedFactorialExperiment(
            numbers=self.DEFAULT_NUMBERS,
            rounds=self.DEFAULT_ROUNDS,
        )

        self._last_threaded_summary = threaded_experiment.run()
        self._last_non_threaded_summary = non_threaded_experiment.run()

        self._display_experiment_summary(self._last_threaded_summary)
        self._display_experiment_summary(self._last_non_threaded_summary)
        self._display_comparison_table(
            threaded_summary=self._last_threaded_summary,
            non_threaded_summary=self._last_non_threaded_summary,
        )

    def _display_experiment_summary(self, summary: ExperimentSummary) -> None:
        """
        Display the 10-round result table and average time.
        """
        print_title(f"{summary.experiment_name.upper()} - 10 ROUND RESULTS")
        print(format_table(self.ROUND_HEADERS, summary.to_summary_rows()))

        print_title(f"{summary.experiment_name.upper()} - SUMMARY STATISTICS")
        print(format_table(self.RESULT_HEADERS, summary.to_statistics_rows()))

        last_round = summary.round_results[-1]
        task_rows = [
            [
                str(result.number),
                result.thread_name,
                str(result.digit_count),
                f"{result.duration_ns:,}",
            ]
            for result in last_round.task_results
        ]

        print_title(f"{summary.experiment_name.upper()} - SAMPLE TASK DETAILS FROM ROUND 10")
        print(format_table(self.TASK_HEADERS, task_rows))

    def _display_comparison_table(
        self,
        threaded_summary: ExperimentSummary,
        non_threaded_summary: ExperimentSummary,
    ) -> None:
        """
        Display final comparison between multithreaded and non-threaded results.
        """
        threaded_average = threaded_summary.average_time_ns
        non_threaded_average = non_threaded_summary.average_time_ns
        difference = abs(threaded_average - non_threaded_average)

        if threaded_average < non_threaded_average:
            conclusion = "Multithreading was faster in this run."
        elif threaded_average > non_threaded_average:
            conclusion = "Non-multithreading was faster in this run."
        else:
            conclusion = "Both approaches had the same average time."

        rows = [
            ["Multithreading average", f"{threaded_average:,.2f} ns"],
            ["Non-multithreading average", f"{non_threaded_average:,.2f} ns"],
            ["Difference", f"{difference:,.2f} ns"],
            ["Conclusion from measured output", conclusion],
        ]

        print_title("FINAL COMPARISON")
        print(format_table(self.RESULT_HEADERS, rows))

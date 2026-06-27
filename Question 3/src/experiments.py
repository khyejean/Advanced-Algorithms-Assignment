"""
Threaded and non-threaded factorial experiments for Question 3.

The assignment requires:
    - 3 separate threads
    - 1 thread for 50!
    - 1 thread for 100!
    - 1 thread for 200!
    - 10 rounds of testing
    - total time in nanoseconds
"""

from threading import Lock, Thread, current_thread
from time import perf_counter_ns

from src.factorial import calculate_factorial
from src.models import ExperimentRoundResult, ExperimentSummary, FactorialTaskResult


class ThreadedFactorialExperiment:
    """
    Calculates factorials using multithreading.

    For every round, this class creates exactly three threads:
        Thread 1 -> calculates 50!
        Thread 2 -> calculates 100!
        Thread 3 -> calculates 200!

    The total elapsed time is calculated using the assignment formula:
        T = End_Time_Of_Thread_Finished_Last - Start_Time_Of_Thread_That_Started_First
    """

    def __init__(self, numbers: list[int], rounds: int = 10) -> None:
        self._numbers = numbers
        self._rounds = rounds

    def run(self) -> ExperimentSummary:
        """
        Run the multithreaded factorial experiment for the required rounds.
        """
        round_results: list[ExperimentRoundResult] = []

        for round_number in range(1, self._rounds + 1):
            round_result = self._run_single_round(round_number)
            round_results.append(round_result)

        return ExperimentSummary(
            experiment_name="Multithreading",
            round_results=round_results,
        )

    def _run_single_round(self, round_number: int) -> ExperimentRoundResult:
        """
        Run one multithreaded experiment round.
        """
        task_results: list[FactorialTaskResult] = []
        result_lock = Lock()
        threads: list[Thread] = []

        for number in self._numbers:
            thread = Thread(
                target=self._worker,
                args=(number, task_results, result_lock),
                name=f"Thread-{number}!",
            )
            threads.append(thread)

        # Start all 3 threads. Each thread records its own actual start time.
        for thread in threads:
            thread.start()

        # Wait until all 3 threads finish.
        for thread in threads:
            thread.join()

        first_thread_start_time = min(result.started_at_ns for result in task_results)
        last_thread_end_time = max(result.finished_at_ns for result in task_results)
        total_time_ns = last_thread_end_time - first_thread_start_time

        task_results.sort(key=lambda result: result.number)

        return ExperimentRoundResult(
            round_number=round_number,
            total_time_ns=total_time_ns,
            task_results=task_results,
        )

    @staticmethod
    def _worker(
        number: int,
        task_results: list[FactorialTaskResult],
        result_lock: Lock,
    ) -> None:
        """
        Worker function executed by each thread.

        It records the start time, calculates the factorial, records the end
        time, and stores the result safely using a lock.
        """
        started_at_ns = perf_counter_ns()
        factorial_value = calculate_factorial(number)
        finished_at_ns = perf_counter_ns()

        task_result = FactorialTaskResult(
            number=number,
            factorial_value=factorial_value,
            digit_count=len(str(factorial_value)),
            thread_name=current_thread().name,
            started_at_ns=started_at_ns,
            finished_at_ns=finished_at_ns,
        )

        with result_lock:
            task_results.append(task_result)


class NonThreadedFactorialExperiment:
    """
    Calculates the same factorials sequentially without multithreading.

    The total time is measured from the start of the first factorial operation
    to the end of the last factorial operation for each round.
    """

    def __init__(self, numbers: list[int], rounds: int = 10) -> None:
        self._numbers = numbers
        self._rounds = rounds

    def run(self) -> ExperimentSummary:
        """
        Run the non-threaded factorial experiment for the required rounds.
        """
        round_results: list[ExperimentRoundResult] = []

        for round_number in range(1, self._rounds + 1):
            round_result = self._run_single_round(round_number)
            round_results.append(round_result)

        return ExperimentSummary(
            experiment_name="Non-Multithreading",
            round_results=round_results,
        )

    def _run_single_round(self, round_number: int) -> ExperimentRoundResult:
        """
        Run one non-threaded experiment round.
        """
        task_results: list[FactorialTaskResult] = []

        start_time_ns = perf_counter_ns()

        for number in self._numbers:
            task_start_ns = perf_counter_ns()
            factorial_value = calculate_factorial(number)
            task_end_ns = perf_counter_ns()

            task_results.append(
                FactorialTaskResult(
                    number=number,
                    factorial_value=factorial_value,
                    digit_count=len(str(factorial_value)),
                    thread_name="MainThread",
                    started_at_ns=task_start_ns,
                    finished_at_ns=task_end_ns,
                )
            )

        end_time_ns = perf_counter_ns()
        total_time_ns = end_time_ns - start_time_ns

        return ExperimentRoundResult(
            round_number=round_number,
            total_time_ns=total_time_ns,
            task_results=task_results,
        )

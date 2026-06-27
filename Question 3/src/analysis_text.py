"""
Report discussion text used by the program output.
"""


def python_threading_discussion() -> str:
    """
    Return a concise discussion on Python multithreading.
    """
    return (
        "Python supports multithreading, but in the standard CPython interpreter, "
        "threads are usually concurrent rather than truly parallel for CPU-bound "
        "Python code. This is because the Global Interpreter Lock (GIL) allows only "
        "one thread to execute Python bytecode at a time. Therefore, the three "
        "factorial calculations may be interleaved by the operating system, but "
        "they normally do not run as three Python bytecode computations at the exact "
        "same time on separate CPU cores. For this factorial experiment, the task is "
        "CPU-bound, so multithreading may not shorten the time taken and may even add "
        "thread creation and scheduling overhead."
    )


def multithreading_findings_discussion() -> str:
    """
    Return report-friendly analysis for the experiment findings.
    """
    return (
        "The factorial calculation is CPU-bound because the processor mainly performs "
        "repeated multiplication. In standard CPython, the Global Interpreter Lock "
        "limits CPU-bound Python threads because only one thread can execute Python "
        "bytecode at a time. As a result, multithreading may not reduce the total "
        "execution time for calculating 50!, 100!, and 200!. The multithreaded version "
        "also has additional overhead because it must create threads, start them, "
        "switch between them, use a lock when storing results, and wait for all threads "
        "to finish. Therefore, the non-threaded version may be similar or faster for "
        "this small CPU-bound experiment. Multithreading is more useful for I/O-bound "
        "tasks, such as downloading several files, reading multiple network responses, "
        "or waiting for database queries, because one thread can continue working "
        "while another thread is waiting for input/output."
    )

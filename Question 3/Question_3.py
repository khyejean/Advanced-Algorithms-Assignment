"""
Question 3: Concurrent Process

This program implements:
    1. Factorial calculation for 50!, 100!, and 200!
    2. Big-O discussion for the factorial function
    3. Multithreaded factorial experiment using 3 separate threads
    4. Non-threaded factorial experiment
    5. 10-round timing comparison in nanoseconds

Run:
    python Question_3.py
"""

from src.cli import ConcurrentProcessCLI


def main() -> None:
    """
    Program entry point.
    """
    app = ConcurrentProcessCLI()
    app.run()


if __name__ == "__main__":
    main()

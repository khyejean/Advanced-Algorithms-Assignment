"""
Factorial calculation for Question 3.

This module contains the function that calculates n!, plus a helper that
summarises its Big-O analysis for the report.
"""


def calculate_factorial(number: int) -> int:
    """
    Calculate the factorial of a non-negative integer.

    Formula:
        n! = n x (n - 1) x (n - 2) x ... x 1

    Time complexity:
        O(n), because the loop performs one multiplication for each integer
        from 2 to n.

    Space complexity:
        O(1), excluding the storage size of the final large integer.
    """
    if number < 0:
        raise ValueError("Factorial is not defined for negative numbers.")

    result = 1

    for current_number in range(2, number + 1):
        result *= current_number

    return result


def factorial_complexity_rows() -> list[list[str]]:
    """
    Return report-friendly primitive operation analysis for factorial.
    """
    return [
        ["Input validation: number < 0", "1", "Constant operation"],
        ["Initialise result = 1", "1", "Constant operation"],
        ["Loop from 2 to n", "n - 1 iterations", "Runs once for each factor"],
        ["Multiplication result *= current_number", "n - 1", "One multiplication per iteration"],
        ["Assignment back to result", "n - 1", "One assignment per iteration"],
        ["Return result", "1", "Constant operation"],
        ["Overall time complexity", "O(n)", "Linear growth"],
        ["Overall space complexity", "O(1)", "Uses one main result variable"],
    ]

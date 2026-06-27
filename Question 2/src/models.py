"""
Entity models for Question 2.

This module contains the Transaction entity class used by the online
shopping transaction system.
"""

from dataclasses import dataclass
from datetime import date


@dataclass
class Transaction:
    """
    Represents one customer transaction in an online shopping system.

    Attributes:
        transaction_id: Unique transaction ID used for sorting and searching.
        customer_name: Name of the customer who made the transaction.
        product_name: Name of the purchased product.
        amount: Transaction amount.
        transaction_date: Date when the transaction was made.
    """

    transaction_id: str
    customer_name: str
    product_name: str
    amount: float
    transaction_date: date

    def to_row(self) -> list[str]:
        """
        Convert a transaction object into formatted strings for table display.
        """
        return [
            self.transaction_id,
            self.customer_name,
            self.product_name,
            f"RM {self.amount:.2f}",
            self.transaction_date.isoformat(),
        ]

    def __str__(self) -> str:
        """Return a readable single-line transaction description."""
        return (
            f"{self.transaction_id} | {self.customer_name} | {self.product_name} | "
            f"RM {self.amount:.2f} | {self.transaction_date.isoformat()}"
        )

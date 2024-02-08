from os import chdir
from os.path import dirname
from io import open
from sys import exit
from pyarrow.csv import read_csv, ReadOptions, write_csv, WriteOptions
from pyarrow import Table, ArrowInvalid
from datetime import datetime, UTC


class BookDB:
    def __init__(self, filename: str):
        # Assign class attributes
        self.filename: str = filename
        self.__inventory: float = 0.0

        # Change path to script directory
        chdir(dirname(__file__))

        # Create file if it doesn't exist
        open(self.filename, "a+").close()

        # Import CSV data to memory
        try:
            self.data: list[dict[str, str | int | float]] = read_csv(
                input_file=self.filename,
                read_options=ReadOptions(
                    column_names=["ISBN", "Title", "Author", "Quantity", "Price"]
                ),
            ).to_pylist()
        except ArrowInvalid:
            exit()

    # Setup context manager protocol entry
    #
    # We are implementing a way to interact with the context manager protocol
    # so that we can ensure that the CSV we're working with is updated
    # no matter what the circumstance, since changes aren't written to
    # the file immediately and only to memory
    def __enter__(self):
        return self

    # Context manager exit
    def __exit__(self, exc_type, exc_value, exc_tb):  # type: ignore
        self.flush()

    def search(self, isbn: str) -> int:
        # Perform linear search to retrieve index
        pos = -1
        for i, book in enumerate(self.data):
            if book["ISBN"] == isbn:
                pos = i
                break
        return pos

    def read(self, isbn: str = "") -> list[dict[str, str | int | float]]:
        # Retrieve data of specific ISBN if provided
        if isbn != "":
            return [self.data[self.search(isbn)]]

        # Retrieve everything if no ISBN was provided
        return self.data

    def add(
        self, isbn: str, title: str, author: str, quantity: int, price: float
    ) -> int:
        # Check if already exists
        if self.search(isbn) != -1:
            return 1

        # Strip hyphens
        isbn = isbn.replace("-", "")

        # Length check
        if len(isbn) != 13:
            return 2

        # Check if all characters are digits
        if not isbn.isdigit():
            return 3

        # Calculate check digit
        check_digit = (
            sum((int(isbn[i]) * (3 if i & 1 == 1 else 1)) for i in range(12))
        ) % 10

        # Validate the check digit
        if not check_digit == int(isbn[-1]):
            return 4

        # Add hyphens to ISBN
        isbn = (
            isbn[0:3]
            + "-"
            + isbn[3:4]
            + "-"
            + isbn[4:6]
            + "-"
            + isbn[6:12]
            + "-"
            + isbn[12:13]
        )

        # Add data to list
        self.data.append(
            {
                "ISBN": isbn,
                "Title": title,
                "Author": author,
                "Quantity": quantity,
                "Price": price,
            }
        )

        return 0

    # Function to update inventory quantity of given ISBN
    def update_quantity(self, isbn: str, quantity: int) -> None:
        self.data[self.search(isbn)]["Quantity"] = quantity

    # Implement `inventory` property
    @property
    def inventory(self) -> float:
        """Total value of the inventory we have"""
        return self.__inventory

    @inventory.getter
    def inventory(self) -> float:
        for book in self.data:
            self.__inventory += book["Quantity"] * book["Price"]  # type: ignore
        return self.__inventory

    def sale(self, isbn: str, quantity: int) -> bool:
        # Retrieve position of given ISBN
        pos = self.search(isbn)
        if pos == -1:
            return False

        self.data[pos]["Quantity"] -= quantity  # type: ignore

        with open("sales_report.txt", "a+", encoding="utf-8") as file:
            file.writelines(
                [
                    f"ISBN: {isbn}\n",
                    f"Sold: {quantity}\n",
                    f"Value: {self.data[pos]['Price'] * quantity}\n",
                    f"Time: {datetime.now(UTC)}\n",
                    f"Current Inventory: {self.data[pos]["Quantity"]}\n\n",
                ]
            )
        return True

    def flush(self):
        write_csv(
            data=Table.from_pylist(self.data),
            output_file=self.filename,
            write_options=WriteOptions(include_header=False, quoting_style="none"),
        )

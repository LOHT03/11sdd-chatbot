from typing import Dict, List, Tuple

from terminaltables import AsciiTable

from controller.types import MenuItem
from db.db import dbconn


class Menu:
    def __init__(self) -> None:

        # Query database for menu information
        data: List[Tuple[str, str, float]] = dbconn.execute("""
        SELECT courseName,
            dishName,
            dishPrice
        FROM courses,
            dishes
        WHERE courses.courseID = dishes.courseID;
        """).fetchall()

        # Create Instance Properties
        self.menu: Dict[str, Dict[str, float]] = {}
        self.__courselessMenu: Dict[str, float] = {}

        # Parse database information
        for (courseName, dishName, dishPrice) in data:

            # Check if course does not exist in instance menu
            if not courseName in self.menu:

                # Create empty dictionary in the menu for the course
                self.menu[courseName] = {}

            # Add the dish and the price to the course within the menu
            self.menu[courseName][dishName] = float(dishPrice)

            # Add the dish to a courseless menu within the instance
            self.__courselessMenu[dishName] = float(dishPrice)

    def show(self, course: str = None):
        """Print menu to the console, for all courses or a specific course.

        Keyword Arguments:
            course {str} -- (Optional) The course that should be displayed. (default: {None})
        """

        # Create headings for the table
        tableData = [("Meal", "Price")]

        # Check to see if a course was provided
        if course is not None:

            # Get every dish for the course from the instance menu
            for (mealName, mealPrice) in self.menu[course].items():

                # Add the dishes as tuples to the table data
                tableData.append(
                    (mealName.capitalize(), str(f"${mealPrice:.2f}")))
        else:
            # Get every dish for every course in the instance menu
            for course in self.menu:

                # Add the course name as a heading within the table
                tableData.append((course.capitalize(), str("******")))

                # Iterate over dishes in the course
                for meal in self.menu[course].items():

                    # Add the dish to the table data
                    tableData.append(
                        (meal[0].capitalize(), str(f"${meal[1]:5.2f}")))

                # Add an empty line to the table to separate courses
                tableData.append((str(""), str("")))

            # Remove the last empty line of the table data
            tableData.pop()

        # Create a new instance of the table to be printed
        table = AsciiTable(tableData, course.capitalize()
                           if course else "Menu")

        # Justify prices column to the right
        table.justify_columns[1] = "right"
        print()

        # Print the table to the console
        print(table.table)
        print()

    def getDish(self, dishName: str, course: str = None) -> Tuple[str, float]:
        """Returns a tuple containing the dish name and price for a provided dish name
        and optionally a course.

        Arguments:
            dishName {str} -- The name of the dish.

        Keyword Arguments:
            course {str} -- (Optional) The course from which to get the dish (default: {None})

        Raises:
            ValueError: Meal does not exist in the menu.
            ValueError: Course does not exist in the menu.
            ValueError: Dish does not exist within specified course.

        Returns:
            Tuple[str, float] -- Tuple containing the dish name and price.
        """

        # Check to see if a course was provided
        if course is None:

            # Check the instance courselessMenu to check if the dish exists at all
            if dishName not in self.__courselessMenu:
                raise ValueError("Meal does not exist.")
            else:

                # return the dish and price if it does exist
                return (dishName, self.__courselessMenu[dishName])

        # Provided course does not exist in the menu
        elif course not in self.menu:
            raise ValueError("Course does not exist.")

        # Provided course does exist
        else:

            # Dish does not exist in the course
            if dishName not in self.menu[course]:
                raise ValueError("Dish does not exist within course.")

            # Dish does exist, return dish name and price
            else:
                return (dishName, self.menu[course][dishName])

    # Create new static method
    @staticmethod
    def displayTotals(items: List[MenuItem], tableName: str = None):
        """Creates a table for a list of menu items and prints it to the console. Calculates total.

        Arguments:
            items {List[MenuItem]} -- List of menu items to be added to the table.

        Keyword Arguments:
            tableName {str} -- (Optional) Name of the table (default: {None})
        """

        # Create column headings for the table
        tableData = [("Dish", "Qty", "Unit", "Price")]

        # Eventual total for all of the items
        finalTotal: float = 0

        # Eventual total for number of items ordered
        finalQty: int = 0

        # Add items to the table data
        for (dish, price, quantity) in items:

            # Add value to final total
            finalTotal += (price*quantity)

            # Add dish to the table data
            tableData.append(
                (f"{dish.capitalize()}", f"{quantity}", f"${price:.2f}", f"${(price * quantity):.2f}"))

            # Add quantity of dish to the total quantity
            finalQty += quantity

        # Add the footer row displaying the totals for all columns
        tableData.append(
            ("TOTAL", f"{finalQty}", f"---", f"${finalTotal:.2f}"))

        # Create table instance
        table = AsciiTable(tableData, tableName)

        # Justify qty, unit and price columns to the right
        table.justify_columns[1] = "right"
        table.justify_columns[2] = "right"
        table.justify_columns[3] = "right"

        # Add footer separating row
        table.inner_footing_row_border = True

        # Print the table to the console
        print(table.table)

    @property
    def dishes(self) -> List[str]:
        """Return all dishes in the instance menu.

        Returns:
            List[str] -- List of all of the dishes.
        """

        # Create an empty list for the dishes
        menuItems: List[str] = []

        # Iterate over all courses in the instance menu
        for course in self.menu:

            # Get all dishes in the course
            for (dishName, price) in self.menu[course].items():

                # Add the dish name to the list of dishes
                menuItems.append(dishName)

        # Return the list of dishes
        return menuItems


menuInstance = Menu()

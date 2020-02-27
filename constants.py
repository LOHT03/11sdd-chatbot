# Create a menu for customers to reference

from controller.types import CompleteMenu, MenuItem
from typing import Dict, List

menu: CompleteMenu = {
    "entrees": {
        "fairy bread": 3.00,
        "witchetty grub": 5.00
    },
    "main": {
        "kangaroo": 16.00,
        "meat pie": 7.00
    },
    "dessert": {
        "tim tam": 0.50,
        "pavlova": 4.00
    }
}

orders: Dict[str, Dict[int, List[MenuItem]]] = {
    "Jim": {
        1: [("prawns", 1.20), ("steak", 16.00)]
    }
}

# Create a menu for customers to reference

from controller.types import CompleteMenu, MenuItem
from typing import Dict, List

menu: CompleteMenu = {
    "starter": {
        "snails": 1.20,
        "prawns": 3.00
    },
    "main": {
        "steak": 16.00,
        "lasagna": 15.00
    },
    "dessert": {
        "cake": 6.00,
        "jelly": 4.00
    }
}

orders: Dict[str, Dict[int, List[MenuItem]]] = {
    "Jim": {
        1: [("prawns", 1.20), ("steak", 16.00)]
    }
}

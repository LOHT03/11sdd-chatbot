# Create a menu for customers to reference

from typing import Dict, List, Tuple

menu = {
    "starters": {
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

orders: Dict[str, Dict[int, List[Tuple[str, float]]]] = {
    "Jim": {
        1: [("prawns", 1.20), ("steak", 16.00)]
    }
}

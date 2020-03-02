from typing import Tuple, Dict, List
from terminaltables import AsciiTable


MenuItem = Tuple[str, float]
CompleteMenu = Dict[str, Dict[str, float]]
OrderHistory = Dict[int, List[MenuItem]]

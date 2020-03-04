from typing import Dict, List, Tuple


MenuItem = Tuple[str, float, int]
CompleteMenu = Dict[str, Dict[str, float]]
OrderHistory = Dict[str, List[MenuItem]]

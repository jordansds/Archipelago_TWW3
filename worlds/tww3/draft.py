from __future__ import annotations
from typing import TYPE_CHECKING
#if TYPE_CHECKING:
#    from .world import TWW3World

brt = {}

factionToItemTable: dict[str, list[dict]] = {
    "bretonnia": [brt],
    "carcassonne": [brt]
}


itemTables = factionToItemTable.get("itemTables")
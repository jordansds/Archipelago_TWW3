from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .world import TWW3World

def setVictoryEvent(world: TWW3World) -> None:
    world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory", world.player)
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .world import TWW3World
from BaseClasses import ItemClassification
import math
from worlds.generic.Rules import add_rule

def setVictoryEvent(world: TWW3World) -> None:
    world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory", world.player)

def setBalance(world: TWW3World) -> None:
    worldRegion = world.get_region("Old World")

    world.item_name_groups = {
        "Unlocks": set()
    }

    if world.options.balance:
        counter = 0
        for item in world.multiworld.itempool:
            if item.classification == ItemClassification.progression and item.name != "Administrative Capacity":
                world.item_name_groups["Unlocks"].add(item.name)
                counter += 1

        print(counter)

        for index, location in enumerate(worldRegion.locations):
            requiredUnlockItems = min(math.floor(index / (5 * world.options.checks_per_location)) * (world.options.checks_per_location * 5 * world.options.balance/100 - 1), counter)#len(world.item_name_groups["Unlocks"]))
            print(f"{location}: {requiredUnlockItems}")
            add_rule(location, lambda state, count=requiredUnlockItems: state.has_group("Unlocks", world.player, count))

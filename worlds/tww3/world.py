from typing import Dict, Any, Mapping, ClassVar
from worlds.AutoWorld import World
from BaseClasses import Region
from .options import TWW3Options
from .locations_table import settlements
import settings
from . import items, locations

#class TWW3Location(Location):  # or from Locations import MyGameLocation
#    game = "Total War Warhammer 3"  # name of the game/world this location is in

class TWW3Settings(settings.Group):
    class TWW3Path(settings.FolderPath):
        """Installation Path to the TWW3 folder, so that input and output files can be written."""
        description = "Total War Warhammer 3 Installation Folder. Where the .exe is."

    tww3_path: TWW3Path = TWW3Path("C:/Program Files (x86)/Steam/steamapps/common/Total War WARHAMMER III")

class TWW3World(World):
    """Insert description of the world/game here."""
    game = "Total War Warhammer 3"  # name of the game/world
    options_dataclass = TWW3Options  # options the player can set
    options: TWW3Options  # typing hints for option results
    settings: ClassVar[TWW3Settings]  # will be automatically assigned from type hint
    origin_region_name = "Old World"
    topology_present = False # show path to required location checks in spoiler
    
    item_list = []
    item_name_to_id = {data.name: item_id for item_id, data in items.item_table.items()}
    
    locations = [f"Empire Size {i} ({j})" for i in range(1,566) for j in range(10)]
    location_name_to_id = {k: v for v, k in enumerate(locations, start=1)}
    
    sm: settlements.Settlement_Manager = None
    
    def generate_early(self) -> None:
        self.player_faction = settlements.lord_name_to_faction_dict[self.options.starting_faction]
        self.sm: settlements.Settlement_Manager = settlements.Settlement_Manager(self.random)
        self.settlement_table, self.horde_table = self.sm.shuffle_settlements(self.player_faction, self.options.max_range) 

    def create_regions(self) -> None:
        
        worldRegion = Region("Old World", self.player, self.multiworld)
        self.multiworld.regions.append(worldRegion)
        
        locations.createAllLocations(self)

    def create_items(self) -> None:
        items.createAllItems(self)

    def fill_slot_data(self) -> Mapping[str, Any]:
        """
        Return the `slot_data` field that will be in the `Connected` network package.

        This is a way the generator can give custom data to the client.
        The client will receive this as JSON in the `Connected` response.

        :return: A dictionary to be sent to the client when it connects to the server.
        """
        slot_data: Dict = {}
        
        slot_data["PlayerFaction"] = self.options.starting_faction.value
        if self.options.tech_shuffle.value == True:
            slot_data["ProgressiveTechs"] = self.options.progressive_technologies.value
        else:
            slot_data["ProgressiveTechs"] = False
        if self.options.building_shuffle.value == True:
            slot_data["ProgressiveBuildings"] = self.options.progressive_buildings.value
        else:
            slot_data["ProgressiveBuildings"] = False
        if self.options.unit_shuffle.value == True:
            slot_data["ProgressiveUnits"] = self.options.progressive_units.value
        else:
            slot_data["ProgressiveUnits"] = False
        slot_data["StartingTier"] = self.options.starting_tier.value
        slot_data["RandomizePersonalities"] = self.options.RandomizePersonalities.value
        slot_data["RitualShuffle"] = self.options.ritual_shuffle.value
        slot_data["Settlements"] = self.settlement_table
        slot_data["Hordes"] = self.horde_table
        slot_data["FactionCapitals"] = self.sm.get_capital_dict()
        slot_data["Items"] = self.item_list
        slot_data["checksPerLocation"] = self.options.checks_per_location.value
        slot_data["numberOfLocations"] = self.options.number_of_locations.value

        return slot_data
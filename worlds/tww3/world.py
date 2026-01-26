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
        
        
        # Create Region
        """
        world_region = Region("Old World", self.player, self.multiworld)

        if self.options.balance == True:
            self.item_name_groups = {
                "Unlocks": set()
            }
            for item, value in self.item_table.items():
                if value.classification == ItemClassification.progression and value.faction == self.player_faction:
                    self.item_name_groups["Unlocks"].add(value.name)
                    
        
        
        # Check if player has a starting region. If they do, then skip the first few checks to prevent the game from fulfilling checks before game start.
        # If the player is really lucky and starts with more than 4 settlements, then they will still autocomplete some checks, but not as many.
        for faction in settlements.faction_table:
            if faction[0] == self.player_faction:
                if faction[2] == True:
                    startingCheck = 5
                else:
                    startingCheck = 1
        
        # Fill location checks based on number of locations and checks per location
        for i in range(startingCheck, self.options.number_of_locations + 1):
            
            locName = f"Empire Size {i}"
            
            if i != self.options.number_of_locations: # Generate all but last location, which is saved for the victory event
            
                for j in range(self.options.checks_per_location):
                    subLocName = f"{locName} ({j})"
                    locId = self.location_name_to_id[subLocName]

                    location = TWW3Location(self.player, subLocName, locId, world_region)
                    add_rule(location, lambda state, new_sum=(i-startingCheck): state.has_group("Unlocks", self.player, new_sum))
                    world_region.locations.append(location) 
                    
            else: # Add victory event in the last location
                location = TWW3Location(self.player, locName, None, world_region)
                add_rule(location, lambda state, new_sum=(i-startingCheck): state.has_group("Unlocks", self.player, new_sum))
                world_region.locations.append(location)  
                
                # Create Victory item and place it in the last location
                victory = items.TWW3Item("Victory", ItemClassification.progression, None, self.player)
                location.place_locked_item(victory)
                
                rules.setVictoryEvent(self)

        # Register region to multiworld
        self.multiworld.regions.append(world_region)
        self.location_amount = len(world_region.locations)
        """

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
# Map Loader / Manager - Mc_Snurtle
# imports
import json


class MapLoader:
    
    def __init__(self, map_name: str):
        
        with open(f'maps/{map_name}.json', 'r') as map:
            map_data = json.load(map)
            
        self.NIGHT = map_data.get("NIGHT", True)
        self.WIDTH = map_data.get("WIDTH", 0)
        self.HEIGHT = map_data.get("HEIGHT", 0)
        self.SPAWN = map_data.get("SPAWN")
        self.LAYOUT = map_data.get("MAP", [])


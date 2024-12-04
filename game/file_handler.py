import numpy as np
import json
import os

class FileHandler:
    """Singleton pattern for game configuration"""
    __instance = None
    
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance
    
    def save_game(self, controller, save_name: str):
        """Save game state to user file"""
        with open(f'save/{save_name}.json', 'w') as f:
            json.dump({
                "grid": controller.model.grid.tolist(),
                "paused": controller.paused
            }, f)
    
    def load_game(self, controller, save_name: str):
        """Load game state from user file"""
        if os.path.exists(f"save/{save_name}.json"):
            with open(f'save/{save_name}.json', 'r') as f:
                data = json.load(f)
                controller.paused = data["paused"]
                controller.model.grid = np.array(data["grid"])
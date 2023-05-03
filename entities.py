import base64
from pathlib import Path
from PIL import Image, ImageOps
import PIL
from io import BytesIO

class PlayerTurn:
    def __init__(self, action: str):
        self.action: str = action

class Player:
    def __init__(self, identifier: str, description: str, items: str, objective: str, starting_location: str):
        self.identifier: str = identifier
        self.description: str = description
        self.objective: str = objective
        self.location: str = starting_location
        self.items: list[str] = []
        for item in items.split("\n"):
            item = item.strip()
            item.replace("  ", " ")
            if item == "":
                continue
            if item[0] == "-":
                item = item[1:].strip()
            if item[-1] == ".":
                item = item[:-1].strip()
            if item == "":
                continue
            self.items.append(item)
        self.health: int = 100
        self.max_health: int = 100

        self.turn_history: list[PlayerTurn] = []

    def play_action(self, action: str):
        self.turn_history.append(PlayerTurn(action))

    def __str__(self):
        return f"{self.identifier} at {self.location} with {self.health} HP"

    def __repr__(self):
        return f"{self.identifier} at {self.location} with {self.health} HP"

class DungeonMasterTurn:
    def __init__(self, action: str):
        self.action: str = action

class DungeonMaster:
    def __init__(self, player_first_text: str, world_description: str, player: Player, quest_story: str):
        self.history: list[str] = []
        self.player_history: list[DungeonMasterTurn] = []

        self.player_history.append(DungeonMasterTurn(player_first_text))

        self.player_summaries: list[str] = [f"Starts in location '{player.location}'"]

        self.world_description: str = world_description

        self.quest_story: str = quest_story

    def player_result(self, action: str):
        self.player_history.append(DungeonMasterTurn(action))

    def player_summary_result(self, summary: str):
        self.player_summaries.append(summary)

    def __str__(self):
        return f"Dungeon Master"

    def __repr__(self):
        return f"Dungeon Master"

class World:
    def __init__(self, world_description: str):
        self.description: str = world_description



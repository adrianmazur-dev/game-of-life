from abc import ABC, abstractmethod
from game.file_handler import FileHandler

class Command(ABC):
    def __init__(self, controller):
        self.controller = controller

    @abstractmethod
    def execute(self):
        pass

class NextGenerationCommand(Command):
    def execute(self):
        self.controller.model.next_generation()

class TogglePauseCommand(Command):
    def execute(self):
        self.controller.paused = not self.controller.paused

class SaveGameCommand(Command):
    def __init__(self, controller, save_name: str):
        super().__init__(controller)
        self.save_name = save_name

    def execute(self):
        FileHandler().save_game(self.controller, self.save_name)

class LoadGameCommand(Command):
    def __init__(self, controller, save_name: str):
        super().__init__(controller)
        self.save_name = save_name

    def execute(self):
        FileHandler().load_game(self.controller, self.save_name)
        self.controller.model.notify()

class ClearGridCommand(Command):
    def execute(self):
        self.controller.model.grid.fill(0)
        self.controller.model.notify()
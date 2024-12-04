import time
import pygame
from typing import Dict
from game.command import Command
from game.view import GameView
from game.model import GameModel

class GameController:
    def __init__(self, model: GameModel, view: GameView, ):
        self.model = model
        self.view = view
        self.paused = True
        self.last_update = 0

        self.commands: Dict[str, Command] = {}
        self.model.attach(view)

    def register_command(self, name: str, command: Command):
        self.commands[name] = command

    def execute_command(self, name: str):
        if name in self.commands:
            self.commands[name].execute()

    def _handle_input(self) -> bool:
        mouse_buttons = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                button_handled = False
                for button in self.view._buttons:
                    if button.is_hovered(event.pos):
                        self.execute_command(button.command_name)
                        button_handled = True
                        break
                if button_handled:
                    break

            if (event.type == pygame.MOUSEMOTION and mouse_buttons[0]) or (event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_just_pressed()[0]):
                self._handle_mouse_drag(event.pos, True)

            if (event.type == pygame.MOUSEMOTION and mouse_buttons[2]) or (event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_just_pressed()[2]):
                self._handle_mouse_drag(event.pos, False)

        return True

    def _handle_mouse_drag(self, pos, draw_alive: bool):
        x = pos[0] // self.view.cell_width
        y = pos[1] // self.view.cell_height
        if 0 <= x < self.model.grid.shape[0] and 0 <= y < self.model.grid.shape[1]:
            self.model.grid[x, y] = draw_alive
            self.model.notify()

    def run(self):
        """Main loop"""
        running = True
        self.view.update(self.model)
        while running:
            running = self._handle_input()

            current_time = time.time() * 1000
            if (not self.paused and current_time - self.last_update) >= self.model.config.tick_interval:
                self.execute_command("next")
                self.last_update = current_time
        
        pygame.quit()
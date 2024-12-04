import pygame
from typing import List
from game.model import GameModel, Observer, Subject
from game.config import Config

class GameView(Observer):
    def __init__(self, config: Config):
        self.config = config
        self.screen = pygame.display.set_mode((config.width, config.height))
        self.cell_width = config.width // config.n_cells_x
        self.cell_height = config.height // config.n_cells_y
        self._buttons: List[Button] = []

    def _draw_frame(self, model: GameModel):
        self.screen.fill(self.config.colors['white'])
        self._draw_grid()
        self._draw_alive_cells(model)
        self._draw_buttons()
        pygame.display.flip()

    def _draw_grid(self):
        for top in range(0, self.config.height, self.cell_height):
            for left in range(0, self.config.width, self.cell_width):
                cell = pygame.Rect(left, top, self.cell_width, self.cell_height)
                pygame.draw.rect(self.screen, self.config.colors['gray'], cell, 1)

    def _draw_alive_cells(self, model: GameModel):
        for top in range(self.config.n_cells_y):
            for left in range(self.config.n_cells_x):
                if model.grid[left, top] == 1:
                    cell = pygame.Rect(left * self.cell_width, top * self.cell_height, self.cell_width, self.cell_height)
                    pygame.draw.rect(self.screen, self.config.colors['black'], cell)

    def _draw_buttons(self):
        for button in self._buttons:
            button.draw(self.screen, self.config.colors["green"], self.config.colors["black"])

    def add_button(self, button: 'Button'):
        self._buttons.append(button)

    def update(self, subject: Subject):
        self._draw_frame(subject)


class Button():
    def __init__(self, left: int, top: int, width: int, height: int, name: str, command_name: str):
        self.rect = pygame.Rect(left, top, width, height)
        self.name = name
        self.command_name = command_name

    def draw(self, screen: pygame.Surface, color: tuple, font_color: tuple):
        pygame.draw.rect(screen, color, self.rect)
        text = pygame.font.Font().render(self.name, True, font_color)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def is_hovered(self, pos) -> bool:
        return self.rect.collidepoint(pos)
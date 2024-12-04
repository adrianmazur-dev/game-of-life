import pygame
import game.command as Command
from game.model import GameModel
from game.view import GameView, Button
from game.config import Config
from game.controller import GameController

def main():
    pygame.init()

    config = Config()
    model = GameModel(config)
    view = GameView(config)

    controller = GameController(model, view)
    controller.register_command("next", Command.NextGenerationCommand(controller))
    controller.register_command("toggle", Command.TogglePauseCommand(controller))
    controller.register_command("save_to_user_state", Command.SaveGameCommand(controller, 'user_state'))
    controller.register_command("load_user_save", Command.LoadGameCommand(controller, 'user_state'))
    controller.register_command("clear_grid", Command.ClearGridCommand(controller))

    controller.register_command("load_map_1", Command.LoadGameCommand(controller, 'map_1'))
    controller.register_command("load_map_2", Command.LoadGameCommand(controller, 'map_2'))

    view.add_button(Button(config.ui_padding + (config.button_width + config.ui_padding) * 0, config.ui_padding, config.button_width, config.button_height, "Next", "next"))
    view.add_button(Button(config.ui_padding + (config.button_width + config.ui_padding) * 1, config.ui_padding, config.button_width, config.button_height, "Toggle", "toggle"))
    view.add_button(Button(config.ui_padding + (config.button_width + config.ui_padding) * 2, config.ui_padding, config.button_width, config.button_height, "Save", "save_to_user_state"))
    view.add_button(Button(config.ui_padding + (config.button_width + config.ui_padding) * 3, config.ui_padding, config.button_width, config.button_height, "Load my save", "load_user_save"))
    
    view.add_button(Button(config.ui_padding, (config.height - (config.ui_padding + config.button_height) * 1), config.button_width, config.button_height, "Clear", "clear_grid"))
    view.add_button(Button(config.ui_padding, (config.height - (config.ui_padding + config.button_height) * 2), config.button_width, config.button_height, "Map 1", "load_map_1"))
    view.add_button(Button(config.ui_padding, (config.height - (config.ui_padding + config.button_height) * 3), config.button_width, config.button_height, "Map 2", "load_map_2"))

    controller.run()

main()
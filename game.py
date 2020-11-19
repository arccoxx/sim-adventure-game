# Import external libraries.
import random
import os
import pygame
import pygame_gui

from collections import deque

# Import Pygame GUI elements directly for ease of access.
from pygame_gui import UIManager, PackageResource
from pygame_gui.elements import UIWindow
from pygame_gui.elements import UITextEntryLine
from pygame_gui.elements import UITextBox
from pygame_gui.windows import UIMessageWindow

# Import the rest of our code.
import utilities
import config
import commands
import player
import scenes

# Load the player's save file and retrieve their save data.
save = utilities.Save()

# Create a player object using the player's save data.
player_data = player.Player()

# We'll use this empty string later to store our response history.
response_history = ""

# Check to see if the player is in a scripted sequence.
if player_data.scene is not None: # If they are, give them a response based upon their current scene.
    if player_data.scene == config.scene_id_newgame:
        response = scenes.Introduction(None)
        response_history += response
else: # If they aren't, give them a generic response.
    response = "Welcome back, {}. You are still {:,} slimes in debt.<br><br>What would you like to do now?".format(
        player_data.name, player_data.debt)
    response_history += response

class Window(UIWindow):
    def __init__(self, rect, ui_manager):
        super().__init__(rect, ui_manager)

        self.text_block = UITextBox(response, pygame.Rect((25, 25), (845, 380)), self.ui_manager, container = self)

        self.text_entry = UITextEntryLine(pygame.Rect((50, 550), (700, 50)), self.ui_manager, container = self)

class Options:
    def __init__(self):
        self.resolution = (800, 600)

class Game:
    def __init__(self):
        # Start up Pygame.
        pygame.init()

        # Title the window our game runs in.
        pygame.display.set_caption(config.game_name)
        
        self.options = Options()
        
        # Define the dimensions of our game's window.
        self.window_surface = pygame.display.set_mode(self.options.resolution)
        self.window_surface.blit(pygame.image.load("media/images/background.png"), (0, 0))

        self.background_surface = None

        self.ui_manager = UIManager(self.options.resolution, PackageResource(package='media.themes', resource='theme.json'))

        self.text_block = None
        self.text_entry = None

        self.message_window = None

        self.recreate_ui()

        self.clock = pygame.time.Clock()
        self.time_delta_stack = deque([])
        self.running = True

    def recreate_ui(self):
        self.ui_manager.set_window_resolution(self.options.resolution)
        self.ui_manager.clear_and_reset()

        self.background_surface = pygame.Surface(self.options.resolution)
        self.background_surface.fill(self.ui_manager.get_theme().get_colour('dark_bg'))
        self.background_surface.blit(pygame.image.load("media/images/background.png"), (0, 0))

        self.text_entry = UITextEntryLine(pygame.Rect((50, 550), (700, 50)), self.ui_manager, object_id = "#text_entry")
        self.text_block = UITextBox(response, pygame.Rect((50, 25), (700, 500)), self.ui_manager, object_id = "#text_block")


    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            self.ui_manager.process_events(event)            

            if event.type == pygame.USEREVENT:
                if (event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == '#text_entry'):
                    # Turn the user's input into a string.
                    message = event.text

                    # Begin the response message. Start with repeating the user's input.
                    response = "<b><i>> {message}</i></b>".format(message = message)

                    # Create a player object using the player's save data.
                    player_data = player.Player()

                    # Check to see if the player is in a scripted sequence.
                    if player_data.scene is not None: # If they are...
                        if player_data.scene == config.scene_id_newgame: # If the player has started the game for the first time.
                            response += ("<br>" * 4) + scenes.Introduction(message)
                    else: # If they aren't...
                        response += ("<br>" * 4) + utilities.parse_message(message)

                    # End the response with some decoration. ^_^
                    response += ("<br>" * 4) + ("-" * 20) + ("<br>" * 4)

                    # Add this response to our response history, and then send the entire history to be rendered.
                    global response_history
                    response += response_history
                    response_history = response

                    # Render the response.
                    self.text_block = UITextBox(response, pygame.Rect((50, 25), (700, 500)), self.ui_manager, object_id = "#text_block")

    def run(self):
        while self.running:
            time_delta = self.clock.tick() / 1000
            
            # Check for inputs from the player.
            self.process_events()

            # Respond to inputs.
            self.ui_manager.update(time_delta)

            # Draw the graphics.
            self.window_surface.blit(self.background_surface, (0, 0))
            self.ui_manager.draw_ui(self.window_surface)

            pygame.display.update()

# Start the game.
if __name__ == '__main__':
    app = Game()
    app.run()
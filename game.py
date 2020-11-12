#!/usr/bin/python3

# This is a simple text adventure game made by the SIM Technology Group.

# Import external libraries.
import pygame_gui
from pygame.locals import *
import pygame
import os
import json
import pygame

# Import the rest of our code.
import utilities
import config
import commands
import player
import scenes

# Begin interpreting the code.
print("Loading...")

# Starts the game, and begins the infinite loop of asking for inputs and sending responses.
pygame.init()
pygame.display.set_caption(config.game_name)
os.environ['SDL_VIDEO_CENTERED'] = '1'



clock = pygame.time.Clock()

save = utilities.Save()

output = None

# Load the player's save file and retrieve their data.
player_data = player.Player()

if player_data.scene is not None:
    if player_data.scene == config.scene_id_newgame:
        response = scenes.Introduction(None)
        output = utilities.generate_output(response)
        output_text = response
else:
    response = "Welcome back, {}. You are still {:,} slimes in debt.<br><br>What would you like to do now?".format(
        player_data.name, player_data.debt)
    output = utilities.generate_output(response)
    output_text = response

running = True

while running:
    frameTime = clock.tick(60)
    time_delta = frameTime / 1000.0

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        utilities.ui_manager.process_events(event)

        utilities.generate_command_line()

        if event.type == USEREVENT:
            if event.user_type == "ui_text_entry_finished":
                # Turn the user's input into a string.
                message = event.text

                # Begin creating the response message. Render all previous inputs and responses before moving on to the current set.
                response = "<i>> " + message + "</i>"

                # Loads the player's save file and retrieve their data.
                player_data = player.Player()

                # If the player is currently within a scripted sequence.
                if player_data.scene is not None:
                    # If the player has started the game for the first time.
                    if player_data.scene == config.scene_id_newgame:
                        response += "<br><br>" + \
                            scenes.Introduction(message)

                # If the player is the open game.
                else:
                    response += "<br><br>" + \
                        utilities.parse_message(message)

                response += "<br><br>" + ("-" * 200) + "<br><br>" + output_text

                # Delete the previously rendered text.
                output.kill()
                # Output the new response (which contains all the previous inputs and responses).
                output = utilities.generate_output(response)
                # Save what we just output as a string for the next loop.
                output_text = response

    utilities.ui_manager.update(time_delta)
    # Draw the background.
    utilities.screen.blit(pygame.image.load("assets/background.png"), (0, 0))

    utilities.ui_manager.draw_ui(utilities.screen)

    pygame.display.flip()  # flip all our drawn stuff onto the scree

pygame.quit()  # exited game loop so quit pygame

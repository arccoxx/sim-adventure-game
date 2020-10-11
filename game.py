#!/usr/bin/python3

# This is a simple text adventure game made by the SIM Technology Group.

# Begin interpreting the code.
print("Loading...")

# Import external libraries.
import asyncio
import json

# Import the rest of our code.
import utilities
import config
import commands
import player

# Starts the game, and begins the infinite loop of asking for inputs and sending responses.
async def start_game():
    on_load = "Done! {game_name} has now loaded. Currently running version {version}.".format(game_name = config.game_name, version = config.game_version)
    on_load += "\n" + ("=" * 10) + "\n"
    print(on_load)

    # Return a Player object, either using a default template or using data retireved from a save file.
    player_data = player.Player()

    # If no save file was found, or no data could be retireved.
    if player_data.new_game is True:
        # Print out a brief introduction.
        print("Welcome to the world of {game_name}!".format(game_name = config.game_name))

        # Ask for the player's character name.
        player_name = input("What is your name?" + "\n>")

        # Save the new data to the save file.
        player_data.name = player_name
        player_data.persist()
        
        # Provide feedback to the player.
        print("Greetings, {name}. A new save file has been created for you.".format(name = player_data.name))

    # If a save file was found, and the data was retrieved.
    else:
        # Provide feedback to the player.
        print("Welcome back to {game_name}, {name}! Your save file has been loaded.".format(game_name = config.game_name, name = player_data.name))
    
    # Provide the inital prompt that will begin the infinite loop of asking for inputs and sending responses.
    inital_prompt = "\nWhat will you do now?"
    
    await utilities.send_message(inital_prompt + "\n>")

# After everything is loaded, start the game.
asyncio.run(start_game())
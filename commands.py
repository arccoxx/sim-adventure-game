# Import external libraries.
import random

# Import other parts of our code.
import utilities
import player
import config

# Class to send general data about an interaction to a command.
class Command:
    command = ""
    tokens = []
    tokens_count = 0
    message = None


    def __init__(
        self,
        tokens = [],
        message = None,
    ):
        self.tokens = tokens
        self.message = message

        if len(tokens) >= 1:
            self.tokens_count = len(tokens)
            self.command = tokens[0]

# Gives a brief overview of information about the game.
async def help(cmd):
    response = "This game was created by the Interrelated Technology Group."

    await utilities.send_message(utilities.format_message(response))

async def debug(cmd):
    response = "Hello!"

    await utilities.send_message(utilities.format_message(response))

# Mine for slime in The Mines!
async def mine(cmd):
    player_data = player.Player()

    # Checks to see if the player is in the right location.
    if player_data.location == config.location_mines:
        # Select a random number from 1 to 100 to provide the user with.
        mine_yield = random.randint(1, 100)

        # Add the slime to the player's slimes.
        player_data.slimes += mine_yield
        player_data.persist()

        response = "You mined {mine_yield} slime!".format(mine_yield = mine_yield)
    
    else:
        response = config.text_invalid_location.format(location_name = config.location_mines)

    await utilities.send_message(utilities.format_message(response))

# Returns all of the data from your save file.
async def data(cmd):
    player_data = player.Player()
    
    response = "You name is {name}. ".format(name = player_data.name)
    response += "You stand in {location}. ".format(location = player_data.location)
    response += "You currently have {slimes} slimes. ".format(slimes = player_data.slimes)

    await utilities.send_message(utilities.format_message(response))

# Ends the game.
async def exit(cmd):
    print("\n" + "Goodbye.")
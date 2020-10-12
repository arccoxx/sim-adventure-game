# Import external libraries.
import random
import time
import asyncio

# Import other parts of our code.
import utilities
import player
import config
import map

move_counter = 0

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
    # Get the player's data.
    player_data = player.Player()

    # Checks to see if the player is in the right location.
    if player_data.location == config.location_id_the_mines:
        # Select a random number from 1 to 100 to provide the user with.
        mine_yield = random.randint(1, 100)

        # Add the slime to the player's slimes.
        player_data.slimes += mine_yield
        player_data.persist()

        response = "You mined {mine_yield} slime!".format(mine_yield = mine_yield)
    
    else:
        required_location = config.id_to_location.get(config.location_id_the_mines)
        response = config.text_invalid_location.format(location_name = required_location.name)

    await utilities.send_message(utilities.format_message(response))

# Returns all of the data from your save file.
async def data(cmd):
    # Get the player's data.
    player_data = player.Player()
    
    response = "You name is {name}. ".format(name = player_data.name)
    
    # Match the current location identifier found in the player's data to a Location object using the id_to_location array in the config file, then store it here.
    current_location = config.id_to_location.get(player_data.location)
    response += "You stand in {location}. ".format(location = current_location.name)

    response += "You currently have {slimes} slimes. ".format(slimes = player_data.slimes)

    await utilities.send_message(utilities.format_message(response))

# Look around at your surroundings.
async def look(cmd):
    # Get the player's data.
    player_data = player.Player()
    
    # Match the current location identifier found in the player's data to a Location object using the id_to_location array in the config file, then store it here.
    location = config.id_to_location.get(player_data.location)

    response = "You stand in {location_name}.\n{location_description}".format(location_name = location.name, location_description = location.description)

    if location.neighbors is not None:
        response += "\n{location_name} is connected to:".format(location_name = location.name)
        for neighbor in location.neighbors:
            neighbor_location = config.id_to_location.get(neighbor)
            response += "\n{neighbor_name}".format(neighbor_name = neighbor_location.name)

    await utilities.send_message(utilities.format_message(response))

# Ends the game.
async def exit(cmd):
    print("\n" + "Goodbye.")

# Move around the map.
async def move(cmd):
    # Whatever the player inputs after the move command itself.    
    target = utilities.flattenTokens(cmd.tokens[1:])
    
    # If the player doesn't input anything after the move command.
    if target == None or len(target) == 0:
        response = "Where do you want to go to?"
        await utilities.send_message(utilities.format_message(response))
    
    # Get the player's data.
    player_data = player.Player()
    
    # Match the current location identifier found in the player's data to a Location object using the id_to_location array in the config file, then store it here.
    current_location = config.id_to_location.get(player_data.location)
    # Do the same thing for the target location.
    target_location = config.id_to_location.get(target)

    # If the target location identifier can't be matched to a Location object in the id_to_location array.
    if target_location == None:
        response = "That is not a valid location."
        await utilities.send_message(utilities.format_message(response))

    # If you are already in your target location.
    if target_location.id == player_data.location:
        response = "You are already there."
        await utilities.send_message(utilities.format_message(response))

    # If your location has no neighbors, or if your target location has no neighbors.
    if len(current_location.neighbors.keys()) == 0 or len(target_location.neighbors.keys()) == 0:
        response = "You don't know how to get there."
        await utilities.send_message(utilities.format_message(response))

    else:
        # Plot a course towards your target location.
        path = map.path_to(location_start = current_location.id, location_end = target_location.id, player_data = player_data)
    
        # Display how long it will take to reach the target location, in seconds.
        response_move_eta = "It's about {seconds} seconds away.".format(seconds = path.cost % 60)

        # Give feedback to the player.
        await utilities.send_message("\n" + "You begin walking to {target_location}.".format(target_location = target_location.name) + " " + response_move_eta, new_prompt = False)
        
        
        # List all of the steps on the path to the target location.
        step_list = []
        for step in path.steps:
            step_list.append(step.name)

        # Move to the target location.
        for move in range(1, len(path.steps)):
            # Define the current step.
            step = path.steps[move]

            # Sleep for the travel time inbetween the player's current location and their next location.
            travel_time = current_location.neighbors.get(step.id)
            await asyncio.sleep(travel_time)
            
            # Define the current location as the previously upcoming location.
            current_location = step
            
            # Get the player's data, again, just in case anything changed.
            player_data = player.Player()
            
            # If the player is in a new location.
            if player_data.location != current_location.id:
                # Define the player's current location as their new location.
                player_data.location = current_location.id
                player_data.persist()

                # If the player has entered their target location.
                if player_data.location == target_location.id:
                    await utilities.send_message(utilities.format_message("You enter {current_location}.".format(current_location = current_location.name)))
                    break
                
                # If the player has entered an area on their way to their target location.
                else:
                    # Prompt the user if they would like to stop walking to their target location and explore their current location. Then, flatten the input.
                    prompt_stop = input(utilities.format_message("You enter {current_location} on your way to {target_location}. Do you want to stop walking to {target_location} and explore here?".format(current_location = current_location.name, target_location = target_location.name)))                 
                    
                    # If they accept the prompt to stop walking, break the loop.
                    if utilities.flattenTokens(prompt_stop) in config.accept_inputs:
                        await utilities.send_message(utilities.format_message("You stop in {current_location}.".format(current_location = current_location.name)))
                        break

                    # If they decide to keep walking, continue the loop.
                    else:
                        await utilities.send_message("\n" + "You continue walking to {target_location}".format(target_location = target_location.name), new_prompt = False)

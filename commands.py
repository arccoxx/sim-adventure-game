# Import external libraries.
import random
import time
import pygame

# Import other parts of our code.
import utilities
import player
import config
import map
import item

move_counter = 0

# Class to send general data about an interaction to a command.


class Command:
    command = ""
    tokens = []
    tokens_count = 0
    message = None

    def __init__(
        self,
        tokens=[],
        message=None,
    ):
        self.tokens = tokens
        self.message = message

        if len(tokens) >= 1:
            self.tokens_count = len(tokens)
            self.command = tokens[0]

def debug(cmd):
    response = "Hello!"

    return response

# Gives a brief overview of information about the game.
def help(cmd):
    response = "This game was created by the Interrelated Technology Group."

    return response

# Mine for slime in The Mines!
def mine(cmd):
    # Get the player's data.
    player_data = player.Player()

    # Checks to see if the player is in the right location.
    if player_data.location == config.location_id_the_mines:
        if player_data.hunger < 100:
            # Select a random number from 1 to 100 to provide the user with.
            mine_yield = random.randint(1, 100)

            # Add the slime to the player's slimes.
            player_data.slimes += mine_yield
            player_data.hunger += 5
            player_data.persist()

            response = "You mined {mine_yield} slime!".format(
                mine_yield=mine_yield)
            
            mine_sound = pygame.mixer.Sound("assets/mine.wav")
            pygame.mixer.Sound.play(mine_sound)
        else:
            response = "You're too hungry to mine any more slime! You'll have to eat something..."

    else:
        required_location = config.id_to_location.get(
            config.location_id_the_mines)
        response = config.text_invalid_location.format(
            location_name=required_location.name)

    return response

# Returns all of the data from your save file.
def data(cmd):
    # Get the player's data.
    player_data = player.Player()

    response = "You name is {name}. ".format(name=player_data.name)

    # Match the current location identifier found in the player's data to a Location object using the id_to_location array in the config file, then store it here.
    current_location = config.id_to_location.get(player_data.location)
    response += "You stand in {location}. ".format(
        location=current_location.name)

    response += "You currently have {slimes} slimes. ".format(
        slimes=player_data.slimes)

    return response

# Look around at your surroundings.
def look(cmd):
    # Get the player's data.
    player_data = player.Player()

    # Match the current location identifier found in the player's data to a Location object using the id_to_location array in the config file, then store it here.
    location = config.id_to_location.get(player_data.location)

    response = "You stand in {location_name}.<br>{location_description}".format(
        location_name=location.name, location_description=location.description)

    if location.neighbors is not None:
        response += "<br><br>{location_name} is connected to:".format(
            location_name=location.name)
        for neighbor in location.neighbors:
            neighbor_location = config.id_to_location.get(neighbor)
            response += "<br>{neighbor_name}".format(
                neighbor_name=neighbor_location.name)

    return response

#Move around the map.
def move(cmd):
    # Temporarily disable move command.
    response = "This command is temporarily disabled! To change your location, open up your save.json in any text editor and change your 'location' to your desired destination. Hit save, then use the look command to confirm you've moved."
    return response
    
    # # Whatever the player inputs after the move command itself.
    # target = utilities.flattenTokens(cmd.tokens[1:])

    # # If the player doesn't input anything after the move command.
    # if target == None or len(target) == 0:
    #     response = "Where do you want to go to?"
    #     return response

    # # Get the player's data.
    # player_data = player.Player()

    # # Match the current location identifier found in the player's data to a Location object using the id_to_location array in the config file, then store it here.
    # current_location = config.id_to_location.get(player_data.location)
    # # Do the same thing for the target location.
    # target_location = config.id_to_location.get(target)

    # # If the target location identifier can't be matched to a Location object in the id_to_location array.
    # if target_location == None:
    #     response = "That is not a valid location."
    #     return response

    # # If you are already in your target location.
    # if target_location.id == player_data.location:
    #     response = "You are already there."
    #     return response

    # # If your location has no neighbors, or if your target location has no neighbors.
    # if len(current_location.neighbors.keys()) == 0 or len(target_location.neighbors.keys()) == 0:
    #     response = "You don't know how to get there."
    #     return response

    # else:
    #     # Plot a course towards your target location.
    #     path = map.path_to(location_start=current_location.id,
    #                        location_end=target_location.id, player_data=player_data)

    #     # Display how long it will take to reach the target location, in seconds.
    #     response_move_eta = "It's about {seconds} seconds away.".format(
    #         seconds=path.cost % 60)

    #     # Give feedback to the player.
    #     await utilities.send_message("\n" + "You begin walking to {target_location}.".format(target_location=target_location.name) + " " + response_move_eta, new_prompt=False)

    #     # List all of the steps on the path to the target location.
    #     step_list = []
    #     for step in path.steps:
    #         step_list.append(step.name)

    #     # Move to the target location.
    #     for move in range(1, len(path.steps)):
    #         # Define the current step.
    #         step = path.steps[move]

    #         # Sleep for the travel time inbetween the player's current location and their next location.
    #         travel_time = current_location.neighbors.get(step.id)
    #         await asyncio.sleep(travel_time)

    #         # Define the current location as the previously upcoming location.
    #         current_location = step

    #         # Get the player's data, again, just in case anything changed.
    #         player_data = player.Player()

    #         # If the player is in a new location.
    #         if player_data.location != current_location.id:
    #             # Define the player's current location as their new location.
    #             player_data.location = current_location.id
    #             player_data.persist()

    #             # If the player has entered their target location.
    #             if player_data.location == target_location.id:
    #                 await utilities.send_message(utilities.format_message("You enter {current_location}.".format(current_location=current_location.name)))
    #                 break

    #             # If the player has entered an area on their way to their target location.
    #             else:
    #                 # Prompt the user if they would like to stop walking to their target location and explore their current location. Then, flatten the input.
    #                 prompt_stop = input(utilities.format_message("You enter {current_location} on your way to {target_location}. Do you want to stop walking to {target_location} and explore here?".format(
    #                     current_location=current_location.name, target_location=target_location.name)))

    #                 # If they accept the prompt to stop walking, break the loop.
    #                 if utilities.flattenTokens(prompt_stop) in config.accept_inputs:
    #                     await utilities.send_message(utilities.format_message("You stop in {current_location}.".format(current_location=current_location.name)))
    #                     break

    #                 # If they decide to keep walking, continue the loop.
    #                 else:
    #                     await utilities.send_message("\n" + "You continue walking to {target_location}".format(target_location=target_location.name), new_prompt=False)

# Order an item.
def order(cmd):
    # Whatever the player inputs after the move command itself.
    target = utilities.flattenTokens(cmd.tokens[1:])

    # If the player doesn't input anything after the order command.
    if target == None or len(target) == 0:
        response = "What do you want to order?"
        return response

    # Match the desired order to an Item object using the item_map array in the config file, then store it here.
    desired_order = config.item_map.get(target)

    # If the desired order identifier can't be matched to an Item object in the item_map array.
    if desired_order == None:
        response = "That is not a valid item."
        return response
    else:
        # Check to see if the player can buy the found item.
        if desired_order.value is not None and desired_order.vendor is not None:
            # Get the player's data.
            player_data = player.Player()

            # If the player is in the location of the vendor selling the item.
            if desired_order.vendor != player_data.location:
                response = "You cannot buy that item here."
                return response

            # If the player does not have enough slime to buy the desired order.
            if desired_order.value > player_data.slimes:
                response = "You do not have enough slime to order this item! A {order} costs {price}, and you only have {slimes}!".format(order = desired_order.name, price = desired_order.value, slimes = player_data.slimes) 
                return response
            else:
                # Spend the slime necessary to buy the item.
                player_data.slimes -= desired_order.value
                player_data.persist()
                
                # Actually create the item.
                item.create_item(desired_order)

                response = "You order a {item}!".format(item = desired_order.name, description = desired_order.description)
                return response

# Eat something.
def eat(cmd):
    # Whatever the player inputs after the move command itself.
    target = utilities.flattenTokens(cmd.tokens[1:])

    # If the player doesn't input anything after the eat command.
    if target == None or len(target) == 0:
        response = "What do you want to eat?"
        return response

    # Search through the player's inventory for the sought item.
    sought_item = item.search_for_item(target)

    # If we don't find the item in the player's inventory.
    if sought_item == None:
        response = "You don't have one of those."
        return response
    
    # If the player can eat the item.
    if sought_item.satiation == None:
        response = "You can't eat that!"
        return response
    else:
        # Get the player's data.
        player_data = player.Player()
        player_data.hunger -= sought_item.satiation 
        player_data.persist()

        # Eat the item.
        item.delete_item(target)
        response = "You chomp into the {item}! {description}".format(item = sought_item.name, description = sought_item.description)
        return response
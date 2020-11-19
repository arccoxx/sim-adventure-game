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
from item import get_inventory

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
    if player_data.location == config.location_id_mines:
        has_pickaxe = item.search_for_item(sought_item = "pickaxe")

        if has_pickaxe is None:
            desired_order = config.item_map.get("pickaxe")
            item.create_item(desired_order)

            response = "But, you have no pickaxe! Luckily, there's a spare on the floor. You pick it up, and can now mine."
            return response

        if player_data.hunger < 100:
            has_pickaxe.durability -= 1

            pickaxe_broken = False
            if has_pickaxe.durability <= 0:
                pickaxe_broken = True
                item.delete_item(has_pickaxe.id)
            else:
                item.edit_item(sought_item=has_pickaxe.id, property="durability", new_value=has_pickaxe.durability)

            # Select a random number from 1 to 100 to provide the user with.
            mine_yield = random.randint(1, 100)

            # Add the slime to the player's slimes.
            player_data.slimes += mine_yield
            player_data.hunger += 5
            player_data.persist()

            response = "You mined {mine_yield} slime!".format(
                mine_yield=mine_yield)
            
            if pickaxe_broken:
                response += "<br>But your pickaxe broke!"
            
            mine_sound = pygame.mixer.Sound("assets/mine.wav")
            pygame.mixer.Sound.play(mine_sound)
        else:
            response = "You're too hungry to mine any more slime! You'll have to eat something..."

    else:
        required_location = config.id_to_location.get(
            config.location_id_mines)
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

# Move around the world.
def move(cmd):
    # Define this variable as the first token the player input after the command itself.
    target = utilities.flattenTokens(cmd.tokens[1:])

    # If the player didn't input anything after the command.
    if target == None or len(target) == 0:
        response = "Where do you want to go to?"
        return response

    # Get the player's data.
    player_data = player.Player()

    # Match the current location identifier found in the player's data to a Location object using the id_to_location array in the config file, then store it here.
    current_location = config.id_to_location.get(player_data.location)
    # Do the same thing for the "target" variable, which we will assume is a location.
    target_location = config.id_to_location.get(target)

    # If the target location identifier can't be matched to a Location object in the id_to_location array.
    if target_location == None:
        response = "That is not a valid location."
        return response

    # If you are already in your target location.
    if target_location.id == player_data.location:
        response = "You are already there."
        return response

    # If your current location has no neighbors, or if your target location has no neighbors, or if your target location is not a neighborhood of your current location.
    if len(current_location.neighbors.keys()) == 0 or len(target_location.neighbors.keys()) == 0 or target_location.id not in current_location.neighbors.keys():
        response = "You don't know how to get there from here."
        return response

    else:
        # Change the player's current location to their target location.
        player_data.location = target_location.id
        player_data.persist()

        response = "You enter {current_location}.".format(current_location=target_location.name)
        return response

# Order an item.
def menu(cmd):
    player_data = player.Player()

    current_location = config.id_to_location.get(player_data.location)

    list_of_items_for_sale = []

    for item in config.item_list:
        if item.vendor == current_location.id:
            item_listing = "<b>{}</b>: {} slimes<br>".format(item.name, item.value)
            list_of_items_for_sale.append(item_listing)
        else:
            pass
        
    if len(list_of_items_for_sale) == 0:
        response = "There are no items for sale here."
        return response
    else:
        nice_list_of_items_for_sale = utilities.format_nice_list(list_of_items_for_sale)

        response = "There are the following items for sale:<br>{}".format(nice_list_of_items_for_sale)
        return response


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
def inventory(cmd):
    inventory = get_inventory()

    if inventory == None or len(inventory) == 0:
        response = "You aren't holding any items."
        return response

    response = "You are holding the following items:<br>"

    for item in inventory:
        response += "{}<br>".format(inventory[item]['name'])
    
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

# Deposit some slime into your loan shark's bank account.
def deposit(cmd):
    # Get the player's data.
    player_data = player.Player()

    if player_data.location != config.location_id_loan_agency:
        required_location = config.id_to_location.get(config.location_id_loan_agency)

        response = config.text_invalid_location.format(location_name=required_location.name)
        return response
    
    # Define this variable as the first token the player input after the command itself.
    amount = int(utilities.flattenTokens(cmd.tokens[1:]))

    # If the player didn't input anything after the command.
    if amount == None or amount == 0:
        response = "How much slime do you want to deposit?"
        return response

    # Get the player's data.
    player_data = player.Player()

    # If the player tries to deposit more slimes than they have.
    if amount > player_data.slimes:
        response = "You can't deposit that much slime, you only have {:,}.".format(player_data.slimes)
        return response

    else:
        # Deposit the slime.
        player_data.slimes -= amount
        player_data.debt -= amount
        player_data.persist()

        response = "You dump {:,} slime into the ATM.".format(amount)

        if player_data.debt <= 0:
            response += "\nGood job!"
        return response

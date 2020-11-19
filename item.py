# Import external libraries.
import json
import config
import utilities

# The object model for locations on the map.
class Item:
	# These values are default placeholders.

	# The unique identifier for this item. All lowercase, no spaces.
	id = ""

	# The type of item it is; Whether it's a general purpose item, a piece of food, or something else.
	type = ""

	# The nice, proper name for this place. May contain uppercase letters, and spaces.
	name = ""

	# The description provided when inspecting it. TODO: Add inspecting.
	description = ""
	
	# The price of this item if it is sold at a vendor. 
	value = None

	# The vendor this item is sold at.
	vendor = None

	# The amount hunger restored if this item is eaten.
	satiation = None

	# The amount of times the item can be used before breaking.
	durability = None

	def __init__(
		self,
		id,
		type,
		name,
		description,
		value = None,
		vendor = None,
		satiation = None,
		durability = None,
	):
		self.id = id
		self.type = type
		self.name = name
		self.description = description
		self.value = value
		self.vendor = vendor
		self.satiation = satiation
		self.durability = durability

def get_inventory():
	with open('save.json') as save_file:
		# Load the player's save file and retrieve their inventory data.
		save_data = utilities.Save()
		inventory = save_data.data['items']

		return inventory

def create_item(desired_item):
	with open('save.json') as save_file:
		# Load the player's save file and retrieve their inventory data.
		save_data = utilities.Save()
		inventory = save_data.data['items']

		used_id_strings = inventory.keys()
		used_id_integers = [int(id) for id in used_id_strings]

		index = int(max(used_id_integers)) + 1 if inventory != {} else 1

		new_item = {
			index: {
				"id": desired_item.id,
				"type": desired_item.type,
				"name": desired_item.name,
				"description": desired_item.description,
			}
		}

		if desired_item.value != None:
			new_item[index]["value"] = desired_item.value
		
		if desired_item.vendor != None:
			new_item[index]["vendor"] = desired_item.vendor
		
		if desired_item.satiation != None:
			new_item[index]["satiation"] = desired_item.satiation
		
		if desired_item.durability != None:
			new_item[index]["durability"] = desired_item.durability

		inventory.update(new_item)
		save_data.persist()

def search_for_item(sought_item):
	with open('save.json') as save_file:
		# Load the player's save file and retrieve their inventory data.
		save_data = utilities.Save()
		inventory = save_data.data['items']

		for item in inventory:
			if inventory[item]['id'] == sought_item:
				item_object = Item(
								id = inventory[item]['id'],
								type = inventory[item]['type'],
								name = inventory[item]['name'],
								description = inventory[item]['description'],
							)
				
				if "value" in inventory[item].keys():
					item_object.value = inventory[item]["value"]
				
				if "vendor" in inventory[item].keys():
					item_object.vendor = inventory[item]["vendor"]
				
				if "satiation" in inventory[item].keys():
					item_object.satiation = inventory[item]["satiation"]
				
				if "durability" in inventory[item].keys():
					item_object.durability = inventory[item]["durability"]

				return item_object


def delete_item(sought_item):
	with open('save.json') as save_file:
		# Load the player's save file and retrieve their inventory data.
		save_data = utilities.Save()
		inventory = save_data.data['items']

		for item in inventory:
			if inventory[item]['id'] == sought_item:
				del inventory[item]
				save_data.persist()
				break

def edit_item(sought_item, property, new_value):
	with open('save.json') as save_file:
		# Load the player's save file and retrieve their inventory data.
		save_data = utilities.Save()
		inventory = save_data.data['items']

		for item in inventory:
			if inventory[item]['id'] == sought_item:
				inventory[item][property] = new_value
				save_data.persist()
				break
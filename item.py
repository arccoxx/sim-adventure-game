import json
import utilities

class Item:
	# The unique, flattened identifier for this item. All lowercase, no spaces.
	id = ""

	# The type of item it is, wether it's a general purpose item, a piece of food, or something else.
	type = ""

	# The name of the item.
	name = ""

	# The item's description.
	description = ""
	
	# The price of this item if sold at a shop. 
	value = None

	# The shop this item is sold at.
	vendor = None

	# The amount the player's belly fills up if this item is eaten.
	satiation = None

	def __init__(
		self,
		id,
		type,
		name,
		description,
		value,
		vendor,
		satiation,
	):
		self.id = id
		self.type = type
		self.name = name
		self.description = description
		self.value = value
		self.vendor = vendor
		self.satiation = satiation

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
								value = inventory[item]['value'],
								vendor = inventory[item]['vendor'],
								satiation = inventory[item]['satiation']
							)

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
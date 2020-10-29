import json
import utilities

class Item:
	# The unique, flattened identifier for this item. All lowercase, no spaces.
	id = ""

	# The name of the item.
	name = ""

	# The item's description.
	description = ""

	def __init__(
		self,
		id,
		name,
		description
	):
		self.id = id
		self.name = name
		self.description = description


def search_for_item(sought_item):
	with open('save.json') as save_file:
		# Load the player's save file and retrieve their inventory data.
		save_data = utilities.Save()
		inventory = save_data.data['items']

		for item in inventory:
			if inventory[item]['name'] == sought_item:
				return inventory[item]


def delete_item(sought_item):
	with open('save.json') as save_file:
		# Load the player's save file and retrieve their inventory data.
		save_data = utilities.Save()
		inventory = save_data.data['items']

		for item in inventory:
			if inventory[item]['name'] == sought_item:
				del inventory[item]
				save_data.persist()
				break


def create_item(id, name, description):
	with open('save.json') as save_file:
		# Load the player's save file and retrieve their inventory data.
		save_data = utilities.Save()
		inventory = save_data.data['items']

		used_id_strings = inventory.keys()
		used_id_integers = [int(id) for id in used_id_strings]

		index = int(max(used_id_integers)) + 1 if inventory != {} else 1

		y = {
			index: {
				"id": id,
				"name": name,
				"description": description
			}
		}

		# appending data to emp_details
		inventory.update(y)
		save_data.persist()

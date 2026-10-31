# tests.py
import random
from system_storage import System_Inventory
from system_creatures import System_Creature
from system_items import all_items
from debug_games import DEBUG
from utils import clear_screen

clear_screen()
print(f"<{'Novos Testes'.center(40, ' ')}>", end="\n\n\n")


debug = DEBUG(True)

def tests_inventory(user, item_test):
	item = all_items.get(item_test["id"])
	debug.print("Testando inventario:")
	for amount in item_test.get("amounts", []):
		_, total = user.inventory.search_item(item.get("id", "%")).values()
		esperado = total + amount
		user.inventory.add_item(item, amount)
		_, total = user.inventory.search_item(item.get("id", "%")).values()
		if (total == esperado):
			debug.print(f" {item.get('name')}, {amount} -> {total} Esperado: {esperado}, Resultado: [ OK ]")
		else:
			debug.print(f" {item.get('name')}, {amount} -> {total} Esperado: {esperado}, Resultado: [ ERROR ]")
	debug.print("TESTES COM INVENTARIO CONCLUIDO.\n\n\n")

def tests_game_states():
	from main import GamePlay
	app = GamePlay()
	app.debug.activated = False
	app.start()
	npc.location = ['elven-high', 'marketplace-local']
	app.entities_in_world[npc.get_id()] = npc
	for key in npc.brain.ocupations.keys():
		npc.brain.ocupations[key] = random.uniform(0.0000, 0.0003)
		print(f"{key} : {npc.brain.ocupations[key]}")
	print(app.discover_item_in_marketplace(npc))

item_test = {
	'id': random.choice(list(all_items.keys())),
	'amounts': [10, 18, 203],
}
npc = System_Creature("id:0123")
tests_inventory(npc, item_test)
tests_game_states()
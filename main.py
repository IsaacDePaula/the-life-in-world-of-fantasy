from system_creatures import System_Creature
from system_map_directions import map_sheet
from utils import table_informations, table_show_label
from utils import selection_options, format_option, clear_screen
from jobs import System_dungeons, System_hunter, System_plants
from slave_marketplaces import Marketplace_slave
from slave_interaction import Interaction_slave
from system_storage import Interaction_Storage
from system_storage import System_Chests
from marketplaces import System_Marketplace
from system_magic import System_Effects
from system_magic import Interface_Arcane
from SaveGame import System_Save_Game
from system_time import System_Time
from plants import PLANTS_IN_WORLD
from system_crafts import RECEIVES
from system_items import all_items
from debug_games import DEBUG
import random, os


path_root = os.getcwd()

def status_player(user, sys_timer):
	from utils import table_informations
	turn_day = "Manhã"
	hr = sys_timer.get_h()
	if hr >= 6 and hr < 12:
		turn_day = "Manhã"
	if hr >= 12 and hr < 18:
		turn_day = "Tarde"
	if hr >= 18 and hr < 24:
		turn_day = "Noite"
	if hr >= 0 and hr < 6:
		turn_day = "Madrugada"
	data = {
		"nome": user.profile.name,
		"raça": user.profile.race,
		"sexo": "Feminino" if user.profile.gender == "f" else "Masculino",
		"saúde": f"{int(user.get_hp())}/ {int(user.get_hp_max())}",
		"Mana": f"{int(user.get_mp())}/ {int(user.get_mp_max())}",
		"Energia": f"{int(user.get_st())}/ {int(user.get_st_max())}",
		"Horário": f"{turn_day} {sys_timer.date()}",
		"Dinheiro": f"{user.inventory.get_coins()} G",
	}
	return table_informations(data, f"Status de {user.profile.name}")


class GamePlay(object):
	def __init__(self):
		self.entities_in_world = {}
		self.debug = DEBUG(True)

	def add_creature(self, entitie):
		idname = entitie.get_id()
		if idname not in self.entities_in_world:
			self.entities_in_world[idname] = entitie

	def get_creature(self, idname):
		return self.entities_in_world.get(idname, False)

	def remove_create(self, idname):
		if idname in self.entities_in_world and not 'player' in self.entities_in_world:
			del self.entities_in_world[idname]

	def event_game(self, result):
		_, data = result
		location_possible = data.get('local', [])
		if data.get("text") == "search-plants":
			if data.get("local") in PLANTS_IN_WORLD:
				all_plants_local = PLANTS_IN_WORLD[data.get("local")]
				self.sys_plants.set_all_plants_area(all_plants_local)
				self.sys_plants.interaction(self.entities_in_world.get("player"))
				self.tick += 0.3
		if data.get("text") == 'chest':
			player = self.entities_in_world.get("player")
			self.chest.interaction(player)
		if data.get("text") == "sleep":
			player = self.entities_in_world.get("player")
			value = data.get("value", 0)
			can_sleep = False
			if value > 0:
				if player.get_coins() >= value:
					player.inventory.remover_item("gold", value)
					can_sleep = True
			else:
				can_sleep = True
			if can_sleep:
				self.save_game()
				player.set_st(player.get_st_max())
				player.set_mp(player.get_mp_max())
				print("Jogo Salvo com Sucesso!")
				print("Status recuperado você descansou.")
			else:
				print("Você tem dinheiro seu vagabundo. vai embora! é 50 moeda de ouro seu arrombado.")
			input("\n\nPressione Enter")
		if data.get("text") == "pause-game":
			self.pause_screen()
		if data.get("text") == "arcane-game":
			player = self.entities_in_world.get("player")
			self.sys_arcane.interaction(player)
		if data.get("text") == "beast-room":
			player = self.entities_in_world.get("player")
			self.sys_interaction_slaves.interaction(player)
		if data.get("text") == "market-slave-local":
			self.sys_marketblack.main(
				self.entities_in_world.get("player"))
		if data.get("text") == "inventory-game":
			self.sys_interaction_storage.inventory(
				self.entities_in_world.get("player"))
		if data.get("text") == "equipments-game":
			self.sys_interaction_storage.equipment(
				self.entities_in_world.get("player"))
		if data.get("text") == "monster-hunt":
			group_player = [
				self.entities_in_world.get("player")
			]
			members_companions = self.entities_in_world.get(
				"player").relationships.get_members_per_tag("companion")
			for npc_id in members_companions:
				npc = self.get_creature(npc_id)
				if npc != False:
					group_player.append(npc)
			self.sys_hunter.start_hunter(data.get("local", "elven-high"), group_player)
			self.tick += 0.3
		if data.get("text") in ["blacksmith-local", "alchemist-local", "hunter-local"]:
			local = data.get("local")
			type_n = data.get("text").replace("-local", '')
			if local in self.marketplaces:
				if type_n in self.marketplaces[local]:
					player = self.entities_in_world.get("player")
					self.marketplaces[local][type_n].main(player)
					self.tick += 0.3
		if location_possible != []:
			location_possible = [x for x in map_sheet[location_possible].keys()]
		if data.get('text') in location_possible:
			back_of_one_florest = self.entities_in_world.get("player").location[1]=="florest-local"
			self.entities_in_world.get('player').location[1] = data.get('text', 'main')
			self.entities_in_world.get('player').location[0] = data.get('local', 'elven-high')
			if not data.get("text") == "main" or back_of_one_florest:
				self.tick += 0.3

	def constructor(self, options, title, subtitle):
		if self.can_show_scene:
			result = selection_options(options, title, subtitle)
			self.event_game(result)
			self.can_show_scene = False

	def scenes(self):
		self.can_show_scene = True
		if self.main_game_config:
			self.main_screen()
			return
		elif self.entities_in_world.get("player").get_hp() <= 0:
			self.screen_death()
		else:
			kingdom, local = self.entities_in_world.get('player').location
			scene = map_sheet[kingdom][local]
			title, options = scene.get('title', ''), scene.get('options', [])
			title = status_player(
				self.entities_in_world.get("player"),
				self.sys_chrono)+f'\n\n{self.tick:.1f} {self.sys_chrono.string()}\n\n'+title
			subtitle = 'Escolha uma opção: '
			if self.tick >= 1:
				self.update_all_mobs()
				self.tick = 0
			self.constructor(options, title, subtitle)

	def search_item_in_marketplace(self, user, item_id, amount_need):
		local = user.location[0]
		marketplaces = self.marketplaces.get(local, {})
		for key, marketplace in marketplaces.items():
			if marketplace.own != user:
				result = marketplace.buy(user, item_id, amount_need)
				if type(result) == list:
					sucess, coins, reason = result
					self.debug.print(sucess, coins, reason)
					return sucess
				if result is None:
					self.debug.print("não tem o item poha vai tomar no cu")
				self.debug.print(result)
		return False

	def discover_item_in_marketplace(self, user):
		pass

	def search_item_in_florest(self, user, item_id, amount_need):
		all_plants = [x for x in self.sys_plants.plants_now if x.havest() != False]
		sucess = False
		reason = "Sem motivos ainda."
		for plant in all_plants:
			if sucess == True:
				break
			for item_fruit, amount in [x for x in plant.items_for_havests.items()]:
				item = all_items.get(item_fruit, False)
				amount_collect = amount_need
				if item_fruit == item_id:
					if item != False:
						if amount_need > amount:
							amount_collect = amount
						user.inventory.add_item(item, amount_collect)
						plant.items_for_havests[item_fruit] -= amount_collect
						sucess = True
						reason = "Encontrado na floresta."
						break
			if len([x for x in plant.items_for_havests.values() if x > 0]) <= 0:
				plant.reset_values()
		return sucess, reason

	def update_all_mobs(self, timeout=3):
		self.sys_chrono.add_timer(h=timeout)
		self.sys_plants.update_all_plants(h=timeout, m=0, d=0)
		for npc in self.entities_in_world.values():
			npc.chrono.add_timer(h=timeout)
			category_items = {
				"hunter": [
					"resource", "food", "meat", "hunting",
					"leather", "hide", "bone", "fur", "pelt",
					"feather", "fang", "claw"],
				"blacksmith": [
					"material", "ore", "metal", "ingot",
					"iron", "steel", "gold", "silver", "copper",
					"weapon", "sword", "shield", "armor",
					"equipment", "crafting"],
				"alchemist": [
					"ingredient", "herb", "plant", "flower",
					"root", "mushroom", "fungus", "potion",
					"elixir", "poison", "healing", "alchemy",
					"magic", "resistance", "essence", "crystal"]
			}
			if not npc.control:
				self.debug.print(f"NOME: {npc.profile.name} / Ocupação: {max(npc.level.skills, key=npc.level.skills.get)}")
				action = npc.brain.daily()
				self.debug.print("Ação:", action)
				if action == 'ocupation':
					local = npc.location[0]
					occupation = npc.level.get_skill_occupation()
					marketplaces_local = self.marketplaces.get(local, {})
					marketplaces = npc.get_franchisees()
					result, status = npc.brain.get_progress()
					if status == False:
						crafts_disponibles = npc.brain.knowledge_crafts*2
						if len(crafts_disponibles) > 0:
							craft = random.choice(crafts_disponibles)
							self.debug.print(craft)
							can_craft_item = True
							for item_id, amount in craft.get("craft", {}).items():
								slots, total = npc.inventory.search_item(item_id).values()
								self.debug.print(f"id: {item_id} = ({total} / {amount})")
								if not total >= amount:
									result = self.search_item_in_marketplace(npc, item_id, amount-total)
									self.debug.print("RESULT:", result)
									self.debug.print("Conseguiu o item?", "sim" if result else "não")
									if result == False:
										result, reason = self.search_item_in_florest(npc, item_id, amount)
										self.debug.print(result, reason)
									if not result:
										can_craft_item = False
								else:
									self.debug.print("Tenho a quantidade desse item! :D")
							if can_craft_item:
								self.debug.print("fabricando o item..")
								npc.brain.set_progress(craft, h=timeout)
							else:
								npc.inventory.add_coins(2)
							self.debug.print("")
						else:
							if occupation == "hunter":
								items_ids = [
									("leak", random.randint(-3, 3)),
									("meat", random.randint(-4, 4)),
									("stick", random.randint(-2, 2))
								]
								items_ids = [x for x in items_ids if x[1] > 0]
								self.debug.print("Caçador conseguiu:")
								for item_id, amount in items_ids:
									if amount > 0:
										self.debug.print(f" {item_id}: {amount}")
										item = all_items.get(item_id, False)
										if item:
											value = amount
											division = int(value / len(marketplaces))
											for marketplace in marketplaces:
												if value > 0:
													marketplace.add_item(item_id, value)
													value -= division
								else:
									if not len(items_ids) > 0:
										self.debug.print(" Nada!")
								npc.inventory.add_coins(3)
					elif status == "incomplete":
						npc.brain.set_progress(result, h=timeout)
						self.debug.print("continuo criando item")
					elif status == "complete":
						for item_id, amount in result.items():
							item = all_items.get(item_id, False)
							for marketplace in marketplaces:
								marketplace.add_item(item_id, amount)
							npc.inventory.add_coins(max(3, int(item.get("value", 15)/3)))
							self.debug.print(f" {item.get('name')} fabricado com sucesso!")
						npc.brain.remove_progress()
				else:
					npc.brain.event(action)
				npc.brain.update()
				self.debug.print("-"*40)

	def screen_death(self):
		options = [
			format_option("Carregar utimo jogo Salvo", {"text": "load"}),
			format_option("Começar Novo Jogo", {"text": "new-game"}),
			format_option("Menu do principal", {"text": "menu-game"}),
			format_option("Sair do Jogo", {"text": "exit-game"}),
		]
		while(True):
			selected = selection_options(options,
				"Você morreu sua saude chegou a zero, o que você quer fazer?",
				"Escolha uma opção: ")
			self.event_game(selected)

	def main_screen(self):
		options = [
			format_option("Novo Jogo", {"text": "new-game"}),
			format_option("Continuar Jogo", {"text": "continue-game"}),
			format_option("Opção do Jogo", {"text": "options-game"}),
			format_option("Creditos", {"text": "about-game"}),
			format_option("Sair do Jogo", {"text": "exit-game"}),
		]
		self.constructor(options, "Bem Vindo Ao Mundo de The Life In World Of Fantasy", "Escolha uma opção: ")

	def pause_screen(self):
		options = [
			format_option("Retornar", {"text": "return-game", "default": True}),
			format_option("Inventario", {"text": "inventory-game"}),
			format_option("Equipamentos", {"text": "equipments-game"}),
			format_option("Conhecimentos Arcanos", {"text": "arcane-game"}),
			format_option("Terminal", {"text": "code-game"}),
			format_option("Menu Principal", {"text": "menu-game"}),
			format_option("Sair do Jogo", {"text": "exit-game"}),
		]
		while(True):
			selected = selection_options(options, "Jogo Pausado.", "Escolha uma opção: ")
			if selected[1]['text'] == 'return-game':
				break
			self.event_game(selected)

	def save_game(self):
		from slave_marketplaces import get_age_range

		player = self.entities_in_world.get("player")

		name = player.profile.name
		race = player.profile.race

		folder_savegame = os.path.join(path_root, "savegame")
		self.filename = os.path.join(folder_savegame,
			f"player-{name}-{race}-{get_age_range(player)}.json")
		if not os.path.isdir(folder_savegame):
			os.mkdir(folder_savegame)
		path = os.path.join(*self.filename)
		self.sys_save_game.save_game(self.filename)
		clear_screen()
		input(table_show_label("Progresso Salvo!", "Sua jornada foi salva com sucesso. Continue sua aventura de onde parou!"))

	def start(self):
		self.wait = True
		self.main_game_config = False
		self.entities_in_world = {}
		self.sys_chrono = System_Time(6, 0, 234, 3245)
		self.sys_plants = System_plants()
		self.sys_interaction_storage = Interaction_Storage()
		self.sys_interaction_slaves = Interaction_slave(self)
		self.sys_arcane = Interface_Arcane(self)
		self.sys_hunter = System_hunter()
		self.sys_save_game = System_Save_Game(self)
		self.sys_marketblack = Marketplace_slave(self,
			None, species=['human'])
		self.sys_marketblack.generator()
		self.tick = 1

		config_player = {
			"name": "Calanguinho Mago",
			"race": "human",
			"gender": "m",
			"age": 24,
			"location": ["elven-high", "main"]
		}
		player = System_Creature("player")
		player.control = True
		player.profile.name = config_player["name"]
		player.profile.race = config_player["race"]
		player.profile.gender = config_player["gender"]
		player.chrono.set_values("y", config_player["age"])
		player.location = config_player["location"]
		player.inventory.add_coins(120)
		self.chest = System_Chests()
		self.entities_in_world['player'] = player

		agentes = {
			'blacksmith': {'name': "Raul", 'gender': "m", 'local': "elven-high"},
			'alchemist': {'name': "Rebeca", 'gender': "f", 'local': "elven-high"},
			'hunter': {'name': "Richard", 'gender': "m", 'local': "elven-high"},
		}

		self.marketplaces = {
			key: {} for key in map_sheet.keys()
		}
		for key, value in agentes.items():
			name, gender, local = value.values()
			npc = System_Creature(f"{key}-00123-{local}")
			npc.profile.name = name
			npc.level.skills[key] += 1
			npc.brain.ocupations[key] += 0.01
			npc.location = [local, "main"]
			for recive in [x for x in RECEIVES if key in x['requisites']]:
				npc.brain.knowledge_crafts.append(recive)
			self.marketplaces[local][key] = System_Marketplace(npc)
			self.entities_in_world[npc.get_id()] = npc
			npc.add_franchisee(self.marketplaces[local][key])
		timeout = int(24*5)
		for i in range(timeout):
			self.update_all_mobs(3)
		self.debug.input("\n\nPressione Enter Para Prosseguir.")

	def update(self):
		self.scenes()

	def main(self):
		self.start()
		while(self.wait):
			self.update()


if __name__ == '__main__':
	game = GamePlay()
	game.main()
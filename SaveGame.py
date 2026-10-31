# SaveGame.py
from system_creatures import System_Creature
from system_items import all_items
import json


class System_Save_Game(object):
	def __init__(self, world):
		self.world = world

	def save_game(self, file_save):
		try:
			h = self.world.sys_chrono.get_h()
			m = self.world.sys_chrono.get_m()
			d = self.world.sys_chrono.get_d()
			y = self.world.sys_chrono.get_y()
			data_game_state = {
				"creatures": {},
				"marketplaces": {},
				"plants-in-world": {},
				"timer_world": {'h':h, 'm':m, 'd': d, 'y': y},
			}
			for npc_id, npc in self.world.entities_in_world.items():
				data_game_state["creatures"][npc_id] = {
					"id": npc.get_id(),
					"name": npc.profile.name,
					"race": npc.profile.race,
					"control": npc.control,
					"gender": npc.profile.gender,
					"age": npc.chrono.data,
					"brain": {
						"personalite": npc.brain.personalite,
						"needs": npc.brain.needs,
						"desires": npc.brain.desires,
						"ocupations": npc.brain.ocupations,
						"progress": npc.brain.progress,
						"knowledge_crafts": npc.brain.knowledge_crafts,
						"foods": npc.brain.foods,
					},
					"level": npc.level.get_level(),
					"exp": npc.level.get_exp(),
					"skills": npc.level.skills,
					"titles": npc.titles.titles,
					"status": npc.status.status,
					"magic":{
						'spells': npc.magic.spellbook,
						'effects': dict([
							(
								key,
								{
									"effect_id":effect.effect_id,
									"turns":effect.turns,
									"mod":effect.mod
								}
							)
							for key, effect in npc.magic.all_effects]),
					},
					"relationships": {
						"status": npc.relationships.status,
						"knowledge": npc.relationships.knowledge,
					},
					"attributes": npc.attributes.attributes,
					"inventory": [(x.get_item(), x.get_amount())
						for x in npc.inventory.slots
						if not x.is_empty()],
					"equipment": [(y, x.get_item(), x.get_amount())
						for y, x in npc.equipment.slots.items()
						if not x.is_empty()],
					"items": npc.items_drop,
					"location": npc.location,
					"missions": npc.missions,
				}
			for kingdom, marketplaces in self.world.marketplaces.items():
				if not kingdom in data_game_state["marketplaces"]:
					data_game_state["marketplaces"][kingdom] = {}
				for local, marketplace in marketplaces.items():
					data_game_state["marketplaces"][kingdom][local] = {
						"own": marketplace.own.get_id(),
						"inventory": {id_item: amount
							for id_item, amount in marketplace.items.items()}
					}
			for plant in self.world.sys_plants.plants_now:
				h = plant.clock.get_h()
				m = plant.clock.get_m()
				d = plant.clock.get_d()
				y = plant.clock.get_y()
				data_game_state['plants-in-world'][plant.id] = {
					"haverts": plant.can_havest,
					"items_havest": plant.items_for_havests,
					"clock": {"h": h, "m": m, "d": d, "y": y}
				}
			data_string = json.dumps(data_game_state, indent=4)
			with(open(file_save, 'w', encoding="utf-8")) as f:
				f.write(data_string)
			return f"Jogo Salvo com sucesso, armazenado no arquivo: {file_save}"
		except:
			return f"ocorreu algum erro durante o salvamento por favor verifique as variaveis."

	def load_game(self, file_save):
		from system_magic import Effect
		try:
			with(open(file_save, "r", encoding='utf-8')) as f:
				data = json.loads(f.read())
		except:
			return f"Erro ao carregar o mundo pelo arquivo: {file_save}"
		self.world.sys_chrono.data = data.get("timer_world",
			self.world.sys_chrono.data)
		for npc_id, information in data.get("creatures", {}).items():
			npc = System_Creature(npc_id)
		
			npc.control = information.get("control", npc.control)
			npc.profile.name = information.get("name", npc.profile.name)
			npc.profile.race = information.get("race", npc.profile.race)
			npc.profile.gender = information.get("gender", npc.profile.gender)

			npc.chrono.data = information.get("age", npc.chrono.data)

			npc.brain.personalite = information["brain"].get("personalite", npc.brain.personalite)
			npc.brain.needs = information["brain"].get("needs", npc.brain.needs)
			npc.brain.desires = information["brain"].get("desires", npc.brain.desires)
			npc.brain.ocupations = information["brain"].get("ocupations", npc.brain.ocupations)
			npc.brain.progress = information["brain"].get("progress", npc.brain.progress)
			npc.brain.knowledge_crafts = information["brain"].get("knowledge_crafts", npc.brain.knowledge_crafts)
			npc.brain.foods = information["brain"].get("foods", npc.brain.foods)

			npc.level.level = information.get("level", npc.level.level)
			npc.level.skills = information.get("skills", npc.level.skills)
			npc.level.exp = information.get("exp", npc.level.exp)
			
			npc.titles.titles = information.get("titles", npc.titles.titles)
			
			npc.status.status = information.get("status", npc.status.status)
			
			npc.items_drop = information.get("items", npc.items_drop)
			
			npc.attributes.attributes = information.get("attributes", npc.attributes.attributes)
			
			npc.relationships.knowledge = information["relationships"].get("knowledge", npc.relationships.knowledge)
			npc.relationships.status = information["relationships"].get("status", npc.relationships.status)
			
			npc.magic.spellbook = information["magic"].get("spells", npc.magic.spellbook)
			for key, effect in information["magic"].get("effect", {}).items():
				effect = Effect(effect["effect_id"], effect["turns"], effect["mod"])
				npc.magic.all_effects[key] = effect
			
			npc.location = information.get("location", npc.location)
			
			npc.missions = information.get("missions", npc.missions)
			
			for item, amount in information.get("inventory", []):
				npc.inventory.add_item(item, amount)
			
			for tag, item, amount in information.get("equipment", []):
				npc.equipment.slots[tag].set_item(item)
				npc.equipment.slots[tag].set_amount(amount, False)
			
			self.world.entities_in_world[npc_id] = npc
		
		for kingdom, marketplaces in data.get("marketplaces", {}).items():
			for local, data_marketplace in marketplaces.items():
				own, inventory = data_marketplace.items()
				self.world.marketplaces[kingdom][local].own = self.world.get_creature(own)
				self.world.marketplaces[kingdom][local].items = inventory
		
		plants = {x.id: x for x in self.world.sys_plants.plants_now}
		for id_plant, values in data.get('plants-in-world', {}).items():
			can_havest, items_for_havests, clock = values.values()
			plants[id_plant].clock.can_havest = can_havest
			plants[id_plant].items_for_havests = items_for_havests
			plants[id_plant].clock.data = clock
		return f"carregamento concluido pelo arquivo: {file_save}"


if __name__=="__main__":
	from main import GamePlay
	world = GamePlay()
	file = "savegame/save_game_test.json"
	app = System_Save_Game(world)
	world.start()
	print("Salvo:", app.save_game(file))
	print("Carregamento:", app.load_game(file))
	for id, npc in world.entities_in_world.items():
		print(id, npc.control)
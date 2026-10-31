# system_ai_npcs.py
import copy
import random
from system_items import all_items


class AI(object):
	def __init__(self, entitie):
		self.entitie = entitie
		self.personalite = {
			'courage': random.random(),
			'aggressiveness': random.random(),
			'sociability': random.uniform(-0.3, 0.3),
		}
		self.needs = {
			"hunger": random.random(),
			"energy": random.random(),
			"social": random.random(),
		}
		self.desires = {
			'ocupation': random.uniform(0.0, 0.5),
			'discipline': random.uniform(0.0, 0.5),
		}
		self.desires_objective = {}
		self.ocupations = {
			'mage': 0,
			'swordsman': 0,
			'warrior': 0,
			'blacksmith': 0,
			'lumberjack': 0,
			'hunter': 0,
			'warlock': 0,
			'alchemist': 0,
		}

		self.progress = {}
		self.knowledge_crafts = []
		self.knowledge_items = {}
		self.foods = 0

	def forms_new_process(self, craft):
		key = craft.get("id")
		if not self.progress:
			self.progress[key] = {
				"status": "incomplete",
				"craft": craft,
				"timer": {"h": 0, "m": 0, "d": 0}
			}

	def add_timer_craft(self, data, h=0, m=0, d=0):
		data["timer"]["h"] += h
		data["timer"]["m"] += m
		data["timer"]["d"] += d
		template = [
			["m", 60, "h", 1],
			["h", 24, "d", 1],
		]
		for kd, vd, ki, vi in template:
			while(data["timer"][kd] >= vd):
				data["timer"][kd] -= vd
				data["timer"][ki] += vi
		return data

	def set_progress(self, craft, h=0, m=0):
		# função que calcula o tempo percorrido.
		self.forms_new_process(craft)
		key = craft.get("id")
		data = self.progress[key]
		self.progress[key] = self.add_timer_craft(data, h=h, m=m)

	def get_progress(self):
		keys = list(self.progress.keys())
		if len(self.progress) > 0:
			craft = self.progress[keys[0]]["craft"]

			date = self.progress[keys[0]]["timer"]
			h, m, d = date.values()
			craft_timer = craft["timer"]
			timeout_craft = (craft_timer["d"] * (24 * 60)) + (craft_timer["h"] * 60) * craft_timer["m"]
			timeout_progress = (date["d"] * (24 * 60)) + (date["h"] * 60) + date["m"]
			if timeout_progress >= timeout_craft:
				self.progress[keys[0]]["status"] = "complete"
				return [craft["items"], "complete"]
			return [self.progress[keys[0]], "incomplete"]
		return [False, False]

	def remove_progress(self):
		keys = list(self.progress.keys())
		if len(self.progress) > 0:
			del(self.progress[keys[0]])
			return True
		return False

	def complete_objective(self, key):
		if key in self.desires_objective:
			del(self.desires_objective[key])

	def add_objective(self, key, weight):
		self.desires_objective[key] = weight

	def combate(self):
		atk_list = [
			self.ocupations.get("swordsman", 0.0),
			self.ocupations.get("lumberjack", 0.0),
			self.ocupations.get("warrior", 0.0),
			self.ocupations.get("hunter", 0.0),
			self.ocupations.get("blacksmith", 0.0),
			self.personalite.get("aggressiveness", 0.0) * 0.05,
		]
		hp, hp_max = self.entitie.get_hp(), self.entitie.get_hp_max()
		mp, mp_max = self.entitie.get_mp(), self.entitie.get_mp_max()
		st, st_max = self.entitie.get_st(), self.entitie.get_st_max()

		potion = 1 if self.entitie.inventory.search_item("potion-hp50")["total"] > 0 else 0
		spellbook = 1 if len(self.entitie.magic.spellbook) > 0 else 0
		spellbook_offense = 1 if len([x['type'] == 'mgk-offensive' for x in self.entitie.magic.spellbook.values()]) > 0 else 0
		spellbook_defense = 1 if len([x['type'] == 'mgk-defense' for x in self.entitie.magic.spellbook.values()]) > 0 else 0
		spellbook_suport = 1 if len([x['type'] == 'mgk-suport' for x in self.entitie.magic.spellbook.values()]) > 0 else 0

		value_hp = hp / hp_max
		value_mp = mp / mp_max
		value_st = st / st_max

		if len(atk_list) > 0:
			atk_value = sum(atk_list) / len(atk_list)
		else:
			atk_value = 0
		value_es = (self.personalite.get("courage", 0.0) * (1.0 - (value_hp+0.2))) * 0.009
		mgk_value = (self.ocupations.get("mage", 0.0) + self.ocupations.get("warlock", 0.0) + (value_mp * 0.02) / 4)
		prioridade = {
			"atk": max(0.0005, atk_value-(1.0-value_st)),
			"nda": max(0.0005, 1.0 - value_st),
			"mgk-offensive": spellbook_offense * (max(0.0005, mgk_value)),
			"mgk-defense": spellbook_defense * (max(0.0005, (value_hp+(self.personalite.get("courage", 0.0) * 0.001))/2)*0.01),
			"escape": max(0.0006, value_es),
			"use-potion": potion * max(0.0005, 1.0 - value_hp)
		}
		if False:
			print("id:", self.entitie.get_id())
			for key, values in prioridade.items():
				print(key, ":", values)
		return max(prioridade, key=prioridade.get)

	def get_value_desires_objective(self):
		max_n = 0
		max_k = None
		for key, values in self.desires_objective.items():
			if values > max_n:
				max_n = values
				max_k = key
		return max_k, max_n

	def daily(self):
		prioridade = {
			"eat": self.needs.get("hunger"),
			"sleep": 1.0 - self.needs.get("energy"),
			"social": sum([
				self.needs.get("social"),
				self.personalite["sociability"]])/2,
			"ocupation": sum([
				self.desires["ocupation"],
				self.desires["discipline"]])/2,
		}
		key, value = self.get_value_desires_objective()
		if not key is None:
			prioridade[key] = min(0.6, value + self.desires.get("ocupation", 0))
		action = max(prioridade, key=prioridade.get)
		if action == "eat":
			if not self.foods > 1:
				action = "buy-foods"
				if not self.entitie.inventory.get_coins() >= 20:
					action = "ocupation"
		return action

	def update(self):
		self.needs["hunger"] = min(1.0, max(0.0, self.needs["hunger"] + 0.01))
		self.needs["energy"] = min(1.0, max(0.0, self.needs["energy"] - 0.01))
		self.needs["social"] = min(1.0, max(0.0, self.needs["social"] + 0.01))

	def event(self, action):
		text_lines = ""
		if action == "eat":
			self.needs["hunger"] = min(1.0, max(0.0, self.needs["hunger"] - 1.0))
			self.needs["energy"] = min(1.0, max(0.0, self.needs["energy"] - 0.03))
			text_lines += "Decidir comer algo."
			self.foods -= 1
		if action == "sleep":
			self.needs["energy"] = min(1.0, max(0.0, self.needs["energy"] + 1.0))
			self.needs["hunger"] = min(1.0, max(0.0, self.needs["hunger"] + 0.3))
			text_lines += "Decidir dormir, estou precisando."
		if action == "social":
			self.needs["social"] -= 1.0
			self.needs["energy"] = min(1.0, max(0.0, self.needs["energy"] + 0.03))
			self.needs["hunger"] = min(1.0, max(0.0, self.needs["hunger"] + 0.3))
			text_lines += "Decidir socializar um pouco tava meio depre."
		if action == "ocupation":
			money = random.randint(1, 30)
			self.needs["energy"] = min(1.0, max(0.0, self.needs["energy"] + (0.03*8)))
			self.needs["hunger"] = min(1.0, max(0.0, self.needs["hunger"] + (0.03*8)))
			self.entitie.inventory.add_item(all_items["gold"], money)
			value = sum([x > 0 for x in self.ocupations.values()])
			if not value > 0:
				for key in self.ocupations:
					self.ocupations[key] += random.uniform(0.001, 0.002)
			prioridade = max(self.ocupations, key=self.ocupations.get)
			self.ocupations[prioridade] += 0.001
			text_lines += f"Decidir focar um pouco no meu trabalho. E conseguir {money} G trabalhando de {prioridade}"
		if action == "buy-foods":
			self.foods += 1
			self.entitie.inventory.set_coins(-20)
			text_lines += "Decidir comprar comida, e conseguir 1 por 20 moedas"
		return text_lines

def view_data(data, _min=0.0, _max=1.0):
	graphic = ['muito baixo', 'baixo', 'medio', 'alto', 'muito alto']
	graphic = [(x, i) for i, x in enumerate(graphic)]
	division = _max / len(graphic)
	text_lines = ""
	for key, value in data.items():
		text_lines += f" {key.upper()} : "
		can = False
		for word, n in reversed(graphic):
			if value >= n * division and value < (n+1) * division:
				text_lines += f"{word.upper()} {value:.3f}\n"
				can = True
		if not can:
			if value < _min:
				text_lines += f"{graphic[0][0].upper()} {value:.3f}\n"
			if value >= _max:
				text_lines += f"{graphic[-1][0].upper()} {value:.3f}\n"
	return text_lines


if __name__=="__main__":
	from system_creatures import System_Creature
	from system_items import all_items
	from utils import clear_screen

	clear_screen()

	def action_result(npc, target, action):
		damage = npc.get_damage()
		defense = target.get_defense()
		if action == "use-potion":
			npc.inventory.remover_item("potion-hp50", 1)
			npc.set_st(-((npc.get_st_max()/15)))
			npc.set_hp(50)
			return "POTION"
		if action == "mgk-offensive":
			npc.set_st(-((npc.get_st_max()/10)))
			npc.set_mp(-((npc.get_mp_max()/4)))
			damage *= 2.4
		if action == 'mgk-defense':
			npc.set_st(-((npc.get_st_max()/5)))
			npc.set_mp(-((npc.get_mp_max()/4)))
			damage = int(0.5 * damage)
		if action == "atk":
			npc.set_st(-((npc.get_st_max()/10)))
		if action == 'nda':
			npc.set_st(((npc.get_st_max()/4)))
			npc.set_mp(((npc.get_mp_max()/4)))
			return "NDA"
		if action == "escape":
			return "ESCAPE"
		if action in ['atk', 'mgk-defense', 'mgk-offensive']:
			npc.set_hp(-damage)
			return "DAMAGE"

	npc = System_Creature("mercador")
	npc.level.skills["blacksmith"] += 1

	npc1 = System_Creature("npc1")
	npc2 = System_Creature("npc2")
	
	# cerebro do npc
	npc.brain = AI(npc)
	npc.inventory.add_item(all_items.get("potion-hp50"), 5)
	turns = 0
	entitie_escape = False
	while(npc1.get_hp() > 0 and npc2.get_hp() > 0 and not entitie_escape):
		for npc in [npc1, npc2]:
			turns += 1
			action = npc.brain.combate()
			npc.brain.update()
			print("="*40)
			print(f"hp: {int(npc.get_hp())}/ {int(npc.get_hp_max())}")
			print(f"mp: {int(npc.get_mp())}/ {int(npc.get_mp_max())}")
			print(f"st: {int(npc.get_st())}/ {int(npc.get_st_max())}")
			print(f"Potions: {npc.inventory.search_item('potion-hp50')['total']}")
			print("")

			print(f" Action: {str(action).upper()}")
			target = npc1 if npc2 == npc else npc2
			result = action_result(npc, target, action)
			if action == "escape":
				print(f"NPC: {npc.get_id()} fugiu!")
				entitie_escape = True
	if npc.get_hp() <= 0:
		print("\nAcabou morrendo.")
	print(f"\n\nforam {turns} jogados pelo npc.\n\n")

	if False:
		for npc in [npc1, npc2]:
			print(f"NPC: {npc.get_id()}")
			print(f" PERSONALIDADE:\n{view_data(npc.brain.personalite)}")
			print(f" NECESSIDADES:\n{view_data(npc.brain.needs)}")
			print(f" OCUPAÇÃO:\n{view_data(npc.brain.ocupations)}")
			print()


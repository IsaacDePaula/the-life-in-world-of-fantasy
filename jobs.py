from utils import selection_options, format_option, only_number, clear_screen
import random
from system_items import all_items
from system_time import System_Time
from system_battle import System_Battle

plant_ids = [
	'nightshade', 'silverthorn', 'bloodroot',
	'dragons-tongue', 'winters-bite', 'dreamleaf',
	'bloomlotus', 'firethorn', 'weavegrass',
	'liferoot', 'starbloom', 'rotshroom',
	'mindthorn', 'gravedust', 'zapthistle',
	'sirens-call', 'deaths-beckon', 'shadowleaf',
	'cinderroot', 'graveflower'
]


class Plant(object):
	def __init__(self, name_id, name, items, h=0, m=0, d=0, y=0):
		self.id = name_id
		self.name = name
		self.timer = {'h': h, 'm': m, 'd': d, 'y': y}
		self.clock = System_Time(0, 0, 0, 0)
		self.items_havest = items
		self.can_havest = False
		self.items_for_havests = {}

	def count_time_need(self):
		time_plant_need = sum([
			(self.timer["y"] * self.clock.get_bd() * 24 * 60),
			(self.timer["d"] * 24 * 60),
			(self.timer["h"] * 60),
			(self.timer["m"])
		])
		return time_plant_need

	def count_time_in_progress(self):
		time_plant_progress = sum([
			(self.clock.get_y() * self.clock.get_bd() * 24 * 60),
			(self.clock.get_d() * 24 * 60),
			(self.clock.get_h() * 60),
			(self.clock.get_m())
		])
		return time_plant_progress

	def in_progress(self):
		n1 = self.count_time_in_progress()
		n2 = self.count_time_need()
		return n1 / n2

	def update_timer(self, h, m, d):
		if not self.can_havest:
			self.clock.add_timer(h, m, d)
			
			if self.in_progress() >= 1.0 and not self.can_havest:
				self.can_havest = True
				for id_item in self.items_havest:
					_min, _max = self.items_havest[id_item].values()
					amount = random.randint(_min, _max)
					self.items_for_havests[id_item] = amount

	def reset_values(self):
		self.can_havest = False
		for key in 'hmdy':
			self.clock.set_values(key, 0)
		self.items_for_havests = {}

	def havest(self):
		if self.can_havest:
			return self.items_for_havests
		else:
			return False


class System_plants(object):
	def __init__(self) -> None:
		self.all_plants = plant_ids
		self.plants_now = []
		self.days_down = 0
		self.generator_plants()

	def set_all_plants_area(self, all_plants):
		self.all_plants = all_plants

	def generator_plants(self):
		if self.days_down <= 0:
			for id_plant in plant_ids:
				item = all_items.get(id_plant, False)
				if item != False:
					h = random.randint(2, 24*3)
					new_plant = Plant(
						name_id=f"plant-{id_plant}",
						name=f"Planta {item.get('name')}",
						items={id_plant: {'min': 3, "max": 10}},
						h=h, m=0, d=0, y=0)
					self.plants_now.append(new_plant)
					# new_plant.update_timer(h=h, m=0, d=0)
			self.days_down = 1

	def options_plant(self, mob, plant, only_confirm_get_all=False):
		while(True):
			options = [
				format_option('Pegar' if plant.can_havest else None, {'text': 'get', 'default': True}),
				format_option('Volter', {'text': 'back', 'default': not plant.can_havest}),
			]
			items = []
			for item_id, values in plant.items_havest.items():
				_min, _max = values.values()
				item = all_items[item_id]
				items.append({"item": item, "min": _min, "max": _max})

			title = 'Informações:\n'
			title += f' Nome: {plant.name}\n'
			title += "Items Colhiveis:"
			for data in items:
				item, _min, _max = data.values()
				title += f" Nome: {item.get('name')}\n"
				title += f" descrição: {item.get('descrition', '...')}\n"
				title += f" Colheita gera: entre {_min} e {_max}\n"
				title += "\n"
			text_of_progressing = f'Em Progresso para colheita {(plant.in_progress() * 100):^.2f}%'
			title += f" Colheta: {('Pronta' if plant.can_havest else text_of_progressing)}\n\n"
			for item_id, amount in plant.items_for_havests.items():
				item = all_items[item_id]
				title += f" {item.get('name')} {amount}\n"
			if not only_confirm_get_all:
				select = selection_options(options, title,
					"Escolha uma opção: ")[1]['text']
			else:
				select = options[0][1]['text']
			if select == 'back':
				break
			if select == 'get':
				for item_id, amount in plant.items_for_havests.items():
					item = all_items[item_id]
					options = []
					for i in range(1, amount, max(1, int(amount/4))):
						options.append(format_option(f"Pegar {i}", {"text": i}))
					options.append(format_option("Pegar tudo (Padrão)", {"text": amount, 'default': True}))
					options.append(format_option("Deixa para lá", {"text": "back"}))
					amount_g = selection_options(options,
						f"Tem {amount} e você quer pegar quantas {item.get('name')}?",
						"Escolha uma opção: ")[1]["text"]
					if amount_g == 'back':
						break
					plant.items_for_havests[item_id] -= amount_g
					if plant.items_for_havests[item_id] <= 0:
						plant.reset_values()
					clear_screen()
					mob.inventory.add_item(item, amount_g)
					input(f"Foi adicionado ao seu inventario x{amount_g} {item['name']}!\n\nPressione Enter!")
				break

	def interaction(self, mob):
		while True:
			options = []
			for plant in self.plants_now:
				name = plant.name
				progress = min(1.0, plant.in_progress())
				op = format_option(f"{name} ({(progress*100):^.2f}% Para colheita)", {"text": plant})
				options.append(op)

			can_havest_all = any([x for x in self.plants_now if x.in_progress()>=1.0])
			if can_havest_all:
				options.append(format_option("pegar todos pronto pra colheita", {"text": "all-items", "default": True}))
			options.append(format_option('voltar', {'text': 'back', 'default': not can_havest_all}))
			select = selection_options(options,
				"Plantas encontradas no local",
				"Escolha uma opção: ")[1]['text']
			if select == 'back':
				break
			elif select == "all-items":
				clear_screen()
				print("Colhendo todas as plantas do local.")
				for plant in self.plants_now:
					if plant.can_havest:
						for item_id, amount in plant.items_for_havests.items():
							plant.items_for_havests[item_id] -= amount
							item = all_items.get(item_id)
							mob.inventory.add_item(item, amount)
							print(f" Foi adicionado ao seu inventario x{amount} {item['name']}!")
							plant.reset_values()
				input("\nPressione Enter")
			else:
				self.options_plant(mob, select)

	def update_all_plants(self, h, m, d):
		for plant_obj in self.plants_now:
			plant_obj.update_timer(h, m, d)


class System_hunter(object):
	def __init__(self) -> None:
		self.__races = {
			"elven-high": {
				'goblin': {'baby': 0, "adults": 40, "old": 12, "rate": 0.01},
				'wolf': {'baby': 2, "adults": 14, "old": 1, "rate": 0.02},
			}
		}
		self.sys_battle = System_Battle()

	def generator_new_battle(self, species, level=1, amount=None):
		from system_creatures import System_Creature
		from utils import generator_id
		from system_species import select_specie

		size_group = random.randint(len(species), len(species)+2)
		if type(amount) == int:
			size_group = amount
		group = [
			System_Creature(f"battle-id-{generator_id(20)}")
			for x in range(size_group)]

		size_increment = 4

		species_attributes = [" " for x in range(len(group))]

		reserve = {x:int(len(species_attributes)/len(species)) for x in species}

		for i in range(len(species_attributes)):
			name = ""
			for key, value in reserve.items():
				if value > 0:
					name = key
					reserve[key] -= 1
					species_attributes[i] = key
					break
				species_attributes[i] = random.choice(species)
				break

		for i, npc in enumerate(group):
			specie_data = select_specie(species_attributes[i])
			npc.level.set_level(min(1, level+random.randint(-1, 1)))
			npc.profile.get_race(species_attributes[i])
			npc.profile.gender = random.choice([x for x in specie_data.get("gender", "fm")])
			npc.status.set_status_max('hp-max', specie_data.get("hp", npc.get_hp_max()))
			npc.status.set_status_max('mp-max', specie_data.get("mp", npc.get_mp_max()))
			npc.status.set_status_max('st-max', specie_data.get("st", npc.get_st_max()))
			attributes = {
				'str': [npc.get_str, npc.set_str], # força padrão do mob / combate
				'dex': [npc.get_dex, npc.set_dex], # destreze padrão do mob / consegui usar arma ou ferramenta
				'con': [npc.get_con, npc.set_con], # constituição padrão do mob / ordem de ataque em combate
				'int': [npc.get_int, npc.set_int], # inteligência padrão do mob / facilidade em aprender magia
				'wis': [npc.get_wis, npc.set_wis], # sabedoria padrão do mob / julgamento
				'cha': [npc.get_cha, npc.set_cha], # carisma padrão do mob / persuasão
			}
			npc.items_drop = specie_data.get("items", {})
			for key, value in attributes.items():
				get_attribute, set_attribute = value
				set_attribute(specie_data.get("attributes", {}).get(key, get_attribute()), False)
		return group

	def collect_rewards(self, data):
		from utils import clear_screen

		def get_items_in_battle(user, data):
			from system_items import all_items
			all_items_disponibles = {}
			for npc in data["lose"]["dead"]:
				for id_item, amount in npc.items_drop.items():
					if not id_item in all_items_disponibles:
						all_items_disponibles[id_item] = 0
					all_items_disponibles[id_item] += amount
			while(True):
				options = []
				all_items_disponibles = {x: y
					for x, y in all_items_disponibles.items()
					if y > 0}
				if len(all_items_disponibles) > 0:
					for id_item, amount in all_items_disponibles.items():
						item = all_items.get(id_item, False)
						if not item:
							print(id_item, amount)
							continue
						options.append(format_option(f'{amount}x {item.get("name")}', {"text": id_item, "item": item, "amount": amount}))
					options.append(format_option("Pegar Todos Items", {"text": "all-items"}))
					options.append(format_option("Voltar", {"text": "back"}))
					if user.control:
						selected = selection_options(options, "Você venceu, esses são os drops da batalha:", "Escolha uma opção: ")[1]
						clear_screen()
					else:
						selected = {"text": "all-items"}
					if selected["text"] == "back":
						return True
					elif selected["text"] == "all-items":
						text_console = ""
						for _, op in options[:len(options)-2]:
							amount = op["amount"]
							name = op["item"]["name"]
							user.inventory.add_item(op["item"], op["amount"])
							text_console += f" Foram adicionandos ao seu inventario x{amount} de {name} com sucesso.\n"
						text_console += "\nPressione Enter."

						if user.control:
							input(text_console)
						return True
					else:
						amount = selected["amount"]
						name = selected["item"]["name"]
						user.inventory.add_item(selected["item"], selected["amount"])
						all_items_disponibles[selected["text"]] -= selected["amount"]
						text_console = f"foram adicionandos ao seu inventario x{amount} de {name} com sucesso.\nPressione Enter."

						if user.control:
							input(text_console)
				else:
					return False

		clear_screen()
		# print(data)
		lose = data["lose"]["dead"]
		dead = data["lose"]["dead"]
		actions = data["win"]["actions"]

		for npc in data['win']["group"]:
			n = len(actions.get(npc.get_id(),
			 []))
			exp = int(n * max(1, len(dead)) * max(1, len(lose)) * (1500 * npc.level.rate) * 2.4)
			npc.level.set_exp(exp)
			if npc.control:
				if exp <= 0:
					input("Você não recebeu experiência, pois ficou parado e não fez nada.\nPressione Enter.")
				elif exp > 0:
					input(f"Você recebeu {exp} de experiência.\nPressione Enter.")
			get_items_in_battle(npc, data)

	def start_hunter(self, data_local, group_a):
		options = [
			format_option(x, {"text": x})
			for x in self.__races.get(data_local, [])]
		options.append(format_option("Voltar", {"text": "back"}))

		count = 0
		while(True):
			if any([x.control for x in group_a]):
				selected = selection_options(
					options, "Caçar na Area:",
					"Escolha uma opção: ")[1]['text']
			else:
				if count == 0:
					selected = random.choice(options[:-1])[1]['text']
				else:
					selected = options[-1][1]['text']
				count += 1
			if selected == "back":
				break
			group_b = self.generator_new_battle([selected], random.randint(1, 10))

			self.sys_battle.init_battle(group_a, group_b, limiter_hp=0)
			result = self.sys_battle.start_battle(any([x.control for x in group_a]))
			self.collect_rewards(result)
			all_control = []
			for npc in group_a:
				if npc.control:
					all_control.append(npc.get_hp()<=0)
			if all(all_control):
				break


class System_dungeons(object):
	def __init__(self):
		pass


if __name__=='__main__':
	from utils import generator_id
	from system_storage import Interaction_Storage
	from system_creatures import System_Creature
	from plants import PLANTS_IN_WORLD

	def generator_name(size=3):
		siglas = []

		for v in 'aeiou':
			for c in 'qwrtypsdfghjklzxcvbnm':
				siglas.append(c+v)
		siglas.extend(['sh', 'th', 'oh'])
		return ''.join([
			random.choice(siglas)
			for x in range(size)
		])

	mob = System_Creature('1')
	plant = Plant(
		name_id="plant-test",
		name="Planta Elcalipito",
		h=6, m=0, d=123,
		items={
			"nightshade": {'min': 0, "max": 5},
		}
	)

	group = [
		System_Creature(f"Jogador-{generator_id(20)}")
		for x in range(1)]
	for npc in group:
		npc.profile.name = generator_name(random.randint(2, 4))
		npc.set_str(10000, False)
		npc.edit_status_max("hp-max", 9999)
	mob = random.choice(group)
	mob.control = True

	app = System_plants()
	app.interaction(mob)

	sys_hunter = System_hunter()
	group_b = sys_hunter.generator_new_battle(["human"], random.randint(1, 10))
	sys_hunter.sys_battle.init_battle(group, group_b, limiter_hp=0)
	result = sys_hunter.sys_battle.start_battle(True)
	sys_hunter.collect_rewards(result)

	interaction = Interaction_Storage()

	options = [
		format_option("tem item", {'text': True}),
		format_option("sair", {'text': False, "default": True}),
	]
	selected = True
	while(selected):
		selected = selection_options(options, "Selecione", "Selecione: ")[1]['text']
		if selected == True:
			interaction.inventory(mob)
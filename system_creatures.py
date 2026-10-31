from system_time import System_Time
from system_storage import System_Inventory, System_Equipments
from system_relationship import System_Tree_Family
from system_magic import System_Status_spellbook
from system_ai_npcs import AI


class System_Attributes(object):
	def __init__(self, strength=10, dexterity=10, constitution=10, intelligence=10, wisdom=10, charisma=10):
		self.attributes = {
			'str': strength, # força padrão do mob / combate
			'dex': dexterity, # destreze padrão do mob / consegui usar arma ou ferramenta
			'con': constitution, # constituição padrão do mob / ordem de ataque em combate
			'int': intelligence, # inteligência padrão do mob / facilidade em aprender magia
			'wis': wisdom, # sabedoria padrão do mob / julgamento
			'cha': charisma # carisma padrão do mob / persuasão
		}
	
	def set_attributes(self, strength=10, dexterity=10, constitution=10, intelligence=10, wisdom=10, charisma=10):
		self.attributes = {
			'str': strength, # força padrão do mob / combate
			'dex': dexterity, # destreze padrão do mob / consegui usar arma ou ferramenta
			'con': constitution, # constituição padrão do mob / ordem de ataque em combate
			'int': intelligence, # inteligência padrão do mob / facilidade em aprender magia
			'wis': wisdom, # sabedoria padrão do mob / julgamento
			'cha': charisma # carisma padrão do mob / persuasão
		}
		for key in self.attributes.keys():
			self.set_attribute(key, 0)

	def get_attribute(self, key):
		return self.attributes.get(key, False)

	def set_attribute(self, key, value, increment=True):
		if key in self.attributes:
			if increment:
				self.attributes[key] += value
			else:
				self.attributes[key] = value
		if self.attributes[key] < 0:
			self.attributes[key] = 0


class System_Skills(object):
	def __init__(self) -> None:
		self.level = 1
		self.exp = 0
		self.exp_base = 324
		self.rate = 0.03

		self.skills = {
			'blacksmith': 0,
			'hunter': 0,
			'lumberjack': 0,
			'alchemist': 0,
		}

	def get_skill_occupation(self):
		return max(self.skills, key=self.skills.get)

	def get_base(self):
		return self.exp_base * self.level

	def get_exp(self):
		return self.exp

	def set_exp(self, amount, increment=True):
		if increment:
			self.exp += amount
		else:
			self.exp = amount
		while(self.get_exp() >= self.get_base()):
			self.exp -= self.get_base()
			self.set_level(1)

	def set_level(self, amount, increment=True):
		if increment:
			self.level += amount
		else:
			self.level = amount
		if self.level < 1:
			self.level = 1

	def get_level(self):
		return self.level


class System_Title(object):
	def __init__(self) -> None:
		self.titles = []

	def set_title(self, titles):
		for title in titles:
			if not title in self.titles:
				self.titles.append(title)
	
	def get_titles(self):
		return tuple([x for x in self.titles])

	def search_title(self, title):
		if title in self.get_titles():
			return True
		return False


class System_Status(object):
	def __init__(self, health=100, stamina=100, mana=100):
		self.status = {
			'hp': health,
			'hp-max': health,
			'st': stamina,
			'st-max': stamina,
			'mp': mana,
			'mp-max': mana,
		}

		self.get_hp = lambda :self.get_status('hp')
		self.get_st = lambda :self.get_status('st')
		self.get_mp = lambda :self.get_status('mp')

		self.set_hp = lambda value, increment=True:self.set_status('hp', value, increment)
		self.set_st = lambda value, increment=True:self.set_status('st', value, increment)
		self.set_mp = lambda value, increment=True:self.set_status('mp', value, increment)

		self.get_hp_max = lambda: self.get_status('hp-max')
		self.get_st_max = lambda: self.get_status('st-max')
		self.get_mp_max = lambda: self.get_status('mp-max')

	def set_status_max(self, key, amount):
		key_index, _ = key.split("-")
		porcents = self.get_status(key_index) / self.status[key]
		self.status[key_index] = int(amount * porcents)
		self.status[key] = amount
		self.set_status(key_index, 0, True)

	def get_status(self, key):
		return self.status.get(key, None)

	def set_status(self, key, value, increment=True):
		if increment:
			if key in self.status:
				self.status[key] += value
		else:
			if key in self.status:
				self.status[key] = value
		if self.status[key] < 0:
			self.status[key] = 0
		if self.status[key] > self.status[f"{key}-max"]:
			self.status[key] = self.status[f"{key}-max"]


class System_Profile(object):
	def __init__(self, name, race, gender):
		self.name = name
		self.race = race
		self.gender = gender

	def get_race(self, race):
		if race != self.race:
			self.race = race


class System_Creature(object):
	def __init__(self, idname):
		self.idname = idname
		self.control = False
		self.titles = System_Title()
		self.inventory = System_Inventory()
		self.equipment = System_Equipments(self)
		self.magic = System_Status_spellbook(self)
		self.brain = AI(self)
		self.relationships = System_Tree_Family()
		self.profile = System_Profile(name=None, race='human', gender='f')
		self.level = System_Skills()
		self.franchisee = []
		self.items_drop = {}
		self.location = [None, None]
		self.status = System_Status(
			health=100,
			stamina=100,
			mana=100)
		self.attributes = System_Attributes(
			strength=10,
			dexterity=10,
			constitution=10,
			intelligence=10,
			wisdom=10,
			charisma=10)

		self.chrono = System_Time(0, 0, 0, 0)

		self.missions = {'missions-currents': [], 'missions-completes': []}

		self.get_id = lambda: self.idname

		self.get_hp = lambda :self.status.get_status('hp')
		self.get_st = lambda :self.status.get_status('st')
		self.get_mp = lambda :self.status.get_status('mp')

		self.set_hp = lambda value, increment=True:self.status.set_status('hp', value, increment)
		self.set_st = lambda value, increment=True:self.status.set_status('st', value, increment)
		self.set_mp = lambda value, increment=True:self.status.set_status('mp', value, increment)

		self.get_hp_max = self.status.get_hp_max
		self.get_st_max = self.status.get_st_max
		self.get_mp_max = self.status.get_mp_max

		self.edit_status_max = lambda key, value: self.status.set_status_max(key, value)

		self.get_str = lambda :self.attributes.get_attribute('str')
		self.get_dex = lambda :self.attributes.get_attribute('dex')
		self.get_con = lambda :self.attributes.get_attribute('con')
		self.get_int = lambda :self.attributes.get_attribute('int')
		self.get_wis = lambda :self.attributes.get_attribute('wis')
		self.get_cha = lambda :self.attributes.get_attribute('cha')

		self.set_str = lambda value, increment=True:self.attributes.set_attribute('str', value, increment)
		self.set_dex = lambda value, increment=True:self.attributes.set_attribute('dex', value, increment)
		self.set_con = lambda value, increment=True:self.attributes.set_attribute('con', value, increment)
		self.set_int = lambda value, increment=True:self.attributes.set_attribute('int', value, increment)
		self.set_wis = lambda value, increment=True:self.attributes.set_attribute('wis', value, increment)
		self.set_cha = lambda value, increment=True:self.attributes.set_attribute('cha', value, increment)

	def add_franchisee(self, markeplace):
		self.franchisee.append(markeplace)

	def get_coins(self):
		return self.inventory.get_coins()

	def remove_franchisee(self, markeplace):
		if marketplace in self.franchisee:
			self.franchisee.remove(markeplace)

	def get_franchisees(self):
		return [x for x in self.franchisee]

	def set_id(self, mob_id):
		if self.idname == mob_id:
			self.idname = mob_id

	def get_damage(self):
		data = {
			"str": [self.get_str(), int],
			"con": [self.get_con(), int],
			"atk": [self.equipment.get_damage_equip(), float],
			"str + con": [(self.get_str() + self.get_con()) * 2, int],
			"mod": [self.level.get_level() * 0.08, float],
		}
		# D=(W+F×0,25) × M
		W, F, M = [data.get(x, [0, int])[0] for x in ["atk", "str", "mod"]]
		data["dano"] = [
			((W + F) * 7.25) * M, int
		]
		value, dtype = data.get("dano", [0, float])
		return dtype(value)

	def get_defense(self):
		data = {
			"con": [self.get_con(), int],
			"def": [self.equipment.get_defense_equip(), int],
			"mod": [1.0+(self.level.get_level() * 0.05), float],
		}
		DEF, _ = data.get("def", [0, None])
		MOD, _ = data.get("mod", [0.001, None])
		CON, _ = data.get("con", [0, None])
		CON = CON / (CON + 300)
		return CON + DEF

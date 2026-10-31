# slave_marketplaces.py
import random
from system_creatures import System_Creature
from jobs import System_hunter
from utils import clear_screen
from utils import generator_name
from utils import table_informations
from utils import selection_options
from utils import table_show_label
from utils import format_option
from utils import generator_id

def get_age_range(user):
	age = user.chrono.get_y()
	age_range = ""
	if age >= 0 and age <= 3:
		age_range = "bêbê"
	if age > 3 and age <= 9:
		age_range = "criança"
	if age > 9 and age <= 14:
		age_range = "pré-adolescente"
	if age > 14 and age <= 17:
		age_range = "adolescente"
	if age > 17 and age <= 21:
		age_range = "joven adulto"
	if age > 21 and age <= 50:
		age_range = "adulto"
	if age > 50 and age <= 60:
		age_range = "idoso"
	if age > 60:
		age_range = "ansião"
	return age_range


class Marketplace_slave(object):
	def __init__(self, world, own, species=['human']):
		self.species = species
		self.world = world
		self.hunter = System_hunter()
		self.colletions = []

	def generator(self):
		amount = random.randint(len(self.species) + 1, len(self.species) + 5)
		level = random.randint(1, 10)
		group = self.hunter.generator_new_battle(
			self.species, level, amount)
		for npc in group:
			npc.set_id(generator_id(25, "@ID:"))
			npc.profile.name = generator_name(random.randint(2, 3))
			npc.chrono.set_values("y", random.randint(1, 40))
		self.colletions = [x for x in group]

	def description_npc(self, user):
		age = user.chrono.get_y()
		age_range = get_age_range(user)
		value = self.get_value(user)
		data = {
			"nome": user.profile.race if user.profile.name is None else user.profile.name,
			"idade": f"{age}, {age_range}",
			"valor": f"{value} G",
			'dano': user.get_damage(),
			'defesa': f"{user.get_defense()*100:^.2f}% (Redução de dano)",
		}
		return table_informations(data, "Descrição do Escravo")

	def choose_slave(self, master, slave):
		options = [
			format_option("Comprar", {"text": "buy"}),
			format_option("voltar", {"text": "back"})
		]
		while(True):
			selected = selection_options(options,
				f"{self.description_npc(slave)}\n\nO que quer fazer?",
				"Escolha uma opção: ")[1]['text']
			if selected == 'back':
				break
			else:
				value = self.get_value(slave)
				if self.maker_contract(master, slave):
					master.inventory.remover_item("gold", value)
					self.colletions.remove(slave)
					break
				else:
					clear_screen()
					gold = master.get_coins()
					value = self.get_value(slave)
					result = table_show_label("Aviso !!!!", f"O valor é {value} G e você tem só {gold} G!\nVocê não tem dinheiro. :/")
					input(result)

	def maker_contract(self, master, slave, ignore_cust=False):
		value = self.get_value(slave)
		if master.get_coins() >= value or ignore_cust:
			slave.relationships.add_tags(master, "master")
			master.relationships.add_tags(slave, "slave")
			slave.location = [x for x in master.location]
			self.world.add_creature(slave)
			return True
		return False

	def get_value(self, user):
		a = [
			(user.get_str, 0.01), (user.get_dex, 0.01),
			(user.get_con, 0.01), (user.get_int, 0.01),
			(user.get_wis, 0.01), (user.get_cha, 0.01),
		]
		value = user.level.get_level() * 320
		y = user.chrono.get_y()
		mult = max(0, (1.0 - (y / 100)))
		
		for n, m in a:
			value += (n() * m) * value
		value += mult * value
		return int(value)

	def buy(self, user):
		while(True):
			options = []
			for npc in self.colletions:
				age = npc.chrono.get_y()
				age_range = get_age_range(npc)
				value = self.get_value(npc)
				op = format_option(
					f"{npc.profile.race} {age_range}, {value} G",
					{"text": npc, "value": value})
				options.append(op)
			options.append(
				format_option("voltar",
					{
						"text": "back",
						"hotkey": ["b", 'v'],
						"default": True
					}
				))
			selected = selection_options(options,
				"Feras disponiveis para compra:",
				"Escolha uma opção: ")[1]["text"]
			if selected == "back":
				break
			else:
				self.choose_slave(user, selected)

	def sell_slave(self, master, slave):
		from system_items import all_items
		value = int(self.get_value(slave) * 0.9)
		options = [
			format_option("Vender a fera", {'text': "sell"}),
			format_option("Deixar pra lá", {"text": "back"})
		]
		while(True):
			title = f"{self.description_npc(slave)}\n\nQuer mesmo vender esta fera?"
			selected = selection_options(options, title, "Escolha uma opção: ")[1]['text']
			if selected == "back":
				break
			elif selected == 'sell':
				slave.relationships.remove_tag("master", master)
				master.relationships.remove_tag("slave", slave)
				master.inventory.add_item(
					all_items.get("gold"), value)
				break

	def sell(self, user):
		while(True):
			options = []
			for npc_id in user.relationships.get_members_per_tag("slave"):
				npc = self.world.get_creature(npc_id)
				if npc != False:
					age = npc.chrono.get_y()
					age_range = get_age_range(npc)
					value = int(self.get_value(npc) * 0.9)
					op = format_option(
						f"{npc.profile.race} {age_range}, {value} G",
						{"text": npc, "value": value})
					options.append(op)
			options.append(format_option("voltar", {"text": "back"}))
			selected = selection_options(options, "Feras que você tem:", "Escolha uma opção: ")[1]["text"]
			if selected == "back":
				break
			else:
				self.sell_slave(user, selected)

	def main(self, user):
		options = [
			format_option("comprar feras", {"text": "buy"}),
			format_option("vender feras", {"text": "sell"}),
			format_option("voltar", {"text": "back"}),
		]
		while(True):
			selected = selection_options(options,
				"Barraca de escravos:",
				"Escolha uma opção: ")[1]["text"]
			if selected == "back":
				break
			if selected == 'buy':
				self.buy(user)
			if selected == 'sell':
				self.sell(user)


class Dumb:
	def __init__(self):
		self.entities_in_world = {}

	def add_creature(self, mob):
		idname = mob.get_id()
		if not idname in self.entities_in_world:
			self.entities_in_world[idname] = mob

	def get_creature(self, idname):
		return self.entities_in_world.get(idname, False)

	def remove_creature(self, idname):
		if idname in self.entities_in_world and not 'player' in self.entities_in_world:
			del self.entities_in_world[idname]


if __name__=="__main__":
	from system_items import all_items

	proprietario = System_Creature("o012")
	app = Marketplace_slave(Dumb(), proprietario, species=['human'])
	app.generator()
	for npc in app.colletions:
		print(app.description_npc(npc), end="\n\n")

	user = System_Creature("player")
	user.inventory.add_item(all_items["gold"], 12300)

	app.buy(user)
	app.sell(user)
	print(user.relationships.get_members_per_tag("slave"))
	print(user.relationships.knowledge)
	print("\nGold:", user.get_coins())
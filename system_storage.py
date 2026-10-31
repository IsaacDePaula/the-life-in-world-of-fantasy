class Slot(object):
	def __init__(self, tag):
		self.tag = tag
		self.info = None
		self.amount = 0

	def get_item(self):
		if self.info is None:
			return False
		else:
			return self.info

	def set_item(self, item):
		self.info = item

	def get_amount(self):
		return self.amount

	def set_amount(self, amount, increment=True):
		if increment:
			self.amount += amount
		else:
			self.amount = amount
		if self.amount < 0:
			self.amount = 0

	def is_empty(self):
		return self.info is None

	def update_slot(self):
		if self.info is None or self.amount < 1:
			self.info = None
			self.amount = 0

class System_Inventory(object):
	def __init__(self):
		self.slots = []
		self.limiter = 9999
		self.init_all_slots()

	def init_all_slots(self):
		for i in range(10*10):
			self.slots.append(Slot(f"#slot:{i}"))

	def get_coins(self):
		slots, total = self.search_item("gold").values()
		return total

	def set_coins(self, amount):
		slots, total = self.search_item("gold").values()
		if total >= amount:
			for slot in slots:
				increment = amount
				if slot.get_amount() < amount:
					increment = slot.get_amount()
				slot.set_amount(-increment)
				amount -= increment
				slot.update_slot()

	def add_coins(self, amount):
		from system_items import all_items
		item = all_items.get("gold")
		self.add_item(item, amount)

	def remover_coins(self, amount):
		self.remover_item("gold", amount)

	def search_item(self, itemID):
		information = {'slots':[], 'total':0}
		for slot in self.slots:
			if slot.is_empty():
				continue
			if not slot.get_item() is None:
				if slot.get_item()['id'] == itemID:
					information['slots'].append(slot)
					information['total'] += slot.get_amount()
		return information

	def increment_item(self, total, need):
		values = [1, 9, 25, 50, 75, 99, 999, 9999, 99999, 999999, self.limiter]
		increment = 0
		for i in [x for x in values if x <= self.limiter]:
			if i <= need and i+total <= self.limiter:
				increment = i
		return increment

	def organize(self):
		self.slots = [x for x in sorted(self.slots, key=lambda n: n.get_amount())]
		self.slots = self.slots[::-1]

	def get_slots(self):
		return [x for x in self.slots if not x.is_empty()]

	def add_item(self, item, amount):
		for slot in self.slots:
			if amount <= 0:
				continue
			if slot.is_empty():
				slot.set_item(item)
				increment = self.increment_item(slot.get_amount(), amount)
				while(increment > 0 and amount > 0):
					increment = self.increment_item(slot.get_amount(), amount)
					slot.set_amount(increment)
					amount -= increment
			elif slot.get_item() == item:
				increment = self.increment_item(slot.get_amount(), amount)
				while(increment > 0 and amount > 0):
					increment = self.increment_item(slot.get_amount(), amount)
					slot.set_amount(increment)
					amount -= increment
		if amount > 0:
			i = len(self.slots)
			self.slots.append(Slot(f"#slot:{i}"))
			self.add_item(item, amount)
		self.organize()

	def remover_item(self, itemID, amount):
		slots, total = self.search_item(
			itemID).values()
		if total >= amount:
			for slot in slots:
				if amount <= 0:
					break
				increment = amount if amount <= slot.get_amount() else slot.get_amount()
				slot.set_amount(-increment)
				amount -= increment
				slot.update_slot()
		return amount <= 0


class System_Equipments(object):
	def __init__(self, entitie):
		self.entitie = entitie
		self.slots = {
			'head': Slot("head"),
			'body': Slot("body"),
			'legs': Slot("legs"),
			'foot': Slot("foot"),
			'hand-r': Slot("hand-r"),
			'hand-l': Slot("hand-l"),
		}

	def get_damage_equip(self):
		damage = [slot.get_item().get("damage", 0)
			for slot in self.slots.values()
		if not slot.is_empty()]
		return sum(damage)

	def get_defense_equip(self):
		defense = [slot.get_item().get("defense", 0)
			for slot in self.slots.values()
		if not slot.is_empty()]
		return sum(defense)

	def equip_item(self, item, direction="r"):
		set_slot = item.get("slot", False)
		if set_slot == "hand":
			set_slot += f"-{direction}"
		slot = self.slots[set_slot]
		item_in_slot = slot.get_item()
		amount_in_slot = slot.get_amount()
		slot.set_item(item)
		slot.set_amount(1, False)
		return item_in_slot, amount_in_slot

	def unquip_item(self, slot):
		item_in_slot = slot.get_item()
		amount_in_slot = slot.get_amount()
		slot.set_amount(0, False)
		slot.update_slot()
		return item_in_slot, amount_in_slot		


class System_Transfery(object):
	@staticmethod
	def exchanger(self, user, target, slot):
		item = slot.get_item()
		amount = slot.get_amount()
		target.inventory.add_item(item, amount)
		slot.set_amount(0, False)
		slot.update_slot()


class System_Chests(object):
	def __init__(self):
		self.inventory = System_Inventory()

	def interaction(self, user):
		options = [
			format_option("Mover para o báu", {"text": 'user_to_chest'}),
			format_option("Remover do báu", {"text": 'chest_to_user'}),
			format_option("Voltar", {"text": 'back', 'default': True}),
		]
		while(True):
			selected = selection_options(options,
				"Báu local", "Escolha uma opção: ")[1]['text']
			if selected == "back":
				break
			elif selected == 'chest_to_user':
				self.chest_to_user(user)
			elif selected == 'user_to_chest':
				self.user_to_chest(user)

	def user_to_chest(self, user):
		while(True):
			options = []
			for slot in user.inventory.slots:
				if slot.is_empty():
					continue
				item = slot.get_item()
				name = item.get("name")
				amount = slot.get_amount()
				options.append(format_option(f"{amount}x {name}", {'text': slot}))
			options.append(format_option("Voltar", {"text": False, 'default': True}))

			selected = selection_options(options,
				"Escolha um item para mover para báu!",
				"Escolha uma ação: ")[1]['text']
			if selected == False:
				break
			else:
				item = selected.get_item()
				amount = selected.get_amount()
				print(f"{amount}x {item.get('name')} foi transferido com sucesso ao báu.")
				System_Transfery.exchanger(user, self, selected)
				input("\n\nPressione Enter")

	def chest_to_user(self, user):
		while(True):
			options = []
			for slot in self.inventory.slots:
				if slot.is_empty():
					continue
				item = slot.get_item()
				name = item.get("name")
				amount = slot.get_amount()
				options.append(format_option(f"{amount}x {name}", {'text': slot}))
			options.append(format_option("Voltar", {"text": False, 'default': True}))

			selected = selection_options(options,
				"Escolha um item para remover do báu!",
				"Escolha uma ação: ")[1]['text']
			if selected == False:
				break
			else:
				item = selected.get_item()
				amount = selected.get_amount()
				print(f"{amount}x {item.get('name')} foi removido do báu com sucesso.")
				System_Transfery.exchanger(self, user, selected)
				input("\n\nPressione Enter")


from utils import format_option, selection_options
class Interaction_Storage(object):
	def selected_direction_slot_hand(self):
		options = [
			format_option("Mão Direita", {"text": "r"}),
			format_option("Mão Esquerda", {"text": "l"}),
			format_option("Mão Padrão", {"text": "r", "default": True}),
		]
		return selection_options(options,
			"Deseja equipar este item em qual mão?",
			"Escolha uma opção: ")[1]['text']

	def edit_item(self, user, slot):
		from utils import clear_screen
		while(True):
			item = slot.get_item()
			# input(f'{item}')
			text_consumible = "Usar"
			if not "consumible" in item.get("type", []):
				text_consumible = None
			text_equipable = "Equipar"
			if item.get("equip", False) == False:
				text_equipable = None
			text_discart = "Descartar"
			options = [
				format_option(text_consumible, {'text': 'use'}),
				format_option(text_equipable, {'text': 'equip'}),
				format_option(text_discart, {'text': 'discart'}),
				format_option('Voltar', {'text': 'back', 'default': True}),
			]
			title = "Status:\n"
			title += f" Nome: {item['name']}\n"
			title += f" descrição: {item['description']}\n\n"
			title += f'O que quer fazer com x{slot.get_amount()} {slot.get_item()["name"]}:'
			select = selection_options(options, title,
				'Escolha uma opção: ')[1]['text']
			if select == 'back':
				slot.update_slot()
				break
			if select == "equip":
				direction = 'r'
				if item.get("slot") == "hand":
					direction = self.selected_direction_slot_hand()
				item_result, amount = user.equipment.equip_item(item, direction)
				clear_screen()
				print("Resultado:")
				if type(item_result) == dict:
					user.inventory.add_item(item_result, amount)
					print(f" Foi desequipado {item_result.get('name')} com sucesso!")
				slot.set_amount(-1); slot.update_slot()
				print(f" {item.get('name')} foi equipado com sucesso!")
				input(f"\nPressione enter para continuar.")
				if not slot.get_amount() > 0:
					break

	def open_inventory_for_equip(self, user, slot):
		while(True):
			key_slot = slot.tag.split("-")[0]
			items_in_inventory_equipable = []
			damage_current = 0
			defense_current = 0
			if not slot.is_empty():
				damage_current = slot.get_item().get("damage", 0)
				defense_current = slot.get_item().get("defense", 0)

			for slot_inventory in user.inventory.get_slots():
				item = slot_inventory.get_item()
				amount = slot_inventory.get_amount()
				if item.get("slot", False) == key_slot:
					damage = item.get("damage", 0)
					defense = item.get("defense", 0)
					damage_text = f'{"+" if damage > damage_current else "-"}{item.get("damage", 0)}'
					if damage == damage_current:
						damage_text = f'{item.get("damage", 0)}'
					defense_text = f'{"+" if defense > defense_current else "-"}{(item.get("defense", 0)*100):^.2f}%'
					if defense == defense_current:
						defense_text = f'{(item.get("defense", 0)*100):^.2f}%'
					name = f"{amount}x {item.get('name')} [ATK: {damage_text}, DEF: {defense_text}]"
					items_in_inventory_equipable.append(format_option(name, {'text': slot_inventory}))
			
			items_in_inventory_equipable.append(format_option("voltar", {"text": "back"}))
			selected = selection_options(items_in_inventory_equipable,
				f"Items que podem ser equipados nesse slot: [{key_slot}]",
				"Escolha uma opção: ")[1]['text']
			if selected == "back":
				break
			else:
				direction = "r"
				if key_slot == 'hand':
					_, direction = slot.tag.split("-")
				item = selected.get_item()
				item_result, amount_result = user.equipment.equip_item(item, direction)
				selected.set_amount(-1); selected.update_slot()
				print(f"{item.get('name')} foi equipado com sucesso!")
				if not item_result == False:
					print(f" Adicionado {amount_result}x {item_result.get('name')} ao seu inventario!")
				input("\nPressione Enter.")
				break

	def get_informations_equipments(self, user):
		texts_lines = "Dados de Equipamentos\n"
		total_damage_in_equipments = 0
		total_defense_in_equipments = 0
		max_x = max([len(x) for x in user.equipment.slots.keys()])
		for tag, slot in user.equipment.slots.items():
			key_slot = tag
			damage = 0
			if not slot.is_empty():
				damage = slot.get_item().get("damage", 0)
			defense = 0
			if not slot.is_empty():
				defense = slot.get_item().get("defense", 0)
			texts_lines += f" {key_slot.ljust(max_x, ' ')}: ATK: {damage} / DEF: {(defense * 100):^.2f}%\n"
			total_damage_in_equipments += damage
			total_defense_in_equipments += defense
		texts_lines += f"\nTotal Dano: {total_damage_in_equipments}\n"
		texts_lines += f"Total Defesa: {(total_defense_in_equipments*100):^.2f}%\n"
		return texts_lines

	def equipment(self, user):
		while(True):
			options = []
			for tag, slot in user.equipment.slots.items():
				text = f"{tag} -> "
				if not slot.is_empty():
					item = slot.get_item()
					name = item.get("name")
					damage = item.get("damage")
					defense = item.get("defense")
					text += f"{name} / ATK: {damage} / DEF: {(defense * 100):^.2f}%"
				else:
					text += "Nada Equipado"
				options.append(format_option(text, {'text': slot}))
			options.append(format_option("Voltar", {'text': "back"}))
			title = self.get_informations_equipments(user)
			selected_slot = selection_options(options, 
				f"{title}\nEquipamentos de {user.profile.name}:",
				"Escolha uma opção: ")[1]['text']
			if selected_slot == "back":
				break
			else:
				self.open_inventory_for_equip(user, selected_slot)

	def inventory(self, user):
		while(True):
			options = []
			for slot in user.inventory.slots:
				if slot.is_empty():
					continue
				name = slot.get_item()['name']
				options.append(
					format_option(
						f'SLOT: x{slot.get_amount()} {name}',
						{'text': slot, 'amount': slot.get_amount()}))
			options.append(format_option('Voltar', {'text': 'back', 'default': True}))
			select = selection_options(options,
				f"Inventario de {user.profile.name}:",
				"Escolha uma opção: ")[1]
			if select['text'] == 'back':
				break
			self.edit_item(user, select['text'])


if __name__=='__main__':
	from system_creatures import System_Creature
	from system_items import all_items
	import random

	user = System_Creature('id:user')
	sys = Interaction_Storage()
	for item in all_items.values():
		user.inventory.add_item(item, random.randint(1, 2))
	# sys.inventory(user)
	while(True):
		options = [
			format_option('Inventario', {'text': 'inventory'}),
			format_option('Equipamentos', {'text': 'equipment'}),
			format_option('adicionar item aleatorio', {'text': 'random:item', 'default': True})
		]
		select = selection_options(options, '', "Escolha uma ação: ")[1]['text']
		if select == 'back':
			break
		elif select == 'inventory':
			sys.inventory(user)
		elif select == "equipment":
			sys.equipment(user)
		elif select == 'random:item':
			item = all_items[random.choice(list(all_items.keys()))]
			amount = random.randint(1, 10)

			input(f"Adicionado x{amount} {item['name']} no seu inventario.")
			user.inventory.add_item(item, amount)

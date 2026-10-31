# slave_interaction.py
import random
from slave_marketplaces import get_age_range
from utils import format_option, selection_options, clear_screen, table_show_label

TEXT_GROUP_NO_COMPANION = " (ESTÁ NO GRUPO DE COMBATE)"
TEXT_GROUP_NOT_COMPANION = " (NÃO ESTÁ NO GRUPO DE COMBATE)"


class Interaction_slave(object):
	def __init__(self, world):
		self.world = world

	def get_description(self, slave):
		text_lines = ""
		return text_lines

	def options_interactions(self, user, slave):
		while(True):
			options = []
			if user.relationships.search_tag("companion", slave):
				options.append(format_option("Remover do Grupo", {"text":"remover"}))
			else:
				options.append(format_option("Adicionar ao Grupo", {"text":"add"}))
			options.extend([
				format_option("Conversar", {"text": "chat"}),
				format_option("Ensinar a lutar", {"text": "lesson"}),
				format_option("Equipar Item", {"text": "equip-item"}),
				format_option("Dar item", {"text": "give-item"}),
				format_option("Dar comida", {"text": "food"}),
				format_option("Voltar", {"text": "back"}),
			])
			title_increment = self.get_description(slave)
			selected = selection_options(options, f"{title_increment}\n\nO que quer fazer?", "Escolha uma opção: ")[1]["text"]
			if selected == "back":
				break
			elif selected == "add":
				user.relationships.add_tags(slave, "companion")
			elif selected == "remover":
				user.relationships.remove_tag("companion", slave)
			elif selected == "chat":
				clear_screen()
				texts_lines = ""
				if random.random() > 0.3:
					texts_lines += f"você fala para {slave.profile.name} escuta e se sente melhor."
				else:
					texts_lines += f"você fala para {slave.profile.name} escuta e fica um pouco mais assustada."
				input(table_show_label("Resultado", texts_lines))

	def get_item(self, user, type_item=["weapon"]):
		options = []
		for slot in user.inventory.slots:
			if slot.is_empty():
				continue
			item = slot.get_item()
			amount = slot.get_amount()
			name = item.get("name")
			can_continue = False
			for tag in type_item:
				if can_continue:
					break
				if tag in item.get("type"):
					can_continue = True
			if not can_continue:
				continue
			options.append(
				format_option(f"{amount}x {name}", {'text': slot}))
		options.append(format_option("cancelar", {'text': False}))
		return selection_options(options, "Selecione um item:",
			"Escolha uma opção: ")[1]['text']

	def equip_item(self, user, target, slot):
		item = slot.get_item()
		item_r, amount_r = target.equipment.equip_item(item)
		if not item_r is None:
			user.inventory.add_item(item_r, amount_r)


	def information_equipments(self, user):
		user_name = user.profile.name
		if user_name is None:
			user_name = user.profile.race+user.profile.gender
		texts_lines = f"Equipamentos de {user_name}\n"
		for key, slot in user.equipment.slots.items():
			if slot.is_empty():
				continue
			item = slot.get_item()
			damage = item.get("damage", 0)
			defense = item.get("defense", 0.0) * 100
			text = f"{key} | ATK: {damage} DEF: {defense:^.2f}%%\n"
			texts_lines += text
		return texts_lines

	def get_item_per_slot(self, user, slot_tag=None):
		options = []
		for slot in user.inventory.slots:
			if slot.is_empty():
				continue
			item = slot.get_item()
			if item.get("slot", False) == slot_tag:
				name = item.get("name")
				amount = slot.get_amount()
				defense = item.get("defense", 0) * 100
				damage = item.get("damage", 0)
				text = f"{amount}x {name} def: {defense}%% atk: {damage}"
				options.append(format_option(text, {'text': slot}))
		options.append(format_option("Voltar", {"text": False}))
		return selection_options(options,
			"Item compativel com o slot de equipamento: ",
			"Escolha uma opção: ")[1]['text']

	def apply_equip_in_slot(self, user, target, slot):
		while(True):
			options = [
				format_option("Equipar item" if slot.is_empty() else None, {'text': "equip"}),
				format_option("Trocar equipamento" if not slot.is_empty() else None, {'text': "change"}),
				format_option("Desequipar item" if not slot.is_empty() else None, {'text': "unquip"}),
				format_option("Voltar", {'text': "back"}),
			]
			title = "Não há nada equipado\n"
			title += "Quer fazer o que?"
			selected = selection_options(options, title, "Escolha uma opção: ")[1]['text']
			if selected == "back":
				break

	def interaction_equipments(self, user, target):
		while(True):
			title = self.information_equipments(target)
			title += "\nO que quer fazer?"
			options = []
			for key, slot in target.equipment.slots.items():
				text = f"{key}"
				damage = 0
				defense = 0
				if not slot.is_empty():
					item = slot.get_item()
					damage = item.get('damage', 0)
					defense = item.get('defense', 0) * 100
					text += f" ATK: {damage} DEF: {defense}"
				options.append(format_option(text, {'text': slot}))
			options.append(format_option("voltar", {"text": "back"}))
			selected = selection_options(options, title, "Escolha uma opção: ")[1]['text']
			if selected == "back":
				break
			else:
				self.apply_equip_in_slot(user, target, selected)

	def interaction(self, user):
		while(True):
			options = []
			companions = user.relationships.get_members_per_tag("companion")
			for npc_id in user.relationships.get_members_per_tag("slave"):
				npc = self.world.get_creature(npc_id)
				if npc != False:
					name = npc.profile.name
					name = "Sem nome" if name is None else name
					race = npc.profile.race
					text = f"{name} {race}"
					if npc.profile.gender in "fh":
						text = f"Uma {get_age_range(npc)} {race} {name}"
						if npc.get_id() in companions:
							text += TEXT_GROUP_NO_COMPANION
						op = format_option(text, {"text": npc})
						options.append(op)
					if npc.profile.gender == "m":
						text = f"Um {get_age_range(npc)} {race} {name}"
						op = format_option(text, {"text": npc})
						if npc.get_id() in companions:
							text += TEXT_GROUP_NO_COMPANION
						options.append(op)
			options.append(format_option("Voltar", {"text": "back"}))
			selected = selection_options(options,
				"Feras que estão com você:",
				"Escolha uma opção: ")[1]["text"]
			if selected == "back":
				break
			else:
				self.options_interactions(
					user, selected)


if __name__=="__main__":
	from system_creatures import System_Creature
	from slave_marketplaces import Marketplace_slave
	from slave_marketplaces import Dumb
	from system_items import all_items

	world = Dumb()
	market = Marketplace_slave(world, None)
	market.generator()

	user = System_Creature("Calango")
	user.profile.name = "Comedor de Cu"
	world.add_creature(user)

	for item in all_items.values():
		user.inventory.add_item(item, random.randint(1, 2))

	slaves = []
	for i in range(len(market.colletions)):
		npc = market.colletions[i]
		if not npc in slaves:
			slaves.append(npc)

	for npc in slaves:
		market.maker_contract(user, npc, ignore_cust=True)

	# for npc in slaves:
	# 	print(world.get_creature(npc.get_id()))
	# input(f"len: {len(slaves)}, knowledge: {user.relationships.knowledge}, Amount knowledge: {len(user.relationships.knowledge)}")

	app = Interaction_slave(world)
	app.interaction(user)

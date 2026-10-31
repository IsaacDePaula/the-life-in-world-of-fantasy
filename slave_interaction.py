# slave_interaction.py

import random

from slave_marketplaces import get_age_range
from utils import (
	format_option,
	selection_options,
	clear_screen,
	table_show_label
)


TEXT_GROUP_NO_COMPANION = " (ESTÁ NO GRUPO DE COMBATE)"
TEXT_GROUP_NOT_COMPANION = " (NÃO ESTÁ NO GRUPO DE COMBATE)"


class Interaction_slave(object):

	def __init__(self, world):
		self.world = world

	# ---------------------------------------------------------
	# INFORMAÇÕES DO NPC
	# ---------------------------------------------------------

	def get_description(self, slave):
		name = slave.profile.name or "Sem nome"
		race = slave.profile.race or "Desconhecida"

		gender = slave.profile.gender

		genders = {
			"f": "Feminino",
			"m": "Masculino",
			"h": "Hermafrodita"
		}

		gender_name = genders.get(
			gender,
			str(gender).capitalize() if gender else "Não informado"
		)

		attack = slave.get_damage()
		defense = slave.get_defense() * 100

		return (
			f"Nome: {name}\n"
			f"Raça: {race}\n"
			f"Sexo: {gender_name}\n"
			f"Ataque: {attack:.2f}\n"
			f"Defesa: {defense:.2f}%"
		)

	def _show_result(self, message):
		clear_screen()
		input(table_show_label("Resultado", message))

	# ---------------------------------------------------------
	# UTILITÁRIOS
	# ---------------------------------------------------------

	@staticmethod
	def _item_types(item):
		item_types = item.get("type", []) or []

		if isinstance(item_types, str):
			return [item_types]

		return item_types

	@staticmethod
	def _remove_from_slot(slot, amount=1):
		if slot is None or slot.is_empty() or amount <= 0:
			return False

		if slot.get_amount() < amount:
			return False

		slot.set_amount(-amount)
		slot.update_slot()

		return True

	@staticmethod
	def _get_equipment_key(item_slot, direction="r"):
		if item_slot == "hand":
			return f"hand-{direction}"

		return item_slot

	# ---------------------------------------------------------
	# MENU PRINCIPAL
	# ---------------------------------------------------------

	def options_interactions(self, user, slave):

		while True:

			options = []

			if user.relationships.search_tag("companion", slave):
				options.append(
					format_option(
						"Remover do Grupo",
						{"text": "remover"}
					)
				)
			else:
				options.append(
					format_option(
						"Adicionar ao Grupo",
						{"text": "add"}
					)
				)

			options.extend([
				format_option("Conversar", {"text": "chat"}),
				format_option("Ensinar a lutar", {"text": "lesson"}),
				format_option("Equipar Item", {"text": "equip-item"}),
				format_option("Dar item", {"text": "give-item"}),
				format_option("Dar comida", {"text": "food"}),
				format_option("Voltar", {"text": "back"})
			])

			selected = selection_options(
				options,
				self.get_description(slave) + "\n\nO que quer fazer?",
				"Escolha uma opção: "
			)[1]["text"]

			if selected == "back":
				break

			elif selected == "add":
				user.relationships.add_tags(slave, "companion")

			elif selected == "remover":
				user.relationships.remove_tag("companion", slave)

			elif selected == "chat":
				self.interaction_chat(slave)

			elif selected == "lesson":
				# Implementação reservada para o futuro.
				pass

			elif selected == "equip-item":
				self.interaction_equip_item(user, slave)

			elif selected == "give-item":
				self.give_item(user, slave)

			elif selected == "food":
				self.give_food(user, slave)

	# ---------------------------------------------------------
	# CONVERSAR
	# ---------------------------------------------------------

	def interaction_chat(self, slave):

		roll = random.randint(1, 20)

		if roll >= 11:

			message = (
				f"A conversa com {slave.profile.name or 'o NPC'} "
				f"foi bem-sucedida!\n"
				f"Resultado do dado: {roll}/20"
			)

		else:

			message = (
				f"{slave.profile.name or 'O NPC'} não parece "
				f"disposto a conversar agora.\n"
				f"Resultado do dado: {roll}/20"
			)

		self._show_result(message)

	# ---------------------------------------------------------
	# SELEÇÃO DE ITENS DO INVENTÁRIO
	# ---------------------------------------------------------

	def get_item(self, user, type_item=None, equipment_slot=None):

		options = []

		for inventory_slot in user.inventory.slots:

			if inventory_slot.is_empty():
				continue

			item = inventory_slot.get_item()

			if not item:
				continue

			if type_item:
				item_types = self._item_types(item)

				if not any(tag in item_types for tag in type_item):
					continue

			if equipment_slot:

				item_slot = item.get("slot")

				if equipment_slot.startswith("hand-"):

					if item_slot != "hand":
						continue

				elif item_slot != equipment_slot:
					continue

			options.append(
				format_option(
					f"{inventory_slot.get_amount()}x "
					f"{item.get('name', 'Item sem nome')}",
					{"text": inventory_slot}
				)
			)

		options.append(
			format_option("Voltar", {"text": False})
		)

		return selection_options(
			options,
			"Selecione um item:",
			"Escolha uma opção: "
		)[1]["text"]

	# ---------------------------------------------------------
	# EQUIPAR ITEM
	# ---------------------------------------------------------

	def equip_item(self, user, target, inventory_slot, direction="r"):

		if (
			inventory_slot is None
			or inventory_slot is False
			or inventory_slot.is_empty()
		):
			return False

		item = inventory_slot.get_item()

		if not item:
			return False

		item_slot = item.get("slot")

		equipment_key = self._get_equipment_key(
			item_slot,
			direction
		)

		if equipment_key not in target.equipment.slots:
			return False

		# Remove primeiro do inventário para evitar duplicação.
		if not self._remove_from_slot(inventory_slot, 1):
			return False

		try:

			old_item, old_amount = target.equipment.equip_item(
				item,
				direction=direction
			)

		except (KeyError, TypeError, AttributeError):

			# Devolve o item ao inventário caso o equipamento falhe.
			user.inventory.add_item(item, 1)
			return False

		# Devolve o equipamento anterior ao mestre.
		if old_item:
			user.inventory.add_item(old_item, old_amount)

		return True

	# ---------------------------------------------------------
	# DESEQUIPAR ITEM
	# ---------------------------------------------------------

	def unequip_item(self, user, target, equipment_key):

		if equipment_key not in target.equipment.slots:
			return False

		equipment_slot = target.equipment.slots[equipment_key]

		if equipment_slot.is_empty():
			return False

		item, amount = target.equipment.unquip_item(
			equipment_slot
		)

		if not item:
			return False

		user.inventory.add_item(item, amount)

		return True

	# ---------------------------------------------------------
	# MENU DE AÇÕES DO SLOT
	# ---------------------------------------------------------

	def apply_equip_in_slot(self, user, target, equipment_key):

		if equipment_key not in target.equipment.slots:
			return False

		equipment_slot = target.equipment.slots[equipment_key]

		while True:

			options = []

			if equipment_slot.is_empty():

				options.append(
					format_option(
						"Equipar",
						{"text": "equip"}
					)
				)

			else:

				options.extend([
					format_option(
						"Troca de equipamento",
						{"text": "swap"}
					),
					format_option(
						"Desequipar item",
						{"text": "unequip"}
					)
				])

			options.append(
				format_option(
					"Voltar",
					{"text": "back"}
				)
			)

			selected = selection_options(
				options,
				self.information_equipments(target)
				+ f"\nSlot selecionado: {equipment_key}\n\n"
				+ "O que deseja fazer?",
				"Escolha uma opção: "
			)[1]["text"]

			if selected == "back":
				return False

			# ---------------------------------------------
			# EQUIPAR
			# ---------------------------------------------

			if selected == "equip":

				inventory_slot = self.get_item(
					user,
					equipment_slot=equipment_key
				)

				if inventory_slot is False:
					continue

				direction = (
					equipment_key[-1]
					if equipment_key.startswith("hand-")
					else "r"
				)

				item = inventory_slot.get_item()

				if self.equip_item(
					user,
					target,
					inventory_slot,
					direction
				):

					self._show_result(
						f"{item.get('name', 'Item')} foi equipado "
						f"em {target.profile.name or 'NPC'}."
					)

					return True

				self._show_result(
					"Não foi possível equipar esse item."
				)

			# ---------------------------------------------
			# TROCAR EQUIPAMENTO
			# ---------------------------------------------

			elif selected == "swap":

				inventory_slot = self.get_item(
					user,
					equipment_slot=equipment_key
				)

				if inventory_slot is False:
					continue

				direction = (
					equipment_key[-1]
					if equipment_key.startswith("hand-")
					else "r"
				)

				new_item = inventory_slot.get_item()

				if self.equip_item(
					user,
					target,
					inventory_slot,
					direction
				):

					self._show_result(
						f"Equipamento trocado com sucesso!\n"
						f"Novo item: {new_item.get('name', 'Item')}\n"
						f"O equipamento anterior foi devolvido "
						f"ao seu inventário."
					)

					return True

				self._show_result(
					"Não foi possível trocar o equipamento."
				)

			# ---------------------------------------------
			# DESEQUIPAR
			# ---------------------------------------------

			elif selected == "unequip":

				item = equipment_slot.get_item()

				if self.unequip_item(
					user,
					target,
					equipment_key
				):

					self._show_result(
						f"{item.get('name', 'Item')} foi removido "
						f"do equipamento de "
						f"{target.profile.name or 'NPC'}.\n"
						f"O item foi devolvido ao seu inventário."
					)

					return True

				self._show_result(
					"Não foi possível desequipar esse item."
				)

	# ---------------------------------------------------------
	# MENU DE EQUIPAMENTOS DO NPC
	# ---------------------------------------------------------

	def interaction_equip_item(self, user, target):

		while True:

			options = []

			for key, slot in target.equipment.slots.items():

				label = key

				if slot.is_empty():

					label += " | Nada equipado"

				else:

					item = slot.get_item()

					label += (
						f" | {item.get('name', 'Item')}"
						f" | ATK: {item.get('damage', 0)}"
						f" | DEF: "
						f"{item.get('defense', 0) * 100:.2f}%"
					)

				options.append(
					format_option(
						label,
						{"text": key}
					)
				)

			options.append(
				format_option(
					"Voltar",
					{"text": "back"}
				)
			)

			selected = selection_options(
				options,
				self.information_equipments(target)
				+ "\nSelecione um slot de equipamento:",
				"Escolha uma opção: "
			)[1]["text"]

			if selected == "back":
				# Retorna diretamente ao menu principal do NPC.
				break

			self.apply_equip_in_slot(
				user,
				target,
				selected
			)

	# ---------------------------------------------------------
	# DAR ITEM
	# ---------------------------------------------------------

	def give_item(self, user, target):

		selected = self.get_item(user)

		if selected is False:
			return

		item = selected.get_item()

		if not item:
			self._show_result(
				"Não foi possível entregar esse item."
			)
			return

		if not self._remove_from_slot(selected, 1):

			self._show_result(
				"Não foi possível retirar o item do inventário."
			)
			return

		target.inventory.add_item(item, 1)

		self._show_result(
			f"Você entregou 1x {item.get('name', 'Item')} "
			f"para {target.profile.name or 'o NPC'}."
		)

	# ---------------------------------------------------------
	# DAR COMIDA
	# ---------------------------------------------------------

	def give_food(self, user, target):

		brain = getattr(target, "brain", None)

		if brain is None or not hasattr(brain, "foods"):

			self._show_result(
				"Esse NPC não possui um sistema de alimentação."
			)
			return

		selected = self.get_item(
			user,
			type_item=["food"]
		)

		if selected is False:
			return

		item = selected.get_item()

		if not item:
			self._show_result(
				"Não foi possível entregar essa comida."
			)
			return

		if not self._remove_from_slot(selected, 1):

			self._show_result(
				"Não foi possível retirar a comida do inventário."
			)
			return

		brain.foods += 1

		self._show_result(
			f"Você entregou 1x {item.get('name', 'Comida')} "
			f"para {target.profile.name or 'o NPC'}.\n"
			f"Comidas armazenadas: {brain.foods}."
		)

	# ---------------------------------------------------------
	# INFORMAÇÕES DOS EQUIPAMENTOS
	# ---------------------------------------------------------

	def information_equipments(self, creature):

		creature_name = (
			creature.profile.name
			or creature.profile.race
		)

		lines = (
			f"Equipamentos de {creature_name}\n"
			f"Ataque total: {creature.get_damage():.2f}\n"
			f"Defesa total: "
			f"{creature.get_defense() * 100:.2f}%\n\n"
		)

		for key, slot in creature.equipment.slots.items():

			if slot.is_empty():

				lines += f"{key}: Nada equipado\n"

			else:

				item = slot.get_item()

				damage = item.get("damage", 0)
				defense = item.get("defense", 0) * 100

				lines += (
					f"{key}: {item.get('name', 'Item')}\n"
					f"  ATK: {damage}\n"
					f"  DEF: {defense:.2f}%\n"
				)

		return lines

	# ---------------------------------------------------------
	# MENU DE CRIATURAS
	# ---------------------------------------------------------

	def interaction(self, user):

		while True:

			options = []

			companions = (
				user.relationships.get_members_per_tag("companion")
			)

			for npc_id in user.relationships.get_members_per_tag(
				"slave"
			):

				npc = self.world.get_creature(npc_id)

				if npc is False:
					continue

				name = npc.profile.name or "Sem nome"
				race = npc.profile.race
				age = get_age_range(npc)

				if npc.profile.gender in ("f", "h"):

					label = f"Uma {age} {race} {name}"

				else:

					label = f"Um {age} {race} {name}"

				if npc.get_id() in companions:
					label += TEXT_GROUP_NO_COMPANION

				options.append(
					format_option(
						label,
						{"text": npc}
					)
				)

			options.append(
				format_option(
					"Voltar",
					{"text": "back"}
				)
			)

			selected = selection_options(
				options,
				"Criaturas sob seu controle:",
				"Escolha uma opção: "
			)[1]["text"]

			if selected == "back":
				break

			self.options_interactions(
				user,
				selected
			)


# -------------------------------------------------------------
# TESTE
# -------------------------------------------------------------

if __name__ == "__main__":

	import random

	from system_creatures import System_Creature
	from slave_marketplaces import Marketplace_slave, Dumb
	from system_items import all_items

	world = Dumb()

	market = Marketplace_slave(world, None)
	market.generator()

	user = System_Creature("Calango")
	user.profile.name = "Calango"

	world.add_creature(user)

	for item in all_items.values():
		user.inventory.add_item(
			item,
			random.randint(1, 2)
		)

	slaves = list(dict.fromkeys(market.colletions))

	for npc in slaves:
		market.maker_contract(
			user,
			npc,
			ignore_cust=True
		)

	app = Interaction_slave(world)
	app.interaction(user)
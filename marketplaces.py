# marketplaces.py
import random
from utils import format_option, selection_options
from system_items import all_items


class System_Marketplace(object):
	def __init__(self, own):
		self.items = {}
		self.own = own
		self.rate = 1.2

	def add_item(self, itemID, amount):
		if not itemID in self.items:
			self.items[itemID] = 0
		self.items[itemID] += amount

	def remove_item(self, itemID, amount):
		if self.items.get(itemID, 0) >= amount:
			self.items[itemID] -= amount
			self.update()

	def update(self):
		self.items = {key: value
			for key, value in self.items.items()
			if value > 0}

	def show_information_item(self, user, data, amount_default=None):
		from utils import table_informations, clear_screen
		
		item = data.get("item", {})
		table = {
			"Nome": item.get("name", "Sem Nome"),
			"Descrição": item.get("description", "..."),
			"Slot": item.get("slot") if item.get("slot", False) else None,
			"Dano": item.get("damage") if item.get("slot", False) else None,
			"Defesa": f'{(item.get("defense") * 100):.1f}%' if item.get("slot", False) else None,
			"Valor": int(item.get("value") * self.rate),
		}
		table = dict([(key, value)
			for key, value in table.items()])
		information = table_informations(
			table, f"informações {item.get('name')}.")
		information += f"\n\n Seus coins: {user.inventory.get_coins()} G"
		while(True):
			options = [
				format_option("comprar o item", {'text': True}),
				format_option("Voltar", {'text': False, "default": True}),
			]
			if user.control:
				selected = selection_options(options,
					f"{information}\n\nO que deseja fazer?",
					"Escolha uma opção: ")[1]
				clear_screen()
			else:
				if amount_default > 0:
					selected = options[0][1]
			if selected["text"] == False:
				if not user.control:
					return False, 0, "COMPRA CANCELADA"
				break
			elif not user.control:
				amount_slot = data.get("amount", 0)
				amount_collect = amount_default
				if amount_default > amount_slot:
					amount_collect = amount_slot
				coins_need = int((item.get("value", 0) * self.rate) * amount_collect)
				if user.get_coins() >= coins_need:
					user.inventory.remover_coins(coins_need)
					user.inventory.add_item(item, amount_collect)
					if not self.own is None:
						self.own.inventory.add_coins(coins_need)
					self.remove_item(item.get("id"), amount_collect)
					if amount_collect == amount_default:
						return True, coins_need, "COMPRADO"
					else:
						return False, coins_need, "COMPRADO ABAIXO DO DINHEIRO"
				else:
					return False, coins_need, "SEM DINHEIRO"
			else:
				coins = int(item.get("value") * self.rate)
				# if data.get("amount", 0):
				if user.inventory.get_coins() >= coins:
					user.inventory.remover_coins(coins)
					user.inventory.add_item(item, 1)
					if not self.own is None:
						self.own.inventory.add_coins(coins)
					self.remove_item(item.get("id"), 1)
					if user.control:
						input(f"1x de {item.get('name')} foi adicionado ao seu inventario com sucesso.")
				else:
					if user.control:
						input("Você não tem moedas para comprar isso.")

	def buy(self, user, item_id_search=None, amount_search_id=None):
		while(True):
			options = []
			for itemID, value in self.items.items():
				item = all_items[itemID]
				op = format_option(f"x{value} {item['name']}", {'text': itemID, "item": item, "amount": value})
				options.append(op)
			options.append(format_option("voltar", {'text': 'back'}))
			if user.control:
				selected = selection_options(options,
					f"Bem vindo a minha venda:\nSeus Coins: {user.get_coins()} G",
					"Escolha uma opção: ")[1]
			else:
				selected = options[-1][1]
				have_item_need = False
				for text, data in options:
					# print(data.get("text") == item_id_search, f"{data.get('text')} == {item_id_search}")
					if data.get("text", "") == item_id_search:
						have_item_need = True
						selected = data
						break
			if selected['text'] == "back":
				break
			if user.control:
				self.show_information_item(user, selected)
			else:
				return self.show_information_item(user, selected, amount_search_id)

	def show_information_item_sell(self, item):
		from utils import table_informations
		table = {
			"Nome": item.get("name", "Sem Nome"),
			"Descrição": item.get("description", "..."),
			"Slot": item.get("slot") if item.get("slot", False) else None,
			"Dano": item.get("damage") if item.get("slot", False) else None,
			"Defesa": f'{(item.get("defense") * 100):.1f}%' if item.get("slot", False) else None,
			"Valor": int(item.get("value") * self.rate),
		}
		table = dict([(key, value)
			for key, value in table.items()
			if not value is None])
		information = table_informations(
			table, f"informações {item.get('name')}.")
		return information

	def sell(self, user):
		from utils import clear_screen
		while(True):
			options = []
			for slot in user.inventory.slots:
				if slot.is_empty():
					continue
				if slot.get_item().get("id") == "gold":
					continue
				name = slot.get_item().get("name")
				amount = slot.get_amount()
				options.append(format_option(f"{amount}x {name}", {'text': slot}))
			if len(options) > 2:
				options.append(format_option("Vender tudo", {"text": "all-items"}))
			options.append(format_option("Voltar", {"text": "back"}))
			coins = 0
			if not self.own is None:
				coins = self.own.inventory.get_coins()
			title = f"Olá, quer vender o que?\n Coins do vendedor: {coins} G"
			selected = selection_options(options,
				title, "Escolha uma opção: ")[1]['text']
			if selected == 'back':
				break
			elif selected == "all-items":
				for text, data in options[:len(options)-2]:
					slot = data.get("text")
					if slot.is_empty():
						continue
					item = slot.get_item()
					amount = slot.get_amount()
					value = item.get("value", 1)
					value_in_coins = amount * value
					user.inventory.add_item(
						all_items["gold"], value_in_coins)
					if not self.own is None:
						self.own.inventory.remover_coins(value_in_coins)
						self.own.inventory.add_item(item, amount)
					slot.set_amount(-amount)
					slot.update_slot()
			else:
				item = selected.get_item()
				value = item.get("value", 0)
				options_n = [
					format_option(f"Vender {x}", {'text': x})
					for x in range(1, selected.get_amount(), max(1, int(selected.get_amount()/4)))]
				options_n.append(format_option("Tudo desse item", {"text": selected.get_amount()}))
				selected_amount = selection_options(options_n,
					f"{self.show_information_item_sell(item)}\nQuer vender quantos?", "Escolha uma opção: ")[1]['text']
				clear_screen()
				texts_lines = "Resultado:\n"
				texts_lines += f" Removido {selected_amount}x {item.get('name')} com sucesso do seu inventario!\n"
				texts_lines += f" Adiciona {selected_amount * value} Moedas de ouro com sucesso ao seu inventario!\n"
				texts_lines += "\nPressione Enter"
				value_in_coins = selected_amount * value
				if not self.own is None:
					self.own.inventory.add_item(item, selected_amount)
					self.own.inventory.add_coins(value_in_coins)
				user.inventory.add_coins(value_in_coins)
				selected.set_amount(-selected_amount)
				selected.update_slot()
				input(texts_lines)
				continue

	def main(self, user):
		options = [
			format_option("comprar items", {"text": "buy"}),
			format_option("vender items", {"text": "sell"}),
			format_option("voltar", {"text": "back"}),
		]
		while(True):
			selected = selection_options(options, "Compra e venda", "Escolha uma opção: ")[1]['text']
			if selected == "back":
				break
			elif selected == 'sell':
				self.sell(user)
			elif selected == 'buy':
				self.buy(user)


if __name__=="__main__":
	from system_crafts import RECEIVES
	from system_creatures import System_Creature
	from system_ai_npcs import AI

	from system_storage import Interaction_Storage

	interaction = Interaction_Storage()

	npc = System_Creature("mercador")
	npc.level.skills["blacksmith"] += 1
	
	# cerebro do npc
	npc.brain = AI(npc)
	npc.brain.ocupations["ferreiro"] += 0.01

	user = System_Creature("Jogador")
	user.inventory.add_item(all_items["gold"], 100)

	market = System_Marketplace(npc)

	for _ in range(int(12/3)):
		action = npc.brain.daily()
		if action == "ocupação":
			selected_tools = random.choice(RECEIVES)
			if random.random() < 0.9:
				for key, value in selected_tools.get("items").items():
					market.add_item(key, value)
				npc.inventory.add_item(all_items["gold"], int(20/3))
		else:
			print(action, npc.brain.event(action))

	market.buy(user)
	interaction.inventory(user)

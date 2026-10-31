import random
from utils import selection_options, format_option, clear_screen


def get_name(user):
	name_user = "Sem Nome"
	if not user is None:
		if user.profile.name is None:
			name_user = f"{user.profile.race} Sem Nome"
		else:
			name_user = f"{user.profile.name}"
	return name_user.title()

def apply_damage(damage, defense):
	return max(damage * (1.0 - defense), 0)

def table_informations(data, title="Diagrama\n"):
	text = title
	for info in data:
		name, hp = info.values()
		text += f'+name: {name}\n-HP: {hp}\n'
	return text.strip()


class System_Battle(object):
	def __init__(self):
		from system_magic import System_magic, System_Effects
		self.sys_magic = System_magic(None)
		self.sys_effects = System_Effects(None)

	def bar_collections(self, mob):
		def collect_data(mob):
			return {
				'name': get_name(mob),
				'hp': f'{mob.get_hp():^.2f}/ {mob.get_hp_max():^.2f}',
			}
		group_a = self.get_group(mob, ally=True)['group']
		group_b = self.get_group(mob, ally=False)['group']

		text_line = ''
		text_group_a = table_informations([collect_data(x) for x in group_a], 'Aliados:\n').split('\n')
		text_group_b = table_informations([collect_data(x) for x in group_b], 'inimigos:\n').split('\n')
		dx = len(text_group_a) - len(text_group_b)
		if dx < 0:
			text_group_a.extend([' ' for x in range(dx*-1)])

		if dx > 0:
			text_group_b.extend([' ' for x in range(dx)])

		max_x = max([len(x) for x in text_group_a])
		max_y = max([len(x) for x in text_group_b])

		text_line = '\n'.join([
			f' {x.ljust(max_x, " ")} | {y.ljust(max_y, " ")} '
			for x, y in zip(text_group_a, text_group_b)])
		return text_line

	def apply_damage(self, damage, defense):
		return max(damage * (1.0 - defense), 0)

	def get_group(self, mob, ally=True):
		if ally:
			return self.group_a if mob in self.group_a['group'] else self.group_b
		else:
			return self.group_b if mob in self.group_a['group'] else self.group_a

	def update_all_events_in_battle(self):
		self.dead_in_combate = []
		self.turn_escape_in_battle = []
		for event in self.all_events_in_battle:
			user = event['user']
			target = event['target']
			action = event['action']
			spell = event['spell']
			if user in self.turn_escape_in_battle:
				continue
			name_user = get_name(user)
			name_target = get_name(target)
			
			if not spell is None:
				self.text_result_events_battle.append(f"{name_user} usou a magia {spell['name']} em {name_target}")
				target.set_hp(target.get_hp(), increment=True)
				user.set_st(-user.get_st_max()/10)
				if target.get_hp() <= self.limiter_hp and not target in self.dead_in_combate:
					self.turn_escape_in_battle.append(target)

			elif action == 'atk':
				if target in self.turn_escape_in_battle:
					self.text_result_events_battle.append(
						f"{name_user} tentou atacar {name_target} porem o alvo fugiu.")
					user.set_st(-user.get_st_max()/8)
					continue
				if target in self.dead_in_combate:
					self.text_result_events_battle.append(
						f"{name_user} tentou atacar {name_target} porem o alvo já hávia sido derrotado.")
					user.set_st(-user.get_st_max()/8)
					continue
				text_lines = f"{name_user} tentou atacar {name_target}."
				if random.randint(-1, 20) > 1:
					damage = user.get_damage()
					defense = target.get_defense()

					damage_total = self.apply_damage(damage, defense)

					strength = damage_total
					self.set_actions(user, "atk")
					if random.randint(-1, 20) > -1:
						text_lines += f" Acertou em cheio o alvo. Dando {strength:^.2f}HP de dano."
						target.set_hp(-strength, increment=True)
					else:
						text_lines += f" Acertou em cheio o alvo. Com mais ira e deu {strength*2}HP de dano no inimigo."
						target.set_hp(-(strength*2), increment=True)
				else:
					n = random.randint(0, 3)
					if n == 0:
						text_lines += " Mas acabou errando o golpe."
					if n == 1:
						text_lines += " Mas o inimigo desviou do golpe."
					if n == 2:
						text_lines += " Mas por desatenção acabou errando o golpe."

				self.text_result_events_battle.append(text_lines)
				user.set_st(-(user.get_st_max() / 6))
				if target.get_hp() <= self.limiter_hp and not target in self.dead_in_combate:
					self.dead_in_combate.append(target)

			elif action == 'mgk':
				chance = random.random()
				if chance > 0.02:
					self.sys_magic.cast_spell(user, target, spell)
					for effect_id in spell.get("effects", {}):
						self.sys_effects.update_effects(target, effect_id)
						self.text_result_events_battle.extend([
							x for x in self.sys_effects.chat_log])
						self.sys_effects.chat_log = []
				else:
					if spell.get("type") == "mgk-offensive":
						self.text_result_events_battle.append(f"{name_user} tentou usar uma magia contra {name_target}, mas não surtiu efeito.")
					if spell.get("type") == "mgk-defense":
						self.text_result_events_battle.append(f"{name_user} tentou usar uma magia contra {name_target}, mas não surtiu efeito.")
					if spell.get("type") == "mgk-suport":
						self.text_result_events_battle.append(f"{name_user} tentou usar uma magia para ajudar {name_target}, mas não surtiu efeito.")

			elif action == 'hab':
				self.text_result_events_battle.append(f"{name_user} tentou usar uma habilidade mas não conseguiu.")
				self.set_actions(user, "hab")
				user.set_st(-user.get_st_max()/5)
				if target.get_hp() <= self.limiter_hp and not target in self.dead_in_combate:
					self.dead_in_combate.append(target)

			elif action == 'escape':
				text = f"{name_user} tentou escapar. "
				if random.random() < 0.2:
					self.turn_escape_in_battle.append(user)
					text += "E conseguiu fugiu com sucesso."
				else:
					text += "E não conseguiu na fuga foi interceptado."
				self.text_result_events_battle.append(
					text.strip())
				user.set_st(-user.get_st_max()/10)

			elif action == 'nda':
				self.text_result_events_battle.append(f"{name_user} não fez nada.")
				user.set_st(user.get_st_max()/4)

		for mob in self.turn_escape_in_battle:
			group = self.get_group(mob, True)
			group["group"].remove(mob)
			group["defeated"].append(mob)
		# 
		for mob in [x for x in self.group_a['group']]:
			if mob.get_hp() <= 0:
				self.text_result_events_battle.append(f'{get_name(mob)} foi abatido em combate.')
				self.group_a['dead'].append(mob)
				self.group_a['group'].remove(mob)

		for mob in [x for x in self.group_b['group']]:
			if mob.get_hp() <= 0:
				self.text_result_events_battle.append(f'{get_name(mob)} foi abatido em combate.')
				self.group_b['dead'].append(mob)
				self.group_b['group'].remove(mob)

	def selected_one_target(self, mob, ally=False):
		orden_mobs = []
		for pos, npc in enumerate(self.get_group(mob, ally=ally)["group"]):
			name = npc.profile.name
			if npc.profile.name is None:
				name = f"{npc.profile.race}"
			if npc == mob:
				name += " (VOCÊ)"
			option = format_option(
				f'{name}',
				{'text': npc, 'default': pos == 0})
			orden_mobs.append(option)
		if mob.control:
			orden_mobs.append(format_option("Cancelar", {'text': False}))
			title = "Na batalha você prepara seu ataque e são esses seus alvos."
			if ally:
				title = "Na batalha ver seus aliados, e deseja escolher qual?"
			return selection_options(orden_mobs, title, "Escolha uma opção: ")[1]['text']
		if len(orden_mobs) > 0:
			return orden_mobs[0][1]['text']
		else:
			return False

	def selected_two_target(self, mob, ally=False):
		selected_mobs = []
		orden_mobs = []
		while(len(selected_mobs) < 2):
			group_target = self.get_group(mob, ally=ally)["group"]
			if not len(group_target) >= 3:
				return [group_target[0], group_target[1]]
			if not len(group_target) <= 1:
				return [group_target[0]]
			for pos, npc in enumerate(group_target):
				if npc in selected_mobs:
					continue
				name = npc.profile.name
				if npc.profile.name is None:
					name = f"{npc.profile.race}"
				if npc == mob:
					name += " (VOCÊ)"
				option = format_option(
					f'{name}',
					{'text': npc, 'default': pos == 0})
				orden_mobs.append(option)
			if mob.control:
				orden_mobs.append(format_option("Cancelar", {'text': False}))
				title = "Na batalha você prepara seu ataque e são esses seus alvos."
				if ally:
					title = "Na batalha ver seus aliados, e deseja escolher qual?"
				selected = selection_options(orden_mobs, title, "Escolha uma opção: ")[1]['text']
				if selected == False:
					return False
				selected_mobs.append(selected)
			if len(orden_mobs) > 0:
				return [orden_mobs[0][1]['text'], orden_mobs[1][1]['text']]
		return selected_mobs

	def selected_spells(self, user, type_spell=None):
		while(True):
			options = []
			for spell_id, spell in user.magic.spellbook.items():
				if not type_spell is None:
					if not (spell.get("type", None) == type_spell):
						continue
				name = spell.get("name", "Unknown")
				options.append(format_option(
					f"{name} custo: {spell.get('cust')} MP", {"text": spell}))
			options.append(format_option("voltar", {"text": 'back'}))
			selected_spell = selection_options(options,
				"Magias que podem ser utilzidas:",
				"Escolha uma opção: ")[1]['text']
			if user.control == False:
				new_options = []
				for option in options:
					if option[1]["text"] != "back":
						if user.get_mp() >= option[1]["text"].get("cust"):
							new_options.append(option)
				return new_options[0][1]["text"]
			if selected_spell == "back":
				break
			else:
				return selected_spell

	def selected_spells_process(self, user):
		spell = self.selected_spells(user)
		if spell == False:
			ally = spell.get("type", "") in ["mgk-suporte"]
			area_max = spell.get("area-max", "one")
			if area_max == "one":
				target = self.selected_one_target(user, ally=ally)
				if not target == False:
					self.all_events_in_battle.append(format_event(user=user, target=target, action="mgk", spell=spell))
					return True
			elif area_max == 'two':
				targets_spell = self.selected_two_target(user, ally=ally)
				if targets_spell != False:
					for target in targets_spell:
						self.all_events_in_battle.append(
							format_event(
								user=user, target=target, action="mgk", spell=spell))
					return True
			elif area_max == 'max':
				for target in self.get_group(user, ally=ally):
					self.all_events_in_battle.append(format_event(user=user, target=target, action="mgk", spell=spell))
				return True
		return False

	def event_in_battle(self, mob):
		turns_points = 5

		def format_event(user, target=None, action=None, spell=None):
			return {'user': user, 'target': target, 'action': action, 'spell': spell}

		cust_st = {
			'atk': (10, -1), # [-]
			'mgk': ( 5, -1), # [-]
			'hab': (10, -1), # [-]
			'nda': ( 4,  1), # [+]
		}

		while(int(turns_points) > 0):
			options = [
				format_option('Atacar', {'data': 'atk', 'hotkey': ['a']}),
				format_option('Usar Magia', {'data': 'mgk', 'hotkey': ['m']}),
				format_option('Usar Habilidade', {'data': 'hab', 'hotkey': ['d']}),
				format_option('Usar Item', {'data': 'item', 'hotkey': ['i']}),
				format_option('Não Fazer Nada', {'data': 'nda', 'hotkey': ['r'], 'default': True}),
			]
			title = f"{self.bar_collections(mob)}\n\n{mob.profile.name} - {turns_points} points left"
			subtitle = "Escolha uma ação: "
			selected_type = None
			if mob.control:
				selected_option = selection_options(options, title, subtitle)[1]['data']
			else:
				selected_option = mob.brain.combate()
				if selected_option.startswith("mgk"):
					selected_option, selected_type = selection_options.split('-')

			if selected_option == 'atk':
				target = self.selected_one_target(mob)
				if not target is False:
					self.all_events_in_battle.append(format_event(user=mob, target=target, action='atk'))
					turns_points -= 5

			elif selected_option == 'mgk':
				if self.selected_spells_process(mob):
					turns_points -= 5

			elif selected_option == 'escape':
				self.all_events_in_battle.append(format_event(user=mob, action='escape'))
				turns_points -= 5

			elif selected_option == 'hab':
				# self.all_events_in_battle.append(format_event(user=mob, action='hab'))
				# turns_points -= 5
				input("Esse função ainda não foi implementada.")

			elif selected_option in ['item', 'use-potion']:
				# turns_points -= 2.5
				if self.use_item(mob):
					turns_points -= 2.5

			elif selected_option == 'nda':
				self.all_events_in_battle.append(format_event(user=mob, action='nda'))
				turns_points -= 5

	def use_item(self, user):
		while(True):
			options = []
			for slot in user.inventory.slots:
				if slot.is_empty():
					continue
				item = slot.get_item()
				amount = slot.get_amount()
				name = item.get("name")
				if "potion" in item.get("type"):
					options.append(
						format_option(f"{amount}x {name}", {"text": slot}))
			options.append(format_option("Voltar", {"text": False}))
			selected = selection_options(options,
				"Items que pode ser usado:",
				"Escolha uma opção: ")[1]["text"]
			if selected == False:
				return False
			else:
				slot = selected
				item = slot.get_item()
				self.sys_effects.chat_log = []
				for effect_id in item.get("effect"):
					self.sys_effects.add_effect(
						target=user,
						effect_id=effect_id,
						element="no-element",
						turns=1)
					self.sys_effects.update_effects(
						user, effect_id)
				user_name = user.profile.name
				if user_name is None:
					user_name = user.profile.race
				clear_screen()
				print(f"{user_name}, usou item {item.get('name')} resultado:")
				for text in self.sys_effects.chat_log:
					print(f" {text}")
				input("\n\nPressione Enter")
				return True

	def set_actions(self, mob, action):
		group = self.get_group(mob, True)
		if not mob.get_id() in group["actions"]:
			group["actions"][mob.get_id()] = []
		group["actions"][mob.get_id()].append(action)

	def init_battle(self, group_a, group_b, limiter_hp=0):
		self.group_a = {'group': group_a, 'tag': 'A', 'defeated': [], 'dead': [], 'actions': {}}
		self.group_b = {'group': group_b, 'tag': 'B', 'defeated': [], 'dead': [], 'actions': {}}

		self.limiter_hp = limiter_hp

		self.turns = 0

	def start_battle(self, show_text_no_combate=False):
		inbattle = lambda: len(self.group_a['group']) > 0 and len(self.group_b['group']) > 0
		control_player = [x for x in self.group_a["group"] if x.control]
		if len(control_player) > 0:
			while inbattle():
				self.all_events_in_battle = []
				self.text_result_events_battle = []
				for mob in self.group_a['group']:
					self.event_in_battle(mob)
				for mob in self.group_b['group']:
					self.event_in_battle(mob)

				self.update_all_events_in_battle()
				if len(self.text_result_events_battle) > 0 and show_text_no_combate:
					clear_screen()
					text_results = "Em Batalha:\n "
					text_results += '\n '.join(self.text_result_events_battle)
					input(text_results+"\n\nPressione ENTER para continuar...")

				else:
					if inbattle():
						clear_screen()
						if show_text_no_combate:
							if len(self.text_result_events_battle) > 0:
								text_results = '\n'.join(self.text_result_events_battle)
								print(text_results+"\n\nPressione ENTER para continuar...")
							print(self.bar_collections(self.group_a['group'][0]))
		else:
			while(inbattle()):
				all_events_in_battle = []
				text_result_events_battle = []
				group_a = self.group_a["group"]
				group_b = self.group_b["group"]
				dead = []
				for npc in group_a+group_b:
					if npc in dead:
						continue
					action = npc.brain.combate()
					npc.brain.update()
					damage = npc.get_damage()
					if action == "use-potion":
						npc.set_st(-((npc.get_st_max()/15)))
						npc.set_hp(50)
						npc.inventory.remover_item("potion-hp50", 1)
					if action == "mgk-offensive":
						npc.set_st(-((npc.get_st_max()/10)))
						damage *= 2.3
						target = self.selected_one_target(
							npc, ally=False)
						if target is False:
							continue
						defense = target.get_defense()
						damage = max(0, damage - defense)
						if not target in dead:
							if random.random() < (npc.get_con() / 100):
								target.set_hp(-int(damage))
					if action == 'mgk-defense':
						npc.set_st(-((npc.get_st_max()/5)))
						npc.set_mp(-((npc.get_mp_max()/4)))
						damage = int(2.5 * damage)
						target = self.selected_one_target(
							npc, ally=False)
						if target is False:
							continue
						defense = target.get_defense()
						damage = max(0, damage - defense)
						if not target in dead:
							if random.random() < (npc.get_con() / 100):
								target.set_hp(-int(damage))
					if action == "atk":
						npc.set_st(-((npc.get_st_max()/10)))
						target = self.selected_one_target(
							npc, ally=False)
						if target is False:
							continue
						defense = target.get_defense()
						damage = max(0, damage - defense)
						if not target in dead:
							if random.random() < (npc.get_con() / 100):
								target.set_hp(-int(damage))
					if action == 'nda':
						npc.set_st(((npc.get_st_max()/4)))
						npc.set_mp(((npc.get_mp_max()/4)))
					if action == "escape":
						group = self.get_group(npc, ally=True)
						group["defeated"].append(npc)
						group["group"].remove(npc)
					if npc.get_hp() <= self.limiter_hp:
						dead.append(npc)
				for target in [x for x in self.group_a["group"]]:
					if target.get_hp() <= self.limiter_hp:
						self.group_a["dead"].append(target)
						self.group_a["group"].remove(target)
				for target in [x for x in self.group_b["group"]]:
					if target.get_hp() <= self.limiter_hp:
						self.group_b["dead"].append(target)
						self.group_b["group"].remove(target)
		return self.get_win()

	def get_win(self):
		info_result_battle = {
			'tag': None,
			'win':{}, 'lose': {},
			'draw': False,
			'actions':{}
		}
		amount_a = len(self.group_a["group"])
		amount_b = len(self.group_b["group"])

		# print(f"\nA:", amount_a)
		# print(f"B:", amount_b)

		if amount_a == 0 and amount_b == 0:
			info_result_battle['draw'] = True
		if amount_a > 0 and amount_b <= 0:
			info_result_battle['tag'] = "A"
			info_result_battle['win'].update(self.group_a)
			info_result_battle['lose'].update(self.group_b)

		if amount_b > 0 and amount_a <= 0:
			info_result_battle['tag'] = "B"
			info_result_battle['win'].update(self.group_b)
			info_result_battle['lose'].update(self.group_a)
		return info_result_battle



if __name__ == '__main__':
	from system_creatures import System_Creature
	from utils import generator_id, generator_name, clear_screen

	clear_screen()

	generator_id(length=8, init='')
	def generator_mob(idname, specie='human', gender='f'):
		mob = System_Creature(idname)
		if specie in ["human", "elf"]:
			mob.profile.name = generator_name(length=4) # type:ignore
		mob.profile.race = specie
		mob.profile.gender = gender
		return mob

	battle = System_Battle()

	for _ in range(1):
		groups = [
			[
				generator_mob(
					generator_id(length=8, init='@Humanos'),
					specie='human', gender='f')
				for x in range(random.randint(2, 5))
			],
			[
				generator_mob(
					generator_id(length=8, init='@Goblins'),
					specie='goblin', gender='f')
				for x in range(random.randint(2, 5))
			],
		]
		groups[0][1].profile.name = "Taturana" # type:ignore
		groups[0][1].control = True
		battle.init_battle(
			group_a=groups[0],
			group_b=groups[1],
			limiter_hp=0
		)
		#print(battle.bar_collections(groups[0][1]))
		result = battle.start_battle(any([len([i for i in x if i.control]) > 0 for x in groups]))
		print("-----")
		if result["draw"]: # type:ignore
			print("EMPARTE nenhum dos grupos venceu.")
			break
		else:
			text = f"Grupo {result['tag']} "
			text += f"venceu e teve {len(result['win']['group'])} sobreviventes "
			text += f"e {len(result['win']['dead'])} baixas "
			text += f"e {len(result['win']['defeated'])} que fugiram."
			print(text)

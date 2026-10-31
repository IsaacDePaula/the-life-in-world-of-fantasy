# system_magic.py
from utils import format_option, selection_options
from utils import clear_screen, table_show_label

class System_Status_spellbook(object):
	def __init__(self, entitie):
		self.entitie = entitie
		self.spellbook = {}
		self.all_effects = {}
		self.resistences = {
			"fire": 0.0,
			"water": 0.0,
			"earth": 0.0,
			"wind": 0.0,
			"light": 0.0,
			"dark": 0.0,
			"no-element": 0.0,
		}

		self.magic_affinity = {
			"fire": 0.0,
			"water": 0.0,
			"earth": 0.0,
			"wind": 0.0,
			"light": 0.0,
			"dark": 0.0,
			"no-element": 0.0,
		}

		self.level_elements = {
			"fire": {"exp": 0, "level": 1},
			"water": {"exp": 0, "level": 1},
			"earth": {"exp": 0, "level": 1},
			"wind": {"exp": 0, "level": 1},
			"light": {"exp": 0, "level": 1},
			"dark": {"exp": 0, "level": 1},
			"no-element": {"exp": 0, "level": 1},
		}

	def get_base_exp(self, element):
		base_values_difficult = [
			[0.0, 5023],
			[0.3, 512],
			[0.5, 412],
			[0.8, 312],
			[0.9, 245],
		]
		base = max(0, min(1.0, self.level_elements[element].get("level", 1) * self.magic_affinity.get(element, 0.0)))
		for level, value_base in reversed(base_values_difficult):
			if base >= level:
				break
		return base, value_base

	def set_exp_element(self, key, amount, increment):
		base, value_base = self.get_base_exp(key)
		if base > 0:
			if increment:
				self.level_elements[key]["exp"] += amount
			else:
				self.level_elements[key]["exp"] = amount
			while(self.level_elements[key].get("exp") >= value_base):
				self.level_elements[key]["exp"] -= value_base
				self.level_elements[key]["level"] += 1
			else:
				if self.level_elements[key].get("exp") < 0:
					self.level_elements[key]["exp"] = 0


class Effect(object):
	def __init__(self, id, turns, element, caster_id=None, mod=1.0):
		self.id = id
		self.turns = turns
		self.element = element
		self.caster_id = caster_id
		self.mod = mod


class System_Effects(object):
	def __init__(self, world):
		self.world = world
		self.chat_log = []

	def add_effect(self, target, effect_id, element, turns, caster_id=None, mod=1.0):
		if not effect_id in target.magic.all_effects:
			target.magic.all_effects[effect_id] = Effect(
				id=effect_id, element=element, turns=turns,
				caster_id=caster_id, mod=mod)

	def update_effects(self, user, effect_rate=None):
		user_name = user.profile.name
		if user_name is None:
			user_name = user.profile.race+user.profile.gender

		remove_effects = []
		for effect_id, effect in user.magic.all_effects.items():
			if not effect_rate is None:
				if not effect_rate == effect_id:
					continue
			# atualiza os efeitos nas entidades.
			if effect_id.startswith("hp+"):
				hp, value = effect_id.split('+')
				if value.isnumeric():
					value = int(value)
				elif value == 'MAX':
					value = user.get_hp_max()
				increment = int(value * effect.mod)
				redux  = increment * user.magic.resistences.get(effect.element, 0.0)
				increment -= redux
				user.set_hp(increment)
				self.chat_log.append(f"{user_name}, recuperou +{increment} HP.")
			elif effect_id.startswith("mp+"):
				mp, value = effect_id.split('+')
				if value.isnumeric():
					value = int(value)
				elif value == 'MAX':
					value = user.get_hp_max()
				increment = int(value * effect.mod)
				redux  = increment * user.magic.resistences.get(effect.element, 0.0)
				increment -= redux
				user.set_mp(increment)
				self.chat_log.append(f"{user_name}, recuperou +{increment} MP.")
			elif effect_id == "burnout-lv1":
				damage = 18 * effect.mod
				redux  = damage * user.magic.resistences.get(effect.element, 0.0)
				damage -= redux
				damage = int(damage)
				user.set_hp(-int(damage))
				self.chat_log.append(f"{user_name}, tomou {damage} de fogo de dano na saúde.")
				chance = random.choice([0, 25, 75, 100])
				if chance == 25:
					self.add_effect(user, effect_id, element, 2, caster_id=None, mod=1.0)
			elif effect_id == "impact-water-lv1":
				damage = 13 * effect.mod
				redux  = damage * user.magic.resistences.get(effect.element, 0.0)
				damage -= redux
				damage = int(damage)
				user.set_hp(-int(damage))
				self.chat_log.append(f"{user_name}, tomou um impacto de jato de agua que deu {damage} de dano na saúde.")
			elif effect_id == "acid-impact-lv1":
				damage = 13 * effect.mod
				redux  = damage * user.magic.resistences.get(effect.element, 0.0)
				damage -= redux
				damage = int(damage)
				user.set_hp(-int(damage))
				self.chat_log.append(f"{user_name}, tomou um impacto de acido que deu {damage} de dano na saúde.")
			elif effect_id == "impact-rock-lv1":
				damage = 17 * effect.mod
				redux  = damage * user.magic.resistences.get(effect.element, 0.0)
				damage -= redux
				damage = int(damage)
				user.set_hp(-int(damage))
				self.chat_log.append(f"{user_name}, foi atingindo por rajada de pedras tomando {damage} de dano na saúde.")
			elif effect_id == "blade-wind-lv1":
				damage = 16 * effect.mod
				redux  = damage * user.magic.resistences.get(effect.element, 0.0)
				damage -= redux
				damage = int(damage)
				user.set_hp(-int(damage))
				self.chat_log.append(f"{user_name}, foi atingindo por laminas de vento tomando {damage} de dano na saúde.")
			user.magic.resistences[effect.element] += 0.0001

			# atualiza os turnos
			if effect.turns > 0:
				effect.turns -= 1
			if effect.turns == 0:
				remove_effects.append(effect_id)
		for effect_id in remove_effects:
			del(user.magic.all_effects[effect_id])


class System_magic(object):
	def __init__(self, world):
		self.world = world
		self.all_spells_in_world = {}
		self.load_spellbook()

	def load_spellbook(self):
		self.create_new_spell(
			idname="fireball-lv:001",
			name="Bola de fogo nivel 1", element="fire",
			effects=[{"effect": "burnout-lv1", "turns": 1, "mod": 1.0}],
			cust=5, requests={"fire": 1}, type_spell="mgk-offensive",
			area_max='one')
		self.create_new_spell(
			idname="waterjet-lv:001",
			name="Jato de agua nivel 1", element="water",
			effects=[{"effect": "impact-water-lv1", "turns": 1, "mod": 1.0}],
			cust=6, requests={"water": 1}, type_spell="mgk-offensive",
			area_max='one')
		self.create_new_spell(
			idname="a_barrage_of_stones-lv:001",
			name="Rajada de pedra nivel 1", element="earth",
			effects=[{"effect": "impact-rock-lv1", "turns": 1, "mod": 1.0}],
			cust=7, requests={"earth": 1}, type_spell="mgk-offensive",
			area_max='one')
		self.create_new_spell(
			idname="blades-wind-lv:001",
			name="Lamina de vento nivel 1", element="wind",
			effects=[{"effect": "blade-wind-lv1", "turns": 1, "mod": 1.0}],
			cust=7, requests={"wind": 1}, type_spell="mgk-offensive",
			area_max='one')
		self.create_new_spell(
			idname="cure-lite-lv:001",
			name="Luz da cura nivel 1", element="light",
			effects=[{"effect": "hp+50", "turns": 1, "mod": 1.5}],
			cust=5, requests={"light": 1}, type_spell="mgk-suport",
			area_max='one')
		self.create_new_spell(
			idname="cure-lite-lv:002",
			name="Luz da cura nivel 2", element="light",
			effects=[{"effect": "hp+MAX", "turns": 1, "mod": 1.5}],
			cust=5, requests={"light": 1}, type_spell="mgk-suport",
			area_max='max')
		self.create_new_spell(
			idname="Acid-Jet-lv:001",
			name="Jato Acido nivel 1", element="dark",
			effects=[{"effect": "acid-impact-lv1", "turns": 1, "mod": 1.0}],
			cust=5, requests={"dark": 1}, type_spell="mgk-defense",
			area_max="one")

	def create_new_spell(self, idname, name, element, effects, cust, requests, type_spell, area_max):
		self.all_spells_in_world[idname] = {
			"id": idname,
			'name': name,
			"element": element,
			"effects": effects,
			"cust": cust,
			"type": type_spell,
			"requests": requests,
			"area-max": area_max, # one, two, max
		}

	def learning_new_spell(self, caster, spell):
		report_log = []
		name = caster.profile.name
		if name is None:
			name = "Unknown"
		can_learn_new_spell = True
		element = spell.get("element")
		elements_requests = spell.get("requests", {})
		if caster.magic.magic_affinity.get(element, 0.0) > 0:
			for key, point in elements_requests.items():
				level = caster.magic.level_elements[key].get("level", 0)
				if not level >= point:
					report_log.append(f"{name}, não tem level em {key} suficiente, Level Atual: {level} -> Level Necessario: {point}!")
					can_learn_new_spell = False
			if not caster.get_mp_max() >= spell.get("cust"):
				report_log.append(f"{name}, não tem mana suficiente para realizar o feitiço com sucesso. Mana Atual: {caster.get_mp_max()} -> Mana Necessaria: {spell.get('cust')}")
				can_learn_new_spell = False
		else:
			report_log.append(f"{name}, não tem aptidão no elemento necessario dessa magia.")
			can_learn_new_spell = False
		if can_learn_new_spell:
			report_log.append(f"{name}, aprendeu um novo feitiço {spell.get('name')}")
			caster.magic.spellbook[spell.get('id')] = spell
		return can_learn_new_spell, report_log

	def cast_spell(self, caster, target, spell):
		report_log = []
		if caster.get_mp() >= spell.get("cust"):
			effects = spell.get("effects")
			mod_level = caster.magic.magic_affinity.get(spell.get("element", "none"), 0.0)
			for data in effects:
				effect_id, turns, mod = data.values()
				effect = Effect(effect_id, turns,
					element=spell.get("element", None),
					caster_id=caster.get_id(),
					mod=1.0 + mod_level)
				target.magic.all_effects[effect_id] = effect
			return True
		return False


class Interface_Arcane(object):
	def __init__(self, world):
		self.world = world

	def get_informations_base(self, user):
		texts_lines = "Status Base de Magia\n"
		elements = [x[0] for x in user.magic.magic_affinity.items() if x[1] > 0]
		for element in elements:
			level = user.magic.level_elements.get(element, {}).get('level', 0)
			exp = user.magic.level_elements.get(element, {}).get('exp', 0)
			_, base_exp = user.magic.get_base_exp(element)
			resistence = user.magic.resistences.get(element, 0)
			text = f" {element}: {level} (EXP: {exp}/ {base_exp})"
			if resistence > 0.0005:
				text += f" Resistencia: {(resistence*100):^.3f}%"
			texts_lines += text+'\n'
		if not len(elements) > 0:
			texts_lines += " Não tem atributo magico"
		return texts_lines

	def view_effects(self, user):
		texts_lines = "Efeitos Ativos:\n"
		# self.id = id
		# self.turns = turns
		# self.element = element
		# self.caster_id = caster_id
		# self.mod = mod
		for effect in user.magic.all_effects.values():
			effect_id = effect.id
			turns = effect.turns
			element = effect.element
			strong = effect.mod
			# text = f" {effect_id}/ turnos ativos: {turns} / Elemento: {element}/ Poder: {strong:^.2f}\n"
			text = f"[+] {effect_id}\n"
			text += f"    Poder: {strong:^.2f} | Duração: {turns} turno\n"
			texts_lines += text
		return selection_options([
			format_option("voltar", {"text": 'back', "default": True})
		], texts_lines, "Escolha uma opção: ")

	def selected_target(self, user):
		local = user.location
		options_npcs_select = []
		for npc in self.world.entities_in_world.values():
			local_npc = npc.location
			if local_npc == local:
				name_npc = npc.profile.name
				if name_npc is None:
					name_npc = npc.profile.race+npc.profile.gender
				if npc == user:
					name_npc += " (VOCÊ)"
				options_npcs_select.append(format_option(name_npc, {'text': npc}))
		options_npcs_select.append(format_option("voltar", {"text": False}))
		return selection_options(options_npcs_select,
			"Selecione o alvo da magia:",
			"Escolha uma opção: ")[1]['text']

	def use_spell(self, user):
		while(True):
			options = []

			hp = user.get_hp()
			hp_max = user.get_hp_max()

			mp = user.get_mp()
			mp_max = user.get_mp_max()
			
			for spell in user.magic.spellbook.values():
				name = spell.get("name")
				cust = spell.get("cust")
				text = f"{name} ({0 if mp <= 0 else cust/mp}/{int(cust/mp_max)})"
				option = format_option(text, {'text': spell})
				options.append(option)
			
			options.append(format_option("voltar", {'text': 'back'}))

			title = "Seus Status:\n"
			title += f" HP: {int(hp)}/ {hp_max}\n"
			title += f" MP: {int(mp)}/ {mp_max}\n"
			title += "Magias Disponiveis:"
			selected = selection_options(options, 
				title, "Escolha uma opção: ")[1]['text']
			if selected == 'back':
				break
			else:
				spell = selected
				target = self.selected_target(user)
				if target != False:
					self.world.sys_magic.cast_spell(user, target, spell)
					self.world.sys_effects.chat_log = []
					clear_screen()
					for effect in spell.get("effects"):
						self.world.sys_effects.update_effects(user, effect.get("effect"))
					print("Resultado da magia:")
					for text in self.world.sys_effects.chat_log:
						print(f" {text}\n")
					input("Pressione Enter.")

	def interaction(self, user):
		options = [
			format_option("Usar Magia", {"text": "mgk"}),
			format_option("Ver Efeitos Ativos", {"text": "effects"}),
			format_option("Fechar menu", {"text": "back"}),
		]
		while(True):
			title = self.get_informations_base(user)+'\n'
			title += "Conhecimentos Arcanos"
			selected = selection_options(options, title, "Escolha uma opção: ")[1]['text']
			if selected == 'back':
				break
			elif selected == 'effects':
				self.view_effects(user)
			elif selected == 'mgk':
				self.use_spell(user)


if __name__ == "__main__":
	import random
	from system_creatures import System_Creature
	from slave_marketplaces import Dumb

	world  = Dumb()
	sys_magic = System_magic(world)
	sys_effects = System_Effects(world)
	sys_interaction = Interface_Arcane(world)

	world.sys_magic = sys_magic
	world.sys_effects = sys_effects

	npc = System_Creature("testador")
	npc.location = ["beba"]
	target = System_Creature("npc-target")
	target.location = ['beba']
	target.set_hp(-50)
	world.add_creature(npc)
	world.add_creature(target)

	def use_spell(user, target, spell, active_effect=True):
		global sys_effects, sys_magic
		print(f"\n\nHP TARGET: {int(target.get_hp())}/ {target.get_hp_max()}")
		print("Magia selecionada foi:", spell.get("name"))
		result = sys_magic.cast_spell(user, target, spell)
		print(f"Magia lançada contra {target.profile.race}:", "sim" if result else "Não conseguir")
		if active_effect:
			print("Efeitos Resultantes do ataque:")
			for effect_id in spell.get('effects', {}):
				sys_effects.chat_log = []
				print(effect_id)
				sys_effects.update_effects(target, effect_id.get("effect", None))
				for text in sys_effects.chat_log:
					print('', text)
		print(f"HP TARGET: {int(target.get_hp())}/ {target.get_hp_max()}")

	for element in npc.magic.magic_affinity:
		npc.magic.magic_affinity[element] += max(0, random.randint(-1, 1) * random.uniform(0.0, 0.001))
	for spell in sys_magic.all_spells_in_world.values():
		can, phreses = sys_magic.learning_new_spell(npc, spell)
		print("Resultado:")
		for text in phreses:
			print(f" {text}")

	if npc.magic.spellbook != {}:
		spell = random.choice([x for x in npc.magic.spellbook.values()]*2)
		use_spell(npc, target, spell)
		use_spell(npc, npc, spell, False)

	print(f"\n\n{sys_interaction.get_informations_base(npc)}")
	sys_interaction.interaction(npc)
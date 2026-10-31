# labs_in_game.py
import random
from system_creatures import System_Creature
from utils import generator_name


user = System_Creature("wdd")
user.chrono.set_values("y", random.randint(1, 100))

def generator(mob):
	b = [
		mob.set_str, mob.set_dex,
		mob.set_con, mob.set_int,
		mob.set_wis, mob.set_cha,
	]

	for att in b:
		att(random.randint(1, 15))

def get_value(mob):
	a = [
		(mob.get_str, 0.01), (mob.get_dex, 0.01),
		(mob.get_con, 0.01), (mob.get_int, 0.01),
		(mob.get_wis, 0.01), (mob.get_cha, 0.01),
	]
	value = mob.level.get_level() * 144
	y = mob.chrono.get_y()
	mult = 0.90 - (y / 100)
	
	for n, m in a:
		value += (n() * m) * value
	value += mult * value
	return value

mobs = [System_Creature(f"n{x}")
	for x in range(10)]
for npc in mobs:
	generator(npc)
	npc.profile.name = generator_name(3)
	npc.chrono.set_values("y", random.randint(0, 100))
	print("Nome:", npc.profile.name)
	print("Raça:", npc.profile.race)
	print("Sexo:", "Feminino" if npc.profile.gender == "f" else "Masculino")
	print("Idade:", npc.chrono.get_y())
	print(f"gold: {get_value(npc):^.2f} G")
	print("\n")

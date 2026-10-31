from utils import format_option, selection_options
import random


class System_Guild(object):
	def __init__(self) -> None:
		pass

	def get_missions(self, mob):
		while(True):
			level = mob.level.level
			rank = 'F'
			for key, value in dict({'E':5, 'D':7, 'C':13, 'B':15, 'A':18, 'S':30, 'SS':50, 'SX':100}).items():
				if level >= value:
					rank = key
			options = [
				format_option(f'Caçar Goblins {(level / 2 * 100):^.1f}%', {'text': 'goblins', 'level': 2}),
				format_option(f'Caçar Lobos {(level / 5 * 100):^.1f}%', {'text': 'wolfs', 'level': 5}),
				format_option(f'Caçar Dragoes Pretos {(level/13 * 100):^.1f}%', {'text': 'dragon-black', 'level': 13}),
				format_option(f'Caçar Dragoes Verdes {(level/15 * 100):^.1f}%', {'text': 'dragon-green', 'level': 15}),
				format_option(f'Caçar Dragoes Azuis {(level/30 * 100):^.1f}%', {'text': 'dragon-blue', 'level': 30}),
				format_option(f'Caçar Dragoes vermelhos {(level/50 * 100):^.1f}%', {'text': 'dragon-red', 'level': 50}),
				format_option('Voltar', {'text': 'back'})
			]
			title = 'Status Base:\n'
			title += f' Nome: {mob.profile.name}\n'
			title += f' Raça: {mob.profile.race}\n'
			title += f' XP: {mob.level.get_exp()}/ {mob.level.get_base()}\n'
			title += f' Level: {mob.level.level}\n'

			select = selection_options(options, title, 'Escolha uma opção: ')[1]
			hit = [0 for x in range(100)]
			chance = int(level / select['level'] * 100)
			for i in range(chance):
				hit[i] = 1
			if select['text'] == 'back':
				break
			n = random.randint(0, 100)
			input(f"Você foi {('vitorioso' if n <= chance else 'derrotado')}!")


if __name__=='__main__':
	from system_creatures import System_Creature
	mob = System_Creature('id:00012')
	mob.profile.name = "Clanguinhi" # type:ignore
	app = System_Guild()
	app.get_missions(mob)

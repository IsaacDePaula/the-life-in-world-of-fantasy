
# 'race': 'human', # raça
# 'gender': 'fmh', # sexo: masculino, feminino, hermafrodita
# 'attributes': { # atributos
# 	'strength': 10, # força
# 	'dexterity': 10, # destreza
# 	'constitution': 10, # constituição
# 	'intelligence': 10, # inteligencia
# 	'wisdom': 10, # sabedoria
# 	'charisma': 10 # carisma
# },


SPECIES = [
	{
		'race': 'human',
		'gender': 'fmh',
		'hp': 100,
		'mp': 100,
		'st': 100,
		'attributes': {
			'strength': 10,
		},
	},
	{
		'race': 'goblin',
		'gender': 'fmh',
		'hp': 15,
		'mp': 15,
		'st': 15,
		'attributes': {
			'strength': 1,
		},
	},
	{
		'race': 'wolf',
		'gender': 'fmh',
		'hp': 20,
		'mp': 20,
		'st': 20,
		'items': {"leak": 1, 'meat': 2},
		'attributes': {
			'strength': 5,
		},
	},
]

for data in SPECIES:
	if not "items" in data:
		data["items"] = {}
	data["items"][f"crystal-{data.get('race')}"] = 1

def select_specie(race_selected):
	for race in SPECIES:
		if race.get('race') == race_selected:
			return race
	return {}
all_items = {
	'potion-hp50': {
		'id': 'potion-hp50',
		'name': 'Potion',
		'type': ["potion", "healing"],
		'description': 'A small vial of healing potion.',
		'effect': ['hp+50'],
		'value': 10
	},
	'elixir-001': {
		'id': 'elixir-001',
		'name': 'Elixir',
		'type': ["potion", "elixir", "healing", "mana"],
		'description': 'A rare elixir that restores both HP and MP.',
		'effect': ['hp+100', 'mp+50'],
		'value': 50
	},
	'nightshade': {
		'id': 'nightshade',
		'name': 'Nightshade',
		'type': ["ingredient", "herb", "poison", "plant"],
		'description': 'Uma planta venenosa usada como ingrediente no veneno Sangue de Assassino.',
		'effect': ['POISON'],
		'value': 50
	},
	'silverthorn': {
		'id': 'silverthorn',
		'name': 'Silverthorn',
		'type': ["ingredient", "herb", "plant", "magic", "resistance"],
		'description': 'Uma planta mágica usada para criar uma poção contra os efeitos da licantropia.',
		'effect': ['LYCANTHROPY_RESISTANCE'],
		'value': 75
	},
	'bloodroot': {
		'id': 'bloodroot',
		'name': 'Bloodroot',
		'type': ["ingredient", "herb", "root", "blood", "alchemy"],
		'description': 'Uma raiz capaz de produzir um sangue falso extremamente convincente.',
		'effect': ['FAKE_BLOOD'],
		'value': 40
	},
	'dragons-tongue': {
		'id': 'dragons-tongue',
		'name': 'Língua de Dragão',
		'type': ["ingredient", "herb", "spice", "fire", "damage"],
		'description': 'Uma pimenta extremamente ardente que pode causar dano de fogo e liberar chamas.',
		'effect': ['FIRE_DAMAGE', 'BURNING_HANDS'],
		'value': 100
	},
	'winters-bite': {
		'id': 'winters-bite',
		'name': 'Mordida do Inverno',
		'type': ["ingredient", "herb", "plant", "cold", "resistance"],
		'description': 'Uma planta extremamente fria usada para criar resistência contra danos de frio.',
		'effect': ['COLD_RESISTANCE'],
		'value': 80
	},
	'dreamleaf': {
		'id': 'dreamleaf',
		'name': 'Folha dos Sonhos',
		'type': ["ingredient", "herb", "plant", "poison", "sleep"],
		'description': 'Uma folha mística utilizada como ingrediente principal do veneno Essência do Éter.',
		'effect': ['SLEEP'],
		'value': 90
	},
	'bloomlotus': {
		'id': 'bloomlotus',
		'name': 'Lótus Florescente',
		'type': ["ingredient", "flower", "plant", "ornamental", "valuable"],
		'description': 'Uma flor ornamental rara e extremamente valiosa.',
		'effect': ['ORNAMENTAL'],
		'value': 150
	},
	'firethorn': {
		'id': 'firethorn',
		'name': 'Espinheiro de Fogo',
		'type': ["ingredient", "herb", "plant", "fire", "weapon_enchantment"],
		'description': 'Um espinheiro mágico capaz de imbuir temporariamente uma arma com chamas.',
		'effect': ['FIRE_DAMAGE', 'FLAME_TONGUE'],
		'value': 120
	},
	'weavegrass': {
		'id': 'weavegrass',
		'name': 'Grama Tecelã',
		'type': ["ingredient", "herb", "plant", "crafting", "stealth"],
		'description': 'Uma grama mágica utilizada na fabricação de capas que aumentam a capacidade de furtividade.',
		'effect': ['STEALTH'],
		'value': 100
	},
	'liferoot': {
		'id': 'liferoot',
		'name': 'Raiz da Vida',
		'type': ["ingredient", "herb", "root", "healing", "alchemy"],
		'description': 'Uma raiz restauradora utilizada como ingrediente na fabricação de poções de cura.',
		'effect': ['HEALING'],
		'value': 100
	},
	'starbloom': {
		'id': 'starbloom',
		'name': 'Flor Estelar',
		'type': ["ingredient", "flower", "plant", "magic", "detection"],
		'description': 'Uma flor radiante que produz um líquido capaz de revelar criaturas e objetos como o feitiço Fogo das Fadas.',
		'effect': ['FAERIE_FIRE'],
		'value': 125
	},
	'rotshroom': {
		'id': 'rotshroom',
		'name': 'Cogumelo da Podridão',
		'type': ["ingredient", "mushroom", "fungus", "poison", "underdark"],
		'description': 'Um fungo perigoso do Subterrâneo usado na fabricação de veneno drow.',
		'effect': ['POISON', 'DROW_POISON'],
		'value': 150
	},
	'mindthorn': {
		'id': 'mindthorn',
		'name': 'Espinheiro Mental',
		'type': ["ingredient", "herb", "plant", "alchemy", "truth_serum"],
		'description': 'Uma planta rara utilizada como ingrediente principal na fabricação de soros da verdade.',
		'effect': ['TRUTH_SERUM'],
		'value': 130
	},
	'gravedust': {
		'id': 'gravedust',
		'name': 'Pó da Sepultura',
		'type': ["ingredient", "material", "dust", "necrotic", "resistance"],
		'description': 'Um material misterioso utilizado para criar resistência contra danos necróticos.',
		'effect': ['NECROTIC_RESISTANCE'],
		'value': 100
	},
	'zapthistle': {
		'id': 'zapthistle',
		'name': 'Cardo Elétrico',
		'type': ["ingredient", "herb", "plant", "lightning", "resistance"],
		'description': 'Uma planta carregada de energia usada para criar resistência contra danos elétricos.',
		'effect': ['LIGHTNING_RESISTANCE'],
		'value': 100
	},
	'sirens-call': {
		'id': 'sirens-call',
		'name': 'Chamado da Sereia',
		'type': ["ingredient", "flower", "plant", "magic", "charm"],
		'description': 'Uma flor encantadora utilizada como ingrediente na fabricação de poções do amor.',
		'effect': ['CHARM'],
		'value': 125
	},
	'deaths-beckon': {
		'id': 'deaths-beckon',
		'name': 'Chamado da Morte',
		'type': ["ingredient", "herb", "plant", "poison", "toxic"],
		'description': 'Uma planta mortal utilizada como ingrediente no veneno Lágrimas da Meia-Noite.',
		'effect': ['POISON', 'MIDNIGHT_TEARS'],
		'value': 175
	},
	'shadowleaf': {
		'id': 'shadowleaf',
		'name': 'Folha das Sombras',
		'type': ["ingredient", "herb", "plant", "magic", "invisibility"],
		'description': 'Uma folha de origem mágica utilizada na fabricação de poções de invisibilidade.',
		'effect': ['INVISIBILITY'],
		'value': 150
	},
	'cinderroot': {
		'id': 'cinderroot',
		'name': 'Raiz de Brasa',
		'type': ["ingredient", "herb", "root", "fire", "resistance"],
		'description': 'Uma raiz resistente ao calor utilizada para criar resistência contra danos de fogo.',
		'effect': ['FIRE_RESISTANCE'],
		'value': 100
	},
	'graveflower': {
		'id': 'graveflower',
		'name': 'Flor da Sepultura',
		'type': ["ingredient", "flower", "plant", "necromancy", "magic"],
		'description': 'Uma flor misteriosa capaz de produzir um efeito semelhante ao feitiço Falar com os Mortos.',
		'effect': ['SPEAK_WITH_DEAD'],
		'value': 200
	},
	'gold': {
		'id': 'gold',
		'name': 'Moeda de Ouro',
		'type': ["currency", "money", "valuable"],
		'description': 'Um pedaço de ouro achatado',
		'value': 1
	},
	'leak': {
		'id': 'leak',
		'name': 'Couro',
		'type': ["material", "crafting", "leather"],
		'description': 'Couro',
		'value': 20
	},
	'meat': {
		'id': 'meat',
		'name': 'Carne',
		'type': ["resource", "food", "meat", "hunting"],
		'description': 'Carne',
		'value': 12
	},
	'stick': {
		'id': 'stick',
		'name': 'Graveto reto',
		'type': ["resource", "material", "wood", "crafting"],
		'description': '...',
		'value': 2
	},
	'sword-wood': {
		'id': 'sword-wood',
		'name': 'Espada de Madeira',
		'type': ["equipment", "weapon", "sword", "wood", "melee"],
		'description': 'Uma espada simples de madeira, leve e adequada para iniciantes.',
		'equip': True,
		'slot': "hand",
		'damage': 30,
		'defense': 0.0,
		'value': 25
	},

	'shield-wood': {
		'id': 'shield-wood',
		'name': 'Escudo de Madeira',
		'type': ["equipment", "shield", "wood", "defense"],
		'description': 'Um escudo de madeira que ajuda a bloquear ataques inimigos.',
		'equip': True,
		'slot': "hand",
		'damage': 0,
		'defense': 0.05,
		'value': 35
	},

	'elmo-madeira': {
		'id': 'elmo-madeira',
		'name': 'Elmo de Madeira',
		'type': ["equipment", "armor", "helmet", "wood", "defense"],
		'description': 'Um elmo de madeira que protege a cabeça contra impactos.',
		'equip': True,
		'slot': "head",
		'damage': 0,
		'defense': 0.03,
		'value': 20
	},

	'peitoral-madeira': {
		'id': 'peitoral-madeira',
		'name': 'Peitoral de Madeira',
		'type': ["equipment", "armor", "chest", "wood", "defense"],
		'description': 'Um peitoral reforçado que protege o tronco contra golpes.',
		'equip': True,
		'slot': "body",
		'damage': 0,
		'defense': 0.09,
		'value': 55
	},

	'calcas-madeira': {
		'id': 'calcas-madeira',
		'name': 'Calças de Madeira',
		'type': ["equipment", "armor", "legs", "wood", "defense"],
		'description': 'Uma proteção rígida para as pernas, feita de madeira.',
		'equip': True,
		'slot': "legs",
		'damage': 0,
		'defense': 0.06,
		'value': 35
	},

	'botas-madeira': {
		'id': 'botas-madeira',
		'name': 'Botas de Madeira',
		'type': ["equipment", "armor", "boots", "wood", "defense"],
		'description': 'Botas reforçadas que protegem os pés durante o combate.',
		'equip': True,
		'slot': "foot",
		'damage': 0,
		'defense': 0.07,
		'value': 40
	},
}

tags_consumibles = [
	'potion', 'food', 'herb',
	'flower', 'mushroom', 'fungus',
	'root'
]
for item in all_items.values():
	for tag in tags_consumibles:
		if tag in item.get("type", []):
			item['consumible'] = True
			break

from system_species import SPECIES

for specie in SPECIES:
	all_items[f"crystal-{specie['race']}"] = {
		'id': f"crystal-{specie['race']}",
		'name': f"Cristal mágico {specie['race']}",
		'type': ["resource", "material", "crystal", "magic", "species"],
		'description': '...',
		'value': int(12 * specie['attributes'].get('strength', 0.5))
	}
from utils import format_option

map_sheet = {
	'elven-high': {
		'main': {
			'title': 'Reino de Elven High',
			'options': [
				format_option('Taberna Olho de Gato', {'text': 'igg-local', 'local': 'elven-high'}),
				format_option('Mercado de Elven High', {'text': 'marketplace-local', 'local': 'elven-high'}),
				format_option('Guilda Corvo Negro', {'text': 'guild-local', 'local': 'elven-high'}),
				format_option('Floresta Encantos', {'text': 'forest-local', 'local': 'elven-high'}),
				format_option('Ir para Dragon Faces', {'text': 'dragon-faces', 'local': 'elven-high'}),
				format_option('Pausa', {'text': 'pause-game'})
			]
		},
		'igg-local': {
			'title': 'Taberna Olho de Gato',
			'options': [
				format_option('Dormir 50G', {'text': 'sleep', 'local': 'elven-high', "value": 50}),
				format_option('Servos', {'text': 'beast-room', 'local': 'elven-high'}),
				format_option('Mesa de Alquimia', {'text': 'alchemist', 'local': 'elven-high'}),
				format_option('Mesa de Encantamentos', {'text': 'enchants', 'local': 'elven-high'}),
				format_option('Baú Pessoal', {'text': 'chest', 'local': 'elven-high'}),
				format_option('Voltar', {'text': 'main', 'local': 'elven-high', "default": True}),
				format_option('Pausa', {'text': 'pause-game'})
			]
		},
		'marketplace-local': {
			'title': 'Mercado de Elven High',
			'options': [
				format_option('Ferreiro', {'text': 'blacksmith-local', 'local': 'elven-high'}),
				format_option('Alquimista', {'text': 'alchemist-local', 'local': 'elven-high'}),
				format_option('Caçador', {'text': 'hunter-local', 'local': 'elven-high'}),
				format_option('Mercado de feras', {'text': 'market-slave-local', 'local': 'elven-high'}),
				format_option('Voltar', {'text': 'main', 'local': 'elven-high', "default": True}),
				format_option('Pausa', {'text': 'pause-game'})
			]
		},
		'guild-local': {
			'title': 'Guilda Corvo Negro',
			'options': [
				format_option('Buscar missão', {'text': 'search-mission', 'local': 'elven-high'}),
				format_option('Completar missão', {'text': 'complete-mission', 'local': 'elven-high'}),
				format_option('Voltar', {'text': 'main', 'local': 'elven-high', "default": True}),
				format_option('Pausa', {'text': 'pause-game'})
			]
		},
		'forest-local': {
			'title': 'Floresta Encantos',
			'options': [
				format_option('Procurar Plantas', {'text': 'search-plants', 'local': 'elven-high'}),
				format_option('Procurar Monstros e Animais', {'text': 'monster-hunt', 'local': 'elven-high'}),
				format_option('Explorar Masmorras locais', {'text': 'dungeons-local', 'local': 'elven-high'}),
				format_option('Voltar', {'text': 'main', 'local': 'elven-high', "default": True}),
				format_option('Pausa', {'text': 'pause-game'})
			]
		}
	}
}
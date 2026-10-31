import random
import os
import subprocess

def clear_screen():
	if os.name == 'nt':
		subprocess.call('cls', shell=True)
	else:
		subprocess.call('clear', shell=True)

def generator_name(length=2):
	siglas = []
	for v in 'aeiou':
		for c in 'bcdfghjklmnpqrstvwxyz':
			siglas.append(f'{c}{v}')
	return ''.join(random.choice(siglas) for _ in range(length)).capitalize()

def generator_id(length=8, init=''):
	characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
	random_string = ''.join(random.choice(characters) for _ in range(length))
	return f"{init}{random_string}"

def format_option(text=None, data={}) -> list:
	return [text, data]

def selection_options(options, title, subtitle) -> list:
	options_valids = [x for x in options if not x[0] is None]
	max_x = max([len(x[0]) for x in options_valids])+2
	max_y = len(str(len(options_valids)))+2

	if all([not x[1].get("default", False) for x in options_valids]):
		for i in range(len(options_valids)):
			if options_valids[i][1].get("text") == "back":
				options_valids[i][1]["default"] = True

	text_line = f'{title}\n\n'
	for pos, text in enumerate([x[0] for x in options_valids]):
		hotkey = options_valids[pos][1].get('hotkey', [])
		list_hotkey = f"{', '.join([x for x in hotkey])}"
		if hotkey:
			list_hotkey = f' ( {list_hotkey} )'
		text_line += f' [{str(pos+1).center(max_y, " ")}] {text.center(max_x, " ")}{list_hotkey}\n'
	text_line += f'\n{subtitle}'
	while(True):
		clear_screen()
		prompt = input(text_line).strip().lower()
		if prompt.isnumeric():
			n = int(prompt)
			if n > 0 and n <= len(options_valids):
				return options_valids[n-1]
		else:
			if prompt == '':
				for text, data in options_valids:
					if data.get("default") == True:
						return [text, data]
			if prompt.isalpha() and prompt != '':
				for text, data in options_valids:
					if prompt in data.get("hotkey", []):
						return [text, data]

def only_confirm(text, str_1='Sim', str_2='Não', default=None):
	return selection_options([
		format_option(str_1, {'text': True, 'default': default == True}),
		format_option(str_2, {'text': False, 'default': default == False}),
	], text, 'Escolha uma das Respostas: ')[1]['text']

def only_number(title, _min=0, _max=999999):
	while(True):
		n = input(title).strip()
		if n.isnumeric():
			n = int(n)
			if n >= _min and n <= _max:
				title = f"Quer mesmo {n}?"
				options = [
					format_option('Sim', {'text':True, 'default': True}),
					format_option('Não', {'text':False}),
				]
				subtitle = "Escolha uma das opções:"
				if selection_options(options, title, subtitle)[1]:
					return n
				else:
					clear_screen()
					print(f"Por favor apenas números entre {_min} e {_max}!")
			else:
				clear_screen()
				print("Por favor apenas números inteiros!")

def breaklines_text(text, size=32):
	texts_lines = []
	for line in text.split('\n'):
		text_line = ""
		for word in line.split():
			if len(text_line) >= size:
				texts_lines.append(text_line)
				text_line = ""
			text_line += f" {word}"
		if not text_line in texts_lines:
			texts_lines.append(text_line)
	return texts_lines

def table_informations(data, title, size_max_y=20):
	size_w = 6
	size_x = max([len(str(x)) for x in data.keys()]) + size_w

	new_tab_r = []
	for key, value in data.items():
		for i, text in enumerate(breaklines_text(str(value), size_max_y)):
			new_tab_r.append([key if i == 0 else " ", text])
	size_y = max([len(str(value)) for key, value in new_tab_r]) + size_w

	new_tab = {
		f"{str(text_x).center(size_x, ' ')}":f"{str(text_y).center(size_y, ' ')}"
		for text_x, text_y in data.items()}

	size_z = size_x + size_y + 1

	text_lines = []
	text_lines.append(f"|{"-"*((size_x+size_y)+1)}|")
	text_lines.append(f"|{title.center(size_z, " ")}|")
	text_lines.append(f"|{"-"*((size_x+size_y)+1)}|")
	for key, value in new_tab_r:
		text_lines.append(f"|{key.center(size_x, ' ')}|{value.center(size_y, ' ')}|")
	text_lines.append(f"|{"-"*((size_x+size_y)+1)}|")
	return '\n'.join(text_lines)

def table_show_label(title, subtitle):
	title = breaklines_text(title)
	subtitle = breaklines_text(subtitle)

	max_title = max([len(x) for x in title])
	max_subtitle = max([len(x) for x in subtitle])
	size_max = max(max_title, max_subtitle)

	increment = 5

	size_max += increment

	texts_lines = ""
	texts_lines += f"|{''.center(size_max, '-')}|\n"
	for text in title:
		texts_lines += f"|{text.center(size_max, ' ')}|\n"
	texts_lines += f"|{''.center(size_max, '-')}|\n"
	for text in subtitle:
		texts_lines += f"|{text.center(size_max, ' ')}|\n"
	texts_lines += f"|{''.center(size_max, ' ')}|\n"
	texts_lines += f"|{''.center(size_max, ' ')}|\n"
	texts_lines += f"|{''.center(size_max, ' ')}|\n"
	texts_lines += f"|{'Pressione Enter'.center(size_max, ' ')}|\n"
	texts_lines += f"|{''.center(size_max, ' ')}|\n"
	texts_lines += f"|{''.center(size_max, '-')}|\n"

	return texts_lines


if __name__ == '__main__':
	data = {
		"Nome":"Cardo Elétrico",
		"Descrição":"Uma planta carregada de energia usada para criar resistência contra danos elétricos.",
		"Valor": 120,
	}
	print(table_informations(data,
		"Informações de items"))
# runner_app_python.py
from utils import clear_screen
import random
import os

folder_main = os.getcwd()
app_default = os.path.join(folder_main, "main.py")
app_current = app_default


def runner(file):
	try:
		os.system(f'python "{file}"')
	except Exception as inst:
		print()
		print(type(inst))
		print(inst.args)
		print(inst)

def change_file(file):
	global app_default, app_current, folder_main
	if file == "df" and app_current != app_default:
		app_current = app_default
		print("O arquivo padrão foi setado com sucesso.")
		return False
	elif file == "df" and app_current == app_default:
		print("O arquivo padrão já está setado.")
		return False
	elif not app_current.endswith(file):
		app_current = os.path.join(folder_main, file)
		return True
	else:
		return False
		print(f"O arquivo já está selecionado: {file}")

def selected_file(path):
	from utils import format_option, selection_options
	while(True):
		options = [format_option(x, {"text": x})
			for x in os.listdir(path) if not app_current.endswith(x) and x.endswith(".py")]
		options.append(format_option("Voltar", {"text": "back", 'default': True}))
		selected = selection_options(options, "Selecione um Arquivo:", "Escolha uma opção: ")[1]["text"]
		if selected == "back":
			print("Mudanda de programa cancelado.")
			break
		else:
			if change_file(selected):
				print(f"Programa mudado com sucesso.\nRun: {selected}")
			break

while(True):
	try:
		prompt = input("@user: ").strip()
		if prompt == "df":
			change_file("df")
		elif prompt == 'cg':
			selected_file(folder_main)
		elif prompt == 'clear':
			clear_screen()
		else:
			runner(app_current)
	except KeyboardInterrupt:
		os.system("cls")
		print("Programa encerrado")




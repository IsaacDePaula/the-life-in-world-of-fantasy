# debug_games.py
class DEBUG(object):
	def __init__(self, activated=True, register=False):
		self.log_register = []
		self.activated = activated
		self.register = register

	def print(self, *args, truf=" ", end="\n"):
		if self.activated:
			if self.register:
				text = truf.join([x for x in args])+end
				self.log_register.append(text)
			print(*args, end=end)

	def input(self, *args):
		if self.activated:
			if self.register:
				text = truf.join([x for x in args])+end
				self.log_register.append(text)
			return input(*args)

if __name__=="__main__":
	app = DEBUG(False)
	app.print("Uau", "Seu nome é Incrivel.")
	app.input("\n\nPressione Enter Para Continuar.")
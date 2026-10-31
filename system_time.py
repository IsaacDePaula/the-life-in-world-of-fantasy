class System_Time(object):
	def __init__(self, h, m, d, y, base=360):
		self.data = {
			'h': h, # horas
			'm': m, # minutos
			'd': d, # dias
			'y': y # anos
		}
		self.base = base
		
		self.get_h = lambda: self.get_values("h")
		self.get_m = lambda: self.get_values("m")
		self.get_d = lambda: self.get_values("d")
		self.get_y = lambda: self.get_values("y")

	def get_bd(self):
		return self.base

	def add_timer(self, h=0, m=0, d=0, y=0):
		self.data['h'] += h
		self.data['m'] += m
		self.data['d'] += d
		self.data['y'] += y

		templete = [
			['m', 60, 'h', 1], 
			['h', 24, 'd', 1], 
			['d', self.base, 'y', 1]
		]
		for key_i, value_i, key_o, value_o in templete:
			while(self.data[key_i] >= value_i):
				self.data[key_i] -= value_i
				self.data[key_o] += value_o

	def remove_timer(self, h=0, m=0, d=0, y=0):
		self.data['h'] -= h
		self.data['m'] -= m
		self.data['d'] -= d
		self.data['y'] -= y

		templete = [
			['m', 60, 'h', 1], 
			['h', 24, 'd', 1], 
			['d', self.base, 'y', 1]
		]
		for key_i, value_i, key_o, value_o in templete:
			while(self.data[key_i] < 0):
				self.data[key_i] += value_i
				self.data[key_o] -= value_o

	def get_timer(self):
		return [self.get_values(x) for x in 'hmdy']

	def get_values(self, key):
		return self.data.get(key, None)

	def set_values(self, key, value):
		if key in self.data:
			self.data[key] = value

	def date(self):
		dy = self.get_values("d")
		yr = self.get_values("y")
		return f"D{dy}/Y{yr}"

	def string(self):
		hr = self.get_values("h")
		mt = self.get_values("m")

		dy = self.get_values("d")
		yr = self.get_values("y")
		return f"{hr:02d}:{mt:02d}_ D{dy}/Y{yr}"
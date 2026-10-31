# system_relationship.py
class System_Tree_Family(object):
	def __init__(self):
		self.knowledge = {}
		self.status = {}

	def get_members_per_tag(self, tag):
		all_tags = [key
			for key, values in self.knowledge.items()
			if tag in values]
		return all_tags

	def add_tags(self, member, tags):
		key = member.get_id()
		if not key in self.knowledge:
			self.knowledge[key] = []
		if type(tags) == list:
			for key_tag in tags:
				if not key_tag in self.knowledge[key]:
					self.knowledge[key].append(key_tag)
		else:
			if not tags in self.knowledge[key]:
				self.knowledge[key].append(tags)

	def search_tag(self, tag, member):
		if tag in self.knowledge.get(member.get_id(), []):
			return True
		return False

	def remove_tag(self, tag, member):
		key = member.get_id()
		if tag in self.knowledge.get(key, []):
			self.knowledge[key].remove(tag)


class System_Relationship(object):
	def __init__(self, entitie):
		self.base_config = {}

	def register_new_interaction(self, user, target):
		import copy
		base = {
			'affinity': 0, # afinidade
			'attraction': 0, # atração
			'friendship': 0, # amizade
			'respect': 0, # respeito
			'fear': 0, # medo
			'trust': 0, # confiança
		}
		if user.relationships.status.get(target.get_id(), False) == False:
			user.relationships.status[target.get_id()] = copy.deepcopy(base)
		if target.relationships.status.get(user.get_id(), False) == False:
			target.relationships.status[user.get_id()] = copy.deepcopy(base)

	def interaction(self, user, target):
		self.register_new_interaction(user, target)
		options = [
			format_option("Conversar", {"text": 'chat'}),
			format_option("Romance", {"text": 'flirt'}),
			format_option("Insultar", {"text": 'insult'}),
			format_option("Pedir", {"text": 'ask'}),
		]


if __name__=="__main__":
	from system_creatures import System_Creature as sys_creature

	a = sys_creature("npc1")
	b = sys_creature("npc2")

	sys_relationship = System_Relationship(a)


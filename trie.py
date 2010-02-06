class Trie(object):
	def __init__(self, filename = None):
		self.nodes =  {'': {}} # Empty string as root node
		self.suggestions = []
		self.limit = None

		if filename:
			self.add_from_file(filename)

	def add_from_list(self, l):
		for word in l:
			self.add_word(word)

	def add_from_file(self, f):
		file = open(f, 'r')
		for line in file:
			self.add_word(line.rstrip().lower())
		file.close()

	def add_word(self, word):
		current_node = self.nodes[''] # Empty string as root node
		for char in word:
			# If a key is present, set the current node and continue
			if current_node.has_key(char):
				current_node = current_node[char]
			# If no key is found, set the current key to 
			# point to an empty dict and update the current node
			else:
				current_node[char] = {}
				current_node = current_node[char]
		# Append empty node for each full word
		# Without this, subsets (i.e. big from [[big]ger,est]) will not be found
		current_node[''] = None

	def suggest(self, prefix, limit = 0):
		if limit > 0:
			self.limit = limit 
		self.suggestions = [] # Reset suggestions
		current_node = self.nodes['']
		prefix = prefix.rstrip().strip().lower()

		# Loop through the nodes, set the current node
		# if the char is found
		for char in prefix:
			if current_node.has_key(char):
				current_node = current_node[char]
			else:
				current_node = None
				break
		if current_node:
			self.build_suggestions(prefix, current_node)
		return self.suggestions

	def build_suggestions(self, prefix, node):
		self.build_words(prefix, node)
		return self.suggestions

	def build_words(self, prefix, node):
		# Loop through the nodes
		for char, dict in node.items():
			# Append the prefix with each char
			word = prefix + char
			# Recurse if the node has a dict with items
			if dict:
				self.build_words(word, node[char])
			# Otherwise, we've completed a word
			else:
				if self.limit and len(self.suggestions) >= self.limit:
					return
				else:
					self.suggestions.append(word)

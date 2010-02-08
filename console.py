import time, trie

class TrieConsole(object):
	def __init__(self, filename):
		self.trie = trie.Trie()
		print 'Loading file ' + filename
		self.trie.add_from_file(filename)
		self.cursor()
	
	def cursor(self):
		prefix = raw_input('Enter prefix: ')
		t0 = time.time()
		suggestions = self.trie.suggest(prefix)
		t1 = time.time() - t0
		print "Suggestions: %s\nNumber: %s\nTime: %s seconds\n" % ( suggestions, len(suggestions), t1 )
		self.cursor()
		
if __name__ == '__main__':
	try:
		ts = TrieConsole('dict/wordlist.txt')
	except KeyboardInterrupt:
		print ' Interrupt received. Exiting.'

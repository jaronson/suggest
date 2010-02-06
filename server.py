#!/usr/bin/env python
# The basics on the server for clients:
# Request with a normal HTTP header. GET, POST, PUT, DELETE -- it doesn't matter
# The requested resource must be /suggest and the get value prefix= must be set
# otherwise the client will receive a 400 error
# Example: GET /suggest?prefix=mar HTTP/1.1

import sys, os, socket, urlparse, threading
import trie

class SuggestThread(threading.Thread):
	def __init__(self, client, address):
		threading.Thread.__init__(self)
		self.client = client
		self.address = address
		self.cfile = None 

		self.process_request()

	def process_request(self):
		buffer = self.client.recv(1024)
		self.cfile = self.client.makefile('rw', 0)
		if buffer:
			params = self.get_params(buffer)
			if params:
				self.write_response(params)
			else:
				self.write_error()
		else:
			self.write_error()
		self.cfile.close()
		self.client.close()

	def get_params(self, buffer):
		header = buffer.split('\r\n')
		if len(header):
			try:
				print_flush(header[0])
				method, path, protocol = header[0].split(' ')
			except ValueError:
				return False
			if path:
				url = urlparse.urlsplit(path)
				params = urlparse.parse_qs(url.query)
				if params.has_key('prefix'):
					return params
		return False

	def write_response(self, params):
		self.cfile.write('HTTP/1.1 200 OK\r\n') 
		self.cfile.write('Cache-Control: no-cache, must-revalidate\r\n')
		self.cfile.write('Content-Type: text/html\r\n')
		self.cfile.write('\r\n')

		limit = 0
		if params.has_key('limit'):
			limit = int(params['limit'][0])
		suggestions = suggestion_trie.suggest(params['prefix'][0], limit)
		self.cfile.write(str(suggestions).replace("'",'"'))

	def write_error(self):
		self.cfile.write('HTTP/1.1 400 Bad Request\r\n ')
		self.cfile.write('\r\n')

class SuggestServer(object):
	def __init__(self, host, port):
		self.host = host
		self.port = port

		self.make_socket()
		self.listen()

	def __del__(self):
		self.socket.close()

	def make_socket(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.socket.bind((self.host, self.port))
	
	def listen(self):
		self.socket.listen(1)
		print_flush('SuggestServer listening on %s:%s' % ( self.host, self.port ))

		while True:
			client, address = self.socket.accept()
			t = SuggestThread(client, address)

def print_flush(str):
	sys.stdout.write(str)
	sys.stdout.write('\n')
	sys.stdout.flush()

if __name__=='__main__':
	print_flush('Loading word list ...')
	suggestion_trie = trie.Trie('dict/wordlist.txt')
	print_flush('Word list loaded.')

	try:
		ss = SuggestServer('127.0.0.1', 4000)
	except KeyboardInterrupt:
		print_flush(' Interrupt received. Shutting down')
		ss = None

import os
from game137lib import *

clear = lambda: os.system('cls')

class Client(object):
	def __init__(self):
		#================================== INITIALIZE CLIENT ==================================#
		self.ip = '127.0.0.34'
		self.port = 5005
		self.buffer_size = 1024		
		self.current_cards = []
	def start(self):
		#================================== ENTER DETAILS ==================================#
		# self.ip = str(input("Specify Host IP Address: "))
		# self.port = int(input("Specify Port: "))
		self.player_name = input('Enter your player name: ')

		#================================== CONNECT TO SERVER ==================================#
		self.sckt = ClientNetworkHandler(self.ip, self.port, self.player_name)
		self.sckt.joinServer()
		data = self.sckt.sckt.recv(self.buffer_size)
		message = str(data.decode('utf8'))

		#================================== IF ACCEPTED ==================================#
		if message[:2] == NetworkCommand.SERVER_ACCEPT_PLAYER:
			while True:
				x = input('[1] Vote Start\n[2] Leave Lobby\n>>>')

				#================================== ON VOTE ==================================#
				if x == '1':
					print('Waiting for other players to start...')
					self.sckt.voteStart()
					data = self.sckt.sckt.recv(self.buffer_size)
					message = str(data.decode('utf8'))

					#================================== GAME LOOP ==================================#
					if message[:2] == NetworkCommand.SERVER_START_GAME:
						print('Game has commenced')
						data = self.sckt.sckt.recv(self.buffer_size)
						message = str(data.decode('utf8'))
						print(message)
						if message[:2] == NetworkCommand.SERVER_SEND_CARDS:
							card_string = message[2:]
							self.current_cards = card_string.split(' ')
							print('yay')
						else:
							print('wtf')
						# while True:
						# 	data = self.sckt.sckt.recv(self.buffer_size)
						# 	message = str(data.decode('utf8'))
						# 	print(message)
						# 	if message[:2] == NetworkCommand.SERVER_SEND_CARDS:
						# 		card_string = message[2:]
						# 		self.current_cards = card_string.split(' ')
						# 	else:
						# 		break

					break
				#================================== ON LEAVE ==================================#
				elif x == '2':
					print('Leaving Lobby...')
					self.sckt.leaveLobby()
					break
				else:
					print('Bitch, I gave you two choices.')

		#================================== IF NOT ACCEPTED ==================================#
		else:
			print('Server is full.')
		print('Closing Game...')
		self.sckt.close()

c = Client()
c.start()
import game137lib
import os
clear = lambda: os.system('cls')

class Client(object):
	def __init__(self):
		#================================== INITIALIZE CLIENT ==================================#
		self.ip = '127.0.0.1'
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
		data = self.sckt.recv(self.buffer_size)
		message = str(data.decode('utf8'))

		#================================== IF ACCEPTED ==================================#
		if message[:2] == NetworkCommand.SERVER_ACCEPT_PLAYER:
			while True:
				x = input('[1] Vote Start\n[2] Leave Lobby')

				#================================== ON VOTE ==================================#
				if x == '1':
					print('Waiting for other players to start...')
					data = self.sckt.recv(self.buffer_size)
					message = str(data.decode('utf8'))

					#================================== GAME LOOP ==================================#
					if message[:2] == NetworkCommand.SERVER_START_GAME:
						while True:
							data = self.sckt.recv(self.buffer_size)
							message = str(data.decode('utf8'))
							if message[:2] == NetworkCommand.SERVER_SEND_CARDS:
								card_string = message[2:]
								self.current_cards = [card_string[i:i+2] for i in range(0, len(card_string), 2)]
								pass #TODO
							else:
								pass
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
		sckt.close()
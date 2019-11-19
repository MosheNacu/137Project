import os
from game137lib import *

clear = lambda: os.system('cls')

class Client(object):
	def __init__(self):
		#================================== INITIALIZE CLIENT ==================================#
		self.ip = '127.0.0.34'
		self.port = 5005
		self.buffer_size = 1024
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
						print('Game has commenced...')
						while True:
							data = self.sckt.sckt.recv(self.buffer_size)
							message = str(data.decode('utf8'))
							if message[:2] == NetworkCommand.SERVER_SEND_CARDS:
								card_string = message[2:]
								current_cards = card_string.split(' ')
								#================================== WIN CHECK ==================================#
								winConditionValue = current_cards[0][:-1]
								if len([w for w in current_cards if w[:-1] == winConditionValue]) == len(current_cards):
									print('Your cards are complete! Hurry and put down your cards!\n[1] Put Down Cards')
									while True:
										try:
											x = int(input('>>>'))
											if(x == 1):
												self.sckt.putDown()
												break
											print('That is not a choice.')
											continue
										except:
											print('That is not a choice.')
											continue
									break
								#================================== CHOOSE CARD ==================================#
								while True:
									print('Choose the card to pass to your right!')
									for i in range(len(current_cards)):
										print("[{0}] {1}".format(i+1, current_cards[i]))
									try:
										x = int(input('>>>'))
										if(x > 0 and x < 5):
											break
										print('Please type your card again.')
										continue
									except:
										print('Please type your card again.')
										continue
								self.sckt.chooseCard(current_cards[x-1])
							#================================== SOMEONE ELSE WON ==================================#
							elif message[:2] == NetworkCommand.SERVER_WINNER_DECLARED:
								print('Someone has already won! Hurry and put down your cards!\n[1] Put Down Cards')
								while True:
									try:
										x = int(input('>>>'))
										if(x == 1):
											self.sckt.putDown()
											break
										print('That is not a choice.')
										continue
									except:
										print('That is not a choice.')
										continue
								break
							else:
								break
					break
				#================================== ON LEAVE ==================================#
				elif x == '2':
					print('Leaving Lobby...')
					self.sckt.leaveLobby()
					break
				else:
					print('Please choose one of the two choices.')

		#================================== IF NOT ACCEPTED ==================================#
		else:
			print('Server is full.')
		print('Closing Game...')
		self.sckt.close()

c = Client()
c.start()
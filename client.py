import game137lib
import os
clear = lambda: os.system('cls')

class Client(object):
	def __init__(self):
		self.sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.msgBuilder = MsgGen()
		self.currentPlayers = ""
	def start(self):
		# self.serverIP = str(input("Specify Host IP Address: "))
		# self.serverPort = int(input("Specify Port: "))
		self.serverIP = '127.0.0.1'
		self.serverPort = 5005
		self.buffer_size = 1024
		self.sckt.connect((self.serverIP, self.serverPort))

		self.name = input('Enter your player name: ')
		joinMessage = self.msgBuilder.build(self.name, MsgGen.CLIENT_JOIN_GAME)
		self.sckt.send(joinMessage)
		joinReply = self.sckt.recv(Client.BUFFER_SIZE)
		self.currentPlayers = self.msgBuilder.getString(joinReply)
		print("Waiting for Players: {0}".format(self.currentPlayers))
		if self.msgBuilder.getType(joinReply) == MsgGen.SERVER_ACCEPT_PLAYER:
			while True:
				clear()
				x = input('[1] Vote Start\n[2] Leave Room\n> ')
				if len(x) > 2 && x[:2] == ">>1":
					pass
				else if len(x) > 2 && x[:2] == ">>2":
					pass
				else if len(x) > 0:
					
		else:
			print('Server is full.')
		sckt.close()


msg = str(data.decode('utf8'))
if (msg == "AC"):
	while True:
		print("Waiting for other players")
		print("[1] Vote Start")
		print("[2] Leave Room")
		x = input()
s.close()
print ("received data:", data)
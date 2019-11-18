import game137lib

class Server(object):
	def __init__(self):
		self.ip = '127.0.0.1'
		self.port = 5005
		self.buffer_size = 1024
	def start(start):
		self.players = []
		self.sckt = ServerNetworkHandler(self.ip, self.port, self.buffer_size)
		while True: # server loop
			while True: # invite loop
				conn, addr = sckt.accept()
				data = conn.recv(BUFFER_SIZE)
				msg = str(data.decode('utf8'))
				if msg[0:2] == "JG": 			#checks if player is joining game
					if(len(players) < 13):
						players.append(Player(conn, addr, msg[3:])) 	#adds player
						print(players[0].playerName)
						conn.send("AC".encode('utf8'))
					else:
						conn.send("RJ".encode('utf8'))
				if msg[0:2] == "VT":


		conn.close()
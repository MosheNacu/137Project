import socket

class Player:
	def __init__(self, conn, addr, playerName):
		self.conn = conn
		self.addr = addr
		self.playerName = playerName
		self.vote = False

TCP_IP = '127.0.0.3'
TCP_PORT = 5005
BUFFER_SIZE = 1024
print("server is up and running ...")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

players = []	#key: player name   value:conn

while True: 							#server loop
	while True: 						#invite loop
		conn, addr = s.accept()
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


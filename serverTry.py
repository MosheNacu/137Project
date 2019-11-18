import socket
import threading

class Player:
	def __init__(self, conn, addr, playerName):
		self.conn = conn
		self.addr = addr
		self.playerName = playerName
		self.vote = False

class yaboi (threading.Thread):
	def __init__(self, player):
		threading.Thread.__init__(self)
		self.player = player
	def run(self):
		while True:
			data = self.player.conn.recv(BUFFER_SIZE)
			msg = str(data.decode('utf8'))
			self.player.conn.send("ya boi {0}".format(msg).encode('utf8'))
			if msg == "end":
				break



TCP_IP = '127.0.0.5'
TCP_PORT = 5005
BUFFER_SIZE = 1024
print("server is up and running ...")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

threads = []
players = []	#key: player name   value:conn

while True: 						#invite loop
	conn, addr = s.accept()
	print("accept")
	newplayer =Player(conn, addr, "ya boi")
	print("added new")
	players.append(newplayer) 	#adds player
	newyaboi = yaboi(newplayer)
	threads.append(newyaboi)
	newyaboi.start()
	print("started ya boi")
	# if msg[0:2] == "JG": 			#checks if player is joining game
	# 	if(len(players) < 13):
	# 		players.append(Player(conn, addr, msg[3:])) 	#adds player
	# 		print(players[0].playerName)
	# 		conn.send("AC".encode('utf8'))
	# 	else:
	# 		conn.send("RJ".encode('utf8'))
	# if msg[0:2] == "VT":
for t in threads:
	t.join()

conn.close()
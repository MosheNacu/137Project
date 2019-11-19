# import game137lib
# import threading
from game137lib import *

r = threading.RLock()
class PlayerSocketThread (threading.Thread):
	def __init__(self, sckt, player):
		#================================== INITIALIZE SOCKET THREAD ==================================#
		threading.Thread.__init__(self)
		self.player = player
		self.sckt = sckt
		self.buffer_size = 1024
	def run(self):
		#================================== THREAD FOR EACH PLAYER CONNECTION ==================================#
		while True:
			data = self.player.conn.recv(self.buffer_size)
			message = str(data.decode('utf8'))
			if message[:2] == NetworkCommand.CLIENT_VOTE_START:
				print('Client Vote Start')
				self.player.vote = True

			elif message[:2] == NetworkCommand.CLIENT_LEAVE:
				self.sckt.removePlayer(self.player)
				print("{0} Left The Lobby...".format(self.player.player_name))

			elif message[:2] == NetworkCommand.CLIENT_CHOOSE_CARD:
				print('Client Choose Card')

			elif message[:2] == NetworkCommand.CLIENT_PUT_DOWN:
				print('Client Put Down')

class Server(object):
	def __init__(self):
		#================================== INITIALIZE SERVER ==================================#
		self.ip = '127.0.0.34'
		self.port = 5005
		self.buffer_size = 1024
		self.players = []
		self.threads = []
		self.baseDeck = [[str(i)+x for x in ['D', 'H', 'S', 'C']] for i in range(1,14)]
	#================================== THREAD LOCKS FOR PLAYER LIST ==================================#
	def addPlayer(self, player):
		r.acquire()
		self.players.append(player)
		r.release()

	def removePlayer(self, player):
		r.acquire()
		self.players.remove(player)
		r.release()

	def getPlayers(self):
		return list(self.players)
		

	def start(self):
		#================================== START SERVER ==================================#
		self.sckt = ServerNetworkHandler(self.ip, self.port, self.buffer_size)

		#================================== LOBBY LOOP ==================================#
		while True:

			self.sckt.setTimeOut(1.0)
			#================================== RECEIVE PLAYER JOIN ==================================#
			try:
				conn, addr = self.sckt.socketAccept()
				data = conn.recv(self.buffer_size)
				message = str(data.decode('utf8'))
				if message[:2] == NetworkCommand.CLIENT_JOIN_GAME:

					#================================== ACCEPT PLAYER IF NOT FULL ==================================#
					new_player = Player(conn, addr, message[2:])
					if(len(self.players) < 13):
						new_thread = PlayerSocketThread(self.sckt, new_player)
						new_thread.start()
						self.addPlayer(new_player)
						self.threads.append(new_thread)
						self.sckt.sendAccept(new_player)

					#================================== REJECT PLAYER IF FULL ==================================#
					else:
						self.sckt.sendReject(newPlayer)
				else:
					conn.close()
			except socket.timeout as e:
				pass

			#================================== VOTE TALLYING ==================================#
			all_players = self.getPlayers()
			total_players = len(all_players)
			vote_count = len([x for x in all_players if x.vote])
			if total_players > 2 and vote_count == total_players:
				print('Game started')
				for x in self.getPlayers():
					try:
						self.sckt.sendStartGame(x)
					except Exception as e:
						print(e)
				break
		self.sckt.setTimeOut(None)
		#================================== GAME LOOP ==================================#
		selected_cards = []
		selected_rand_int = []
		for x in range(len(self.players)):
			rand = random.randint(0, 12)
			if rand in selected_rand_int:
				pass
			else:
				selected_rand_int.append(rand)
				card_set = self.baseDeck[rand]
				selected_cards.extend(card_set)
		random.shuffle(selected_cards)
		print(selected_cards)

		for player in self.players:
			card = ''
			for _ in range(4):
				card = card + selected_cards.pop() + ' '
			self.sckt.sendCards(player, card)
			

		while True:
			continue
		#================================== JOIN THREADS ==================================#
		for t in self.threads:
			t.join()
		print('End')
s = Server()
s.start()
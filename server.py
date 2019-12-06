# import game137lib
# import threading
from game137lib import *
import operator

r = threading.RLock()
class PlayerSocketThread (threading.Thread):
	def __init__(self, server, player):
		#================================== INITIALIZE SOCKET THREAD ==================================#
		threading.Thread.__init__(self)
		self.player = player
		self.server = server
		self.buffer_size = 1024
	def run(self):
		#================================== THREAD FOR EACH PLAYER CONNECTION ==================================#
		while True:
			data = self.player.conn.recv(self.buffer_size)
			message = str(data.decode('utf8'))
			if message[:2] == NetworkCommand.CLIENT_VOTE_START:
				print("{0} voted to start!".format(self.player.player_name))
				self.player.setStateToVoted()

			elif message[:2] == NetworkCommand.CLIENT_LEAVE:
				self.server.removePlayer(self.player)
				print("{0} left the lobby...".format(self.player.player_name))
				break

			elif message[:2] == NetworkCommand.CLIENT_CHOOSE_CARD and Player.WINNER_RANK > 0:
				self.server.sckt.sendWinCondition(self.player)

			elif message[:2] == NetworkCommand.CLIENT_CHOOSE_CARD:
				self.player.setChosenCard(message[2:])
				print("{0} chose to pass the {1} card!".format(self.player.player_name, message[2:]))
				self.player.setStateToChosenCard()

			elif message[:2] == NetworkCommand.CLIENT_PUT_DOWN:
				self.player.placeInRanking()
				if (self.player.ranking == 1):
					for p in self.server.getPlayers():
						self.server.sckt.sendWinCondition(p)
					self.server.sckt.sendWinRanking(self.player)
				elif (self.player.ranking == len(self.server.getPlayers())):
					self.server.sckt.sendLoseRanking(self.player, self.player.ranking)
				else:
					self.server.sckt.sendPlaceRanking(self.player, self.player.ranking)

				print("{0} is rank {1}!".format(self.player.player_name, self.player.ranking))
				self.player.setStateToFinished()
				break

class Server(object):
	def __init__(self):
		#================================== INITIALIZE SERVER ==================================#
		self.ip = '127.0.0.2'
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
		
	def generateInitialCards(self):
		selected_cards = []
		taken_indices = []
		i = 0
		while i < len(self.players):
			index = random.randrange(0, 13)
			if index not in taken_indices:
				taken_indices.append(index)
				four_of_a_kind = self.baseDeck[index]
				selected_cards.extend(four_of_a_kind)
				i += 1
		random.shuffle(selected_cards)
		for player in self.players:
			tempCards = []
			for _ in range(4):
				tempCards.append(selected_cards.pop())
			player.cards = tempCards
			cards_to_send = ' '.join(tempCards)
			print("{0}'s cards are: {1}".format(player.player_name, cards_to_send))
			self.sckt.sendCards(player, cards_to_send)

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
						new_thread = PlayerSocketThread(self, new_player)
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
			vote_count = len([x for x in all_players if x.state == Player.STATE_VOTED])
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
		self.generateInitialCards()
		while True:
			while len([x for x in self.players if x.state == Player.STATE_CHOSEN_CARD]) != len(self.players) and Player.WINNER_RANK == 0:
				continue
			if Player.WINNER_RANK > 0:
				while len([x for x in self.players if x.state == Player.STATE_FINISHED]) != len(self.players):
					continue
				break

			number_of_players = len(self.players)
			for i in range(number_of_players):
				self.players[i].cards.remove(self.players[i].chosenCard)
				if i+1 < number_of_players: 
					self.players[i+1].cards.append(self.players[i].chosenCard)
				elif i+1 == number_of_players: 
					self.players[0].cards.append(self.players[i].chosenCard)
				self.players[i].chosenCard = None
			#swap cards
			for player in self.players:
				player.setStateToChoosingCard()
				print("{0}'s cards are: {1}".format(player.player_name, player.cards))
				self.sckt.sendCards(player, ' '.join(player.cards))

		tempList = sorted(self.players, key=operator.attrgetter('ranking'))
		for x in tempList:
			print("{0} - {1}".format(x.ranking, x.player_name))
		#================================== JOIN THREADS ==================================#
		for t in self.threads:
			t.join()
		print('End')


s = Server()
s.start()
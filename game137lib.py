import socket

class Player:
	def __init__(self, conn, addr, player_name):
		self.conn = conn
		self.addr = addr
		self.player_name = player_name
		self.vote = False
	def sendMessage(self, message):
		self.conn.send(message)

class NetworkCommand(object):
	CLIENT_JOIN_GAME = '01'
	SERVER_ACCEPT_PLAYER = '02'
	SERVER_REJECT_PLAYER = '03'
	CLIENT_VOTE_START = '04'
	CLIENT_LEAVE = '05'
	SERVER_START_GAME = '06'
	SERVER_SEND_CARDS = '07'
	CLIENT_CHOOSE_CARD = '08'
	SERVER_WINNER_DECLARED = '09'
	CLIENT_PUT_DOWN = '10'
	SERVER_RANKINGS = '11'

class ClientNetworkHandler(object):
	def __init__(self, ip, port, player_name):
		self.player_name = player_name
		self.server_ip = ip
		self.server_port = port
		self.sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def close(self):
		self.sckt.close()

	def sendCommand(self, network_command):
		message = network_command.encode('utf8')
		self.sckt.send(message)

	def joinServer(self):
		self.sckt.connect((self.server_ip, self.server_port))
		join_message = "{0}{1}".format(NetworkCommand.CLIENT_JOIN_GAME, self.player_name)
		message = join_message.encode('utf8')
		self.sckt.send(message)

	def voteStart(self):
		sendCommand(NetworkCommand.CLIENT_VOTE_START)

	def leaveLobby(self):
		sendCommand(NetworkCommand.CLIENT_LEAVE)

	def chooseCard(self, chosen_card):
		choose_message = "{0}{1}".format(NetworkCommand.CLIENT_CHOOSE_CARD, chosen_card)
		message = choose_message.encode('utf8')
		self.sckt.send(message)

	def putDown(self, card):
		sendCommand(NetworkCommand.CLIENT_PUT_DOWN)

class ServerNetworkHandler(object):	
	def __init__(self, ip, port, buffer_size):
		self.ip = ip
		self.port = port
		self.buffer_size = buffer_size
		self.sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sckt.bind((self.ip, self.port))
		self.sckt.listen(1)
		print('Server is up and running...')

	def setTimeOut(self, timeout):
		self.sckt.settimeout(timeout)

	def socketAccept(self):
		return self.sckt.accept()

	def sendCommand(self, player, network_command):
		message = network_command.encode('utf8')
		player.conn.send(message)

	def sendAccept(self, player):
		self.sendCommand(player, NetworkCommand.SERVER_ACCEPT_PLAYER)

	def sendReject(self, player)
		self.sendCommand(player, NetworkCommand.SERVER_REJECT_PLAYER)

	def sendStartGame(self, player):
		self.sendCommand(player, NetworkCommand.SERVER_START_GAME)

	def sendCards(self, player, cards):
		message = "{0}{1}".format(NetworkCommand.SERVER_SEND_CARDS, cards).encode('utf8')
		player.conn.send(message)

	def sendWinnerDeclaration(self, player, winner):
		message = "{0}{1}".format(NetworkCommand.SERVER_WINNER_DECLARED, winner).encode('utf8')
		player.conn.send(message)
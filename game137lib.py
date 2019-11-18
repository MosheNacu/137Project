import socket

class Player:
	def __init__(self, sckt, addr, playerName):
		self.sckt = sckt
		self.addr = addr
		self.playerName = playerName
		self.vote = False
	def sendMessage(self, message):
		sckt.send(message)

class NetworkCommand(object):
	GENERAL_MESSAGE = '00'
	CLIENT_JOIN_GAME = '01'
	SERVER_ACCEPT_PLAYER = '02'
	SERVER_REJECT_PLAYER = '03'
	CLIENT_VOTE_START = '04'
	CLIENT_LEAVE = '05'

class ClientNetworkHandler(object):
	def __init__(self, ip, port, player_name):
		self.player_name = player_name
		self.serverIP = ip
		self.serverPort = port
		self.sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sckt.connect((self.serverIP, self.serverPort))
	def sendCommand(self, networkCommand):
		message = networkCommand.encode('utf8')
		sckt.send(message)

	def joinServer(self):
		message = "{0}:{1}".format(NetworkCommand.CLIENT_JOIN_GAME, player_name)
		joinMessage = message.encode('utf8')
		sckt.send(joinMessage)

	def voteStart(self):
		sendCommand(NetworkCommand.CLIENT_VOTE_START)



class ServerNetworkHandler(object):	
	def __init__(self, ip, port, buffer_size):
		self.ip = ip
		self.port = port
		self.buffer_size = buffer_size
		self.sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sckt.bind((self.ip, self.port))
		self.sckt.listen(1)
		print("Server is up and running ...")

	def sendCommand(self, player, networkCommand):
		message = networkCommand.encode('utf8')
		player.sckt.send(message)

	def 


# class MsgGen(object):
# 	GENERAL_MESSAGE = "00"
# 	CLIENT_JOIN_GAME = "01"
# 	SERVER_ACCEPT_PLAYER = "02"
# 	SERVER_REJECT_PLAYER = "03"
# 	CLIENT_VOTE_START = "04"
# 	CLIENT_LEAVE = "05"

# 	@classmethod
# 	def build(cls, msg, msgType):
# 		s = "{1}:{0}".format(msg, msgType)
# 		return s.encode('utf8')

# 	@classmethod
# 	def getMessageType(cls, msg):
# 		msg = msg.decode('utf8')
# 		return msg[:2]

# 	@classmethod
# 	def getString(cls, msg):
# 		msg = msg.decode('utf8')
# 		try:
# 			s = msg[2:]
# 			return s
# 		except:
# 			return None
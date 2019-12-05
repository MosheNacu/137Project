import tkinter.ttk as ttk
import tkinter as tk
from game137lib import *
import threading

r = threading.RLock()

class CompleteGamePanel(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.alreadyPutDown = False
		self.buffer_size = 1024
		self.buildWindow()
		self.setWindowIcon()
		self.loadGraphics()
		self.buildCanvas()
		self.startMenu()
		self.window.mainloop()
	def buildWindow(self):
		self.window = tk.Tk()
		self.window.title("1-2-3 PASS ")
		self.window.geometry("640x480")
		self.window.resizable(0,0)
	def buildCanvas(self):
		self.canvas = tk.Canvas(self.window, width=640, height=480, background='#0d4f0a', highlightthickness=0)
		self.canvas.grid(column = 0, row = 0)
	def setWindowIcon(self):
		windowIcon = tk.PhotoImage(file = './graphics/game_icon.png')
		self.window.iconphoto(True, windowIcon)
	def loadGraphics(self):
		self.deckImages = {}

		self.someOneAlreadyWonBackground = tk.PhotoImage(file = './graphics/someonealreadywon.png')
		self.pickACardBackground = tk.PhotoImage(file = './graphics/pickacard.png')
		self.menuBackground = tk.PhotoImage(file = './graphics/menu.png')
		self.instructionBackground = tk.PhotoImage(file = './graphics/instructions.png')
		self.loseBackground = tk.PhotoImage(file = './graphics/lose.png')
		self.notloseBackground = tk.PhotoImage(file = './graphics/notlose.png')
		self.waitingBackground = tk.PhotoImage(file = './graphics/waiting.png')
		self.waitingCardBackground = tk.PhotoImage(file = './graphics/waitingcard.png')
		self.winBackground = tk.PhotoImage(file = './graphics/win.png')
		self.joinSettingsBackground = tk.PhotoImage(file = './graphics/joinsettings.png')
		self.joinSettingsErrorBackground = tk.PhotoImage(file = './graphics/joinsettingserror.png')

		self.goBackButtonImage = tk.PhotoImage(file = './graphics/button_go-back.png')
		self.placeDownButtonImage = tk.PhotoImage(file = './graphics/button_place-down.png')
		self.passButtonImage = tk.PhotoImage(file = './graphics/button_pass.png')
		self.instructionButtonImage = tk.PhotoImage(file = './graphics/button_instructions.png')
		self.leaveLobbyButtonImage = tk.PhotoImage(file = './graphics/button_leave-lobby.png')
		self.voteStartButtonImage = tk.PhotoImage(file = './graphics/button_vote-start.png')
		self.exitGameButtonImage = tk.PhotoImage(file = './graphics/button_exit-game.png')
		self.startGameButtonImage = tk.PhotoImage(file = './graphics/button_start-game.png')

		for i in range(1,14):
			for j in ['D', 'H', 'S', 'C']:
				tempID = "{0}{1}".format(i, j)
				tempPath = "./graphics/deck/{0}.png".format(tempID)
				self.deckImages[tempID] = tk.PhotoImage(file = tempPath)
	def startMenu(self):
		self.clearCanvas()
		currentBackground = self.canvas.create_image(0, 0, image=self.menuBackground, anchor=tk.NW)
		startButton = self.canvas.create_image(10, 380, image=self.startGameButtonImage, anchor=tk.NW)
		self.canvas.tag_bind(startButton, '<ButtonPress-1>', (lambda event: self.startJoinOptions()))
		instructionButton = self.canvas.create_image(220, 380, image=self.instructionButtonImage, anchor=tk.NW)
		self.canvas.tag_bind(instructionButton, '<ButtonPress-1>', (lambda event: self.startInstructions()))
		exitButton = self.canvas.create_image(430, 380, image=self.exitGameButtonImage, anchor=tk.NW)
		self.canvas.tag_bind(exitButton, '<ButtonPress-1>', (lambda event: self.window.destroy()))
	def startJoinOptions(self):
		self.clearCanvas()
		currentBackground = self.canvas.create_image(0, 0, image=self.joinSettingsBackground, anchor=tk.NW)
		ip_textfield = tk.Entry(self.canvas)
		ip_textfield.insert(0, "127.0.0.1")
		port_textfield = tk.Entry(self.canvas)
		port_textfield.insert(0, "5005")
		player_textfield = tk.Entry(self.canvas)
		player_textfield.insert(0, "Player")
		self.canvas.create_window(170, 140, window = player_textfield, height=30, width=300, anchor=tk.NW)
		self.canvas.create_window(170, 230, window = ip_textfield, height=30, width=300, anchor=tk.NW)
		self.canvas.create_window(170, 310, window = port_textfield, height=30, width=300, anchor=tk.NW)
		startButton = self.canvas.create_image(220, 380, image=self.startGameButtonImage, anchor=tk.NW)
		self.canvas.tag_bind(startButton, '<ButtonPress-1>', (lambda event: self.connectToServer(ip_textfield, port_textfield, player_textfield)))
	def startJoinOptionsError(self, ip="127.0.0.1", port="5005", player="Player"):
		self.clearCanvas()
		currentBackground = self.canvas.create_image(0, 0, image=self.joinSettingsErrorBackground, anchor=tk.NW)
		ip_textfield = tk.Entry(self.canvas)
		ip_textfield.insert(0, ip)
		port_textfield = tk.Entry(self.canvas)
		port_textfield.insert(0, port)
		player_textfield = tk.Entry(self.canvas)
		player_textfield.insert(0, player)
		self.canvas.create_window(170, 140, window = player_textfield, height=30, width=300, anchor=tk.NW)
		self.canvas.create_window(170, 230, window = ip_textfield, height=30, width=300, anchor=tk.NW)
		self.canvas.create_window(170, 310, window = port_textfield, height=30, width=300, anchor=tk.NW)
		startButton = self.canvas.create_image(220, 380, image=self.startGameButtonImage, anchor=tk.NW)
		self.canvas.tag_bind(startButton, '<ButtonPress-1>', (lambda event: self.connectToServer(ip_textfield, port_textfield, player_textfield)))
	def connectToServer(self, ip, port, username):
		try:
			self.networkHandler = ClientNetworkHandler(ip.get(), int(port.get()), username.get())
			self.networkHandler.joinServer()
			data = self.networkHandler.sckt.recv(self.buffer_size)
			message = str(data.decode('utf8'))
			if message[:2] == NetworkCommand.SERVER_ACCEPT_PLAYER:
				self.startLobby()
			else:
				self.startJoinOptionsError(ip.get(), port.get(), username.get())
		except Exception as e:
			print(e)
			self.startJoinOptionsError(ip.get(), port.get(), username.get())
	def startLobby(self):
		self.clearCanvas()
		voteStartButton = self.canvas.create_image(220, 200, image=self.voteStartButtonImage, anchor=tk.NW)
		self.canvas.tag_bind(voteStartButton, '<ButtonPress-1>', (lambda event: self.sendVoteStart()))
		leaveLobbyButton = self.canvas.create_image(220, 300, image=self.leaveLobbyButtonImage, anchor=tk.NW)
		self.canvas.tag_bind(leaveLobbyButton, '<ButtonPress-1>', (lambda event: self.sendLeaveLobby()))
	def sendVoteStart(self):
		self.clearCanvas()
		currentBackground = self.canvas.create_image(0, 0, image=self.waitingBackground, anchor=tk.NW)
		self.start()
		self.networkHandler.voteStart()
	def sendLeaveLobby(self):
		self.networkHandler.leaveLobby()
		self.startMenu()
	def startInstructions(self):
		self.clearCanvas()
		currentBackground = self.canvas.create_image(0, 0, image=self.instructionBackground, anchor=tk.NW)
		goBackButton = self.canvas.create_image(360, 420, image=self.goBackButtonImage, anchor=tk.NW)
		self.canvas.tag_bind(goBackButton, '<ButtonPress-1>', (lambda event: self.startMenu()))
	def startRound(self, cards=['3S', '4S', '5S', '6S'], forcePlacedown=False):
		self.clearCanvas()
		winConditionValue = cards[0][:-1]
		if (len([w for w in cards if w[:-1] == winConditionValue]) == len(cards)):
			firstCard = self.canvas.create_image(31, 100, image=self.deckImages[cards[0]], anchor=tk.NW)
			secondCard = self.canvas.create_image(183, 100, image=self.deckImages[cards[1]], anchor=tk.NW)
			thirdCard = self.canvas.create_image(609, 100, image=self.deckImages[cards[2]], anchor=tk.NE)
			fourthCard = self.canvas.create_image(457, 100, image=self.deckImages[cards[3]], anchor=tk.NE)
			placeDownButton = self.canvas.create_image(220, 350, image=self.placeDownButtonImage, anchor=tk.NW)
			self.canvas.tag_bind(placeDownButton, '<ButtonPress-1>', (lambda event: self.putDown()))

		elif forcePlacedown:
			currentBackground = self.canvas.create_image(0, 0, image=self.someOneAlreadyWonBackground, anchor=tk.NW)
			placeDownButton = self.canvas.create_image(220, 350, image=self.placeDownButtonImage, anchor=tk.NW)
			self.canvas.tag_bind(placeDownButton, '<ButtonPress-1>', (lambda event: self.putDown()))

		else:
			currentBackground = self.canvas.create_image(0, 0, image=self.pickACardBackground, anchor=tk.NW)
			firstCard = self.canvas.create_image(31, 100, image=self.deckImages[cards[0]], anchor=tk.NW)
			secondCard = self.canvas.create_image(183, 100, image=self.deckImages[cards[1]], anchor=tk.NW)
			thirdCard = self.canvas.create_image(609, 100, image=self.deckImages[cards[2]], anchor=tk.NE)
			fourthCard = self.canvas.create_image(457, 100, image=self.deckImages[cards[3]], anchor=tk.NE)
			self.canvas.tag_bind(firstCard, '<ButtonPress-1>', (lambda event: self.sendCard(cards[0])))
			self.canvas.tag_bind(secondCard, '<ButtonPress-1>', (lambda event: self.sendCard(cards[1])))
			self.canvas.tag_bind(thirdCard, '<ButtonPress-1>', (lambda event: self.sendCard(cards[2])))
			self.canvas.tag_bind(fourthCard, '<ButtonPress-1>', (lambda event: self.sendCard(cards[3])))
			
	def sendCard(self, card):
		self.networkHandler.chooseCard(card)
		self.clearCanvas()
		currentBackground = self.canvas.create_image(0, 0, image=self.waitingCardBackground, anchor=tk.NW)
	def putDown(self):
		r.acquire()
		self.alreadyPutDown = True
		self.networkHandler.putDown()
		self.clearCanvas()
		currentBackground = self.canvas.create_image(0, 0, image=self.waitingCardBackground, anchor=tk.NW)
		r.release()
	def clearCanvas(self):
		self.canvas.delete("all")
	def run(self):
		while True:
			data = self.networkHandler.sckt.recv(self.buffer_size)
			message = str(data.decode('utf8'))
			if message[:2] == NetworkCommand.SERVER_SEND_CARDS:
				r.acquire()
				if(not self.alreadyPutDown):
					card_string = message[2:]
					current_cards = card_string.split(' ')
					self.startRound(cards=current_cards)
				r.release()
			elif message[:2] == NetworkCommand.SERVER_WINNER_DECLARED:
				self.startRound(forcePlacedown=True)
				break
		while True:
			data = self.networkHandler.sckt.recv(self.buffer_size)
			message = str(data.decode('utf8'))
			if message[:2] == NetworkCommand.SERVER_RANKINGS_WIN:
				self.clearCanvas()
				currentBackground = self.canvas.create_image(0, 0, image=self.winBackground, anchor=tk.NW)
				break
			elif message[:2] == NetworkCommand.SERVER_RANKINGS_LOSE:
				self.clearCanvas()
				currentBackground = self.canvas.create_image(0, 0, image=self.loseBackground, anchor=tk.NW)
				break
			elif message[:2] == NetworkCommand.SERVER_RANKINGS_PLACE:
				self.clearCanvas()
				currentBackground = self.canvas.create_image(0, 0, image=self.notloseBackground, anchor=tk.NW)
				break
x = CompleteGamePanel()
import sys

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

import client_gui_support

import os
from tkinter import messagebox
from tkinter import * 
from tkinter.ttk import *
from game137lib import *

choice = 0
card_index = 0
put_down = 0
winner_declared = 0

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = tk.Tk()
    top = Menu_Panel (root)
    client_gui_support.init(root, top)
    root.mainloop()

def vp_start_game_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root.destroy()
    root = tk.Tk()
    top = Game_Panel (root)
    client_gui_support.init(root, top)
    root.mainloop()

def vp_start_lobby_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root.destroy()
    root = tk.Tk()
    top = Lobby (root)
    client_gui_support.init(root, top)
    root.mainloop()

w = None
def create_Game_Panel(root, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    rt = root
    w = tk.Toplevel (root)
    top = Game_Panel (w)
    client_gui_support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_Game_Panel():
    global w
    w.destroy()
    w = None

class Game_Panel:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'

        top.geometry("803x582+550+136")
        top.minsize(1, 1)
        top.maxsize(1905, 1050)
        top.resizable(1, 1)
        top.title("1-2-3 PASS ")
        top.configure(background="#0d4f0a")
        top.configure(highlightcolor="black")

        global winner_declared

        self.pass_button = tk.Button(top)
        self.pass_button.place(relx=0.223, rely=0.842, height=31, width=131)
        self.pass_button.configure(activeforeground="white")
        self.pass_button.configure(activeforeground="#916626")
        self.pass_button.configure(background="#6b4b1c")
        self.pass_button.configure(text='''PASS''')

        self.put_down_button = tk.Button(top)
        self.put_down_button.place(relx=0.623, rely=0.842, height=31, width=131)
        self.put_down_button.configure(activeforeground="white")
        self.put_down_button.configure(activeforeground="#916626")
        self.put_down_button.configure(background="#6b4b1c")
        self.put_down_button.configure(text='''PUT DOWN''')
        self.put_down_button.configure(state="disabled", command=self.putDown)

        winConditionValue = Client.cards[0][:-1]
        if (len([w for w in Client.cards if w[:-1] == winConditionValue]) == len(Client.cards) or winner_declared == 1):
            self.put_down_button.configure(state="normal")

        self.card_1 = tk.Button(top)
        self.card_1.place(relx=0.112, rely=0.378, height=191, width=121)
        self.card_1.configure(activebackground="#00f4f4")
        file_1 = str(Client.cards[0])
        self._img1 = tk.PhotoImage(file="./deck/"+file_1+".png")
        self.card_1.configure(image=self._img1)
        self.card_1.configure(pady="0", command=self.chooseCard1)

        self.card_2 = tk.Button(top)
        self.card_2.place(relx=0.548, rely=0.378, height=191, width=121)
        self.card_2.configure(activebackground="#00f4f4")
        file_2 = str(Client.cards[1])
        self._img2 = tk.PhotoImage(file="./deck/"+file_2+".png")
        self.card_2.configure(image=self._img2)
        self.card_2.configure(pady="0", command=self.chooseCard2)

        self.card_3 = tk.Button(top)
        self.card_3.place(relx=0.324, rely=0.378, height=191, width=121)
        self.card_3.configure(activebackground="#00f4f4")
        file_3 = str(Client.cards[2])
        self._img3 = tk.PhotoImage(file="./deck/"+file_3+".png")
        self.card_3.configure(image=self._img3)
        self.card_3.configure(pady="0", command=self.chooseCard3)

        self.card_4 = tk.Button(top)
        self.card_4.place(relx=0.76, rely=0.378, height=191, width=121)
        self.card_4.configure(activebackground="#00f4f4")
        file_4 = str(Client.cards[3])
        self._img4 = tk.PhotoImage(file="./deck/"+file_4+".png")
        self.card_4.configure(image=self._img4)
        self.card_4.configure(pady="0", command=self.chooseCard4)

        self.player_name = tk.Label(top)
        self.player_name.place(relx=0.112, rely=0.069, height=71, width=409)
        self.player_name.configure(activebackground="#f9f9f9")
        self.player_name.configure(anchor='w')
        self.player_name.configure(background="#0d4f0a")
        self.player_name.configure(font="-family {Kalimati} -size 15")
        self.player_name.configure(justify='left')
        self.player_name.configure(foreground="#ffffff")
        string = "PLAYER: " + Client.player_name
        self.player_name.configure(text=string)
        
        if winner_declared == 1:
            messagebox.showwarning("Someone has already won! Hurry and put down your cards!")
            self.put_down_button.configure(state="normal")

        self.quit_button = tk.Button(top)
        self.quit_button.place(relx=0.834, rely=0.086, height=31, width=60)
        self.quit_button.configure(activebackground="#f9f9f9")
        self.quit_button.configure(background="#aa0000")
        self.quit_button.configure(text='''QUIT''', command=self.quit_game)

    def quit_game(self):
        global root
        root.destroy()
        vp_start_gui()

    def putDown(self):
        global root
        global put_down
        put_down = 1
        root.quit()

    def chooseCard1(self):
        global root
        global card_index
        card_index = 0
        root.quit()

    def chooseCard2(self):
        global root
        global card_index
        card_index = 1
        root.quit()

    def chooseCard3(self):
        global root
        global card_index
        card_index = 2
        root.quit()

    def chooseCard4(self):
        global root
        global card_index
        card_index = 3
        root.quit()

class Menu_Panel:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'

        top.geometry("803x582+550+136")
        top.minsize(1, 1)
        top.maxsize(1905, 1050)
        top.resizable(1, 1)
        top.title("1-2-3 PASS ")
        top.configure(background="#0d4f0a")
        top.configure(highlightcolor="black")

        self.Frame1 = tk.Frame(top)
        self.Frame1.place(relx=0.0, rely=0.0, relheight=1.022, relwidth=1.002)
        self.Frame1.configure(relief='groove')
        self.Frame1.configure(borderwidth="2")
        self.Frame1.configure(relief="groove")
        self.Frame1.configure(background="#000000")

        self.Label1 = tk.Label(self.Frame1)
        self.Label1.place(relx=0.211, rely=0.067, height=81, width=489)
        self.Label1.configure(activebackground="#f9f9f9")
        self.Label1.configure(background="#000000")
        self.Label1.configure(font="-family {Karumbi} -size 72")
        self.Label1.configure(foreground="#ffffff")
        self.Label1.configure(text='''1-2-3 Pass''')

        self.ip_textfield = tk.Text(self.Frame1)
        self.ip_textfield.place(relx=0.472, rely=0.319, relheight=0.057
                , relwidth=0.306)
        self.ip_textfield.configure(background="white")
        self.ip_textfield.configure(font="TkTextFont")
        self.ip_textfield.configure(selectbackground="#c4c4c4")
        self.ip_textfield.configure(wrap="word")

        self.port_textfield = tk.Text(self.Frame1)
        self.port_textfield.place(relx=0.472, rely=0.42, relheight=0.057
                , relwidth=0.306)
        self.port_textfield.configure(background="white")
        self.port_textfield.configure(font="TkTextFont")
        self.port_textfield.configure(selectbackground="#c4c4c4")
        self.port_textfield.configure(wrap="word")

        self.player_textfield = tk.Text(self.Frame1)
        self.player_textfield.place(relx=0.472, rely=0.521, relheight=0.057
                , relwidth=0.306)
        self.player_textfield.configure(background="white")
        self.player_textfield.configure(font="TkTextFont")
        self.player_textfield.configure(selectbackground="#c4c4c4")
        self.player_textfield.configure(wrap="word")

        self.ip_label = tk.Label(self.Frame1)
        self.ip_label.place(relx=0.273, rely=0.319, height=31, width=149)
        self.ip_label.configure(activebackground="#f9f9f9")
        self.ip_label.configure(background="#000000")
        self.ip_label.configure(foreground="#ffffff")
        self.ip_label.configure(text='''Server's IP Address:''')

        self.port_label = tk.Label(self.Frame1)
        self.port_label.place(relx=0.261, rely=0.42, height=31, width=149)
        self.port_label.configure(activebackground="#f9f9f9")
        self.port_label.configure(anchor='e')
        self.port_label.configure(background="#000000")
        self.port_label.configure(foreground="#ffffff")
        self.port_label.configure(text='''Server's Port:''')

        self.player_label = tk.Label(self.Frame1)
        self.player_label.place(relx=0.261, rely=0.521, height=31, width=149)
        self.player_label.configure(activebackground="#f9f9f9")
        self.player_label.configure(anchor='e')
        self.player_label.configure(background="#000000")
        self.player_label.configure(foreground="#ffffff")
        self.player_label.configure(text='''Player's Name:''')

        self.start_button = tk.Button(self.Frame1)
        self.start_button.place(relx=0.398, rely=0.672, height=31, width=171)
        self.start_button.configure(activebackground="#f9f9f9")
        self.start_button.configure(text='''START GAME''', command=self.start_game)

        self.quit_button_menu = tk.Button(self.Frame1)
        self.quit_button_menu.place(relx=0.398, rely=0.756, height=31, width=171)

        self.quit_button_menu.configure(activebackground="#f9f9f9")
        self.quit_button_menu.configure(text='''QUIT GAME''', command=root.destroy)

    def start_game(self):
        ip = self.ip_textfield.get("1.0", "end-1c")
        port = self.port_textfield.get("1.0", "end-1c")
        player_name = self.player_textfield.get("1.0", "end-1c")
        c = Client()
        c.start(ip, port, player_name)

class Lobby:
	def __init__(self, top=None):
		_bgcolor = '#d9d9d9'  # X11 color: 'gray85'
		_fgcolor = '#000000'  # X11 color: 'black'
		_compcolor = '#d9d9d9' # X11 color: 'gray85'
		_ana1color = '#d9d9d9' # X11 color: 'gray85' 
		_ana2color = '#d9d9d9' # X11 color: 'gray85' 

		top.geometry("600x450+411+139")
		top.title("Lobby")
		top.configure(background="#000000")

		self.Text1 = tk.Text(top)
		self.Text1.place(relx=0.567, rely=0.089, relheight=0.809, relwidth=0.373)

		self.Text1.configure(background="#000000")
		self.Text1.configure(borderwidth="0")
		self.Text1.configure(font="TkTextFont")
		self.Text1.configure(foreground="#ffffff")
		self.Text1.configure(highlightbackground="#d9d9d9")
		self.Text1.configure(highlightcolor="black")
		self.Text1.configure(insertbackground="black")
		self.Text1.configure(selectbackground="#c4c4c4")
		self.Text1.configure(selectforeground="black")
		self.Text1.configure(width=224)
		self.Text1.configure(wrap='word')
		self.Text1.configure(state="disabled")

		self.vote_1_button = tk.Button(top)
		self.vote_1_button.place(relx=0.183, rely=0.2, height=44, width=122)
		self.vote_1_button.configure(activebackground="#d9d9d9")
		self.vote_1_button.configure(activeforeground="#000000")
		self.vote_1_button.configure(background="#000000")
		self.vote_1_button.configure(disabledforeground="#a3a3a3")
		self.vote_1_button.configure(foreground="#ffffff")
		self.vote_1_button.configure(highlightbackground="#d9d9d9")
		self.vote_1_button.configure(highlightcolor="black")
		self.vote_1_button.configure(pady="0")
		self.vote_1_button.configure(text='''Vote Start''')
		self.vote_1_button.configure(width=122, command=self.start_vote)

		self.leave_button = tk.Button(top)
		self.leave_button.place(relx=0.183, rely=0.4, height=44, width=123)
		self.leave_button.configure(activebackground="#d9d9d9")
		self.leave_button.configure(activeforeground="#000000")
		self.leave_button.configure(background="#000000")
		self.leave_button.configure(disabledforeground="#a3a3a3")
		self.leave_button.configure(foreground="#ffffff")
		self.leave_button.configure(highlightbackground="#d9d9d9")
		self.leave_button.configure(highlightcolor="black")
		self.leave_button.configure(pady="0")
		self.leave_button.configure(text='''Leave Lobby''')
		self.leave_button.configure(width=127, command=self.leave_lobby)

		self.instructions_button = tk.Button(top)
		self.instructions_button.place(relx=0.183, rely=0.578, height=44, width=123)
		self.instructions_button.configure(activebackground="#d9d9d9")
		self.instructions_button.configure(activeforeground="#000000")
		self.instructions_button.configure(background="#000000")
		self.instructions_button.configure(disabledforeground="#a3a3a3")
		self.instructions_button.configure(foreground="#ffffff")
		self.instructions_button.configure(highlightbackground="#d9d9d9")
		self.instructions_button.configure(highlightcolor="black")
		self.instructions_button.configure(pady="0")
		self.instructions_button.configure(text='''Instructions''')
		self.instructions_button.configure(width=123, command=self.show_instructions)

	def start_vote(self):
		global choice
		global root
		choice = 1
		root.quit()
	def leave_lobby(self):
		global choice
		global root
		choice = 2
		root.destroy()
		vp_start_gui()
	def show_instructions(self):
		self.Text1.configure(state="normal")
		text = '===== How to play =====\nAll players must first vote to start\nYou will be dealt four cards labeled from 1-4\nThe goal is to complete four cards of the same number or face\nSelect which card you will want to discard from your hand by typing a number from 1-4\nYou will recieve a discarded card from the player on your left\nOnce a player completes their hand, they enter 1 to place your hand down.\nThe remaining players race to put their hand down\nThe last player to put down their hand loses\n'
		self.Text1.insert(tk.INSERT, text)
		self.Text1.configure(state="disabled")

class Client(object):
    def __init__(self):
        #================================== INITIALIZE CLIENT ==================================#
        # self.ip = '127.0.0.34'
        # self.port = 5005
        self.buffer_size = 1024
    def start(self, ip, port, name):
        #================================== ENTER DETAILS ==================================#
        # self.ip = str(input("Specify Host IP Address: "))
        # self.port = int(input("Specify Port: "))
        # self.player_name = input('Enter your player name: ')
        global choice
        self.ip = str(ip)
        self.port = int(port)
        self.player_name = name
        Client.player_name = self.player_name

        #================================== CONNECT TO SERVER ==================================#
        self.sckt = ClientNetworkHandler(self.ip, self.port, self.player_name)
        Client.sckt = self.sckt
        Client.buffer_size = self.buffer_size 
        self.sckt.joinServer()
        data = self.sckt.sckt.recv(self.buffer_size)
        message = str(data.decode('utf8'))

        #================================== IF ACCEPTED ==================================#
        if message[:2] == NetworkCommand.SERVER_ACCEPT_PLAYER:
            while True:
                vp_start_lobby_gui()
                #================================== ON VOTE ==================================#
                if choice == 1:
                    print('Waiting for other players to start...')
                    self.sckt.voteStart()
                    data = self.sckt.sckt.recv(self.buffer_size)
                    message = str(data.decode('utf8'))
                    Client.message = message
                    #================================== GAME LOOP ==================================#
                    if message[:2] == NetworkCommand.SERVER_START_GAME:
                        print('Game has commenced...')

                        while True:
                            global put_down
                            global card_index
                            data = self.sckt.sckt.recv(self.buffer_size)
                            message = str(data.decode('utf8'))
                            if message[:2] == NetworkCommand.SERVER_SEND_CARDS:
                                card_string = message[2:]
                                current_cards = card_string.split(' ')
                                Client.cards = current_cards

                                vp_start_game_gui()

                                if put_down == 1 :
                                    self.sckt.putDown()
                                    break

                                self.sckt.chooseCard(current_cards[card_index])
                    #================================== SOMEONE ELSE WON ==================================#
                    elif message[:2] == NetworkCommand.SERVER_WINNER_DECLARED:
                        global winner_declared
                        winner_declared = 1
                        vp_start_game_gui()
                        while True:
                            if put_down == 1 :
                                self.sckt.putDown()
                                break
                    else:
                        break
                #================================== ON LEAVE ==================================#
                elif choice == 2:
                    print('Leaving Lobby...')
                    self.sckt.leaveLobby()
                    vp_start_gui()
                    break
        #================================== IF NOT ACCEPTED ==================================#
        else:
            print('Server is full.')
        print('Closing Game...')
        self.sckt.close()

if __name__ == '__main__':
    vp_start_gui()






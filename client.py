import socket
# TCP_IP = str(input("Specify Host IP Address: "))
# TCP_PORT = int(input("Specify Port: "))
TCP_IP = "127.0.0.3"
TCP_PORT = 5005
BUFFER_SIZE = 1024
#=============JOIN=================
name = input("Enter player name: ")
MESSAGE = "JG:"+name

#==================================
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE.encode('utf8'))
data = s.recv(BUFFER_SIZE)
msg = str(data.decode('utf8'))
if (msg == "AC"):
	while True:
		print("Waiting for other players")
		print("[1] Vote Start")
		print("[2] Leave Room")
		x = input()
s.close()
print ("received data:", data)


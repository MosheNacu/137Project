import socket
# TCP_IP = str(input("Specify Host IP Address: "))
# TCP_PORT = int(input("Specify Port: "))

TCP_IP = "127.0.0.5"
TCP_PORT = 5005
BUFFER_SIZE = 1024
#=============JOIN=================
name = input("Say hi: ")

#==================================
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
while True:
	x = input("Say hi: ")
	s.send(x.encode('utf8'))
	data = s.recv(BUFFER_SIZE)
	msg = str(data.decode('utf8'))
	print(msg)

s.close()
print ("received data:", data)
import socket
TCP_IP = str(input("Specify Host IP Address: "))
TCP_PORT = int(input("Specify Port: "))
BUFFER_SIZE = 1024
MESSAGE = b"Hello, World!"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.sendall(MESSAGE)
data = s.recv(BUFFER_SIZE)
s.close()
print ("received data:", data)
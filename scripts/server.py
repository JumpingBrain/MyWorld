import socket
from _thread import *
import sys

server = "192.168.1.144"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	s.bind((server, port))
except socket.error as e:
	str(e)


s.listen(2)
print("Waiting for connection, Server Started")



def threaded_client(conn):
	conn.send(str.encode("--connected to chat---"))
	reply = ""
	while 1:
		try:
			data = conn.recv(2048)
			reply = data.decode("utf-8")

			if not data:
				print("Disconnected")
				break
			else:
				print("-Recieved-", reply)
				user_message = str(input(': '))
				#print("Sending : ", user_message)

			conn.sendall(str.encode(user_message))
		except Exception as e:
			print(e)
			break

	print("Lost connection")
	conn.close()


made = 0
while 1:
	conn, addr = s.accept()
	print("Connected to:", addr)

	if not made: 
		start_new_thread(threaded_client, (conn,))
		#made += 1
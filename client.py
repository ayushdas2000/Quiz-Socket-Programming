import socket
import select
import sys
import thread


#create a socket object using socket.socket()
#The arguments passed to socket() specify the address family and socket type
#AF_INET is the INternet address family for IPv4.
#specify the socket type as socket.SOCK_STREAM
#When we do this,the default protocol that is used is TCP.

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


#taking input from client about host
IP_address= raw_input("Enter IP adresss: ")
##port should be same as server
Port = input("Enter Port: ")


##to connect to the host
server.connect((IP_address, int(Port)))


while(1):
	slist = [sys.stdin, server]
	read_socket,write_socket, error_socket = select.select(slist,[],[])
	for i in read_socket:
		if(i!=server):
			message = sys.stdin.readline()
			server.send(message)
			sys.stdout.flush()
		else:
			message = i.recv(2048)
			print message


server.close()
sys.exit()

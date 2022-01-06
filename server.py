###################SERVER FILE################



#we are importing list of question and list of answers from another file data.py
from Data import list_of_questions
from Data import list_of_answers


import sys
import time
import select
import random
import thread
import socket 





#######     DECLARING GLOBAL VARIABLES  ############


#create empty list. WE will store all our clients in this list.
list_of_players=[]

#buzzer list will keep track of which player hs pressed the buzzer
buzzer=[0,0,0]

#score will track of players score. If it is 5 game terminates.
score=[]

#player is the list to keep temporary information of the player.
player=["adrs",-1]






#######SOCKETS AND CONNECTIONS ##############

#create a socket object using socket.socket()
#The arguments passed to socket() specify the address family and socket type
#AF_INET is the INternet address family for IPv4.
#specify the socket type as socket.SOCK_STREAM
#When we do this,the default protocol that is used is TCP.
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


#setsockopt() manipulates options for the socket referred to by the file descriptor sockfd.
#SOL_SOCKET is Used  as the level argument to setsockopt to manipulate the socket-level options
#SO_REUSEADDR:This option controls whether bind should permit reuse of local addresses for this socket.
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#Taking ip address and port no as input.
#If we would  pass 127.0.0.1 as ip address it would listen to only those calls made within the local computer.
IP_address= raw_input("Enter IP adresss: ")
Port = input("Enter Port: ")

#binding the server to the specified port using socket.bind
server.bind((IP_address, int(Port)))


#10 here means that 10 connections are kept waiting if the server is busy and if a 6th socket trys to connect then the connection is refused.
server.listen(10)



#####Functions for quiz####3333

##this function sends msg to all the players
def send_msg_to_all_players(msg):
	for players in list_of_players:
		try:
			players.send(msg)
		except:
			players.close()
			remove(players)
##this function randomly selects a question and sends to the players
def start_quiz():
	buzzer[2] = random.randint(0,10000)%len(list_of_questions)
	if(len(list_of_questions)!=0):
		for connection in list_of_players:
			connection.send(list_of_questions[buzzer[2]])


def end_quiz():
	send_msg_to_all_players("Quiz Over\n")
	buzzer[1]=1
	j = score.index(max(score))
	##we have to check if all questions are over or not. In that case its a TIE.
	if(len(list_of_questions)!=0):
		
		for i in range(len(list_of_players)):
			list_of_players[i].send("Your Score: "+str(score[i]))

	
	sys.exit()


def remove(connection):
    if connection in list_of_players:
        list_of_players.remove(connection)

def player_thread(conn,address):
	conn.send("Welcome!!\nThe game starts when all players join.\nInstruction:\nPress any key as buzzer(prefreably Enter\nEnter the correct option\nFor example: If you think correct option is a then just enter a")


	while(1):
		message = conn.recv(2048)


		##we need to check if all three players have joined or not before starting the game.
		if(len(list_of_players)!=3):
			send_msg_to_all_players("Please wait for game to start")
			break

		##if we recieve a message from a player
		if message:
			if buzzer[0] == 0:
				player[0] = conn    #we use this buzzer list to identify which player has pressed the buzzer first
				buzzer[0] = 1       #when a player presses buzzer we change from 0 to 1
				i = 0 
				while i<len(list_of_players):
					if list_of_players[i] == player[0]:
						break
					i += 1
				player[1] = i
			

			##to check if msg is recieved from the player who pressed buzzer first.
			elif(buzzer[0]==1 and conn==player[0]):
				
				if(message[0] == list_of_answers[buzzer[2]][0]): 
					##player has answered correctly        
					send_msg_to_all_players("Player " + str(player[1]+1) + " +1" + "\n\n")
					print("Correct ans: "+str(list_of_answers[buzzer[2]][0]))
					print("Given ans by Player "+str(player[1]+1)+": " + str(message[0]))
					print("Player " + str(player[1]+1) + " +1" + "\n\n")
					score[i] += 1

					##to end the game whenever player reaches 5 points
					if score[i] >= 5:
						send_msg_to_all_players("Player " + str(player[1]+1) + " WON" + "\n")
						print("Player " + str(player[1]+1) + " WON" + "\n")
						end_quiz()
						sys.exit()
				else:
					send_msg_to_all_players("Player " + str(player[1]+1) + " -0.5" + "\n\n")
					print("Correct ans: "+str(list_of_answers[buzzer[2]][0]))
					print("Given ans by Player"+str(player[1]+1)+": " + str(message[0]))
					print("Player " + str(player[1]+1) + " -0.5" + "\n\n")
					score[i] -= 0.5
				buzzer[0]=0
				if(len(list_of_questions)!=0):
					list_of_questions.pop(buzzer[2])
					list_of_answers.pop(buzzer[2])

				##this condition is for when all questions are used and no more questions are available.
				if(len(list_of_questions)==0):
					send_msg_to_all_players("Its Tie as there are no questions left\n")
					end_quiz()
					sys.exit()
				start_quiz()
			else:
				conn.send(" Player " + str(player[1]+1) + " pressed Buzzer First\n\n")
		else:
			remove(conn)


while(1):

	##accepting connection from players/clients
	connection,address = server.accept()


	##storing each players info in list_of_players
	list_of_players.append(connection)


	score.append(0)
	print("Player "+ str(len(list_of_players))+ " has joined")
	thread.start_new_thread(player_thread,(connection,address))
	time.sleep(1)
	if(len(list_of_players)==3):
		start_quiz()
connection.close()
server.close()
sys.exit()






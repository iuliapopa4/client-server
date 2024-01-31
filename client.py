import socket
import sys


#Here we store the command line arguments of the client
HOST = str(sys.argv[2]) 
PORT = int(sys.argv[1])


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
    #Here we try connecting to the server, on the IP and PORT. If any exception is caught, the client will terminate
    try:
        s.connect((HOST, PORT))
    except:
        print("Cannot connect to server")
        exit()

    
    #Here is the loop of the client
    while True:    
        try:
            data = s.recv(1024)

            #Here we print the messages received from the server, with the exception of SKIP, which is a special word
            if (data.decode() != "SKIP"):
                print("Message received: " + data.decode())

            #Here we check if the server can accept the current connection 
            if (data.decode() == "NOT_ALLOWED"):
                print("Killing client because MAX LIMIT has been reached")
                exit()
            
            #Here we get some input from the user and encode it, and convert it into bytes, so that it's easier to send
            message = bytes(input("->").encode())

            #If we send "!kill", it will kill the server, and calling client
            if message == b"!kill":
                print("Killing server from client.")
                s.sendall(message)
                exit()
            #If we send "!close", it will kill the calling client
            elif message == b"!close":
                print("Killing client.")
                s.sendall(message)
                exit()
            #If we send "!showConnection", the server will send back all the active connections on the server 
            elif message == b"!showConnections":
                s.sendall(message)
                ok = True
                while ok:
                    connections = s.recv(1024)
                    if connections.decode() == "DONE":
                        ok = False
                        break
                    print(connections.decode())
            #If we send an ordinary message, it will send it as it is
            else:
                s.sendall(message)        

        #In case of any exception, it will send the "!close" command to the server, to kill the current connection before killing the client
        except:
            s.sendall(b"!close")
            exit()
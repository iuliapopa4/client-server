import socket
import os
import _thread
import sys
import time




HOST = ""
#Here we store the command line arguments of the server
PORT = int(sys.argv[1])
server = socket.socket()
UserNum = 0
ok = True

greetings = {"Hello", "Hi", "Buna", "Salut"}
clients = dict()

#Handle clients that try connection after the limit has been reached
def clientMAX(connection: socket.socket, address):
    connection.send(str.encode("NOT_ALLOWED"))


#Handle clients that successfully connected to the server
def clientConnect(connection: socket.socket, address: socket.AddressFamily):
    connection.send(str.encode("Client connected: (" + address[0] + " --- " + str(address[1]) + ")"))
    
    #In UserNo we store the current number of the user as to help us show which user typed what.
    global UserNum
    UserNo = UserNum
    while True:
        greetBool = False
        data = connection.recv(1024)

        response = data.decode()

        #Here we check if we get a special message as to send a special message
        if response in greetings:
            connection.sendall("Hello there! I'm your server for today.".encode())
            greetBool = True
            continue

        #In the case no data is sent, close this client connection.
        if not data:
            break

        #In this case, the client will kill the server.
        if response == "!kill":
            print("Killing server...")
            os.system(f"fuser -k {PORT}/tcp")
            global ok
            ok = False
            break

        #In this case, the client will disconnect from the server.
        elif response == "!close":
            UserNum -= 1
            print("User disconnected: (" + str(address[0]) + " --- " + str(address[1]) + ")")
            clients.pop(UserNo)                
            return
        
        #In this case, the client will receive all the active connections on the server.
        elif response == "!showConnections":
            for i,j in clients.items():
                connection.sendall(f"{i} --- {j[1]}".encode())
                time.sleep(0.3)

            #Here we send the DONE message to let the client know that the data has been sent
            time.sleep(0.4)
            connection.sendall("DONE".encode())

            #Here we send another message, SKIP, to prevent the client and server being in a deadlock
            time.sleep(0.4)
            connection.sendall("SKIP".encode())

        elif greetBool == False:
            connection.sendall(response.encode())

        print("User" + str(UserNo) + ": " + data.decode())

    connection.close()



if __name__ == "__main__":
    #Error checking to see if we can create the server to the specific port
    try:
        server.bind((HOST, PORT))
    except socket.error as e:
        print(str(e))
        exit()

    #Printing info messages and starting the server listening
    print("Server is listening...")
    #We print the host ip
    print(socket.gethostbyname(HOST))
    server.listen(10)


    #Handling initialization of threads with new sockets
    while ok:
        Client, Address = server.accept()
        UserNum += 1

        clients[UserNum] = (Client, Address)

        #We can have atmost 2 users as of now
        if (UserNum < 3):
            print("User connected: (" + Address[0] + " --- " + str(Address[1]) + ")")
            _thread.start_new_thread(clientConnect, (Client, Address))
        else:
            print("User(" + Address[0] + " --- " + str(Address[1]) + ")" + " tried connecting, but MAX LIMIT has been reached.")
            _thread.start_new_thread(clientMAX, (Client, Address))
        

    server.close()
# client-server
Usage:
Run the server.py script on a machine. Provide the desired port as a command-line argument (e.g., python server.py 8080).
Run one or more instances of the client.py script on other machines. Provide the server's address and port as command-line arguments (e.g., python client.py 8080 127.0.0.1).

The communication includes special commands like !kill to terminate the server, !close to disconnect a client, and !showConnections to retrieve a list of active connections.
The project utilizes multi-threading to handle multiple client connections simultaneously.

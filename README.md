Scott Gersten
YL91135
sgerste1@umbc.edu

Basic TCP Chat Room

server.py and client.py work together to create a TCP chat room in support of multiple clients. Chats can be made to and from the server, and to and from all clients that are connected. Each client has a unique nickname that they choose. The server is simply called: SERVER

server.py:

To create a chatroom open a PowerShell terminal and navigate to the directory where server.py is located. Run "python server.py" to open the server. 

The instantiation of the server class runs on the local host, with a buffer size of 1024 bytes, the server's name as "SERVER", the termination message as "/kill" and the logfile called "chat_log.log". If the user wishes to change any of these default values, they must change the creation of the server object in main. It should be noted that should a user change the host, the buffer size, or the termination message, these values should also be changed in the client class' instantiation to ensure the program works as intended.

The user will be prompted with entering a TCP port number between 1025 and 65535, inclusive. Then the server will go into listen mode and wait for client connections. Even with no client connections, the server can still send messages by entering the desired message in the buffer and pressing enter. As clients connect, the server will see these connections as well as the alias of the client. They can receive messages from all the connected clients and the messages the server sends will be broadcast to all connected clients. The user can close the server by entering "/kill" as their message. It should be noted that the server will not be allowed to close until all clients are disconnected.

client.py:

To connect clients, open a new PowerShell terminal for every client that you want to connect. Navigate to the directory with client.py and enter "python client.py" to open a client. 

The instantiation of the client class runs on the local host, with a buffer size of 1024 bytes, and the termination message as "/kill". If the user wishes to change any of these default values, they must change the creation of the client object in main. It should be noted that should a user change the host, the buffer size, or the termination message, these values should also be changed in the server class' instantiation to ensure the program works as intended.

The user will be prompted with entering a TCP port number between 1025 and 65535 inclusive. Then the user will be prompted with entering a nickname/alias to be used within the chatroom. This alias can be anything except only whitespace. If the TCP port chosen has no server present on it, the client will then shutdown. If the nickname chosen is either "SERVER" or a nickname already chosen by another client on the server, the client will shutdown. If the TCP port is valid and the nickname is accepted, the client is now connected to the server. The user can now send and receive messages on every client that is connected. The user can close the client by entering "/kill". It should be noted that all clients have to disconnect with this command before the server will be allowed to gracefully shutdown. 

Bonus Features:

This chatroom supports multiple clients being connected to the server. It does this by using threading for each client connected and by keeping a list of all clients and their nicknames currently connected. Messages sent between clients and from the server are broadcast to all clients on the server.

This chatroom gives unique chat ID's to each client that is connected. The chat ID is chosen by the user of the client and the only contraints are that is is not whitespace, not the same name as the server ID, and not the same nickname of another client already on the server. These chat ID's are shown before the message that each client sends. 

This chatroom gives timestamps to every message that is broadcast from the server. Python's datetime library was used to get the current date and time when the message was sent. The timestamp is shown before the sender's ID in the message.

This chatroom creates a .log file on the server side by saving all messages broadcasted from the server to a .log file. These messages include the timestamps and alias' of the clients that sent them. Every time that server is opened, it clears the .log file specified in the server's creation.
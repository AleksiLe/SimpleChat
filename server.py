import threading
import socket
from user import USER

host = '127.0.0.1'
port = 59000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP connection
server.bind((host, port))
server.listen()
clients = []
users = []
channels = {}

# Function to find user by client
def findUserByClient(client):
    for user in users:
        if user.client == client:
            return user
    return None

# Function to find user by alias //not good practice but for recourse purposes ill go with it
def findUserByAlias(alias):
    for user in users:
        if user.alias == alias:
            return user
    return None

# Functions to handle broadcasting of messages for different purposes

def broadcast(message, senderClient):
    try:
        user = findUserByClient(senderClient)
        if user.channel:
            channel = user.channel
            for clients in channels[channel]:
                clients.send(f'[{channel}]{user.alias}: {message}'.encode('utf-8'))
        else:
            senderClient.send('You are not in any channel'.encode('utf-8'))
    except:
        senderClient.send('Error sending your message'.encode('utf-8'))

def serverBroadcast(message):
    for client in clients:
        client.send(message.encode('utf-8'))
    return None

def privateBroadcast(message, senderClient, receiver):
    sendingUser = findUserByClient(senderClient)
    receivingUser = findUserByAlias(receiver)
    if not receivingUser:
        senderClient.send(f'{receiver} is not in the chat room'.encode('utf-8'))
        return None
    else:
        receivingUser.client.send(f'pm from {sendingUser.alias}: {message}'.encode('utf-8'))
        senderClient.send(f'pm to {receiver}: {message}'.encode('utf-8'))


# Functions to handle channels
        
def joinChannel(channel, client):
    try:
        user = findUserByClient(client)
        if user.channel:
            leaveChannel(user.channel, client)

        if channel not in channels:
            channels[channel] = []
        channels[channel].append(client)

        user.changeChannel(channel)
        broadcast(f'{user.alias} has joined {channel}', client)
        return None
    except:
        client.send(f'Error joining {channel}'.encode('utf-8'))

def leaveChannel(channel, client):
    try:
        user = findUserByClient(client)
        if channel in channels and client in channels[channel]:
            channels[channel].remove(client)
        broadcast(f'{user.alias} has left {channel}', client)
        return None
    except:
        client.send(f'Error leaving {channel}'.encode('utf-8'))

# Function to handle clients'connections


def handleClient(client):
    while True:
        try:
            message = client.recv(1024)
            message = message.decode('utf-8')
            if message.startswith('/pm '):
                receiver, message = message.split(' ', 2)[1:3]
                privateBroadcast(message, client, receiver)
            elif message.startswith('/join '):
                channel = message.split(' ', 1)[1]
                joinChannel(channel, client)
            elif message.startswith('/leave'):
                channel = message.split(' ', 1)[1]
                leaveChannel(channel, client)
            else:
                broadcast(message, client)
        except:
            user = findUserByClient(client)
            serverBroadcast(f'{user.alias} has left the chat room!') #optional
            users.remove(user)
            clients.remove(client)
            client.close()
            break
# Main function to receive the clients connection


def receive():
    while True:
        print('Server is running and listening ...')
        client, address = server.accept()
        print(f'connection is established with {str(address)}')
        client.send('alias?'.encode('utf-8'))
        alias = client.recv(1024).decode('utf-8')
        clients.append(client)
        new_user = USER(client, alias)
        users.append(new_user)
        print(f'The alias of this client is {alias}'.encode('utf-8'))
        serverBroadcast(f'{alias} has connected to the chat room') #optional
        client.send('you are now connected!'.encode('utf-8'))
        thread = threading.Thread(target=handleClient, args=(client,))
        thread.start()


if __name__ == "__main__":
    receive()
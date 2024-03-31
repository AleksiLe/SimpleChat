import threading
import socket
print('Welcome to the chat room!')
print('Commands:')
print('/join [channel] - join/switch a channel')
print('/leave [channel] - leave a channel')
print('/pm [alias] [message] - send a private message to an alias')
alias = input('Choose an alias >>> ')
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 59000))


def clientReceive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "alias?":
                client.send(alias.encode('utf-8'))
            else:
                print(message)
        except:
            print('Connection error!')
            client.close()
            break


def clientSend():
    while True:
        message = input("")
        client.send(message.encode('utf-8'))


receive_thread = threading.Thread(target=clientReceive)
receive_thread.start()

send_thread = threading.Thread(target=clientSend)
send_thread.start()
import socket
import threading
import pickle

HOST = socket.gethostname()
PORT = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((HOST, PORT))
server.listen(5)

clients = []
nicknames = []

def send(message):
    message_bytes = pickle.dumps(message)
    to = message["to"]

    if to == "ALL":

        for client, nickname in zip(clients, nicknames):
            if nickname == message["from"]:
                message["text"] = "Me: " + message["text"]
            print(message["from"])
            client.send(message_bytes)

def handle(client):
    while True:
        try:
            message_bytes = client.recv(1024)
            if not message_bytes:
                # Client disconnected
                break

            message = pickle.loads(message_bytes)
            send(message)

        except Exception as e:
            # Handle any exceptions that occur during message handling
            print(f"Error handling message from client: {e}")
            break

    # Client disconnected, remove it from the lists
    if client in clients:
        index = clients.index(client)
        clients.remove(client)
        del nicknames[index]
        broadcast_nicknames()
        client.close()
        print(f"Client '{nicknames[index]}' disconnected.")

def broadcast_nicknames():
    pickled_nicknames = pickle.dumps(nicknames)
    nicknames_list = {"key": "NICKNAMESLIST", "nicknames": pickled_nicknames}
    nickname_list = pickle.dumps(nicknames_list)
    for client in clients:
        client.send(nickname_list)

def receive():
    while True:
        client, address = server.accept()
        # print(f'Connected by: {str(address)}')
        broadcast_nicknames()
        NICK = {"key": "NICK"}
        NICK = pickle.dumps(NICK)
        client.send(NICK)

        nickname_bytes = client.recv(1024)
        nickname_bytes = pickle.loads(nickname_bytes)
        nickname = nickname_bytes["value"].decode('utf-8')

        nicknames.append(nickname)
        clients.append(client)
        broadcast_nicknames()



        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server starting...")
receive()
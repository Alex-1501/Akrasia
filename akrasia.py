#!/usr/bin/python3
import socket
import sys
import threading
import time

client_list = []
BUFFER_SIZE = 1024 * 128
SEPARATOR = "<sep>"

def clear():
    print("\033[H\033[J")

def printMenu():
    print("[1] List Active Clients")
    print("[2] Remove Connected Client")
    print("[3] Start A Shell With A Client\n")
    print("[X] Exit\n")


def startListener(HOST, PORT):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(5)

    while True:
        try:
            conn, addr = s.accept()
        except socket.error:
            print("Cannot assign requested address")
            sys.exit(1)
        finally:
             client_list.append(conn)
        

def activeClients():
     counter = 0

     if len(client_list) < 1:
          clear()
          printMenu()
          return "Error: No Active Clients Connected\n"
     
     clear()
     printMenu()
     for client in client_list:
      counter = counter + 1
      return f"[{counter}] {client.getpeername()}\n"
     
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
        except:
            clear()
            return "\nError: Could Not Remove Client\n"

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
    threading.Thread(target=startListener, args=(HOST, PORT)).start()
    
    print(f"""                             
Listening: {HOST} : {PORT}\n 
""")
    while(isRunning):
        str = ""
        # Print menu but once a user selects an option, it will not be printed again - Redo this logic later makes no sense but works for now
        if menu:
            printMenu()
            menu = False

        option = input("Select An Option: ")

        if option == "1":
            str = activeClients()
            print(str)
        elif option == "2":
            str = activeClients()
            print (str)
            str = removeClient()
            print(str)
            printMenu()
        elif option == "3":
            str = activeClients()
            print(str)
            selectedClientStr = input("To Start A Shell, Type In The Client Number: ")
            selectedClient = int(selectedClientStr)
            x = client_list[selectedClient - 1]
            
        elif option == "X":
            isRunning = False
            for client in client_list:
                client.close()
            print("Exiting\n")
        else:
            clear()
            print("Invalid Option\n")
            menu = True

HOST = sys.argv[1]
PORT = int(sys.argv[2])
main(HOST, PORT)
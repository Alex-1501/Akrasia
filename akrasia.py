import socket
import sys
import threading

client_list = []

def clear():
    print("\033[H\033[J")

def printMenu():
    print("[1] List Active Clients")
    print("[2] Remove Connected Client\n")

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
        

def activeClients(flag):
     counter = 0

     if len(client_list) < 1:
          clear()
          printMenu()
          print("Error: No Active Clients Connected\n")

     if len(client_list) >= 1 and flag == "1":
        clear()
        printMenu()
        for client in client_list:
            print(f"\nClient: {client.getpeername()}")
     elif len(client_list) >= 1 and flag == "2":
          clear()
          printMenu()
          for client in client_list:
            counter = counter + 1
            print(f"[{counter}] {client.getpeername()}\n")

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
            print("\nClient Removed Successfully\n")
        except:
            clear()
            print("\nError: Could Not Remove Client\n")



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
    #print(f"Listening: {HOST} : {PORT}\n")

    while(isRunning):
        # Print menu but once a user selects an option, it will not be printed again - Redo this logic later makes no sense but works for now
        if menu:
            printMenu()
            menu = False

        option = input("Select An Option: ")

        if option == "1":
            activeClients(option)
        elif option == "2":
            activeClients(option)
            removeClient()
            printMenu()
        else:
            print("Invalid Option\n")
            menu = True

HOST = sys.argv[1]
PORT = int(sys.argv[2])
main(HOST, PORT)
import socket
import sys
import threading

client_list = []

def startListener(HOST, PORT):
    connection_list = []

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
     for client in client_list:
        print(f"Client: {client.getpeername()}")    

def main(HOST, PORT):
    print("""                             
   _____     __                                .__           
  /  _  \   |  | __ _______  _____      ______ |__| _____    
 /  /_\  \  |  |/ / \_  __ \ \__  \    /  ___/ |  | \__  \   
/    |    \ |    <   |  | \/  / __ \_  \___ \  |  |  / __ \_ 
\____|__  / |__|_ \  |__|    (____  / /____  > |__| (____  / 
        \/       \/               \/       \/            \/  
""")
    threading.Thread(target=startListener, args=(HOST, PORT)).start()
    print(f"Listening: {HOST} : {PORT}\n")

    print("[1] List Active Clients")
    userInput = input("Enter Here: ")
    if userInput == "1":
            client_thread = threading.Thread(target=activeClients).start()

HOST = sys.argv[1]
PORT = int(sys.argv[2])
main(HOST, PORT)
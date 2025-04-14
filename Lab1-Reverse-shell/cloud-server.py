import socket
import sys

class SocketServer:
    """
    A simple socket server that binds to a specified host and port,
    accepts one connection, and sends commands to the connected client.
    """
    def __init__(self, host="", port=9999):
        """
        Initialize the server with a host and port.
        """
        self.host = host
        self.port = port
        self.socket = None

    def create_socket(self):
        """
        Create the socket for the server.
        """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("Socket created successfully.")
        except socket.error as error:
            print(f"Socket creation error: {error}")
            sys.exit(1)

    def bind_socket(self):
        """
        Bind the socket to the host and port, and start listening for connections.
        """
        try:
            print(f"Binding to port: {self.port}")
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            print("Socket is now listening for connections.")
        except socket.error as error:
            print(f"Socket binding error: {error}")
            sys.exit(1)

    def accept_connection(self):
        """
        Accept an incoming connection and handle communication.
        """
        try:
            conn, address = self.socket.accept()
            print(f"Connection established with IP: {address[0]} on Port: {address[1]}")
            self.send_commands(conn)
            conn.close()
        except socket.error as error:
            print(f"Error accepting connection: {error}")

    def send_commands(self, conn):
        """
        Send commands to the connected client.
        Type 'quit' to end the session.
        """
        while True:
            command = input("Enter command: ")
            if command.lower() == "quit":
                print("Closing connection and shutting down server.")
                conn.close()
                self.socket.close()
                sys.exit(0)
            elif command.strip():
                try:
                    conn.send(command.encode())
                    client_response = conn.recv(1024).decode('utf-8')
                    print(client_response, end="")
                except socket.error as error:
                    print(f"Error during communication: {error}")
                    conn.close()
                    break

def main():
    server = SocketServer()
    server.create_socket()
    server.bind_socket()
    server.accept_connection()

if __name__ == "__main__":
    main()

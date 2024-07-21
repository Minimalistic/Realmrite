import socket
import threading

# Server settings
HOST = '127.0.0.1'
PORT = 65432

clients = []

def handle_client(conn, addr):
    print(f"New connection: {addr}")
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            broadcast(data, conn)
        except:
            break
    conn.close()
    clients.remove(conn)
    print(f"Connection closed: {addr}")

def broadcast(data, sender_conn):
    for client in clients:
        if client != sender_conn:
            client.sendall(data)

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Server listening on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        clients.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    main()
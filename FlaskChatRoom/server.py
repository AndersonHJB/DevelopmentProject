import socket
import threading


class ChatServer:
    def __init__(self, ip='0.0.0.0', port=12345):
        self.ip = ip
        self.port = port
        self.clients = []

    def broadcast(self, message, sender):
        for client in self.clients:
            if client != sender:
                client.sendall(message.encode())

    def handle_client(self, client_socket, client_address):
        print(f"新客户端 {client_address} 已连接")
        self.clients.append(client_socket)

        try:
            while True:
                message = client_socket.recv(1024).decode()
                if not message:
                    break
                print(f"{client_address}: {message}")
                self.broadcast(f"{client_address}: {message}", client_socket)
        finally:
            client_socket.close()
            self.clients.remove(client_socket)
            print(f"客户端 {client_address} 已断开")

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.ip, self.port))
        server_socket.listen(5)
        print(f"聊天服务器在 {self.ip}:{self.port} 上启动")

        try:
            while True:
                client_socket, client_address = server_socket.accept()
                threading.Thread(target=self.handle_client, args=(client_socket, client_address)).start()
        finally:
            server_socket.close()


if __name__ == '__main__':
    chat_server = ChatServer()
    chat_server.start()

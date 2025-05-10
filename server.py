import asyncio
import socket
import json
''' petla:

1. nasluchuje na nowe polaczenie.
2. odbiera od kazdego z uzytkownikow, zapisuje do messages,wysyla do kazdego z uzytkownikow.
3. co jakis czas zapisuje do pliku.


'''
class Server:

    def __init__(self):
        self.clients = set()
        self.BROADCAST_PORT = 9999
        self.BROADCAST_INTERVAL = 2
        #this is going to be incremented by one for each new connection
        self.communication_port = 8888
        self.messages = list()

    def get_local_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('8.8.8.8', 80))
            return s.getsockname()[0]
        except Exception:
            return '127.0.0.1'
        finally:
            s.close()

    def calc_broadcast(self, ip):
        index = ip.rfind('.')+1
        #dirty but works :)
        return ip[:index] + "255"

    async def broadcast_server(self, name):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        ip = self.get_local_ip()
        broadcast_addr = self.calc_broadcast(ip)

        while True:
            #we keep on sending information about how to reach this chat room.
            # communication_port will be changed if a connecttion occurs so each user gets his own port.
            message = json.dumps({"name": name, "host": ip, "port": self.communication_port}).encode()
            self.sock.sendto(message, (broadcast_addr, self.BROADCAST_PORT))
            print(f"[BROADCAST] {name} @ {ip}:{self.port}")
            await asyncio.sleep(self.BROADCAST_INTERVAL)

    async def handle_new_connection(self):

        while True:
            self.sock.bind(("0.0.0.0", self.communication_port))  # Nasłuchiwanie na porcie komunikacyjnym
            self.sock.listen(5)
            client_socket, client_address = self.sock.accept()
            print(f"Nowe połączenie od {client_address}")
            self.clients.append(client_socket)
            self.communication_port+=1

            asyncio.create_task(self.client_loop(client_socket, client_address))

    async def client_loop(self):
        pass


if __name__ =="__main__":
    server = Server()
    server.loop()
    name = "Moj_server"
    asyncio.gather(server.broadcast_server(name), server.handle_new_connection())
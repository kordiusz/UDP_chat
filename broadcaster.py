import asyncio
import json
import socket
import sys

BROADCAST_PORT = 9999
BROADCAST_INTERVAL = 2



def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        return s.getsockname()[0]
    except Exception:
        return '127.0.0.1'
    finally:
        s.close()

def calc_broadcast(ip):
    index = ip.rfind('.')+1
    return ip[:index] + "255"

async def broadcast_server(name, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
   # sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    ip = get_local_ip()
    broadcast_addr = calc_broadcast(ip)
    

    while True:
        message = json.dumps({"name": name, "host": ip, "port": port}).encode()
        sock.sendto(message, (broadcast_addr, BROADCAST_PORT))
        print(f"[BROADCAST] {name} @ {ip}:{port}")
        await asyncio.sleep(BROADCAST_INTERVAL)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Użycie: python broadcaster.py <nazwa_serwera> <port>")
        sys.exit(1)

    name = sys.argv[1]
    port = int(sys.argv[2])
    asyncio.run(broadcast_server(name, port))
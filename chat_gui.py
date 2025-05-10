# main.py
import asyncio
import json
import socket
import threading
import tkinter as tk

from gui import ServerSelectionWindow, ChatWindow

BROADCAST_PORT = 9999


class BroadcastListener(asyncio.DatagramProtocol):
    def __init__(self, gui):
        self.gui = gui

    def datagram_received(self, data, addr):
        try:
            decoded = json.loads(data.decode())
            label = f"{decoded['name']} @ {decoded['host']}:{decoded['port']}"
            self.gui.update_server_list(label, (decoded['host'], int(decoded['port'])))
        except Exception:
            pass


class ChatClientProtocol(asyncio.DatagramProtocol):
    def __init__(self, chat_gui, nickname, server_addr):
        self.chat_gui = chat_gui
        self.nickname = nickname
        self.server_addr = server_addr
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        try:
            msg = json.loads(data.decode())
            nick = msg.get("nick", "???")
            content = msg.get("msg", "")
            self.chat_gui.append_msg(f"{nick}: {content}")
        except Exception:
            self.chat_gui.append_msg(f"[BŁĄD] Nieprawidłowa wiadomość")

    def send_message(self, text):
        payload = json.dumps({
            "nick": self.nickname,
            "msg": text
        }).encode()
        self.transport.sendto(payload, self.server_addr)


def start_tk_loop(root):
    try:
        while True:
            root.update()
    except tk.TclError:
        pass


def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    root = tk.Tk()
    root.geometry("450x400")

    def on_server_selected(server_addr, nickname):
        chat_window = ChatWindow(root, lambda msg: protocol.send_message(msg))

        async def start_chat():
            _, p = await loop.create_datagram_endpoint(
                lambda: ChatClientProtocol(chat_window, nickname, server_addr),
                local_addr=("0.0.0.0", 0)
            )
            nonlocal protocol
            protocol = p

        asyncio.run_coroutine_threadsafe(start_chat(), loop)

    protocol = None
    selection = ServerSelectionWindow(root, on_server_selected)

    loop.run_until_complete(loop.create_datagram_endpoint(
        lambda: BroadcastListener(selection),
        local_addr=("0.0.0.0", BROADCAST_PORT)
    ))

    threading.Thread(target=start_tk_loop, args=(root,), daemon=True).start()

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()


if __name__ == "__main__":
    main()

import tkinter as tk
from tkinter import messagebox, simpledialog
import asyncio
import threading
from discovery import listen_for_servers, broadcast_server_info
from chat_server import start_chat_server
from chat_client import run_chat_client

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LAN Chat")
        self.servers = {}

        self.listbox = tk.Listbox(root, width=50)
        self.listbox.pack(padx=10, pady=10)

        self.join_btn = tk.Button(root, text="Dołącz", command=self.join_server)
        self.join_btn.pack(side=tk.LEFT, padx=10)

        self.host_btn = tk.Button(root, text="Stwórz serwer", command=self.host_server)
        self.host_btn.pack(side=tk.RIGHT, padx=10)

        threading.Thread(target=self.start_discovery_loop, daemon=True).start()

    def update_server_list(self, info):
        key = f"{info['name']} ({info['host']}:{info['port']})"
        if key not in self.servers:
            self.servers[key] = (info['host'], info['port'])
            self.listbox.insert(tk.END, key)

    def join_server(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Brak wyboru", "Wybierz serwer z listy.")
            return
        key = self.listbox.get(selection[0])
        host, port = self.servers[key]
        threading.Thread(target=asyncio.run, args=(run_chat_client(host, port),), daemon=True).start()

    def host_server(self):
        port = simpledialog.askinteger("Port serwera", "Podaj numer portu (np. 8888):", minvalue=1024, maxvalue=65535)
        if not port:
            return

        name = f"Serwer {port}"
        threading.Thread(target=asyncio.run, args=(start_chat_server('0.0.0.0', port),), daemon=True).start()
        threading.Thread(target=asyncio.run, args=(broadcast_server_info(name, port),), daemon=True).start()
        messagebox.showinfo("Serwer uruchomiony", f"Twój serwer działa na porcie {port}.")
        threading.Thread(target=asyncio.run, args=(run_chat_client('127.0.0.1', port),), daemon=True).start()

    def start_discovery_loop(self):
        asyncio.run(listen_for_servers(lambda info: self.root.after(0, self.update_server_list, info)))

if __name__ == '__main__':
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()

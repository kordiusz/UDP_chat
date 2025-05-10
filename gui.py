# gui.py
import tkinter as tk
from tkinter import simpledialog, messagebox


class ServerSelectionWindow:
    def __init__(self, root, on_select):
        self.root = root
        self.on_select = on_select
        self.servers = {}

        self.title = tk.Label(root, text="Dostępne serwery", font=("Arial", 14))
        self.title.pack(pady=(10, 5))

        self.listbox = tk.Listbox(root, width=50, height=10)
        self.listbox.pack(padx=10, pady=5)

        self.join_btn = tk.Button(root, text="Dołącz", command=self.select_server)
        self.join_btn.pack(pady=(5, 10))

    def update_server_list(self, label, addr):
        if label not in self.servers:
            self.servers[label] = addr
            self.listbox.insert(tk.END, label)

    def select_server(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("Brak wyboru", "Wybierz serwer z listy.")
            return
        label = self.listbox.get(selected)
        addr = self.servers[label]

        nickname = simpledialog.askstring("Nick", "Podaj swój nick:")
        if nickname:
            self.on_select(addr, nickname)


class ChatWindow:
    def __init__(self, root, send_callback):
        self.root = root
        self.send_callback = send_callback

        for widget in root.winfo_children():
            widget.destroy()

        self.root.title("Czat LAN")
        self.chat_log = tk.Text(root, state='disabled', height=20)
        self.chat_log.pack(padx=10, pady=10)

        self.entry = tk.Entry(root)
        self.entry.pack(padx=10, pady=(0, 10), fill='x')
        self.entry.bind("<Return>", self.send_msg)

    def send_msg(self, event=None):
        msg = self.entry.get()
        if msg.strip():
            self.send_callback(msg)
            self.entry.delete(0, tk.END)

    def append_msg(self, msg):
        self.chat_log.configure(state='normal')
        self.chat_log.insert(tk.END, msg + '\n')
        self.chat_log.configure(state='disabled')
        self.chat_log.see(tk.END)

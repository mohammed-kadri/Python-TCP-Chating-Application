import socket
import sys
import threading
import tkinter as tk
from tkinter import simpledialog
import tkinter.scrolledtext
import pickle
from PIL import ImageTk, Image
import customtkinter
import time

import tkinter as tk



HOST = "192.168.1.106"
PORT = 9999



class Client:
    def __init__(self, host, port):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.current_disccusion_index = 0
        msg = tk.Tk()
        msg.withdraw()


        self.ChatRooms = []
        self.nickname = ''
        self.nickname = simpledialog.askstring("Login", "Enter your nickname", parent=msg)
        self.gui_done = False
        self.running = True
        gui_thread = threading.Thread(target=self.gui_loop)
        recievread = threading.Thread(target=self.receive)
        gui_thread.start()
        recieve_thread.start()

    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2e_th
        window.geometry(f"{width}x{height}+{x}+{y}")

    def gui_loop(self):
        self.win = tk.Tk()
        self.win.configure(background='white')
        self.win.title(self.nickname)
        window_width = 650
        window_height = 600
        self.center_window(self.win, window_width, window_height)

        main_frame = tk.Frame(self.win, bg='white')
        main_frame.pack(fill='both', expand=True)

        self.win.resizable(False, False)

        self.users_frame = tk.Frame(main_frame, bg='lightgray', padx=10, pady=10)
        self.users_frame.pack(side='left', fill='both')

        users_label = tk.Label(self.users_frame, text='Connected Users:', bg='lightgray', font=('Arial', 14, 'bold'))
        users_label.pack(pady=0)

        public_chat_frame = tk.Frame(main_frame, bg='lightgray', padx=10, pady=10)
        public_chat_frame.pack(side='left', fill='both')

        self.public_chat_button = tk.Button(public_chat_frame, text='Public',
                                            command=lambda: self.switch_conversation(0))
        self.public_chat_button.pack(pady=5)

        self.right_frame = tk.Frame(main_frame, bg='white', padx=10, pady=10)
        self.right_frame.pack(side='left', fill='both', expand=True)

        self.chat_label = tk.Label(self.right_frame, text='Chat:', background='white', font=('Arial', 20))
        self.chat_label.pack(pady=5)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.right_frame)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state='disabled')

        self.msg_label = tk.Label(self.right_frame, text='Message:', background='lightgray', font=('Arial', 15))
        self.msg_label.pack(pady=5)

        self.input_area = tk.Text(self.right_frame, height=3)
        self.input_area.pack(padx=20, pady=5)
        self.input_area.bind('<KeyRelease>', self.send_message)

        self.send_button = tk.Button(self.right_frame, text='Send', command=self.write)
        self.send_button.pack(pady=5)

        self.ChatRooms.append(
            {
                "key": "PUBLIC",
                "messages_area": self.text_area
            }
        )

        self.gui_done = True
        self.win.protocol('WM_DELETE_WINDOW', self.stop)
        self.win.mainloop()

    def switch_conversation(self, order, old_textarea=""):
        self.current_disccusion_index = order
        if self.gui_done:
            for chatroom in self.ChatRooms:
                chatroom["messages_area"].pack_forget()
            self.ChatRooms[order]["messages_area"].pack()
            try:
                old_textarea.pack_forget()
            except:
                pass
        print(self.ChatRooms)

    def update_users_list(self, nicknames):
        while True:
            try:
                print(nicknames)
                for widget in self.users_frame.winfo_children():
                    widget.destroy()
                for nickname in nicknames:
                    user_frame = tk.Frame(self.users_frame, bg='lightgray')
                    user_frame.pack(fill='x', padx=5, pady=2)
                    user_label = tk.Label(user_frame, text=nickname, bg='lightgray')
                    user_label.pack(side='left')
                    if nickname != self.nickname:
                        message_button = tk.Button(user_frame, text='Message',
                                                   command=lambda n=nickname: self.switch_conversation(
                                                       nicknames.index(n) + 1))
                        message_button.pack(side='left')
                break
            except:
                pass
        textarea_created = False
        while textarea_created == False:
            try:
                for nickname in nicknames:
                    if not any(chatroom['key'] == nickname for chatroom in self.ChatRooms):
                        self.new_text_area = tkinter.scrolledtext.ScrolledText(self.right_frame)
                        self.new_text_area.pack(padx=20, pady=5)
                        self.new_text_area.config(state='disabled')
                        self.new_text_area.pack_forget()
                        new_chatroom = {
                            "key": nickname,
                            "messages_area": self.new_text_area
                        }
                        self.ChatRooms.append(new_chatroom)
                    temp_chatroom = self.ChatRooms
                    self.ChatRooms = [chatroom for chatroom in self.ChatRooms if
                                      chatroom['key'] == 'PUBLIC' or chatroom['key'] in nicknames]
                    if not temp_chatroom == self.ChatRooms:
                        missing_textarea = self.get_missing_chatroom(temp_chatroom, self.ChatRooms)["messages_area"]
                        print(self.get_missing_chatroom(temp_chatroom, self.ChatRooms)["key"])
                        self.switch_conversation(0, missing_textarea)
                    textarea_created = True

            except Exception as e:
                print(e)

    def get_missing_chatroom(self, array1, array2):
        for dictionary in array1:
            key = dictionary.get("key")
            if key not in [d.get("key") for d in array2]:
                return dictionary
        return None

    # If no missing key is found
    def send_message_to(self, nickname):
        pass

    def send_message(self, event):
        if event.keysym == 'Return':
            self.write()

    def write(self):
        written_text = self.input_area.get('1.0', 'end')
        to = self.ChatRooms[self.current_disccusion_index]["key"]
        message = {"key": "MESSAGE", "from": self.nickname, "to": to, "text": written_text.strip()}
        message_bytes = pickle.dumps(message)
        if message["text"]:
            self.sock.send(message_bytes)
        self.input_area.delete('1.0', 'end')

    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)

    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024)
                message = pickle.loads(message)
                if message["key"] == 'NICK':
                    nick = {"key": "nickname", "value": self.nickname.encode("utf-8")}
                    nick = pickle.dumps(nick)
                    self.sock.send(nick)
                elif message["key"] == "MESSAGE":
                    if self.gui_done:
                        if message["to"] == "PUBLIC":
                            message_text = message["text"]
                            self.active_text_area = self.ChatRooms[0]["messages_area"]
                            self.active_text_area.config(state=tk.NORMAL)
                            if self.nickname == message["from"]:
                                self.active_text_area.insert(tk.END, 'Me: ' + message_text + '\n')
                            else:
                                self.active_text_area.insert(tk.END, message["from"] + ': ' + message_text + '\n')
                            self.active_text_area.yview(tk.END)
                            self.active_text_area.config(state=tk.DISABLED)

                        elif self.nickname == message["from"]:
                            message_text = message["text"]
                            to_disccusion = 0
                            for index, room in enumerate(self.ChatRooms):
                                if room["key"] == message["to"]:
                                    to_disccusion = index
                                    break
                            self.active_text_area = self.ChatRooms[to_disccusion]["messages_area"]
                            self.active_text_area.config(state=tk.NORMAL)
                            if self.nickname == message["from"]:
                                self.active_text_area.insert(tk.END, 'Me: ' + message_text + '\n')
                            else:
                                self.active_text_area.insert(tk.END, message["from"] + ': ' + message_text + '\n')
                            self.active_text_area.yview(tk.END)
                            self.active_text_area.config(state=tk.DISABLED)

                        else:
                            message_text = message["text"]
                            to_disccusion = 0
                            for index, room in enumerate(self.ChatRooms):
                                if room["key"] == message["from"]:
                                    to_disccusion = index
                                    break
                            self.active_text_area = self.ChatRooms[to_disccusion]["messages_area"]
                            self.active_text_area.config(state=tk.NORMAL)
                            if self.nickname == message["from"]:
                                self.active_text_area.insert(tk.END, 'Me: ' + message_text + '\n')
                            else:
                                self.active_text_area.insert(tk.END, message["from"] + ': ' + message_text + '\n')
                            self.active_text_area.yview(tk.END)
                            self.active_text_area.config(state=tk.DISABLED)
                            pass
                elif message["key"] == 'NICKNAMESLIST':
                    nicknames = pickle.loads(message["nicknames"])
                    self.update_users_list(nicknames)
            except ConnectionAbortedError:
                break


client = Client(HOST, PORT)

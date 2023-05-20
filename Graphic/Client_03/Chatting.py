import tkinter as tk
from tkinter import *
import os
import threading


class Chat:
    def __init__(self, client_socket_game, client_socket_chat):
        self.socket_game = client_socket_game
        self.socket_chat = client_socket_chat

        self.win = tk.Tk()
        self.win.geometry('400x400')
        self.win.title("HalliGalli")

        self.embed = tk.Frame(self.win, width=700, height=700, bg="white")  # creates embed frame for pygame window
        self.embed.grid(columnspan=700, rowspan=700)
        self.embed.pack(side=LEFT)
        os.environ['SDL_WINDOWID'] = str(self.embed.winfo_id())
        os.environ['SDL_VIDEODRIVER'] = 'windib'

        self.frame = tk.Frame(self.win, width=380, height=300, bg="white")
        self.frame.place(x=10, y=50)

        self.scrollbar1 = tk.Scrollbar(self.frame)
        self.scrollbar1.pack(side="right", fill='both')

        self.scrollbar2 = tk.Scrollbar(self.frame, orient="horizontal")
        self.scrollbar2.pack(side="bottom", fill='both')

        self.listbox = tk.Listbox(self.frame, yscrollcommand=self.scrollbar1.set, xscrollcommand=self.scrollbar2.set,
                                  width=50, height=18)
        self.listbox.pack(side="left")
        self.input_text = StringVar()

        self.chat_l1 = Label(self.win, text="chatting", font=("bold", 18), bg="white")
        self.chat_l1.place(x=160, y=10)

        self.chat_e1 = Entry(self.win, width=40, textvariable=self.input_text)
        self.chat_e1.place(x=10, y=360)

        self.send_b = Button(self.win, text="Send", width=5, command=self.send_chat)
        self.send_b.place(x=300, y=360)

        self.clear_b = Button(self.win, text="clear", width=5, command=self.chat_e1.delete(0, END))
        self.clear_b.place(x=350, y=360)

        self.scrollbar1["command"] = self.listbox.yview
        self.scrollbar2["command"] = self.listbox.xview

        self.txt_label = Label(self.win, text="")

        self.receiver_thread_chat = threading.Thread(target=self.recv_chat)
        self.receiver_thread_chat.daemon = True

        self.win.bind("<KeyPress>", self.key_click)
        self.win.bind("<Return>", self.send_chat)
        self.key = 0

        self.listbox.insert(END, "게임에 접속했습니다.")
        self.listbox.insert(END, "F4: 카드 뒤집기 / F8: 종 울리기")
        self.listbox.insert(END, "게임 시작 또는 재시작에 투표하려면 '/시작' 을 입력해주세요. ")
        # self.listbox.insert(END, "강제로 턴 넘기기에 투표하려면 '/턴' 을 입력해주세요.")
        self.listbox.see(END)

    def key_click(self, e):
        # try:
        self.key = e.keysym
        request = ''
        if self.key == "F12":
            print('requested game set to the server.')
            request = 'set'
        elif self.key == "F8":
            print('requested bell ring to the server.')
            request = 'bell'
        elif self.key == "F4":
            print('requested card open to the server.')
            request = 'open'
        self.socket_game.send(request.encode('utf-8'))
        # except ConnectionResetError:
        #     print('서버가 게임 연결을 종료했습니다.')
        # finally:
        #     exit(0)

    def send_chat(self):
        try:
            message = self.input_text.get()
            self.socket_chat.send(message.encode('utf-8'))
            self.chat_e1.delete(0, END)
        except ConnectionAbortedError:
            pass
        except ConnectionResetError:
            pass

    def recv_chat(self):
        try:
            while True:
                message = self.socket_chat.recv(2048).decode('utf-8')
                self.listbox.insert(END, message)
                self.listbox.see(END)
        except ConnectionAbortedError:
            print('클라이언트 사용자가 채팅 연결을 중단했습니다.')
        except ConnectionResetError:
            print('서버가 채팅 연결을 종료했습니다.')
        finally:
            exit(0)

    def run(self):
        self.receiver_thread_chat.start()
        self.win.mainloop()

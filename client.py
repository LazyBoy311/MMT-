from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
from signup import SignUpPage
from note_app import NoteApp
import socket
import threading


HOST = '127.0.0.1'
PORT = 1233
FORMAT = 'utf-8'


class Client():
    def __init__(self, host, port):
        # SOCKET CONNECTION
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))

        self.gui_done = False
        self.running = True

        gui_thread = threading.Thread(target=self.gui_loop)

        gui_thread.start()

    def gui_loop(self):
        self.root = Tk()
        self.root.title('Sign In Page')
        self.root.iconbitmap('images/login.ico')
        self.root.geometry('925x500+300+200')
        self.root.config(bg='#fff')
        self.root.resizable(False, False)

        # Background image
        self.bg = ImageTk.PhotoImage(file='images/login.png')
        self.bg_img = Label(self.root, image=self.bg,
                            bg='white').place(x=50, y=50)

        # SignIn Frame
        self.frame = Frame(self.root, width=350, height=350, bg='white')
        self.frame.place(x=480, y=70)

        self.heading = Label(self.frame, text='Sign in', fg='#57a1f8',
                             bg='white', font=('Helvetica', 35, 'bold'))
        self.heading.place(x=100, y=5)
        self.desc = Label(self.frame, text='E-NOTE: Make your life easier!',
                          fg='#57a1f8', bg='white', font=('Helvetica', 11, 'bold'))
        self.desc.place(x=70, y=70)

        #------------------------Username-------------------------#
        self.user_txt = Label(self.frame, text='Username', font=(
            'Helvetica', 12, 'bold'), fg='black', bg='white')
        self.user_txt.place(x=37, y=100)

        self.user = Entry(self.frame, width=35, fg='black', border=0,
                          bg='white', font=('Helvetica', 11))
        self.user.place(x=40, y=130)

        Frame(self.frame, width=295, height=2, bg='black').place(x=40, y=157)

        #-----------------------Password--------------------------#
        self.code_txt = Label(self.frame, text='Password', font=(
            'Helvetica', 12, 'bold'), fg='black', bg='white')
        self.code_txt.place(x=37, y=170)

        self.code = Entry(self.frame, width=35, fg='black',
                          border=0, bg='white', font=('Helvetica', 11), show="•")
        self.code.place(x=40, y=200)

        Frame(self.frame, width=295, height=2, bg='black').place(x=40, y=227)

        # Show/hide password
        self.show_img = ImageTk.PhotoImage(file='images/show.png')
        self.hide_img = ImageTk.PhotoImage(file='images/hide.png')
        self.show_btn = Button(self.frame, image=self.show_img, command=self.show_password, relief=FLAT,
                               activebackground='white', borderwidth=0, background="white", cursor="hand2")
        self.show_btn.place(x=315, y=200)

        #----------------------Sign In Button----------------------#
        self.sign_in_btn = Button(self.frame, width=42, pady=8, text='Sign in', cursor="hand2",
                                  bg='#57a1f8', fg='white', border=0, command=self.sign_in).place(x=40, y=254)

        # Forgot password
        self.forgot_button = Button(self.frame, text="Forgot Password ?",
                                    font=("Helvetica", 10, "bold underline"), fg="#57a1f8", relief=FLAT,
                                    activebackground="white", borderwidth=0, background="white", cursor="hand2", command=self.forgot_password)
        self.forgot_button.place(x=135, y=300)

        self.label = Label(self.frame, text="Don't have an account?",
                           fg='black', bg='white', font=('Helvetica', 9))
        self.label.place(x=95, y=330)

        self.sign_in_sm = Button(self.frame, width=6, text='Sign up', border=0,
                                 bg='white', cursor='hand2', fg='#57a1f8', command=self.sign_up)
        self.sign_in_sm.place(x=235, y=330)
        #------------------------------------------------------#
        self.gui_done = True
        self.root.protocol("WM_DELETE_WINDOW", self.stop)
        self.root.mainloop()

    def show_password(self):
        self.hide_btn = Button(self.frame, image=self.hide_img, command=self.hide_password, relief=FLAT,
                               activebackground='white', borderwidth=0, background="white", cursor="hand2")
        self.hide_btn.place(x=315, y=200)
        self.code.config(show='')

    def hide_password(self):
        self.show_btn = Button(self.frame, image=self.show_img, command=self.show_password, relief=FLAT,
                               activebackground='white', borderwidth=0, background="white", cursor="hand2")
        self.show_btn.place(x=315, y=200)
        self.code.config(show='•')

    def forgot_password(self):
        self.win = Toplevel()
        window_width = 350
        window_height = 350
        screen_width = self.win.winfo_screenwidth()
        screen_height = self.win.winfo_screenheight()
        position_top = int(screen_height / 4 - window_height / 4)
        position_right = int(screen_width / 2 - window_width / 2)
        self.win.geometry(
            f'{window_width}x{window_height}+{position_right}+{position_top}')
        self.win.title('Forgot Password')
        self.win.iconbitmap('images/aa.ico')
        self.win.configure(background='#f8f8f8')
        self.win.resizable(0, 0)

        # ====== Username ====================
        self.user_entry = Entry(self.win, fg="black", font=(
            "Helvetica", 12, "bold"), highlightthickness=2)
        self.user_entry.place(x=40, y=50, width=256, height=34)
        self.user_entry.config(highlightbackground="black",
                               highlightcolor="black")
        self.user_label = Label(self.win, text='Username', fg="#89898b", bg='#f8f8f8',
                                font=("Helvetica", 11, 'bold'))
        self.user_label.place(x=40, y=20)

        # ====  New Password ==================
        self.new_password_entry = Entry(self.win, fg="black", font=(
            "Helvetica", 12, "bold"), show='•', highlightthickness=2)
        self.new_password_entry.place(x=40, y=130, width=256, height=34)
        self.new_password_entry.config(
            highlightbackground="black", highlightcolor="black")
        self.new_password_label = Label(self.win, text='New Password', fg="#89898b",
                                        bg='#f8f8f8', font=("Helvetica", 11, 'bold'))
        self.new_password_label.place(x=40, y=100)

        # ====  Confirm Password ==================
        self.confirm_password_entry = Entry(self.win, fg="black", font=(
            "Helvetica", 12, "bold"), show='•', highlightthickness=2)
        self.confirm_password_entry.place(x=40, y=210, width=256, height=34)
        self.confirm_password_entry.config(
            highlightbackground="black", highlightcolor="black")
        self.confirm_password_label = Label(self.win, text='Confirm Password', fg="#89898b", bg='#f8f8f8',
                                            font=("Helvetiac", 11, 'bold'))
        self.confirm_password_label.place(x=40, y=180)

        # ======= Update password Button ============
        self.update_pass = Button(self.win, fg='#f8f8f8', text='Update Password', bg='#1b87d2', font=("Helvetica", 14, "bold"),
                                  cursor='hand2', activebackground='#1b87d2', command=self.forgot_psw)
        self.update_pass.place(x=40, y=270, width=256, height=50)

    def forgot_psw(self):
        username = self.user_entry.get()
        password = self.new_password_entry.get()
        new_password = self.confirm_password_entry.get()

        self.user_info = str(
            ["FORGOT-PW", username, password, new_password])
        self.client.send(self.user_info.encode(FORMAT))

        # Receive response
        response = self.client.recv(2048).decode(FORMAT)
        messagebox.showinfo(None, response)
        if response == "Update password successfully":
            self.win.destroy()

    def sign_in(self):
        while self.running:
            try:
                username = self.user.get()
                password = self.code.get()
                self.user_info = str(["SIGN-IN", username, password])
                self.client.send(self.user_info.encode(FORMAT))

                response = self.client.recv(2048).decode(FORMAT)
                messagebox.showinfo(None, response)

                if response == "Login successful!":
                    if self.gui_done:
                        NoteApp(self.root, self.client, self.user_info)
                else:
                    break
            except ConnectionAbortedError:
                break
            except:
                print("[ERROR]: An error occured!")
                self.client.close()
                break

    def sign_up(self):
        self.master = Toplevel()
        SignUpPage(self.master, self.client)

    def stop(self):
        self.running = False
        self.root.destroy()
        self.client.close()
        exit(0)


client = Client(HOST, PORT)

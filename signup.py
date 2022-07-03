from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import socket

FORMAT = 'utf-8'


class SignUpPage:
    def __init__(self, root, client):
        self.root = root
        self.client = client
        self.root.title('Sign Up Page')
        self.root.geometry('925x500+300+200')
        self.root.config(bg='#fff')
        self.root.resizable(False, False)

        # Background image
        self.bg = ImageTk.PhotoImage(file='images/login.png')
        self.bg_img = Label(self.root, image=self.bg,
                            bg='white').place(x=50, y=50)

        # SignUp Frame
        self.frame = Frame(self.root, width=350, height=390, bg='white')
        self.frame.place(x=480, y=70)

        self.heading = Label(self.frame, text='Sign up', fg='#57a1f8',
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

        #------------------------Password-------------------------#
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

        #-------------------------Confirm Password------------------------#
        self.confirm_code_txt = Label(self.frame, text='Confirm Password', font=(
            'Helvetica', 12, 'bold'), fg='black', bg='white')
        self.confirm_code_txt.place(x=37, y=240)

        self.confirm_code = Entry(self.frame, width=35, fg='black',
                                  border=0, bg='white', font=('Helvetica', 11), show="•")
        self.confirm_code.place(x=40, y=270)

        Frame(self.frame, width=295, height=2, bg='black').place(x=40, y=297)

        # Show/hide password
        self.show_btn = Button(self.frame, image=self.show_img, command=self.show_password_confirm, relief=FLAT,
                               activebackground='white', borderwidth=0, background="white", cursor="hand2")
        self.show_btn.place(x=315, y=270)

        #-----------------------Sign Up Button-------------------------------#
        Button(self.frame, width=42, pady=8, text="Sign Up", cursor="hand2",
               bg="#57a1f8", fg="white", border=0, command=self.sign_up).place(x=40, y=320)
        self.label = Label(self.frame, text='I have an account!',
                           fg='black', bg='white', font=('Helvetica', 9))
        self.label.place(x=95, y=368)

        self.sign_in = Button(self.frame, width=6, text='Sign in', border=0,
                              bg='white', cursor='hand2', fg='#57a1f8', command=self.sign_in)
        self.sign_in.place(x=230, y=368)

        #------------------------------------------------------#
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

    def show_password_confirm(self):
        self.hide_btn = Button(self.frame, image=self.hide_img, command=self.hide_password_confirm, relief=FLAT,
                               activebackground='white', borderwidth=0, background="white", cursor="hand2")
        self.hide_btn.place(x=315, y=270)
        self.confirm_code.config(show='')

    def hide_password_confirm(self):
        self.show_btn = Button(self.frame, image=self.show_img, command=self.show_password_confirm, relief=FLAT,
                               activebackground='white', borderwidth=0, background="white", cursor="hand2")
        self.show_btn.place(x=315, y=270)
        self.confirm_code.config(show='•')

    def sign_up(self):
        self.username = self.user.get()
        self.password = self.code.get()
        self.confirm_pw = self.confirm_code.get()

        self.user_info = str(
            ["SIGN-UP", self.username, self.password, self.confirm_pw])
        self.client.send(self.user_info.encode(FORMAT))
        # Receive response
        self.response = self.client.recv(2048)
        self.response = self.response.decode(FORMAT)

        messagebox.showinfo(None, self.response)
        if self.response == "Register successfully":
            self.root.destroy()

    def sign_in(self):
        self.root.destroy()

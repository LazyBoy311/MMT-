from http import client
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import scrolledtext
from tkinter.filedialog import askdirectory, askopenfilename
from tkinter.constants import *
from PIL import ImageTk, Image
import socket
import threading
import json
import os
import io

HOST = '127.0.0.1'
PORT = 1233
FORMAT = 'utf-8'


class NoteApp():
    def __init__(self, root, client, user_info):
        self.client = client
        self.running = True
        self.gui_done = False

        gui_thread = threading.Thread(target=self.gui_loop(root, user_info))

        gui_thread.start()

    def gui_loop(self, root, user_info):
        self.user_info = eval(user_info)
        self.root = root
        self.root.title('E-NOTE')
        self.root.iconbitmap('images/note.ico')
        self.root.geometry('800x600')
        self.root.config(bg='#fff')
        self.root.resizable(False, False)

        # # Background image
        self.bg = ImageTk.PhotoImage(file='images/blank_bg.png')
        self.bg_img = Label(self.root, image=self.bg,
                            bg='white').place(x=0, y=0)

        # NoteApp Frame
        self.frame = Frame(self.root, width=800, height=200, bg='white')
        self.frame.place(x=30, y=140)

        #================== List Notes ======================#
        columns = ('id', 'type', 'content')
        self.tree = ttk.Treeview(
            self.root, columns=columns, show='headings')
        self.tree.column("id", anchor=CENTER, width=80)
        self.tree.column("type", anchor=CENTER, width=200)
        self.tree.column("content", anchor=W, width=400)
        # define headings
        self.tree.heading('id', text='ID')
        self.tree.heading('type', text='TYPE')
        self.tree.heading('content', text='CONTENT')

        self.tree.grid(row=0, column=0, sticky=NSEW)
        self.tree.place(x=60, y=140)
        # add a scrollbar
        scrollbar = ttk.Scrollbar(
            self.root, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')

        #====================== Load Data ================================#
        self.client_notes = self.client.recv(4100000).decode(FORMAT)
        self.client_notes = eval(self.client_notes)
        notes = self.client_notes['note']
        files = self.client_notes['file']
        imgs = self.client_notes['image']
        self.countID = 1
        for note in notes:
            self.tree.insert(
                '', 'end', values=(note['_id'], "Text", f"[Topic: {note['title']}] : {note['content'] if len(note['content']) < 20 else note['content'][0:20:1] + '...'}"))
            self.countID = max(self.countID, int(note['_id'])) + 1
        for img in imgs:
            self.tree.insert(
                '', 'end', values=(img['_id'], "Image", f"[Name]: {img['name']}"))
            self.countID = max(self.countID, int(img['_id'])) + 1
        for file in files:
            self.tree.insert(
                '', 'end', values=(file['_id'], "File", f"[Name]: {file['name']}"))
            self.countID = max(self.countID, int(file['_id'])) + 1
        # ========================= Header =========================== #
        # Brand name
        self.frame1 = Frame(self.root, width=800, height=120, bg='white')
        self.frame1.place(x=0, y=0)
        self.heading = Label(self.frame1, text='E-NOTE', fg='#57a1f8',
                             bg='white', font=('Helvetica', 35, 'bold'))
        self.heading.place(x=320, y=2)
        # User
        self.user = Label(self.frame1, text=f'User: {self.user_info[1]}', fg='black',
                          bg='white', font=('Helvetica', 16, 'bold'))
        self.user.place(x=600, y=60)
        #============= Buttons ====================#
        self.frame2 = Frame(self.root, width=800, height=250, bg='white')
        self.frame2.place(x=0, y=400)
        self.add_txt_btn = Button(self.frame2, width=16, pady=8, text='Add Text',
                                  cursor="hand2", bg='#57a1f8', fg='white', border=0, command=self.add_text)
        self.add_txt_btn.place(x=600, y=20)

        self.add_files_btn = Button(self.frame2, width=16, pady=8, text='Add file',
                                    cursor="hand2", bg='#57a1f8', fg='white', border=0, command=self.add_file)
        self.add_files_btn.place(x=600, y=80)

        self.upload_img_btn = Button(self.frame2, width=16, pady=8, text='Upload Image',
                                     cursor="hand2", bg='#57a1f8', fg='white', border=0, command=self.upload_image)
        self.upload_img_btn.place(x=600, y=140)

        self.delete_btn = Button(self.frame2, width=16, pady=8, text='Delete',
                                 cursor="hand2", bg='red', fg='white', border=0, command=self.delete)
        self.delete_btn.place(x=70, y=20)

        self.view_btn = Button(self.frame2, width=16, pady=8, text='View',
                               cursor="hand2", bg='green', fg='white', border=0, command=self.view)
        self.view_btn.place(x=70, y=80)

        self.download_btn = Button(self.frame2, width=16, pady=8, text='Download',
                                   cursor="hand2", bg='#ad91e7', fg='white', border=0, command=self.download)
        self.download_btn.place(x=70, y=140)
        #------------------------------------------------------#
        self.gui_done = True
        self.root.protocol("WM_DELETE_WINDOW", self.stop)
        self.root.mainloop()

    def stop(self):
        self.running = False
        self.root.destroy()
        self.client.close()
        exit(0)

    def add_text(self):
        self.win = Toplevel()
        window_width = 500
        window_height = 300
        screen_width = self.win.winfo_screenwidth()
        screen_height = self.win.winfo_screenheight()
        position_top = int(screen_height / 4 - window_height / 4)
        position_right = int(screen_width / 2 - window_width / 2)
        self.win.geometry(
            f'{window_width}x{window_height}+{position_right}+{position_top}')
        self.win.title('Text')
        self.win.configure(background='white')
        self.win.resizable(0, 0)

        self.topic_label = Label(self.win, text='Topic:', font=(
            'Helvetica', 12, 'bold'), fg='black', bg='white')
        self.topic_label.place(x=0, y=0)
        self.topic_area = Text(self.win, height=1)
        self.topic_area.config(font=("Helvetica", 14))
        self.topic_area.pack(padx=(80, 20), pady=2)

        self.input_label = Label(self.win, text='NOTES:', font=(
            'Helvetica', 12, 'bold'), fg='black', bg='white')
        self.input_label.place(x=0, y=130)
        self.input_area = Text(self.win, height=10)
        self.input_area.config(font=("Helvetica", 14))
        self.input_area.pack(padx=(80, 20), pady=5)

        self.send_btn = Button(self.win, text="Add note",
                               command=self.write)
        self.send_btn.config(font=("Helvetica", 14))
        self.send_btn.pack(padx=20, pady=5)

    def write(self):
        while self.running:
            self.note_topic = f"{self.topic_area.get('1.0', 'end').strip()}"
            self.note = f"{self.input_area.get('1.0', 'end').strip()}"
            self.user_note = str(
                ["NOTE", self.user_info[1], self.note_topic, self.note, self.countID])
            self.client.send(self.user_note.encode(FORMAT))
            response = self.client.recv(2048).decode(FORMAT)
            if response == "Note successfully created!":
                if self.gui_done:
                    self.tree.insert(
                        '', 'end', values=(self.countID, "Text", f"[Topic: {self.note_topic}] : {self.note if len(self.note) < 20 else self.note[0:20:1] + '...'}"))
                    self.countID += 1
                    self.input_area.delete('1.0', 'end')
                    messagebox.showinfo(None, response)
                    self.win.destroy()
                    break
            elif response == "This title is already exist":
                messagebox.showwarning(
                    title="Warning!", message="This title is already exist")
                break
            else:
                messagebox.showwarning(
                    title="Warning!", message="You must enter a note!")
                break

    def delete(self):
        try:
            self.task_index = self.tree.selection()[0]
            self.id = self.tree.item(self.task_index)['values'][0]
            self.type = self.tree.item(self.task_index)['values'][1]
            self.client.send(
                str(["DEL-NOTE", self.user_info[1], self.id, self.type]).encode(FORMAT))
            self.tree.delete(self.task_index)
        except:
            messagebox.showwarning(
                title="Warning!", message="You must select a note!")

    def upload_image(self):
        img_path = askopenfilename(title='Select Image',
                                   filetypes=[("image", ".jpeg"),
                                              ("image", ".png"),
                                              ("image", ".jpg")])
        if img_path == "":
            return
        img = img_path.split('/')
        self.image = img[len(img) - 1]
        while self.running:
            self.user_image = str(
                ["IMAGE", self.user_info[1], self.image, self.countID])
            self.client.send(self.user_image.encode(FORMAT))
            response = self.client.recv(2048).decode(FORMAT)
            if response == "Image successfully created!":
                with open(img_path, 'rb') as f:
                    self.client.send(f.read())
                    f.close()
                if self.gui_done:
                    self.tree.insert('', 'end', values=(
                        self.countID, "Image", f"[Name]: {self.image}"))
                    self.countID += 1
                    messagebox.showinfo(None, response)
                    break
            elif response == "This title is already exist":
                messagebox.showwarning(
                    title="Warning!", message="This title is already exist")
                break
            else:
                messagebox.showwarning(
                    title="Warning!", message="You must enter a image!")
                break

    def view(self):
        try:
            self.task_index = self.tree.selection()[0]
            self.id = self.tree.item(self.task_index)['values'][0]
            self.type = self.tree.item(self.task_index)['values'][1]
            self.namefile = self.tree.item(self.task_index)['values'][2]
            self.namefile = self.namefile[8:]
            self.client.send(
                str(["VIEW", self.user_info[1], self.id, self.type]).encode(FORMAT))
            if self.type == "Image":
                data = self.client.recv(4100000)
                img = io.BytesIO(data)
                image = Image.open(img)
                image.show()
            elif self.type == "Text":
                data = self.client.recv(4100000)
                data = eval(data)
                Topic = data[0]
                Content = data[1]
                self.win = Toplevel()
                window_width = 500
                window_height = 300
                screen_width = self.win.winfo_screenwidth()
                screen_height = self.win.winfo_screenheight()
                position_top = int(screen_height / 4 - window_height / 4)
                position_right = int(screen_width / 2 - window_width / 2)
                self.win.geometry(
                    f'{window_width}x{window_height}+{position_right}+{position_top}')
                self.win.title('Text')
                self.win.configure(background='white')
                self.win.resizable(0, 0)

                self.topic_label = Label(self.win, text='Topic:', font=(
                    'Helvetica', 12, 'bold'), fg='black', bg='white')
                self.topic_label.place(x=0, y=0)
                self.topic_area = Label(self.win, text=Topic, font=(
                    'Helvetica', 12, 'bold'), fg='black', bg='white')
                self.topic_area.place(x=80, y=0)

                self.input_label = Label(self.win, text='NOTES:', font=(
                    'Helvetica', 12, 'bold'), fg='black', bg='white')
                self.input_label.place(x=0, y=50)

                self.text_area = scrolledtext.ScrolledText(
                    self.win, width=42, height=12, font=("Helvetica", 12))
                # self.text_area.grid(column=0, pady=10, padx=10)
                self.text_area.place(x=80, y=50)
                self.text_area.insert(INSERT, Content)
                self.text_area.config(state=DISABLED)
        except:
            messagebox.showwarning(
                title="Warning!", message="You must select a note!")

    def download(self):
        file_path = askdirectory(title="Select Folder")
        if file_path == "":
            messagebox.showwarning(
                title="Warning!", message="You must enter a file!")
            return
        try:
            self.task_index = self.tree.selection()[0]
            self.id = self.tree.item(self.task_index)['values'][0]
            self.type = self.tree.item(self.task_index)['values'][1]
            self.client.send(
                str(["DOWNLOAD", self.user_info[1], self.id, self.type]).encode(FORMAT))
            if self.type == "Text":
                data = self.client.recv(41000000).decode(FORMAT)
                data = eval(data)
                print(data)
                Topic = data[0]
                Content = data[1]
                with open(f'{file_path}/{Topic}.txt', 'w') as f:
                    f.write(Content)
                f.close()
            else:
                self.namefile = self.tree.item(self.task_index)['values'][2]
                self.namefile = self.namefile.split('[Name]: ')
                self.namefile = self.namefile[len(self.namefile) - 1]
                with open(f"{file_path}/{self.namefile}", 'wb') as f:
                    data = self.client.recv(41000000)
                    f.write(data)
                    f.close()
        except:
            messagebox.showwarning(
                title="Warning!", message="You must enter a file!")

    def add_file(self):
        file_path = askopenfilename(title='Select File',
                                    filetypes=[('text files', '*.txt'),
                                               ('All files', '*.*')]
                                    )
        if file_path == "":
            return
        self.file = file_path.split('/')
        self.file = self.file[len(self.file) - 1]
        while self.running:
            self.user_file = str(
                ["FILE", self.user_info[1], self.file, self.countID])
            self.client.send(self.user_file.encode(FORMAT))
            response = self.client.recv(2048).decode(FORMAT)
            if response == "File successfully created!":
                with open(file_path, 'rb') as f:
                    self.client.send(f.read())
                    f.close()
                if self.gui_done:
                    self.tree.insert('', 'end', values=(
                        self.countID, "File", f"[Name]: {self.file}"))
                    self.countID += 1
                    messagebox.showinfo(None, response)
                    break
            elif response == "This title is already exist":
                messagebox.showwarning(
                    title="Warning!", message="This title is already exist")
                break
            else:
                messagebox.showwarning(
                    title="Warning!", message="You must enter a file!")
                break

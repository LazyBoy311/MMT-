from tkinter import *
from tkinter import messagebox
import pickle


class AddText:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        # Create GUI
        self.frame_tasks = Frame(root)
        self.frame_tasks.pack()

        self.listbox_tasks = Listbox(
            self.frame_tasks, height=10, width=50)
        self.listbox_tasks.pack(side=LEFT)

        self.scrollbar_tasks = Scrollbar(self.frame_tasks)
        self.scrollbar_tasks.pack(side=RIGHT, fill=Y)

        self.listbox_tasks.config(yscrollcommand=self.scrollbar_tasks.set)
        self.scrollbar_tasks.config(command=self.listbox_tasks.yview)

        self.entry_task = Entry(root, width=50)
        self.entry_task.pack()

        self.button_add_task = Button(
            root, text="Add task", width=48, command=self.add_task)
        self.button_add_task.pack()

        self.button_delete_task = Button(
            root, text="Delete task", width=48, command=self.delete_task)
        self.button_delete_task.pack()

        self.button_load_tasks = Button(
            root, text="Load tasks", width=48, command=self.load_tasks)
        self.button_load_tasks.pack()

        self.button_save_tasks = Button(
            root, text="Save tasks", width=48, command=self.save_tasks)
        self.button_save_tasks.pack()

    def add_task(self):
        self.task = self.entry_task.get()
        if self.task != "":
            self.listbox_tasks.insert(END, self.task)
            self.entry_task.delete(0, END)
        else:
            messagebox.showwarning(
                title="Warning!", message="You must enter a task.")

    def delete_task(self):
        try:
            self.task_index = self.listbox_tasks.curselection()[0]
            self.listbox_tasks.delete(self.task_index)
        except:
            messagebox.showwarning(
                title="Warning!", message="You must select a task.")

    def load_tasks(self):
        try:
            self.tasks = pickle.load(open("tasks.dat", "rb"))
            self.listbox_tasks.delete(0, END)
            for task in self.tasks:
                self.listbox_tasks.insert(END, task)
        except:
            messagebox.showwarning(
                title="Warning!", message="Cannot find tasks.dat.")

    def save_tasks(self):
        self.tasks = self.listbox_tasks.get(0, self.listbox_tasks.size())
        pickle.dump(self.tasks, open("tasks.dat", "wb"))


def page():
    root = Tk()
    AddText(root)
    root.mainloop()


if __name__ == '__main__':
    page()

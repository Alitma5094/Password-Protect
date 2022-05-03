import tkinter as tk
from tkinter import ttk, filedialog, Button, Label
from database import load_data, save_data
from crypt import decrypt_data, load_key, encrypt_data
import ast
import json

global data
global key

root = tk.Tk()
root.title("Password Protect")
root.tabs = ttk.Notebook(root)
root.geometry("600x500")

def get_old_data():
    root.filename = filedialog.askopenfilename(
        initialdir="/",
        title="Select file",
    )
    key = load_key(root.filename)
    loaded_data = bytes(load_data(), "ascii")
    decrypted_data = decrypt_data(loaded_data, key)
    new = decrypted_data.decode("ascii")
    data = ast.literal_eval(new)
    for i in data:
        add_tab(i, data[i]["Username"] + " " + data[i]["Password"])
    return


class MyDialog:
    def __init__(self, parent):
        top = self.top = tk.Toplevel(parent)
        self.myLabel = tk.Label(top, text="Enter your information below")
        self.myLabel.grid(row=0, column=0, columnspan=2)
        top.title("New Information")
        top.geometry("200x150")

        self.website = tk.Entry(top)
        self.website.grid(row=1, column=1)
        self.username = tk.Entry(top)
        self.username.grid(row=2, column=1)
        self.password = tk.Entry(top)
        self.password.grid(row=3, column=1)
        self.website_label = Label(top, text="Website: ")
        self.website_label.grid(row=1, column=0)
        self.username_label = Label(top, text="Username: ")
        self.username_label.grid(row=2, column=0)
        self.password_label = Label(top, text="Password: ")
        self.password_label.grid(row=3, column=0)

        self.mySubmitButton = tk.Button(top, text="Submit", command=self.send)
        self.mySubmitButton.grid(row=4, column=0, columnspan=2)

    def send(self):
        website = self.website.get()
        username = self.username.get()
        password = self.password.get()
        self.top.destroy()
        data[website] = {"Username": username, "Password": password}
        add_tab(website, username + " " + password)


def onclick():
    inputdialog = MyDialog(root)
    root.wait_window(inputdialog.top)


def add_tab(title, text):
    frame = ttk.Frame(root.tabs)
    root.tabs.add(frame, text=title)
    label = ttk.Label(frame, text=text)
    label.grid(column=1, row=1)
    root.tabs.grid(row=0, column=1)


def write_data():
    encrypted_data = encrypt_data(json.dumps(data), key)
    save_data(encrypted_data)


def start_gui():
    load_button = Button(root, text="Load Key", command=get_old_data)
    new_button = Button(root, text="New entry", command=onclick)
    save_button = Button(root, text="Save", command=write_data)
    quit_button = Button(root, text="Quit", command=root.quit)

    load_button.grid(row=0, column=0)
    new_button.grid(row=1, column=0)
    save_button.grid(row=2, column=0)
    quit_button.grid(row=3, column=0)

    root.mainloop()

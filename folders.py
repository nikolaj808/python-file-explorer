from tkinter import *
import os
import sys
from functools import partial
from tkinter import messagebox

def startd():
	cwd = os.getcwd()
	slashes = 0
	for i in range(len(cwd)):
		if cwd[i] == "/":
			slashes = slashes + 1
		if slashes == 4:
			return cwd[:i+1]

SIZE = 50
pwd = startd()
btns = {}

def open_file(file_folder):
	result = messagebox.askquestion(find_current(file_folder), "Want to open this file?")
	if result == "yes":
		os.system("subl " + file_folder)

def find_current(folder):
	stuff = folder
	i = -2

	while stuff[i] != "/":
		i = i - 1
	return str(stuff[i+1:-1])

def find_previous():
	global pwd
	stuff = pwd
	i = -2

	while stuff[i] != "/":
		i = i - 1
	return str(stuff[:i+1])

def folder_created():
	global lc, ec, bc, pwd
	folder_found = False
	lc.pack_forget()
	result = str(ec.get())
	ec.delete(0, END)
	result = result.replace(" ", "_")
	entries = os.listdir(pwd)
	if result == "":
		messagebox.showerror("Error", "You have to enter a folder name")
	else:
		for entry in entries:
			if entry == result:
				folder_found = True
				messagebox.showerror("Error", "Folder already exists")
				break
	if not folder_found:
		os.system("mkdir " + pwd + result)
	ec.pack_forget()
	bc.pack_forget()
	list_folders(pwd)

def create_folder():
	global lc, ec, bc, lr, er, br
	btns["Create"].pack_forget()
	btns["Remove"].pack_forget()
	lr.pack_forget()
	er.pack_forget()
	br.pack_forget()
	er.delete(0, END)
	lc.pack(side="top", fill="x")
	ec.pack(side="top", fill="x")
	bc.pack(side="top", fill="x")

def folder_removed():
	global lr, er, br, pwd
	folder_found = False
	lr.pack_forget()
	result = str(er.get())
	er.delete(0, END)
	result = result.replace(" ", "_")
	entries = os.listdir(pwd)
	for entry in entries:
		if entry == result:
			os.system("rmdir " + pwd + result + "/")
			folder_found = True
			break
	if not folder_found:
		messagebox.showerror("Error", "Folder not found")
	er.pack_forget()
	br.pack_forget()
	list_folders(pwd)

def remove_folder():
	global lr, er, br, lc, ec, bc
	btns["Remove"].pack_forget()
	btns["Create"].pack_forget()
	lc.pack_forget()
	ec.pack_forget()
	bc.pack_forget()
	ec.delete(0, END)
	lr.pack(side="top", fill="x")
	er.pack(side="top", fill="x")
	br.pack(side="top", fill="x")

def list_folders(folder):
	global pwd, entries, btns
	pwd = folder
	for stuff in btns:
		btns[stuff].pack_forget()
	entries = os.listdir(pwd)
	for entry in entries:
		if os.path.isdir(pwd + entry + "/"):
			btns[entry] = Button(root, text=entry, bg="black", fg="white", relief="ridge", highlightthickness=0, bd=0, command=partial(list_folders, pwd + entry + "/"))
			btns[entry].pack(side="top", fill="both")
	for entry in entries:
		if not os.path.isdir(pwd + entry + "/"):
			btns[entry] = Button(root, text=entry, bg="green", fg="white", relief="ridge", highlightthickness=0, bd=0, command=partial(open_file, pwd + entry + "/"))
			btns[entry].pack(side="top", fill="x")
	previous = find_previous()
	btns["Back"] = Button(root, text="Back", relief="ridge", highlightthickness=0, bd=0, command=partial(list_folders, previous))
	btns["Back"].pack(side="top", fill="x")
	btns["Create"] = Button(root, text="Create folder", bg="orange", fg="white", relief="ridge", highlightthickness=0, bd=0, command=create_folder)
	btns["Create"].pack(side="top", fill="x")
	btns["Remove"] = Button(root, text="Remove folder", bg="red", fg="white", relief="ridge", highlightthickness=0, bd=0, command=remove_folder)
	btns["Remove"].pack(side="top", fill="x")

root = Tk()
root.configure(background="black")

lc = Label(root, text="New folder name")
ec = Entry(root)
bc = Button(root, text="Create", bg="orange", fg="white", relief="ridge", highlightthickness=0, bd=0, command=folder_created)

lr = Label(root, text="Remove folder name")
er = Entry(root)
br = Button(root, text="Remove", bg="red", fg="white", relief="ridge", highlightthickness=0, bd=0, command=folder_removed)

list_folders(pwd)

root.mainloop()
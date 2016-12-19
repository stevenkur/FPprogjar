from Tkinter import *
root = Tk()
root.title("GUI FTP Client")
def leftClick(event):
	print("left")
def connect():
	print("leftsss")
def exit():
	root.quit()



toolbar = Frame(root, bg="blue")
host = StringVar()
label = Label( toolbar, textvariable=host , bg="blue")
host.set("Host: ")
label.pack(side=LEFT, padx=2, pady=2)
T = Text(toolbar, height=1, width=20)
T.pack(side=LEFT,padx=2, pady=2)

username= StringVar()
label = Label( toolbar, textvariable=username , bg="blue")
username.set("Username: ")
label.pack(side=LEFT, padx=2, pady=2)
T = Text(toolbar, height=1, width=20)
T.pack(side=LEFT,padx=2, pady=2)

password= StringVar()
label = Label( toolbar, textvariable=password , bg="blue")
password.set("Password: ")
label.pack(side=LEFT, padx=2, pady=2)
T = Text(toolbar, height=1, width=20)
T.pack(side=LEFT,padx=2, pady=2)

port= StringVar()
label = Label( toolbar, textvariable=port , bg="blue")
port.set("Port: ")
label.pack(side=LEFT, padx=2, pady=2)
T = Text(toolbar, height=1, width=20)
T.pack(side=LEFT,padx=2, pady=2)

insertButt = Button(toolbar, text="Connect", command=connect)
insertButt.pack(side=LEFT, padx=2, pady=2)
printButt = Button(toolbar, text="Exit", command=exit)
printButt.pack(side=LEFT, padx=2, pady=2)
toolbar.pack(side=TOP, fill=X)

T = Text(root, height=40, width=20)
T.pack(side=TOP,padx=2, pady=2, fill=BOTH)

status = Label(root, text="Preparing", bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)
frame = Frame(root, width=400, height=100)
frame.bind("<Button-1>", leftClick)
frame.pack()
root.mainloop()

from Tkinter import *
root = Tk()
root.title("GUI FTP Server")
def leftClick(event):
	print("left")
def connect():
	print("connect")
def exit():
	root.quit()
def disconnect():
	print("disconnect")


toolbar = Frame(root, bg="blue")
host = StringVar()
label = Label( toolbar, textvariable=host , bg="blue")
host.set("Host: ")
label.pack(side=LEFT, padx=2, pady=2)
T = Text(toolbar, height=1, width=20)
T.pack(side=LEFT,padx=2, pady=2)



port= StringVar()
label = Label( toolbar, textvariable=port , bg="blue")
port.set("Port: ")
label.pack(side=LEFT, padx=2, pady=2)
T = Text(toolbar, height=1, width=20)
T.pack(side=LEFT,padx=2, pady=2)

insertButt = Button(toolbar, text="Start", command=connect)
insertButt.pack(side=LEFT, padx=2, pady=2)
insertButt2 = Button(toolbar, text="Stop", command=disconnect)
insertButt2.pack(side=LEFT, padx=2, pady=2)
printButt = Button(toolbar, text="Exit", command=exit)
printButt.pack(side=RIGHT, padx=2, pady=2)
toolbar.pack(side=TOP, fill=X)

T = Text(root, height=40, width=20)
T.pack(side=TOP,padx=2, pady=2, fill=BOTH)

frame = Frame(root, width=400, height=100)
frame.bind("<Button-1>", leftClick)
frame.pack()
root.mainloop()

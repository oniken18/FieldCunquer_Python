
import tkinter as tk
from GameBoard1 import GameBoard


class Main:

    def __init__(self):

        def StartGame(event):
            self.canvas.destroy()
            app = GameBoard(self.root)

        self.root = tk.Tk()
        self.root.title = 'Login'
        self.canvas = tk.Canvas(self.root, width=500, height=450)
        self.canvas.pack()

        self.frame = tk.Frame(self.root, width=496, height=446)
        self.frame.place(width=496, height=446, x=4, y=4)

        self.butStart = tk.Button(self.frame, text='Start')
        self.butStart.bind("<Button-1>", StartGame)


        self.butStart.place(width=80, x=208, y=190)

        self.root.mainloop()


Game = Main()
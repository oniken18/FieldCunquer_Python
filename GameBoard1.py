import os
import threading
import tkinter as tk

from PIL import Image, ImageTk

from Enemy import Enemy
from Player import Player
from Shape import Shape


class GameBoard:
    AllPoints = []
    LinesPropertiesX = []
    LinesPropertiesY = []
    images = []
    frmLives = []
    Lives = 5
    ShapeArea = 0
    Lvl = 0

    def __init__(self, root):
        canvasWidth = 610
        canvasHeight = 646

        def setSpaceClick(event):
            self.Plr.isSpacePressed = True

        def MovePlayerThread(event):
            if self.Lives == 0:
                return

            if event.char in ('4', '5', '6', '8'):
                if event.char == self.Plr.MovingDirection:
                    return
                else:
                    if self.Plr.MovingDirection != '0':
                        self.Plr.MovingDirection = event.char
                        return

                self.Plr.MovingDirection = event.char
                thread1 = threading.Thread(target=self.Plr.MovePlayer)
                thread1.start()

        def stopMovement(event):
            if self.Plr.MovingDirection == event.char and not self.Plr.isOutLine:
                self.Plr.MovingDirection = '0'

            if event.keycode == 32:
                self.Plr.isSpacePressed = False

        self.root = root

        self.canvas = tk.Canvas(self.root, width=canvasWidth, height=canvasHeight)
        self.canvas.bind("<Key>", MovePlayerThread)
        self.canvas.bind("<KeyRelease>", stopMovement)
        self.canvas.bind("<space>", setSpaceClick)
        self.canvas.pack()

        THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
        img = Image.open(os.path.join(THIS_FOLDER, r'Graphics\pic0.gif'))

        img = img.resize((646, 610), Image.ANTIALIAS)
        self.images.append(ImageTk.PhotoImage(img))

        img = Image.open(os.path.join(THIS_FOLDER, r'Graphics\pic1.gif'))
        img = img.resize((646, 610), Image.ANTIALIAS)
        self.images.append(ImageTk.PhotoImage(img))

        self.image_id = self.canvas.create_image(self.images[0].width() / 2, self.images[0].height() / 2,
                                                 image=self.images[0])

        self.LinesPropertiesY.append(('y', 6, 6, 608, False))
        self.LinesPropertiesY.append(('y', 608, 6, 608, False))
        self.LinesPropertiesX.append(('x', 6, 6, 608, False))
        self.LinesPropertiesX.append(('x', 608, 6, 608, False))

        self.AllPoints = [(6, 6, True), (608, 6, True), (608, 608, True), (6, 608, True)]

        MainLn = self.canvas.create_polygon(6, 6, 608, 6, 608, 608, 6, 608, 6, 6, fill='grey', width=1)
        self.Shp = Shape(MainLn, self)

        frmPlayer = tk.Frame(self.canvas, bg='#FF0000')
        self.Plr = Player(frmPlayer, self)

        frmEnemy = tk.Frame(self.canvas, bg='#00FF00')
        self.Enm = Enemy(frmEnemy, self)

        self.frmBottom = tk.Canvas(self.canvas, bg='#FFFFFF')
        self.frmBottom.place(x=6, y=614, height=30, width=602)

        for i in range(5):
            self.frmLives.append(self.frmBottom.create_oval(90 + (i * 30), 5, 110 + (i * 30), 25, fill='blue'))

        lblLives = tk.Label(self.frmBottom, font=("Courier", 18), text="Lives", bg='#FFFFFF', fg='#000000')
        lblLives.place(x=6, y=0)

        self.canvas.focus_set()
        self.root.mainloop()

    def NextLevel(self):
        self.Enm.stopMovement = True
        self.Lvl = self.Lvl + 1
        self.canvas.itemconfig(self.image_id, image=self.images[1])

        self.LinesPropertiesY.clear()
        self.LinesPropertiesX.clear()
        self.LinesPropertiesY.append(('y', 6, 6, 608, False))
        self.LinesPropertiesY.append(('y', 608, 6, 608, False))
        self.LinesPropertiesX.append(('x', 6, 6, 608, False))
        self.LinesPropertiesX.append(('x', 608, 6, 608, False))
        self.AllPoints.clear()
        self.AllPoints = [(6, 6, True), (608, 6, True), (608, 608, True), (6, 608, True)]

        self.canvas.delete(self.Shp.MainLn)
        del self.Shp

        MainLn = self.canvas.create_polygon(6, 6, 608, 6, 608, 608, 6, 608, 6, 6, fill='grey', width=1)
        self.Shp = Shape(MainLn, self)

        self.Plr.Player.pack_forget()
        self.Plr.Player.destroy()

        frmPlayer = tk.Frame(self.canvas, bg='#FF0000')
        self.Plr = Player(frmPlayer, self.AllPoints, self)

        self.Enm.EnemyV.pack_forget()
        self.Enm.EnemyV.destroy()

        frmEnemy = tk.Frame(self.canvas, bg='#00FF00')
        self.Enm = Enemy(frmEnemy, self)

    def removeLive(self):
        self.Lives = self.Lives - 1
        self.frmBottom.itemconfigure(self.frmLives[self.Lives], state='hidden')

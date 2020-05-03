import ast
import json as json
import threading
import tkinter as tk
from tkinter import messagebox
from typing import Type

import requests
from Enemy import Enemy
from PIL import Image, ImageTk
from Player import Player
from Shape import Shape


class GameBoard:
    AllPoints = []
    AllowedFrames = []
    isOutLine = False
    LinesProperties = []

    def __init__(self, root):

        canvasWidth = 610
        canvasHeight = 610

        def setSpaceClick(event):
            self.P.isSpacePressed = True

        def MovePlayerThread(event):
            if event.char in ('4', '5', '6', '8'):
                if event.char == self.P.MovingDirection:
                    return
                else:
                    if self.P.MovingDirection != '0':
                        self.P.MovingDirection = event.char
                        return

                self.P.MovingDirection = event.char
                thread1 = threading.Thread(target=self.P.MovePlayer)
                thread1.start()

        def stopMovement(event):
            if self.P.MovingDirection == event.char and not self.P.isOutLine:
                self.P.MovingDirection = '0'

            if event.keycode == 32:
                self.P.isSpacePressed = False

        self.root = root
        self.root.title = 'Submarine War'

        self.canvas = tk.Canvas(self.root, width=canvasWidth, height=canvasHeight)
        self.canvas.bind("<Key>", MovePlayerThread)
        self.canvas.bind("<KeyRelease>", stopMovement)
        self.canvas.bind("<space>", setSpaceClick)
        self.canvas.pack()

        filename = 'PIC.JPG'
        img = tk.PhotoImage(file=r"Graphics/picpic.gif")
        self.canvas.create_image(img.width()/2, img.height()/2, image=img)

        MainLn = self.canvas.create_polygon(6, 6, 608, 6, 608, 608, 6, 608, 6, 6, fill='grey', width=1)

        self.LinesProperties.append(('y', 6, 6, 608))
        self.LinesProperties.append(('y', 608, 6, 608))
        self.LinesProperties.append(('x', 6, 6, 608))
        self.LinesProperties.append(('x', 608, 6, 608))

        self.Shape = Shape(MainLn, self.LinesProperties, self.canvas)

        p = (6, 6)
        self.AllPoints.append(p)
        p = (6, 608)
        self.AllPoints.append(p)
        p = (608, 608)
        self.AllPoints.append(p)
        p = (608, 6)
        self.AllPoints.append(p)

        frmPlayer = tk.Frame(self.canvas, bg='#FF0000')
        self.P = Player(frmPlayer, self.LinesProperties, self.AllPoints, self.canvas, self.Shape)

        frmEnemy = tk.Frame(self.canvas, bg='#00FF00')
        self.E = Enemy(frmEnemy, self.LinesProperties, self.canvas)

        self.Shape.setEnemy(self.E)

        self.AllPoints = [(6, 6), (608, 6), (608, 608), (6, 608)]

        self.canvas.focus_set()
        self.root.mainloop()

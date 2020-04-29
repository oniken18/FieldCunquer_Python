import ast
import json as json
import threading
import tkinter as tk
from tkinter import messagebox
from typing import Type
import requests
from PIL import Image, ImageTk
from Pixel import Pixel


class GameBoard:
    AllPoints =[]
    PlayerCenter = ()
    size = 25, 25
    PosX = 3
    PosY = 3
    MovingDirection = '0'
    isSpacePressed = False
    AllowedFrames = []
    isOutLine = False
    LinesProperties = []
    FullShapeLines = ()
    localMaxMove = 608
    localMinMove = 3

    def MakeNewShape(self):
        stop = False
        newShape = []
        currP = (700, 700)
        tempPoints = list(self.AllPoints)

        for p in tempPoints:
            if p[0] <= currP[0]:
                if p[1] < currP[1]:
                    currP = p

        newShape.append(currP)
        tempPoints.remove(currP)

        while len(tempPoints) > 0 and not stop:
            currP = (700, currP[1])
            isFound = False
            for p in tempPoints:
                if p[1] == currP[1]:
                    if p[0] < currP[0]:
                        isFound = True
                        currP = p

            if not isFound:
                currP = (0, currP[1])
                for p in tempPoints:
                    if p[1] == currP[1]:
                        if p[0] > currP[0]:
                            currP = p

            if isFound:
                newShape.append(currP)
                tempPoints.remove(currP)

            currP = (currP[0], 700)
            isFound = False
            if len(tempPoints)>0:
                for p in tempPoints:
                    if p[0] == currP[0]:
                        if p[1] < currP[1]:
                            isFound = True
                            currP = p

                if not isFound:
                    currP = (currP[0], 0)
                    for p in tempPoints:
                        if p[0] == currP[0]:
                            if p[1] > currP[1]:
                                currP = p

                if isFound:
                    newShape.append(currP)
                    tempPoints.remove(currP)
                    
        return newShape

    def getStopPointX(self, direction, startX, Y):
        if direction == '4':
            result = 0
            for ln in self.LinesProperties:
                if ln[0] == 'y':
                    if result < ln[1] < startX and (ln[2] < Y < ln[3] or ln[3] < Y < ln[2]):
                        result = ln[1] - 3
            return result

        elif direction == '6':
            result = 700
            for ln in self.LinesProperties:
                if ln[0] == 'y':
                    if result > ln[1] > startX and (ln[2] < Y < ln[3] or ln[3] < Y < ln[2]):
                        result = ln[1] - 3
            return result

    def getStopPointY(self, direction, startY, X):
        if direction == '8':
            result = 0
            for ln in self.LinesProperties:
                if ln[0] == 'x':
                    if result < ln[1] < startY and (ln[2] < X < ln[3] or ln[3] < X < ln[2]):
                        result = ln[1] - 3
            return result

        elif direction == '5':
            result = 700
            for ln in self.LinesProperties:
                if ln[0] == 'x':
                    if result > ln[1] > startY and (ln[2] < X < ln[3] or ln[3] < X < ln[2]):
                        result = ln[1] - 3
            return result

    def setLineProperties(self, OrgDirection, startP, finishP):

        if OrgDirection == '4':
            self.LinesProperties.append(('x', startP[1], finishP[0], startP[0]))
        elif OrgDirection == '6':
            self.LinesProperties.append(('x', startP[1], startP[0], finishP[0]))
        elif OrgDirection == '8':
            self.LinesProperties.append(('y', startP[0], finishP[1], startP[1]))
        elif OrgDirection == '5':
            self.LinesProperties.append(('y', startP[0], startP[1], finishP[1]))

    def isMoveOnLine(self, Direction, currX, currY):
        currX = currX + 3
        currY = currY + 3
        
        if Direction == '4':
            for ln in self.LinesProperties:
                if ln[0] == 'x':
                    if ln[1] == currY and ln[2] < currX:
                        return ln[2] - 3
            return 0

        if Direction == '6':
            for ln in self.LinesProperties:
                if ln[0] == 'x':
                    if ln[1] == currY and ln[3] > currX:
                        return ln[3]
            return 0

        if Direction == '8':
            for ln in self.LinesProperties:
                if ln[0] == 'y':
                    if ln[1] == currX and ln[2] < currY:
                        return ln[2] -3
            return 0

        if Direction == '5':
            for ln in self.LinesProperties:
                if ln[0] == 'y':
                    if ln[1] == currX and ln[3] > currY:
                        return ln[3]
            return 0

    def isEscapingLine(self, Direction):
        if Direction == '4':
            if self.localMinMove < self.PosX - 0.01 < self.localMaxMove:
                return True
        elif Direction == '6':
            if self.localMinMove < self.PosX + 3 + 0.01 < self.localMaxMove:
                return True
        elif Direction == '8':
            if self.localMinMove < self.PosY - 0.01 < self.localMaxMove:
                return True
        elif Direction == '5':
            if self.localMinMove < self.PosY + 3 + 0.01 < self.localMaxMove:
                return True
        return False

    def MovePlayer(self):
        tkLines = []
        tkFrames = []
        originalDirection = '0'
        localSize = 3
        startPoint = ()
        finishPoint = ()
        StopPoint = 0
        self.isOutLine = False
        isFirstLine = True

        while self.MovingDirection != '0':

            tempMovingTo = self.MovingDirection

            if self.isSpacePressed and not self.isOutLine:
                self.isOutLine = self.isEscapingLine(tempMovingTo)
                print(self.isOutLine)

            if originalDirection != tempMovingTo and not self.isOutLine:
                nextEnablePoint = -1

            if originalDirection != tempMovingTo and self.isOutLine:
                tkWidth = 2
                tkHeight = 2
                StopPoint = 0
                tkFrame = tk.Frame(self.canvas, width=tkWidth, height=tkHeight, bg='#FFFFFF')
                tkFrame.place(x=self.PosX + localSize, y=self.PosY + localSize)
                tkFrames.append(tkFrame)

                t1 = (self.PosX + localSize, self.PosY + localSize)
                tkLines.append(t1)
                self.AllPoints.append(t1)

                if isFirstLine:
                    isFirstLine = False
                    startPoint = (self.PosX + localSize, self.PosY + localSize)
                else:
                    finishPoint = (self.PosX + localSize, self.PosY + localSize)

                    self.setLineProperties(originalDirection, startPoint, finishPoint)

                    startPoint = finishPoint
                    finishPoint = tuple()

                originalDirection = tempMovingTo

            if tempMovingTo == '4':
                if not self.isOutLine:
                    if nextEnablePoint == -1:
                        nextEnablePoint = self.isMoveOnLine('4', self.PosX, self.PosY)
                else:
                    nextEnablePoint = -1

                if StopPoint == 0 and self.isOutLine:
                    StopPoint = self.getStopPointX('4', self.PosX + localSize, self.PosY + localSize)

                if (self.PosX <= nextEnablePoint and not self.isOutLine) or nextEnablePoint == 0 or (self.PosX <= StopPoint and self.isOutLine):
                    self.MovingDirection = '0'
                    break

                temp = round((self.PosX - 0.01) * 100)
                temp = int(temp)
                self.PosX = float(temp / 100)

                self.Player.place(x=self.PosX)

                if self.isOutLine:
                    tkWidth = tkWidth + 0.01
                    tkFrame.place(x=self.PosX + localSize, width=tkWidth)

            elif tempMovingTo == '6':

                if not self.isOutLine:
                    if nextEnablePoint == -1:
                        nextEnablePoint = self.isMoveOnLine('6', self.PosX, self.PosY)
                else:
                    nextEnablePoint = -1

                if StopPoint == 0 and self.isOutLine:
                    StopPoint = self.getStopPointX('6', self.PosX + localSize, self.PosY + localSize)

                if (self.PosX >= nextEnablePoint and not self.isOutLine) or nextEnablePoint == 0 or (self.PosX >= StopPoint and self.isOutLine):
                    self.MovingDirection = '0'
                    break

                temp = round((self.PosX + 0.01) * 100)
                temp = int(temp)
                self.PosX = float(temp / 100)

                self.Player.place(x=self.PosX)

                if self.isOutLine:
                    tkWidth = tkWidth + 0.01
                    tkFrame.place(width=tkWidth)

            elif tempMovingTo == '8':

                if not self.isOutLine:
                    if nextEnablePoint == -1:
                        nextEnablePoint = self.isMoveOnLine('8', self.PosX, self.PosY)
                else:
                    nextEnablePoint = -1

                if StopPoint == 0 and self.isOutLine:
                    StopPoint = self.getStopPointY('8', self.PosY + localSize, self.PosX + localSize)

                if (self.PosY <= nextEnablePoint and not self.isOutLine) or nextEnablePoint == 0 or (self.PosY <= StopPoint and self.isOutLine):
                    self.MovingDirection = '0'
                    break
                temp = round((self.PosY - 0.01) * 100)
                temp = int(temp)
                self.PosY = float(temp / 100)

                self.Player.place(y=self.PosY)

                if self.isOutLine:
                    tkHeight = tkHeight + 0.01
                    tkFrame.place(y=self.PosY + localSize, height=tkHeight)

            elif tempMovingTo == '5':
                if not self.isOutLine:
                    if nextEnablePoint == -1:
                        nextEnablePoint = self.isMoveOnLine('5', self.PosX, self.PosY)
                else:
                    nextEnablePoint = -1

                if StopPoint == 0 and self.isOutLine:
                    StopPoint = self.getStopPointY('5', self.PosY + localSize, self.PosX + localSize)

                if (self.PosY >= nextEnablePoint and not self.isOutLine) or nextEnablePoint == 0 or (self.PosY >= StopPoint and self.isOutLine):
                    self.MovingDirection = '0'
                    break

                temp = round((self.PosY + 0.01) * 100)
                temp = int(temp)
                self.PosY = float(temp / 100)

                self.Player.place(y=self.PosY)

                if self.isOutLine:
                    tkHeight = tkHeight + 0.01
                    tkFrame.place(height=tkHeight)

            finishPoint = (self.PosX + localSize, self.PosY + localSize)

        if len(finishPoint) > 0 and len(startPoint) > 0:

            self.setLineProperties(originalDirection, startPoint, finishPoint)

            startPoint = finishPoint
            finishPoint = tuple()

            t1 = (self.PosX + localSize, self.PosY + localSize)
            tkLines.append(t1)
            self.AllPoints.append(t1)

            for frm in tkFrames:
                frm.pack_forget()
                frm.destroy()

            if len(tkLines) > 1:
                shapePoints = ()
                for point in tkLines:
                    shapePoints = shapePoints + point

                shapePoints = shapePoints + tkLines[0]

                self.canvas.delete(self.MainLn)
                self.AllPoints = self.MakeNewShape()
                Shape = list(self.AllPoints)
                Shape.append(self.AllPoints[0])
                self.MainLn = self.canvas.create_line(Shape, fill='black', width=1)


    def __init__(self, root):

        canvasWidth = 615
        canvasHeight = 615

        def setSpaceClick(event):
            self.isSpacePressed = True

        def MovePlayerThread(event):
            if event.char in ('4', '5', '6', '8'):
                if event.char == self.MovingDirection:
                    return
                else:
                    if self.MovingDirection != '0':
                        self.MovingDirection = event.char
                        return

                self.MovingDirection = event.char
                thread1 = threading.Thread(target=self.MovePlayer)
                thread1.start()

        def stopMovement(event):

            if self.MovingDirection == event.char and not self.isOutLine:
                self.MovingDirection = '0'

            if event.keycode == 32:
                self.isSpacePressed = False

        self.root = root
        self.root.title = 'Submarine War'

        self.canvas = tk.Canvas(self.root, width=canvasWidth, height=canvasHeight)
        self.canvas.bind("<Key>", MovePlayerThread)
        self.canvas.bind("<KeyRelease>", stopMovement)
        self.canvas.bind("<space>", setSpaceClick)
        self.canvas.pack()

        self.MainLn = self.canvas.create_line(6, 6, 608, 6, 608, 608, 6, 608, 6, 6, fill='black', width=1)

        self.LinesProperties.append(('y', 6, 6, 608))
        self.LinesProperties.append(('y', 608, 6, 608))
        self.LinesProperties.append(('x', 6, 6, 608))
        self.LinesProperties.append(('x', 608, 6, 608))

        p = (6,6)
        self.AllPoints.append(p)
        p = (6, 608)
        self.AllPoints.append(p)
        p = (608, 608)
        self.AllPoints.append(p)
        p = (608, 6)
        self.AllPoints.append(p)

        self.canvas.delete(self.MainLn)
        self.AllPoints = self.MakeNewShape()
        Shape = list(self.AllPoints)
        Shape.append(self.AllPoints[0])
        self.MainLn = self.canvas.create_line(Shape, fill='black', width=1)

        self.Player = tk.Frame(self.canvas, bg='#FF0000')
        self.Player.place(width=8, height=8, x=3, y=3)

        self.canvas.focus_set()
        self.root.mainloop()


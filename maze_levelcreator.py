import tkinter as tk
import math
import os
from level import *
os.chdir(os.path.dirname(os.path.realpath(__file__)))

class Mescouilles():
    def __init__(self, size):
        self.size = size
        self.grid = [[self.border_test(i,j) for i in range(self.size)] for j in range(self.size)]

        self.root = tk.Tk()

        self.chsent = tk.Entry(self.root)
        self.chsbtn = tk.Button(self.root, text="Load file", command=lambda:self.loadfile(self.chsent.get()))
        self.canv = tk.Canvas(self.root, width=self.size*10+2, height=self.size*10+2)
        self.entry = tk.Entry(self.root)
        self.svbtn = tk.Button(self.root, text="Save level", command=self.save)

        self.canv.bind("<Button-1>", self.clicked)

        self.chsent.pack()
        self.chsbtn.pack()
        self.canv.pack()
        self.entry.pack()
        self.svbtn.pack()
        
        self.updtdisp()

        self.root.mainloop()

    def loadfile(self, c):
        self.size = len(globals()[c])
        self.canv.config(width=self.size*10+2, height=self.size*10+2)
        self.grid = globals()[c]
        self.updtdisp()
    
    def border_test(self,x,y):
        if x == 0 or y == 0:
            if y == 1:
                return 2
            else:
                return 1
        elif x == self.size - 1 or y == self.size - 1:
            if y == self.size-2:
                return 3
            else:
                return 1

        return 0

    def updtdisp(self):
        self.canv.delete("all")
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == 0:
                    self.canv.create_rectangle(j*10+2, i*10+2, j*10+12, i*10+12, fill='white')
                if self.grid[i][j] == 1:
                    self.canv.create_rectangle(j*10+2, i*10+2, j*10+12, i*10+12, fill='black')
                if self.grid[i][j] == 2:
                    self.canv.create_oval(j*10+3, i*10+3, j*10+11, i*10+11, fill='green', outline='green')
                if self.grid[i][j] == 3:
                    self.canv.create_rectangle(j*10+2, i*10+2, j*10+12, i*10+12, fill='grey', outline="green")
    
    def clicked(self,event):
        if self.grid[math.floor((event.y-2)/10)][math.floor((event.x-2)/10)] == 0:
            self.grid[math.floor((event.y-2)/10)][math.floor((event.x-2)/10)] = 1
        elif self.grid[math.floor((event.y-2)/10)][math.floor((event.x-2)/10)] == 1:
            self.grid[math.floor((event.y-2)/10)][math.floor((event.x-2)/10)] = 0
        self.updtdisp()

    def save(self):
        nb = self.entry.get()
        with open(f"level.py", mode="a") as f:
            f.write(f"\n\n{nb}={str(self.grid)}")
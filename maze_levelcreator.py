import tkinter as tk
from tkinter import messagebox
import math
import os
import level
from level import *
from maze import StartWindow
os.chdir(os.path.dirname(os.path.realpath(__file__)))

class LevelEditor():
    def __init__(self, size):
        self.size = size
        self.grid = [[self.border_test(i,j) for i in range(self.size)] for j in range(self.size)]

        self.root = tk.Tk()

        self.dropdownmenu_list = []
        self.levellist()
        self.dropdownmenu_variable = tk.StringVar(self.root)

        self.start_dropdownmenu = tk.OptionMenu(self.root, self.dropdownmenu_variable, *self.dropdownmenu_list)
        self.choose_button = tk.Button(self.root, text="Load file", command=lambda:self.loadfile(self.dropdownmenu_variable.get()))
        self.canvas = tk.Canvas(self.root, width=self.size*10+2, height=self.size*10+2)
        self.entry = tk.Entry(self.root)
        self.save_button = tk.Button(self.root, text="Save level", command=self.save)

        self.canvas.bind("<Button-1>", self.clicked)

        self.start_dropdownmenu.pack()
        self.choose_button.pack()
        self.canvas.pack()
        self.entry.pack()
        self.save_button.pack()
        
        self.updatedisplay()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def loadfile(self, c):
        self.size = len(globals()[c])
        self.canvas.config(width=self.size*10+2, height=self.size*10+2)
        self.grid = globals()[c]
        self.updatedisplay()

    def levellist(self):
        for element in dir(level):
            if str(element[0:2]) != "__" and str(element) != "test":
                self.dropdownmenu_list.append(element)
    
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

    def updatedisplay(self):
        self.canvas.delete("all")
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == 0:
                    self.canvas.create_rectangle(j*10+2, i*10+2, j*10+12, i*10+12, fill='white')
                if self.grid[i][j] == 1:
                    self.canvas.create_rectangle(j*10+2, i*10+2, j*10+12, i*10+12, fill='black')
                if self.grid[i][j] == 2:
                    self.canvas.create_oval(j*10+3, i*10+3, j*10+11, i*10+11, fill='green', outline='green')
                if self.grid[i][j] == 3:
                    self.canvas.create_rectangle(j*10+2, i*10+2, j*10+12, i*10+12, fill='grey', outline="green")
    
    def clicked(self,event):
        if self.grid[math.floor((event.y-2)/10)][math.floor((event.x-2)/10)] == 0:
            self.grid[math.floor((event.y-2)/10)][math.floor((event.x-2)/10)] = 1
        elif self.grid[math.floor((event.y-2)/10)][math.floor((event.x-2)/10)] == 1:
            self.grid[math.floor((event.y-2)/10)][math.floor((event.x-2)/10)] = 0
        self.updatedisplay()

    def save(self):
        nb = self.entry.get()
        with open(f"level.py", mode="a") as f:
            f.write(f"\n\n{nb}={str(self.grid)}")
        self.levellist()
        StartWindow.levellist(self)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Unsaved changes will be lost. Do you want to quit?"):
            self.root.destroy()
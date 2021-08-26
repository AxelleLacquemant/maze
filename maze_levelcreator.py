import tkinter as tk
from tkinter import messagebox
import math
import random
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

        self.canvas = tk.Canvas(self.root, width=self.size*10+2, height=self.size*10+2)
        self.start_dropdownmenu = tk.OptionMenu(self.root, self.dropdownmenu_variable, *self.dropdownmenu_list)
        self.choose_button = tk.Button(self.root, text="Load file", command=lambda:self.loadfile(self.dropdownmenu_variable.get()), width=17)
        self.random_button = tk.Button(self.root, text="Randomize", command=self.randomize, width=17)
        self.entry = tk.Entry(self.root)
        self.save_button = tk.Button(self.root, text="Save level", command=self.save, width=17)

        self.start_dropdownmenu.config(width=14)

        self.canvas.bind("<Button-1>", self.clicked)

        self.canvas.grid(row=0, column=0, columnspan=3)
        self.start_dropdownmenu.grid(row=1, column=0)
        self.choose_button.grid(row=2, column=0)
        self.random_button.grid(row=2, column=1)
        self.entry.grid(row=1, column=2)
        self.save_button.grid(row=2, column=2)

        self.updatebuttons()
        self.updatedisplay()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def updatebuttons(self):
        uptelements = [self.start_dropdownmenu, self.choose_button, self.random_button, self.save_button]
        for element in uptelements:
            element.config(bg='grey14', foreground='grey98')

        self.root.config(bg='grey98')

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

    def levellist(self):
        for element in dir(level):
            if str(element[0:2]) != "__" and str(element) != "test":
                self.dropdownmenu_list.append(element)

    def loadfile(self, c):
        self.size = len(globals()[c])
        self.canvas.config(width=self.size*10+2, height=self.size*10+2)
        self.grid = globals()[c]
        self.updatedisplay()

    def randomize(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if i != 0 and j != 0 and i != self.size-1 and j != self.size-1:
                    self.grid[i][j] = random.randint(0,1)

        self.updatedisplay()
    
    def clicked(self,event):
        if self.grid[math.floor((event.y-2)/10)][math.floor((event.x-2)/10)] == 0:
            self.grid[math.floor((event.y-2)/10)][math.floor((event.x-2)/10)] = 1
        elif self.grid[math.floor((event.y-2)/10)][math.floor((event.x-2)/10)] == 1:
            self.grid[math.floor((event.y-2)/10)][math.floor((event.x-2)/10)] = 0
        self.updatedisplay()

    def namecheck(self, checkedvar):
        possible = ("a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","x","y","z","0","1","2","3","4","5","6","7","8","9","_","-")
        forbiddenfirst = ("0","1","2","3","4","5","6","7","8","9","-")

        if checkedvar == "":
            checkedvar = "unamed_custom_level"
        testlist = list(checkedvar)

        for i in range(len(list(checkedvar))):
            if list(checkedvar)[i] not in possible:
                testlist.remove(list(checkedvar)[i])
        
        while testlist[0] in forbiddenfirst:
            testlist.remove(testlist[0])

        checkedvar = ''.join(testlist)

        if checkedvar == "":
            checkedvar = "unamed_custom_level"

        return checkedvar

    def save(self):
        nb = self.namecheck(self.entry.get())

        with open(f"level.py", mode="a") as f:
            f.write(f"\n\n{nb}={str(self.grid)}")

        self.levellist()
        StartWindow.levellist(self)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Unsaved changes will be lost. Do you want to quit?"):
            self.root.destroy()
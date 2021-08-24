import tkinter as tk
from tkinter import messagebox
import level
from level import *
from maze_levelcreator import *

class Window:
    def __init__(self, level):
        if level == '':
            level = "test"
        self.size = len(globals()[level])
        self.grid = globals()[level]
        self.gridsave = [[0 for _ in range(len(self.grid[i]))] for i in range(len(self.grid))]
        self.gridcopy()
        self.moves = 0

        self.root = tk.Tk()
        self.root.title("Maze")
        self.root.resizable(0,0)

        self.display_frame = tk.Frame(self.root)
        self.control_frame = tk.Frame(self.root)
        self.info_frame = tk.Frame(self.root)

        self.display_frame.grid(row = 0, column = 0, columnspan=2)
        self.control_frame.grid(row = 0, column = 2, columnspan=1)
        self.info_frame.grid(row = 1, column=0, columnspan=3)

        self.display_screen = tk.Canvas(self.display_frame, width=self.size*10+2, height=self.size*10+2)

        self.display_screen.pack()

        self.display_level = tk.Label(self.info_frame, text="Level: "+str(level))
        self.display_score = tk.Label(self.info_frame, text="Moves: "+str(self.moves))
        self.reset_button = tk.Button(self.info_frame, text="Reset", command=self.reset)

        self.display_level.pack()
        self.display_score.pack()
        self.reset_button.pack()

        self.control_up = tk.Button(self.control_frame, text="ᐃ", width=4, height=2, command=lambda:self.move(0))
        self.control_left = tk.Button(self.control_frame, text="ᐊ", width=4, height=2, command=lambda:self.move(1))
        self.control_right = tk.Button(self.control_frame, text="ᐅ", width=4, height=2, command=lambda:self.move(2))
        self.control_down = tk.Button(self.control_frame, text="ᐁ", width=4, height=2, command=lambda:self.move(3))

        self.control_up.grid(row = 0, column = 1)
        self.control_left.grid(row = 1, column = 0)
        self.control_right.grid(row = 1, column = 2)
        self.control_down.grid(row = 2, column = 1)

        self.y = 0
        self.x = 0
        self.updatedisplay()
        self.findstart()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def gridcopy(self, m=0):
        if m == 0:
            for i in range(len(self.grid)):
                for j in range(len(self.grid[i])):
                    self.gridsave[j][i] = self.grid[j][i]
        if m == 1:
            for i in range(len(self.gridsave)):
                for j in range(len(self.gridsave[i])):
                    self.grid[j][i] = self.gridsave[j][i]

    def updatedisplay(self):
        self.display_screen.delete('all')
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == 0:
                    self.display_screen.create_rectangle(j*10+2, i*10+2, j*10+12, i*10+12, fill='white')
                if self.grid[i][j] == 1:
                    self.display_screen.create_rectangle(j*10+2, i*10+2, j*10+12, i*10+12, fill='black')
                if self.grid[i][j] == 2:
                    self.display_screen.create_oval(j*10+3, i*10+3, j*10+11, i*10+11, fill='green', outline='green')
                if self.grid[i][j] == 3:
                    self.display_screen.create_rectangle(j*10+2, i*10+2, j*10+12, i*10+12, fill='grey', outline="green")
        
        self.display_score.configure(text="Moves: "+str(self.moves))

    def findstart(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid)):
                if self.grid[i][j] == 2:
                    self.x = j
                    self.y = i
                    break

    def move(self, d):
        self.moves += 1
        if d == 0: #up
            if self.grid[self.y-1][self.x] == 0:
                self.grid[self.y][self.x] = 0
                self.grid[self.y-1][self.x] = 2
                self.y = self.y-1
            elif self.grid[self.y-1][self.x] == 3:
                self.grid[self.y][self.x] = 0
                self.display_screen.create_rectangle(self.x*10+2, (self.y-1)*10+2, self.x*10+12, (self.y-1)*10+12, fill='green')
                self.win()
        elif d == 1: #left
            if self.grid[self.y][self.x-1] == 0:
                self.grid[self.y][self.x] = 0
                self.grid[self.y][self.x-1] = 2
                self.x = self.x-1
            elif self.grid[self.y][self.x-1] == 3:
                self.grid[self.y][self.x] = 0
                self.display_screen.create_rectangle((self.x-1)*10+2, self.y*10+2, (self.x-1)*10+12, self.y*10+12, fill='green')
                self.win()
        elif d == 2: #right
            if self.grid[self.y][self.x+1] == 0:
                self.grid[self.y][self.x] = 0
                self.grid[self.y][self.x+1] = 2
                self.x = self.x+1
            elif self.grid[self.y][self.x+1] == 3:
                self.grid[self.y][self.x] = 0
                self.display_screen.create_rectangle((self.x+1)*10+2, self.y*10+2, (self.x+1)*10+12, self.y*10+12, fill='green')
                self.win()
        elif d == 3: #down
            if self.grid[self.y+1][self.x] == 0:
                self.grid[self.y][self.x] = 0
                self.grid[self.y+1][self.x] = 2
                self.y = self.y+1
            elif self.grid[self.y+1][self.x] == 3:
                self.grid[self.y][self.x] = 0
                self.display_screen.create_rectangle(self.x*10+2, (self.y+1)*10+2, self.x*10+12, (self.y+1)*10+12, fill='green')
                self.win()
        self.updatedisplay()

    def reset(self, w=0):
        self.moves = 0
        self.gridcopy(1)
        self.findstart()
        self.updatedisplay()
        if w == 1:
            self.win_window.destroy()

    def quit(self, w=0):
        self.root.destroy()
        if w == 1:
            self.win_window.destroy()

    def win(self):
        self.win_window = tk.Tk()
        self.win_window.title("Win !")

        self.win_text = tk.Label(self.win_window, text="Congratulations ! You made it out of the Maze")
        self.win_reset_button = tk.Button(self.win_window, text="Replay", command=lambda:self.reset(1))
        self.win_quit_button = tk.Button(self.win_window, text="Quit", command=lambda:self.quit(1))

        self.win_text.pack()
        self.win_reset_button.pack()
        self.win_quit_button.pack()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Level progression will be lost. Do you want to quit?"):
            self.reset()
            self.root.destroy()

class StartWindow():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title = "Maze"

        self.dropdownmenu_list = []
        self.levellist()
        self.dropdownmenu_variable = tk.StringVar(self.root)

        self.title_text = tk.Label(self.root, text="The Maze")
        self.start_text = tk.Label(self.root, text="Enter a level:")
        self.start_dropdownmenu = tk.OptionMenu(self.root, self.dropdownmenu_variable, *self.dropdownmenu_list)
        self.start_button = tk.Button(self.root, text="Play", command=lambda:Window(self.dropdownmenu_variable.get()))
        self.levelcreator_text = tk.Label(self.root, text="Enter grid size:")
        self.levelcreator_entry = tk.Entry(self.root)
        self.levelcreator_button = tk.Button(self.root, text="Open Editor", command=lambda:LevelEditor(self.levelcreator_entryverif()))

        self.title_text.grid(row = 0, column = 0, columnspan = 3)
        self.start_text.grid(row = 1, column = 0)
        self.start_dropdownmenu.grid(row = 1, column = 1)
        self.start_button.grid(row = 1, column = 2)
        self.levelcreator_text.grid(row = 2, column = 0)
        self.levelcreator_entry.grid(row = 2, column = 1)
        self.levelcreator_button.grid(row = 2, column = 2)

        self.root.mainloop()

    def levelcreator_entryverif(self):
        if self.levelcreator_entry.get() == "":
            return 49
        elif int(self.levelcreator_entry.get()) < 5:
            return 5
        else:
            return int(self.levelcreator_entry.get())

    def levellist(self):
        for element in dir(level):
            if str(element[0:2]) != "__" and str(element) != "test":
                self.dropdownmenu_list.append(element)

if __name__ == "__main__":
    StartWindow()
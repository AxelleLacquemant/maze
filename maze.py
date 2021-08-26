import tkinter as tk
from tkinter import messagebox
import random
import level
from level import *
from maze_levelcreator import *

class Window:
    def __init__(self, slevel):
        if slevel == '':
            slevel = "test"

        self.size = len(globals()[slevel])
        self.displaysize = 10
        self.playercolor = 'grey28'
        self.floorcolor = 'grey98'
        self.wallcolor = 'grey14'
        self.endcolor = 'grey'

        self.grid = globals()[slevel]
        self.gridsave = [[0 for _ in range(len(self.grid[i]))] for i in range(len(self.grid))]
        self.gridcopy()
        self.moves = 0

        self.root = tk.Tk()
        self.root.title("Maze")
        self.root.resizable(1,1)

        self.dropdownmenu_list = ["Black", "Purple", "Blue", "Cyan", "Green", "Yellow", "Orange", "Red", "Random"]
        self.dropdownmenu_variable = tk.StringVar(self.root)

        self.display_frame = tk.Frame(self.root)
        self.control_frame = tk.Frame(self.root)
        self.info_frame = tk.Frame(self.root)
        
        self.display_frame.pack()
        self.control_frame.pack()
        self.info_frame.pack()

        self.display_screen = tk.Canvas(self.display_frame, width=self.size*self.displaysize+2, height=self.size*self.displaysize+2, bg=self.floorcolor)
        self.displaysize_minbutton = tk.Button(self.display_frame, text="<", command=lambda:self.changesize(0))
        self.displaysize_label = tk.Label(self.display_frame, text="Change size | 10")
        self.displaysize_maxbutton = tk.Button(self.display_frame, text=">", command=lambda:self.changesize(1))

        self.displaysize_minbutton.grid(row=0, column=0)
        self.displaysize_label.grid(row=0, column=1)
        self.displaysize_maxbutton.grid(row=0, column=2)
        self.display_screen.grid(row=1, column=0, columnspan=3)

        self.display_level = tk.Label(self.info_frame, text="Level: "+str(slevel))
        self.display_score = tk.Label(self.info_frame, text="Moves: "+str(self.moves))
        self.reset_button = tk.Button(self.info_frame, text="Reset", command=self.reset)
        self.color_dropdownmenu = tk.OptionMenu(self.info_frame, self.dropdownmenu_variable, *self.dropdownmenu_list)
        self.color_button = tk.Button(self.info_frame, text="Change Theme", command=lambda:self.changecolor(self.dropdownmenu_variable.get()))

        self.color_dropdownmenu.config(width=7)

        self.display_level.grid(row=0, column=0, columnspan=3)
        self.display_score.grid(row=1, column=0, columnspan=3)
        self.color_dropdownmenu.grid(row=2, column=0)
        self.color_button.grid(row=2, column=1)
        self.reset_button.grid(row=2, column=2)
        
        self.root.bind("<Key>", self.keycontrol)

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
        self.updatebuttons()
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
                    self.display_screen.create_rectangle(j*self.displaysize+2, i*self.displaysize+2, j*self.displaysize+(self.displaysize+2), i*self.displaysize+(self.displaysize+2), fill=self.floorcolor, outline=self.wallcolor)
                if self.grid[i][j] == 1:
                    self.display_screen.create_rectangle(j*self.displaysize+2, i*self.displaysize+2, j*self.displaysize+(self.displaysize+2), i*self.displaysize+(self.displaysize+2), fill=self.wallcolor, outline=self.wallcolor)
                if self.grid[i][j] == 2:
                    self.display_screen.create_oval(j*self.displaysize+3, i*self.displaysize+3, j*self.displaysize+(self.displaysize+1), i*self.displaysize+(self.displaysize+1), fill=self.playercolor, outline=self.wallcolor)
                if self.grid[i][j] == 3:
                    self.display_screen.create_rectangle(j*self.displaysize+2, i*self.displaysize+2, j*self.displaysize+(self.displaysize+2), i*self.displaysize+(self.displaysize+2), fill=self.endcolor, outline=self.playercolor)
        
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
                self.display_screen.create_rectangle(self.x*self.displaysize+2, (self.y-1)*self.displaysize+2, self.x*self.displaysize+(self.displaysize+2), (self.y-1)*self.displaysize+(self.displaysize+2), fill=self.playercolor)
                self.win()
            else: 
                self.moves -= 1
        elif d == 1: #left
            if self.grid[self.y][self.x-1] == 0:
                self.grid[self.y][self.x] = 0
                self.grid[self.y][self.x-1] = 2
                self.x = self.x-1
            elif self.grid[self.y][self.x-1] == 3:
                self.grid[self.y][self.x] = 0
                self.display_screen.create_rectangle((self.x-1)*self.displaysize+2, self.y*self.displaysize+2, (self.x-1)*self.displaysize+(self.displaysize+2), self.y*self.displaysize+(self.displaysize+2), fill=self.playercolor)
                self.win()
            else: 
                self.moves -= 1
        elif d == 2: #right
            if self.grid[self.y][self.x+1] == 0:
                self.grid[self.y][self.x] = 0
                self.grid[self.y][self.x+1] = 2
                self.x = self.x+1
            elif self.grid[self.y][self.x+1] == 3:
                self.grid[self.y][self.x] = 0
                self.display_screen.create_rectangle((self.x+1)*self.displaysize+2, self.y*self.displaysize+2, (self.x+1)*self.displaysize+(self.displaysize+2), self.y*self.displaysize+(self.displaysize+2), fill=self.playercolor)
                self.win()
            else: 
                self.moves -= 1
        elif d == 3: #down
            if self.grid[self.y+1][self.x] == 0:
                self.grid[self.y][self.x] = 0
                self.grid[self.y+1][self.x] = 2
                self.y = self.y+1
            elif self.grid[self.y+1][self.x] == 3:
                self.grid[self.y][self.x] = 0
                self.display_screen.create_rectangle(self.x*self.displaysize+2, (self.y+1)*self.displaysize+2, self.x*self.displaysize+(self.displaysize+2), (self.y+1)*self.displaysize+(self.displaysize+2), fill=self.playercolor)
                self.win()
            else: 
                self.moves -= 1
        self.updatedisplay()

    def reset(self, w=0):
        self.moves = 0
        self.gridcopy(1)
        self.findstart()
        self.updatedisplay()
        if w == 1:
            self.win_window.destroy()

    def keycontrol(self, key):
        if key.keycode == 38:
            self.move(0)
        if key.keycode == 37:
            self.move(1)
        if key.keycode == 39:
            self.move(2)
        if key.keycode == 40:
            self.move(3)
        if key.keycode == 82:
            self.reset()
        if key.keycode == 81:
            self.quit()

    def quit(self, w=0):
        self.root.destroy()
        if w == 1:
            self.win_window.destroy()

    def win(self):
        self.win_window = tk.Tk()
        self.win_window.title("Win !")

        self.win_text = tk.Label(self.win_window, text="Congratulations ! You made it out of the Maze")
        self.win_reset_button = tk.Button(self.win_window, text="Replay", command=lambda:self.reset(1))
        self.win_quit_button = tk.Button(self.win_window, text="Quit", command=lambda:[self.reset(), self.quit(1)])

        self.win_text.pack()
        self.win_reset_button.pack()
        self.win_quit_button.pack()

    def changecolor(self, color):
        if color == "":
            color = "Black"
        if color == "Black":
            self.playercolor = 'grey28'
            self.floorcolor = 'grey98'
            self.wallcolor = 'grey14'
            self.endcolor = 'grey'
        if color == "Purple":
            self.playercolor = '#C600F2'
            self.floorcolor = '#FAE3FF'
            self.wallcolor = '#7C0098'
            self.endcolor = '#E56EFF'
        if color == "Blue":
            self.playercolor = '#2A00B9'
            self.floorcolor = '#EFEEFF'
            self.wallcolor = '#230098'
            self.endcolor = '#6440DF'
        if color == "Cyan":
            self.playercolor = '#01AEA6'
            self.floorcolor = '#EEFFFF'
            self.wallcolor = '#008C85'
            self.endcolor = '#00DCD2'
        if color == "Green":
            self.playercolor = '#009C1C'
            self.floorcolor = '#DCFFE2'
            self.wallcolor = '#007315'
            self.endcolor = '#07CD2B'
        if color == "Yellow":
            self.playercolor = '#C7CC13'
            self.floorcolor = '#FEFFEE'
            self.wallcolor = '#C2B106'
            self.endcolor = '#DADF31'
        if color == "Orange":
            self.playercolor = '#DC9718'
            self.floorcolor = '#FFF4EB'
            self.wallcolor = '#AD630B'
            self.endcolor = '#F4AC24'
        if color == "Red":
            self.playercolor = '#CA1212'
            self.floorcolor = '#FFE1E1'
            self.wallcolor = '#9E0000'
            self.endcolor = '#EE1A1A'
        if color == "Random":
            self.playercolor = "#"+("%06x"%random.randint(0,16777215))
            self.floorcolor = 'grey'+str((random.randint(91,98)))
            self.wallcolor = "#"+("%06x"%random.randint(0,16777215))
            self.endcolor = "#"+("%06x"%random.randint(0,16777215))

        self.updatebuttons()
        self.updatedisplay()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Level progression will be lost. Do you want to quit?"):
            self.reset()
            self.root.destroy()

    def updatebuttons(self):
        uptelements = [self.displaysize_minbutton, self.displaysize_maxbutton, self.color_dropdownmenu, self.color_button, self.reset_button, self.control_up, self.control_left, self.control_right, self.control_down]
        for element in uptelements:
            element.config(bg=self.wallcolor, foreground=self.floorcolor)

        uptelementsinv = [self.displaysize_label, self.display_level, self.display_score]
        for element in uptelementsinv:
            element.config(bg=self.floorcolor, foreground=self.wallcolor)

        uptelementsbg = [self.root, self.display_frame, self.control_frame, self.info_frame, self.display_screen]
        for element in uptelementsbg:
            element.config(bg=self.floorcolor)

    def changesize(self, mode):
        if mode == 0 and self.displaysize > 4:
            self.displaysize = self.displaysize-2
            self.displaysize_label.config(text="Change size | "+str(self.displaysize))
        if mode == 1 and self.displaysize < 20:
            self.displaysize = self.displaysize+2
            self.displaysize_label.config(text="Change size | "+str(self.displaysize))

        self.display_screen.config(width=self.size*self.displaysize+2, height=self.size*self.displaysize+2)
        
        self.updatedisplay()

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
        self.start_button = tk.Button(self.root, text="Play", command=lambda:Window(self.dropdownmenu_variable.get()), width=9)
        self.levelcreator_text = tk.Label(self.root, text="Enter grid size:")
        self.levelcreator_entry = tk.Entry(self.root)
        self.levelcreator_button = tk.Button(self.root, text="Open Editor", command=lambda:LevelEditor(self.levelcreator_entryverif()))

        self.start_dropdownmenu.config(width=14)

        self.title_text.grid(row = 0, column = 0, columnspan = 3)
        self.start_text.grid(row = 1, column = 0)
        self.start_dropdownmenu.grid(row = 1, column = 1)
        self.start_button.grid(row = 1, column = 2)
        self.levelcreator_text.grid(row = 2, column = 0)
        self.levelcreator_entry.grid(row = 2, column = 1)
        self.levelcreator_button.grid(row = 2, column = 2)

        self.root.mainloop()

    def levelcreator_entryverif(self):
        try:
            int(self.levelcreator_entry.get())
        except ValueError:
            return 49
        if int(self.levelcreator_entry.get()) < 7:
            return 7
        else:
            return int(self.levelcreator_entry.get())

    def levellist(self):
        for element in dir(level):
            if str(element[0:2]) != "__" and str(element) != "test":
                self.dropdownmenu_list.append(element)

if __name__ == "__main__":
    StartWindow()
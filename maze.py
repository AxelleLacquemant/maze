import tkinter as tk
import os
from level import *
from maze_levelcreator import *
os.chdir(os.path.dirname(os.path.realpath(__file__)))

class Window:
    def __init__(self, level="level1"):
        self.size = len(globals()[level])
        self.grid = globals()[level]
        self.gridsave = [[0 for _ in range(len(self.grid[i]))] for i in range(len(self.grid))]
        self.gridcopy()
        self.moves = 0

        self.root = tk.Tk()
        self.root.title("Maze")
        self.root.resizable(0,0)

        self.disp_frame = tk.Frame(self.root)
        self.cont_frame = tk.Frame(self.root)
        self.info_frame = tk.Frame(self.root)

        self.disp_frame.grid(row = 0, column = 0, columnspan=2)
        self.cont_frame.grid(row = 0, column = 2, columnspan=1)
        self.info_frame.grid(row = 1, column=0, columnspan=3)

        self.disp_scrn = tk.Canvas(self.disp_frame, width=self.size*10+2, height=self.size*10+2)

        self.disp_scrn.pack()

        self.disp_lvl = tk.Label(self.info_frame, text="Level: "+str(level))
        self.disp_scr = tk.Label(self.info_frame, text="Moves: "+str(self.moves))
        self.rstbtn = tk.Button(self.info_frame, text="Reset", command=self.reset)

        self.disp_lvl.pack()
        self.disp_scr.pack()
        self.rstbtn.pack()

        self.cont_u = tk.Button(self.cont_frame, text="ᐃ", width=4, height=2, command=lambda:self.move(0))
        self.cont_l = tk.Button(self.cont_frame, text="ᐊ", width=4, height=2, command=lambda:self.move(1))
        self.cont_r = tk.Button(self.cont_frame, text="ᐅ", width=4, height=2, command=lambda:self.move(2))
        self.cont_d = tk.Button(self.cont_frame, text="ᐁ", width=4, height=2, command=lambda:self.move(3))

        self.cont_u.grid(row = 0, column = 1)
        self.cont_l.grid(row = 1, column = 0)
        self.cont_r.grid(row = 1, column = 2)
        self.cont_d.grid(row = 2, column = 1)

        self.y = 0
        self.x = 0
        self.updtdisp()
        self.findstart()

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

    def updtdisp(self):
        self.disp_scrn.delete('all')
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == 0:
                    self.disp_scrn.create_rectangle(j*10+2, i*10+2, j*10+12, i*10+12, fill='white')
                if self.grid[i][j] == 1:
                    self.disp_scrn.create_rectangle(j*10+2, i*10+2, j*10+12, i*10+12, fill='black')
                if self.grid[i][j] == 2:
                    self.disp_scrn.create_oval(j*10+3, i*10+3, j*10+11, i*10+11, fill='green', outline='green')
                if self.grid[i][j] == 3:
                    self.disp_scrn.create_rectangle(j*10+2, i*10+2, j*10+12, i*10+12, fill='grey', outline="green")
        
        self.disp_scr.configure(text="Moves: "+str(self.moves))

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
                self.disp_scrn.create_rectangle(self.x*10+2, (self.y-1)*10+2, self.x*10+12, (self.y-1)*10+12, fill='green')
                self.win()
        elif d == 1: #left
            if self.grid[self.y][self.x-1] == 0:
                self.grid[self.y][self.x] = 0
                self.grid[self.y][self.x-1] = 2
                self.x = self.x-1
            elif self.grid[self.y][self.x-1] == 3:
                self.grid[self.y][self.x] = 0
                self.disp_scrn.create_rectangle((self.x-1)*10+2, self.y*10+2, (self.x-1)*10+12, self.y*10+12, fill='green')
                self.win()
        elif d == 2: #right
            if self.grid[self.y][self.x+1] == 0:
                self.grid[self.y][self.x] = 0
                self.grid[self.y][self.x+1] = 2
                self.x = self.x+1
            elif self.grid[self.y][self.x+1] == 3:
                self.grid[self.y][self.x] = 0
                self.disp_scrn.create_rectangle((self.x+1)*10+2, self.y*10+2, (self.x+1)*10+12, self.y*10+12, fill='green')
                self.win()
        elif d == 3: #down
            if self.grid[self.y+1][self.x] == 0:
                self.grid[self.y][self.x] = 0
                self.grid[self.y+1][self.x] = 2
                self.y = self.y+1
            elif self.grid[self.y+1][self.x] == 3:
                self.grid[self.y][self.x] = 0
                self.disp_scrn.create_rectangle(self.x*10+2, (self.y+1)*10+2, self.x*10+12, (self.y+1)*10+12, fill='green')
                self.win()
        self.updtdisp()

    def reset(self, w=0):
        self.moves = 0
        self.gridcopy(1)
        self.findstart()
        self.updtdisp()
        if w == 1:
            self.winwdw.destroy()

    def quit(self, w=0):
        self.root.destroy()
        if w == 1:
            self.winwdw.destroy()

    def win(self):
        self.winwdw = tk.Tk()
        self.winwdw.title("Win !")

        self.wintxt = tk.Label(self.winwdw, text="Congratulations ! You made it out of the Maze")
        self.winrstbtn = tk.Button(self.winwdw, text="Replay", command=lambda:self.reset(1))
        self.winqutbtn = tk.Button(self.winwdw, text="Quit", command=lambda:self.quit(1))

        self.wintxt.pack()
        self.winrstbtn.pack()
        self.winqutbtn.pack()

class StartWindow():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title = "Maze"

        self.ttltxt = tk.Label(self.root, text="The Maze")
        self.strtxt = tk.Label(self.root, text="Enter a level:")
        self.strent = tk.Entry(self.root)
        self.strbtn = tk.Button(self.root, text="Play", command=lambda:Window(self.strent.get()))
        self.lctxt = tk.Label(self.root, text="Enter grid size:")
        self.lcent = tk.Entry(self.root)
        self.lcbtn = tk.Button(self.root, text="Open Editor", command=lambda:Mescouilles(self.lcentverif()))

        self.ttltxt.grid(row = 0, column = 0, columnspan = 3)
        self.strtxt.grid(row = 1, column = 0)
        self.strent.grid(row = 1, column = 1)
        self.strbtn.grid(row = 1, column = 2)
        self.lctxt.grid(row = 2, column = 0)
        self.lcent.grid(row = 2, column = 1)
        self.lcbtn.grid(row = 2, column = 2)

        self.root.mainloop()

    def lcentverif(self):
        if self.lcent.get() == "":
            return 49
        elif int(self.lcent.get()) < 5:
            return 5
        else:
            return int(self.lcent.get())

if __name__ == "__main__":
    StartWindow()
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

        self.lvlname = self.getname(slevel)
        self.size = len(globals()[slevel])
        self.displaysize = 16
        self.enemy = False
        self.playercolor = 'green'
        self.floorcolor = 'grey98'
        self.wallcolor = 'grey14'
        self.endcolor = 'grey'
        self.fruitcolor = 'gold'
        self.enemycolor = 'red'
        self.fruittype = 'Coins'
        self.enemytype = 'Minotaur'

        self.grid = globals()[slevel]
        self.gridsave = [[0 for _ in range(len(self.grid[i]))] for i in range(len(self.grid))]
        self.gridcopy()
        self.moves = 0
        self.score = 0

        self.root = tk.Tk()
        self.root.title("Maze")
        self.root.resizable(1,1)

        self.dropdownmenu_list = ["Default", "Forest", "Sea", "Sky", "Space", "Nether", "End", "Random"]
        self.dropdownmenu_variable = tk.StringVar(self.root, "Default")

        self.display_frame = tk.Frame(self.root)
        self.control_frame = tk.Frame(self.root)
        self.info_frame = tk.Frame(self.root)
        
        self.display_frame.pack()
        self.control_frame.pack()
        self.info_frame.pack()

        self.display_screen = tk.Canvas(self.display_frame, width=self.size*self.displaysize+2, height=self.size*self.displaysize+2, bg=self.floorcolor)
        self.displaysize_minbutton = tk.Button(self.display_frame, text="<", command=lambda:self.changesize(0))
        self.displaysize_label = tk.Label(self.display_frame, text="Change size | "+str(self.displaysize))
        self.displaysize_maxbutton = tk.Button(self.display_frame, text=">", command=lambda:self.changesize(1))

        self.displaysize_minbutton.grid(row=0, column=0)
        self.displaysize_label.grid(row=0, column=1)
        self.displaysize_maxbutton.grid(row=0, column=2)
        self.display_screen.grid(row=1, column=0, columnspan=3)

        self.display_level = tk.Label(self.info_frame, text="Level: "+(str(self.lvlname).capitalize()))
        self.display_moves = tk.Label(self.info_frame, text="Moves: "+str(self.moves))
        self.display_score = tk.Label(self.info_frame, text=self.fruittype+": "+str(self.score))
        self.reset_button = tk.Button(self.info_frame, text="Reset", command=self.reset)
        self.color_dropdownmenu = tk.OptionMenu(self.info_frame, self.dropdownmenu_variable, *self.dropdownmenu_list, command=self.changecolor)

        self.color_dropdownmenu.config(width=7)

        self.display_level.grid(row=0, column=0, columnspan=3)
        self.display_moves.grid(row=1, column=0, columnspan=3)
        self.display_score.grid(row=2, column=0, columnspan=3)
        self.color_dropdownmenu.grid(row=3, column=0)
        self.reset_button.grid(row=3, column=2)
        
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
        self.eny = 0
        self.enx = 0
        self.additems(self.grid)
        if self.size > 7 or self.lvlname == "test":
            self.addenemy(self.grid)
        self.updatebuttons()
        self.updatedisplay()
        self.findstart()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.root.mainloop()

    def getname(self, slevel):
        listlvl = list(slevel)
        for i in range(len(listlvl)):
            if listlvl[i] == "_":
                listlvl[i] = " "
        displayname = ""
        for element in listlvl:
            displayname += element
        return displayname

    def gridcopy(self, m=0):
        if m == 0:
            for i in range(len(self.grid)):
                for j in range(len(self.grid[i])):
                    self.gridsave[j][i] = self.grid[j][i]
        if m == 1:
            for i in range(len(self.gridsave)):
                for j in range(len(self.gridsave[i])):
                    self.grid[j][i] = self.gridsave[j][i]

    def additems(self, lvl):
        for i in range(len(lvl)):
            for j in range(len(lvl[i])):
                if lvl[i][j] == 0:
                    nbf = random.randint(0,7)
                    if nbf == 7:
                        lvl[i][j] = 4

    def addenemy(self, lvl):
        self.enemy = False
        while self.enemy == False:
            for i in range(round((len(lvl))/2), len(lvl)):
                for j in range(round((len(lvl))/2), len(lvl)):
                    if lvl[i][j] == 0:
                        nbf = random.randint(0,self.size*self.size)
                        if nbf == 0:
                            lvl[i][j] = 5
                            self.enemy = True
                            return

    def updatedisplay(self):
        self.display_screen.delete('all')

        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == 0:
                    self.display_screen.create_rectangle(j*self.displaysize+2, i*self.displaysize+2, j*self.displaysize+(self.displaysize+2), i*self.displaysize+(self.displaysize+2), fill=self.floorcolor, outline=self.floorcolor)
                if self.grid[i][j] == 1:
                    self.display_screen.create_rectangle(j*self.displaysize+2, i*self.displaysize+2, j*self.displaysize+(self.displaysize+2), i*self.displaysize+(self.displaysize+2), fill=self.wallcolor, outline=self.wallcolor)
                if self.grid[i][j] == 2:
                    self.display_screen.create_rectangle(j*self.displaysize+2, i*self.displaysize+2, j*self.displaysize+(self.displaysize+2), i*self.displaysize+(self.displaysize+2), fill=self.floorcolor, outline=self.floorcolor)
                    self.display_screen.create_oval(j*self.displaysize+3, i*self.displaysize+3, j*self.displaysize+(self.displaysize+1), i*self.displaysize+(self.displaysize+1), fill=self.playercolor, outline=self.playercolor)
                if self.grid[i][j] == 3:
                    self.display_screen.create_rectangle(j*self.displaysize+2, i*self.displaysize+2, j*self.displaysize+(self.displaysize+2), i*self.displaysize+(self.displaysize+2), fill=self.endcolor, outline=self.playercolor)
                if self.grid[i][j] == 4:
                    self.display_screen.create_rectangle(j*self.displaysize+2, i*self.displaysize+2, j*self.displaysize+(self.displaysize+2), i*self.displaysize+(self.displaysize+2), fill=self.floorcolor, outline=self.floorcolor)
                    self.display_screen.create_oval(j*self.displaysize+5, i*self.displaysize+5, j*self.displaysize+(self.displaysize-1), i*self.displaysize+(self.displaysize-1), fill=self.fruitcolor, outline=self.fruitcolor)
                if self.grid[i][j] == 5:
                    self.display_screen.create_rectangle(j*self.displaysize+2, i*self.displaysize+2, j*self.displaysize+(self.displaysize+2), i*self.displaysize+(self.displaysize+2), fill=self.floorcolor, outline=self.floorcolor)
                    self.display_screen.create_oval(j*self.displaysize+2, i*self.displaysize+2, j*self.displaysize+(self.displaysize+2), i*self.displaysize+(self.displaysize+2), fill=self.enemycolor, outline=self.enemycolor)
        
        self.display_moves.configure(text="Moves: "+str(self.moves))
        self.display_score.configure(text=self.fruittype+": "+str(self.score))

    def findstart(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid)):
                if self.grid[i][j] == 2:
                    self.x = j
                    self.y = i
                if self.grid[i][j] == 5:
                    self.enx = j
                    self.eny = i

    def enemybehavior(self):
        self.killplayer()
        self.distx = self.x - self.enx
        self.disty = self.y - self.eny
        
        if self.moves%6 == 0:
            if self.distx < 0:
                self.enemymove(3)
            elif self.distx > 0:
                self.enemymove(1)
            if self.disty < 0:
                self.enemymove(0)
            elif self.disty > 0:
                self.enemymove(2)

        self.killplayer()
        self.updatedisplay()

    def enemymove(self, d):
        if d == 0: #up
            self.grid[self.eny][self.enx] = 0
            self.grid[self.eny-1][self.enx] = 5
            self.eny = self.eny-1
        elif d == 1: #right
            self.grid[self.eny][self.enx] = 0
            self.grid[self.eny][self.enx+1] = 5
            self.enx = self.enx+1
        elif d == 2: #down
            self.grid[self.eny][self.enx] = 0
            self.grid[self.eny+1][self.enx] = 5
            self.eny = self.eny+1
        else: #left
            self.grid[self.eny][self.enx] = 0
            self.grid[self.eny][self.enx-1] = 5
            self.enx = self.enx-1

    def killplayer(self):
        if self.grid[self.eny-1][self.enx] == 2:
            self.grid[self.eny-1][self.enx] = 0
            self.end(1)
        elif self.grid[self.eny][self.enx+1] == 2:
            self.grid[self.eny][self.enx+1] = 0
            self.end(1)
        elif self.grid[self.eny+1][self.enx] == 2:
            self.grid[self.eny+1][self.enx] = 0
            self.end(1)
        elif self.grid[self.eny][self.enx-1] == 2:
            self.grid[self.eny][self.enx-1] = 0
            self.end(1)

    def move(self, d):
        self.moves += 1
        if d == 0: #up
            if self.grid[self.y-1][self.x] == 0:
                self.grid[self.y][self.x] = 0
                self.grid[self.y-1][self.x] = 2
                self.y = self.y-1
            elif self.grid[self.y-1][self.x] == 4:
                self.grid[self.y][self.x] = 0
                self.grid[self.y-1][self.x] = 2
                self.y = self.y-1
                self.score += 25
            elif self.grid[self.y-1][self.x] == 3:
                self.grid[self.y][self.x] = 0
                self.display_screen.create_rectangle(self.x*self.displaysize+2, (self.y-1)*self.displaysize+2, self.x*self.displaysize+(self.displaysize+2), (self.y-1)*self.displaysize+(self.displaysize+2), fill=self.playercolor)
                self.end()
            else: 
                self.moves -= 1
        elif d == 1: #left
            if self.grid[self.y][self.x-1] == 0:
                self.grid[self.y][self.x] = 0
                self.grid[self.y][self.x-1] = 2
                self.x = self.x-1
            elif self.grid[self.y][self.x-1] == 4:
                self.grid[self.y][self.x] = 0
                self.grid[self.y][self.x-1] = 2
                self.x = self.x-1
                self.score += 25
            elif self.grid[self.y][self.x-1] == 3:
                self.grid[self.y][self.x] = 0
                self.display_screen.create_rectangle((self.x-1)*self.displaysize+2, self.y*self.displaysize+2, (self.x-1)*self.displaysize+(self.displaysize+2), self.y*self.displaysize+(self.displaysize+2), fill=self.playercolor)
                self.end()
            else: 
                self.moves -= 1
        elif d == 2: #right
            if self.grid[self.y][self.x+1] == 0:
                self.grid[self.y][self.x] = 0
                self.grid[self.y][self.x+1] = 2
                self.x = self.x+1
            elif self.grid[self.y][self.x+1] == 4:
                self.grid[self.y][self.x] = 0
                self.grid[self.y][self.x+1] = 2
                self.x = self.x+1
                self.score += 25
            elif self.grid[self.y][self.x+1] == 3:
                self.grid[self.y][self.x] = 0
                self.display_screen.create_rectangle((self.x+1)*self.displaysize+2, self.y*self.displaysize+2, (self.x+1)*self.displaysize+(self.displaysize+2), self.y*self.displaysize+(self.displaysize+2), fill=self.playercolor)
                self.end()
            else: 
                self.moves -= 1
        elif d == 3: #down
            if self.grid[self.y+1][self.x] == 0:
                self.grid[self.y][self.x] = 0
                self.grid[self.y+1][self.x] = 2
                self.y = self.y+1
            elif self.grid[self.y+1][self.x] == 4:
                self.grid[self.y][self.x] = 0
                self.grid[self.y+1][self.x] = 2
                self.y = self.y+1
                self.score += 25
            elif self.grid[self.y+1][self.x] == 3:
                self.grid[self.y][self.x] = 0
                self.display_screen.create_rectangle(self.x*self.displaysize+2, (self.y+1)*self.displaysize+2, self.x*self.displaysize+(self.displaysize+2), (self.y+1)*self.displaysize+(self.displaysize+2), fill=self.playercolor)
                self.end()
            else: 
                self.moves -= 1
        self.updatedisplay()
        if self.enemy == True:
            self.enemybehavior()

    def reset(self, w=0):
        self.moves = 0
        self.score = 0
        self.gridcopy(1)
        self.additems(self.grid)
        if self.size > 7 or self.lvlname == "test":
            self.addenemy(self.grid)
        self.findstart()
        self.updatedisplay()
        self.root.bind("<Key>", self.keycontrol)
        if w == 1:
            self.win_window.destroy()

    def keycontrol(self, key):
        if key.keycode == 38: #^
            self.move(0)
        if key.keycode == 37: #<
            self.move(1)
        if key.keycode == 39: #>
            self.move(2)
        if key.keycode == 40: #V
            self.move(3)
        if key.keycode == 82: #q
            self.reset()
        if key.keycode == 81: #q
            self.quit()
        if key.keycode == 109: #-
            self.changesize(0)
        if key.keycode == 107: #+
            self.changesize(1)

    def quit(self, w=0):
        self.root.destroy()
        if w == 1:
            self.win_window.destroy()

    def end(self, mode=0):
        self.root.unbind("<Key>")

        self.win_window = tk.Tk()
        if mode==0:
            self.win_window.title("Win !")
            self.win_text = tk.Label(self.win_window, text="Congratulations ! You made it out of the Maze")
            self.win_score = tk.Label(self.win_window, text="Score: "+str(round(self.score/self.moves*100)))
        if mode==1:
            self.win_window.title("Lost :(")
            self.win_text = tk.Label(self.win_window, text="Oh no ! The "+self.enemytype+" got you!")
            self.win_score = tk.Label(self.win_window, text="Score: "+str(round(self.score/self.moves*100-self.size*100)))

        self.win_reset_button = tk.Button(self.win_window, text="Replay", command=lambda:self.reset(1))
        self.win_quit_button = tk.Button(self.win_window, text="Quit", command=lambda:[self.reset(), self.quit(1)])

        self.win_text.pack()
        self.win_score.pack()
        self.win_reset_button.pack()
        self.win_quit_button.pack()

    def changecolor(self, color):
        if color == "":
            color = "Default"
        if color == "Default":
            self.playercolor = 'green'
            self.floorcolor = 'grey98'
            self.wallcolor = 'grey14'
            self.endcolor = 'grey'
            self.fruitcolor = 'gold'
            self.enemycolor = 'red'
            self.fruittype = 'Coins'
            self.enemytype = 'Minotaur'
        if color == "Forest":
            self.playercolor = '#89805A'
            self.floorcolor = '#E4FFD2'
            self.wallcolor = '#286200'
            self.endcolor = '#89AF4F'
            self.fruitcolor = '#D10000'
            self.enemycolor = '#614E43'
            self.fruittype = 'Berries'
            self.enemytype = 'bear'
        if color == "Sea":
            self.playercolor = '#EFEFEF'
            self.floorcolor = '#B5DAF0'
            self.wallcolor = '#1B184B'
            self.endcolor = '#56A9D8'
            self.fruitcolor = '#E1BFA0'
            self.enemycolor = '#E8852E'
            self.fruittype = 'Smaller fishes'
            self.enemytype = 'bigger fish'
        if color == "Sky":
            self.playercolor = '#A9A9A9'
            self.floorcolor = '#FFFFFF'
            self.wallcolor = '#76ECFF'
            self.endcolor = '#B5FBFF'
            self.fruitcolor = '#FFCC46'
            self.enemycolor = '#525D5F'
            self.fruittype = 'Fruits'
            self.enemytype = 'big bird'
        if color == "Space":
            self.playercolor = '#F1F1F1'
            self.floorcolor = 'black'
            self.wallcolor = '#454545'
            self.endcolor = '#121212'
            self.fruitcolor = '#00FF00'
            self.enemycolor = '#078544'
            self.fruittype = 'Uranium'
            self.enemytype = 'alien'
        if color == "Nether":
            self.playercolor = '#DAD4CF'
            self.floorcolor = '#BB6E65'
            self.wallcolor = '#5B0000'
            self.endcolor = '#C15353'
            self.fruitcolor = '#FED740'
            self.enemycolor = '#272D2E'
            self.fruittype = 'Gold Ingots'
            self.enemytype = 'Wither Skeleton'
        if color == "End":
            self.playercolor = '#302C2F'
            self.floorcolor = '#F4FAD7'
            self.wallcolor = '#370D37'
            self.endcolor = '#8F937B'
            self.fruitcolor = '#258373'
            self.enemycolor = '#B170B1'
            self.fruittype = 'Ender Pearls'
            self.enemytype = 'Ender Dragon'
        if color == "Random":
            self.playercolor = "#"+("%06x"%random.randint(0,16777215))
            self.floorcolor = "#"+("%06x"%random.randint(0,16777215))
            self.wallcolor = "#"+("%06x"%random.randint(0,16777215))
            self.endcolor = "#"+("%06x"%random.randint(0,16777215))
            self.fruitcolor = "#"+("%06x"%random.randint(0,16777215))
            self.enemycolor = "#"+("%06x"%random.randint(0,16777215))
            self.fruittype = 'Strange stuff'
            self.enemytype = 'strange thing'

        self.updatebuttons()
        self.updatedisplay()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Level progression will be lost. Do you want to quit?"):
            self.reset()
            self.root.destroy()

    def updatebuttons(self):
        uptelements = [self.displaysize_minbutton, self.displaysize_maxbutton, self.color_dropdownmenu, self.reset_button, self.control_up, self.control_left, self.control_right, self.control_down]
        for element in uptelements:
            element.config(bg=self.wallcolor, foreground=self.floorcolor)

        uptelementsinv = [self.displaysize_label, self.display_level, self.display_moves, self.display_score]
        for element in uptelementsinv:
            element.config(bg=self.floorcolor, foreground=self.wallcolor)

        uptelementsbg = [self.root, self.display_frame, self.control_frame, self.info_frame, self.display_screen]
        for element in uptelementsbg:
            element.config(bg=self.floorcolor)

        hlbgelements = [self.display_screen, self.color_dropdownmenu]
        for element in hlbgelements:
            element.config(highlightbackground=self.floorcolor)

    def changesize(self, mode):
        if mode == 0 and self.displaysize > 10:
            self.displaysize = self.displaysize-2
            self.displaysize_label.config(text="Change size | "+str(self.displaysize))
        if mode == 1 and self.displaysize < 30:
            self.displaysize = self.displaysize+2
            self.displaysize_label.config(text="Change size | "+str(self.displaysize))

        self.display_screen.config(width=self.size*self.displaysize+2, height=self.size*self.displaysize+2)
        
        self.updatedisplay()

class StartWindow():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Maze")

        self.dropdownmenu_list = []
        self.levellist()
        self.dropdownmenu_variable = tk.StringVar(self.root)

        self.title_text = tk.Label(self.root, text="The Maze")
        self.start_text = tk.Label(self.root, text="Select a level:", width=12)
        self.start_dropdownmenu = tk.OptionMenu(self.root, self.dropdownmenu_variable, *self.dropdownmenu_list)
        self.start_button = tk.Button(self.root, text="Play", command=lambda:Window(self.dropdownmenu_variable.get()), width=12)
        self.levelcreator_text = tk.Label(self.root, text="Enter grid size:", width=12)
        self.levelcreator_entry = tk.Entry(self.root)
        self.levelcreator_button = tk.Button(self.root, text="Open Editor", command=lambda:LevelEditor(self.levelcreator_entryverif()), width=12)

        self.start_dropdownmenu.config(width=14)

        self.title_text.grid(row = 0, column = 0, columnspan = 3, sticky='ew')
        self.start_text.grid(row = 1, column = 0)
        self.start_dropdownmenu.grid(row = 1, column = 1)
        self.start_button.grid(row = 1, column = 2)
        self.levelcreator_text.grid(row = 2, column = 0)
        self.levelcreator_entry.grid(row = 2, column = 1)
        self.levelcreator_button.grid(row = 2, column = 2)

        self.updatebuttons()

        self.root.mainloop()

    def updatebuttons(self):
        uptelements = [self.title_text, self.start_text, self.levelcreator_text, self.start_button, self.levelcreator_button]
        for element in uptelements:
            element.config(bg='grey14', foreground='grey98')

        self.start_dropdownmenu.config(highlightbackground='grey14')

        self.root.config(bg='grey14')

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
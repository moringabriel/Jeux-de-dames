
from tkinter import Tk, Canvas, Label, Button, Frame, EW, NSEW
from random import choice
from math import radians, sqrt, sin, cos, tan
import time
import random

width = 990
height = 600
WIDTH, HEIGHT = width,height
x1,y1,x2,y2=2,2,2,2

TITREJEU = 'MEGA DAMES'
theme_courant = 'Orange'
#color = ['white', '#474757', 'grey12', 'orange']
#color = ['white', '#474757', 'grey12', 'azure4']
#color = ['Base', 'Blue', 'Rose', 'Vert']
#color = ['white', '#474757', 'grey12', 'orange']
#color = ['white', '#474757', 'grey12', 'azure4']  # #theme Default
#color = ['white', 'deep sky blue', 'lightblue', '#F2C53D' ]  # theme Bleu
#color = ['white', 'HotPink2', '#191B46', '#ACBEFF']  # theme rose
color = ['white', 'yellow green', '#2F363F','#EF5E4B']  # theme Vert



animationOn = False

line = 'Le joueur gagnant est:'
counter = 10

class AnimationGagnant(Tk):
    ""
    def __init__(self, activer, nom='Gabriel', color=color, *args, **kwargs):
        # Appel du constucteur de la classe Tk
        Tk.__init__(self, *args, **kwargs)

        self.centrer_la_fenetre()
        self.nom_du_joueur_gagnant = nom
        self.counter = 10
        global animationOn
        animationOn = activer
        random.shuffle(color)
        self.color = color

        #self.withdraw()

        if animationOn:

            self.deiconify()

            self.title("Gagnant")

            self.config(bg='blue')
            self.geometry(f'{width}x{height}')
            #self.resizable(False,False)
            #self.propagate(0)

            self.frame0 = Frame(self,width = width, height=height)  # ,width=canvas_width,height=canvas_height)
            self.frame0.grid(row=0, column=0)
            #self.frame0.propagate(0)

            #self.frame0.grid_columnconfigure(0, weight=1)
            #self.frame0.grid_rowconfigure(0, weight=1)

            # upper_boarder
            self.frame1 = Frame(self.frame0, height=80, width=width, bg='grey12')
            self.frame1.grid(row=0, column=0)
            #self.frame1.propagate(0)

            #self.frame1.grid_columnconfigure(0, weight=1)
            #self.frame1.grid_rowconfigure(0, weight=1)

            # center_boarder
            self.frame2 = Frame(self.frame0, height=height - 160, width=width, bg='pink')
            self.frame2.grid(row=1, column=0)
            #self.frame2.propagate(0)

            self.c = Canvas(self.frame2, width=width, height=height - 160, bg=color[3], highlightthickness=0)
            self.c.grid(row=0, column=0)


            #self.frame2.grid_columnconfigure(0, weight=1)
            #self.frame2.grid_rowconfigure(0, weight=1)

            # lower_boarder
            self.frame3 = Frame(self.frame0, height=80, width=width, bg='grey12')
            self.frame3.grid(row=2, column=0)
            #self.frame3.propagate(0)

            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)

            self.button1 = Button(self.frame3, text='Fermer', fg='white', bg='grey12', relief='groove', width=20, command=self.fermer)
            self.button1.grid(row=0, column=0, padx=420, pady=30)

            self.frame3.grid_columnconfigure(0, weight=1)
            self.frame3.grid_rowconfigure(0, weight=1)

            self.points_animation(300)

            # self.afficher_gagnant(self.c)
            # self.fermer(self.frame2)

            self.mainloop()

        else:
            pass

    def points_animation(self, n):
        ""
        self.n = n

        numpoints = n
        angle = 137.508
        angle2 = 1.61803
        z = .01
        zz = .01

        cval = 3
        a1 = 495
        a2 = 495
        b1 = 220
        b2 = 220
        count = 0
        scale_increment = 0.00
        scale_decrement = 0.01
        np_liste = [200,300,400,500,600,800]
        cycle_animation = True

        if cycle_animation:
            while self.counter > 0:
                for j in range(numpoints):
                    # Affichage du gagnant
                    if j == numpoints * .6 and self.counter > 9:
                        global line
                        self.label1 = Label(self.frame2, text=line, fg=self.color[3], bg='grey12', font=('Arial', 20))
                        self.label1.grid(row=0, column=0)
                        #counter = 1
                    if j == numpoints * .8:
                        line = self.nom_du_joueur_gagnant
                        self.label1['font'] = ('Arial', 50)
                        self.label1['text'] = line
                    # Création de l'animation
                    count = (count + 1) % 2
                    theta = radians(j * angle)
                    # faire spiral
                    x = cval * sqrt(j) * cos(theta)
                    y = cval * sqrt(j) * sin(theta)

                    xx = random.randrange(0, width)
                    yy = random.randrange(0, height)
                    bgs = 2

                    self.c.create_rectangle(xx + bgs*1.5, yy + bgs*1.5, xx - bgs*1.5, yy - bgs*1.5, fill='grey12', outline="", tags='bgs2')
                    self.c.create_rectangle(xx - bgs, yy - bgs, xx + bgs, yy + bgs, fill=self.color[count + 1], outline="", tags='bgs')
                    self.c.create_rectangle(xx + bgs, yy + bgs, xx - bgs, yy - bgs, fill=self.color[count + 2], outline="", tags='bgs')


                    self.c.create_rectangle(x + a1, y + b1, x + a2, y + b2, fill=self.color[count + 1], outline="",  tags='square')
                    a1 = a1 - zz
                    a2 = a2 + zz
                    b1 = b1 + zz
                    b2 = b2 - zz
                    time.sleep(0.00001)
                    self.c.scale('bgs', 495, 220, 1 - scale_decrement, 1 - scale_decrement)
                    self.c.scale('bgs2', 495, 220, 1 - scale_decrement/2, 1 - scale_decrement/2)
                    self.c.scale('square', 495, 220, 1 + scale_increment, 1 + scale_increment)
                    self.c.update()

                    scale_increment += sin(.0001)
                    scale_decrement += sin(.00001)
                numpoints = random.choice(np_liste)

                self.counter -= 1

            self.fermer()
        else:
            pass

    def fermer(self):
        ""
        self.stopAnimation()
        self.destroy()

    def startAnimation(self):
        global animationOn
        animationOn = True
        #animate()

    def stopAnimation(self):
        global animationOn
        animationOn = False

    def centrer_la_fenetre(self):
        "Permet de centrer la fenêtre avec l'écran"
        # Fonctionne pas toute à fait!
        self.windowWidth = self.winfo_reqwidth()
        self.windowHeight = self.winfo_reqheight()
        # Gets both half the screen width/height and window width/height
        self.positionRight = int(self.winfo_screenwidth() / 2 - self.windowWidth * 2)
        self.positionDown = int(self.winfo_screenheight() / 2 - self.windowHeight * 2)
        # Positions the window in the center of the page.
        centre = self.geometry("{}x{}+{}+{}".format(WIDTH, HEIGHT, self.positionRight, self.positionDown))
        return centre


if __name__ == '__main__':
    #anim = AnimationGagnant('Bingo')
    anim = AnimationGagnant(True)



































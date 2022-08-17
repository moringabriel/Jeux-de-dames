# Auteurs: Sarah Lemieux-Montminy et Gabriel Morin
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tkinter import Tk, Toplevel, Label, NSEW, Radiobutton, Entry, StringVar, Frame, NSEW, Button, PhotoImage, \
    Canvas, NW, NE, E, Scrollbar, font, LEFT, CENTER, IntVar, NORMAL, SUNKEN, W, OptionMenu, RAISED, Menu, ttk, FLAT, \
    GROOVE, RIDGE, messagebox, Text, END, DISABLED, BooleanVar, filedialog, ttk

import tkinter.filedialog
from canvas_damier import CanvasDamier
from partie import Partie
from piece import Piece
from position import Position
import os
from animation_gagnant import AnimationGagnant
import random

myFontIcone = ('Deja Vu', 50)
myFontButton = ('Deja Vu', 20)
myFontTexte = ('Deja Vu', 12)
WIDTH, HEIGHT = 990, 600

nom_joueur_un = ''
nom_joueur_deux = ''

TITREJEU = 'MEGA DAMES'
theme_courant = ''
color = []


class JeuDames(Tk):
    """ Gestionnaire des différentes fenêtres du jeu de dames. Affiche la fenêtre programmée
    dans la classe FenetreDemarrer.

    Attributs:
        nom_joueur_un (StrVar): Le nom du joueur blanc.
        nom_joueur_deux (StrVar): Le nom du joueur noir.
        nom_joueur_courant (StrVar): Le nom du joueur devant effectuer un mouvement.

    """

    def __init__(self, *args, **kwargs):
        """ Constructeur de la classe JeuDames.
        """
        Tk.__init__(self, *args, **kwargs)

        # Les propriétés de base de l'interface Tk
        self.minsize(WIDTH, HEIGHT)
        self.title(TITREJEU)
        self.config(background='grey12', padx=10, pady=10)
        self.wm_iconbitmap('md.ico')

        # Paramètres de jeu
        self.nom_joueur_un = StringVar(value="Joueur 1")
        self.nom_joueur_deux = StringVar(value="Joueur 2")
        self.nom_joueur_courant = StringVar()

        # Centrer la fenêtre avec les dimensions de l'écran
        self.centrer_la_fenetre()

        # Création d'un conteneur servant à contenir les différentes fenêtres
        container = Frame(self)
        container.pack(side="right", fill="both", expand=True)
        container.config(background='dim grey', padx=1, pady=1)

        # Redimension automatique des éléments de l'objet conteneur
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

        # Initialisation d'un dictionnaire de fenêtres
        self.frames = {}

        # Création des fenêtres
        for Fenetre in (FenetreDemarrer, FenetreConfiguration, FenetrePartie, FenetreReglements):
            frame = Fenetre(container, controller=self)
            self.frames[Fenetre] = frame
            frame.grid(row=0, column=0, sticky=NSEW)
            frame.config(background='grey12')
            frame.propagate(0)

        # Mise en avant plan d'une fenêtre de départ
        self.montrer_fenetre(FenetreDemarrer)

    def atteindre_fenetre(self, fenetre):
        """Méthode qui permet d'atteindre les attributs d'un certain objet de type Fenêtre à partir d'une autre classe.

        Args:
            fenetre: Les instances d'objet des différentes classes de fenêtre.

        """

        return self.frames[fenetre]

    def montrer_fenetre(self, fenetre):
        """Méthode qui permet de mettre en avant plan un certain objet de type Fenêtre par le déclenchement d'une
           commande de Widget (command= lambda: controller.montrer_fenetre(Nom_de_la_classe_de_fenêtre)

        Args:
             fenetre: Les instances d'objet des différentes classes de fenêtre.

        """

        # Mise en avant plan de la fenêtre
        frame = self.frames[fenetre]
        frame.tkraise()
        self.actualiser_couleurs()

    def actualiser_couleurs(self):
        """" Méthode qui permet d'actualiser l'état des fenêtres en fonction du déroulement de la partie.

        """

        # couleur index 1 de la liste de couleur du thême courant
        c = color[1]

        # FenetreDemarrer
        self.frames[FenetreDemarrer].frame0['background'] = c
        self.frames[FenetreDemarrer].fd_frame1['background'] = c
        self.frames[FenetreDemarrer].fd_label1['background'] = c

        # FenetreReglement
        self.frames[FenetreReglements].frame4['background'] = c
        self.frames[FenetreReglements].label1['background'] = c
        self.frames[FenetreReglements].label2['background'] = c
        self.frames[FenetreReglements].frame0['background'] = c

        # FenetrePartie
        self.frames[FenetrePartie].frame0['background'] = c
        self.frames[FenetrePartie].canvas_damier.config(background=c, bd=0)
        self.frames[FenetrePartie].joueur['background'] = c
        self.frames[FenetrePartie].label_nom_joueur_courant['background'] = c
        self.frames[FenetrePartie].cadre_points['background'] = c
        self.frames[FenetrePartie].blanc1['background'] = c
        self.frames[FenetrePartie].noir1['background'] = c
        self.frames[FenetrePartie].stat1['background'] = c
        self.frames[FenetrePartie].stat2['background'] = c
        self.frames[FenetrePartie].stat3['background'] = c
        self.frames[FenetrePartie].stat4['background'] = c
        self.frames[FenetrePartie].stat5['background'] = c
        self.frames[FenetrePartie].stat6['background'] = c
        self.frames[FenetrePartie].cadre_informations['background'] = c
        self.frames[FenetrePartie].cadre_boutons['background'] = c
        self.frames[FenetrePartie].tour_joueur['background'] = c
        self.frames[FenetrePartie].joueur['background'] = c
        self.frames[FenetrePartie].jouer_cadre['background'] = c

        # Désactive la méthode montrer_position_sources()
        self.frames[FenetrePartie].montrer_positions_sources = False

    def centrer_la_fenetre(self):
        """ Méthode qui permet de centrer la fenêtre avec l'écran.

        """

        # Assigner les dimensions du widget référant aux dimensions de la fenêtre
        self.windowWidth = self.winfo_reqwidth()
        self.windowHeight = self.winfo_reqheight()

        # Récupérer la largeur et la hauteur de l'écran/2 et la largeur et la hauteur de la fenêtre
        self.positionRight = int(self.winfo_screenwidth() / 2 - self.windowWidth * 2)
        self.positionDown = int(self.winfo_screenheight() / 2 - self.windowHeight * 2)

        # Centrer la fenêtre avec le centre de l'écran
        centre = self.geometry("{}x{}+{}+{}".format(WIDTH, HEIGHT, self.positionRight, self.positionDown))
        return centre

    def afficher_historique(self):
        """ Méthode qui permet l'affichage en Toplevel d'un objet de la classe FenetreHistorique.

        """

        # Ouverture de la fenêtre historique
        fenetre_historique = FenetreHistorique(self)
        self.wait_window(fenetre_historique)


class FenetreHistorique(Toplevel):
    """ Interface graphique de la classe FenetreHistorique.

    Description:
        Fenêtre qui affiche l'historique de chacun des déplacements de la partie courante et qui offre au joueur
        la possibilité de sauvegarder cet historique sur un fichier.txt. Pour ce faire, la méthode accède à un fichier
        temporaire écrit lors de l'exécution du bouton Afficher l'historique de la fenêtre FenêtrePartie.

    """

    def __init__(self, master):
        """Constructeur de la classe FenetreHistorique.
        """
        super().__init__(master)

        # Attributs
        # Pour l'ouverture du fichier text
        self.texte = ""
        # Pour la lecture du fichier text
        self.gamedata = ""

        # Paramètres
        self.wm_maxsize(472, HEIGHT)
        self.config(background='grey12', padx=10, pady=10)
        self.resizable(False, False)

        # Contrôle de l'application
        self.centrer_la_fenetre()
        self.master = master
        self.transient(master)
        self.grab_set()

        # Titre de la fenêtre
        self.label_h1 = Label(self, bg='grey12', fg='white', text='Historique', font=myFontButton)
        self.label_h1.grid(row=0)

        # Widget text pour l'affichage du fichier PartieCourante_FichierTemporaire.txt
        self.text_h1 = Text(self)
        self.text_h1.grid(row=1)

        #  Gestion d'erreurs pour récupérer le fichier temporaire d'historique
        try:
            # Ouverture du fichier
            self.texte = open('PartieCourante_FichierTemporaire.txt', 'r')
            # Sauvegarde en mémoire du fichier
            self.gamedata = self.texte.readlines()
        except IOError:
            # Sauvegarde en mémoire du fichier
            self.gamedata = 'Fichier endommagé. Vous pouvez réessayer.'

        # Écriture du fichier dans le widget text
        for x in self.gamedata:
            self.text_h1.insert(END, x)

        # Cadre pour contenir les boutons
        self.cadre_bouton_h1 = Frame(self, bg='grey12')
        self.cadre_bouton_h1.grid(row=2)

        # Boutons pour la sauvegarde du fichier text
        self.button_h1 = Button(self.cadre_bouton_h1, text='Enregistrer', relief=GROOVE, bd=2, width=24,
                                command=self.enregistrer_txt)
        self.button_h1.grid(row=0, column=0, padx=10, pady=(15, 5))

        # Bouton pour fermer la fenêtre Toplevel
        self.button_h2 = Button(self.cadre_bouton_h1, text='Fermer', relief=GROOVE, bd=2, width=24,
                                command=self.fermer)
        self.button_h2.grid(row=0, column=1, padx=10, pady=(15, 5))

        # Redimension automatique des éléments de la fenêtre
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def enregistrer_txt(self):
        """ Méthode qui permet la sauvegarde sur un fichier.txt de l'historique de la partie courante

        """

        # Fenêtre de dialogue qui permet de choisir une destination de sauvegarde
        f = tkinter.filedialog.asksaveasfile(mode='w', defaultextension=".txt")
        if f is None:
            return
        # Récupération de l'information à sauvegarder
        text2save = str(self.text_h1.get(1.0, END))
        # Écriture du fichier.txt
        f.write(text2save)
        f.close()

    def fermer(self):
        """ Méthode qui permet la fermeture de la fenêtre Toplevel FenêtreHistorique

        """

        # Bouton pour fermer la fenêtre Toplevel
        self.text_h1.config(state=NORMAL)
        self.text_h1.delete(1.0, END)

        # On redonne le contrôle au parent.
        self.grab_release()
        self.master.focus_set()
        self.destroy()

    def centrer_la_fenetre(self):
        """ Méthode qui permet de centrer la fenêtre avec l'écran.

        """

        # Assigner les dimensions du widget référant aux dimensions de la fenêtre
        self.windowWidth = self.winfo_reqwidth()
        self.windowHeight = self.winfo_reqheight()

        # Récupérer la largeur et la hauteur de l'écran/2 et la largeur et la hauteur de la fenêtre
        self.positionRight = int(self.winfo_screenwidth() / 2 - self.windowWidth * 2)
        self.positionDown = int(self.winfo_screenheight() / 2 - self.windowHeight * 2)

        # Centrer la fenêtre avec le centre de l'écran
        centre = self.geometry("{}x{}+{}+{}".format(WIDTH, HEIGHT, self.positionRight, self.positionDown))
        return centre


class FBase(Frame):
    """ Interface graphique de la classe FBase.

    Description:
        Création de la classe FBase, qui sert de parent aux classes correspondant aux fenêtres subséquentes.

    Attributs:
        self.themes (liste): Choix de thèmes de couleurs
        self.color1 (liste): Liste de couleurs associées au thème Base
        self.color2 (liste): Liste de couleurs associées au thème Bleu
        self.color3 (liste): Liste de couleurs associées au thème Orange
        self.color4 (liste): Liste de couleurs associées au thème Vert

    """

    def __init__(self, parent, controller):
        """ Constructeur de la class FBase. Définitons d'attributs de base.
        """
        Frame.__init__(self, parent)

        # Contrôleur
        self.controller = controller

        # Attributs des couleurs

        # Choix du thème de couleur
        self.theme_courant = 'Base'

        # Liste des thèmes possibles
        self.themes = ['Base', 'Bleu', 'Orange', 'Vert']

        # Palette thème Base
        self.color1 = ['white', '#25303B', 'grey12', 'azure4']
        # Palette thème Bleu
        self.color2 = ['white', '#61809E', 'lightblue', '#F2C53D']
        # Palette thème Orange
        self.color3 = ['white', '#DA9C57', '#191B46', '#ACBEFF']
        # Palette thème Vert
        self.color4 = ['white', '#71A16C', '#2F363F', '#EF5E4B']

        # Palette de couleurs sélectionnées pour l'interface
        self.color = self.choix_de_theme()

        # Cadre de base
        self.frame0 = Frame(self, background=self.color[1], width=WIDTH, height=HEIGHT)
        self.frame0.grid(row=0, column=0, sticky=NSEW)
        self.frame0.config(padx=10, pady=10)

        # Redimension automatique des éléments de la fenêtre
        self.frame0.grid_columnconfigure(0, weight=1)
        self.frame0.grid_rowconfigure(0, weight=1)

    def choix_de_theme(self):
        """ Méthode qui gère l'assignation de la palette de couleur en fonction du thème de couleurs choisi.

            return:
                self.color (liste): couleurs associées au thème courant
        """

        if self.theme_courant == self.themes[0]:
            # Palette thème Base
            self.color = self.color1
        elif self.theme_courant == self.themes[1]:
            # Palette thème Bleu
            self.color = self.color2
        elif self.theme_courant == self.themes[2]:
            # Palette thème Orange
            self.color = self.color3
        else:
            # Palette thème vert
            self.color = self.color4

        global color
        # Mise à jour de la variable globale pour avoir un accès actualisé
        color = (self.color)
        return self.color


class FenetreDemarrer(FBase):
    """ Interface graphique de la classe FenetreDemarrer.

    Description:
        Fenêtre d'accueil du jeu. Permet d'accéder à la configuration du jeu avant l'accès à la partie.

    """

    def __init__(self, parent, controller):
        """ Constructeur de la class FenetreDemarrer. Disposition des «widgets» dans la fenêtre.
        """
        FBase.__init__(self, parent, controller)

        # Cadre principal
        self.fd_frame1 = Frame(self.frame0, bg=self.color[1], width=WIDTH, height=HEIGHT)
        self.fd_frame1.grid(row=0, column=0, padx=10, pady=10)

        # Titre
        self.fd_label1 = Label(self.fd_frame1, fg=self.color[0], bg=self.color[1], text=TITREJEU, font=myFontIcone)
        self.fd_label1.grid(column=0, row=0)

        # Bouton démarrer pour accéder à la configuration
        self.fd_button1 = Button(self.fd_frame1, borderwidth=0, state='normal',
                                 relief=GROOVE, bd=3, text=">>>>>>>>>>>>>  DÉMARRER  <<<<<<<<<<<<<", font=('Arial', 16),
                                 command=lambda: controller.montrer_fenetre(FenetreConfiguration))
        self.fd_button1.grid(row=1, padx=10, pady=10, sticky=NSEW)

        # Redimension automatique des éléments de la fenêtre
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)


class FenetreReglements(FBase):
    """ Interface graphique de la classe FenetreReglement.

    Description:
        Fenêtre permettant l'affichage des règles du jeu.

    """

    def __init__(self, parent, controller):
        """ Constructeur de la class FenetreReglement. On dispose les «widgets» dans la fenêtre
        pour visualiser les règlements du jeu.
        """
        FBase.__init__(self, parent, controller)

        # Main frame
        self.frame4 = Frame(self.frame0, bg=self.color[1], width=WIDTH, height=HEIGHT)
        self.frame4.grid(row=0, column=0, padx=10, pady=10)

        # Label règlements
        self.label1 = Label(self.frame4, text='RÈGLEMENTS', fg='white')
        self.label1.grid(row=0, column=0, padx=10, pady=10)
        self.label1['font'] = myFontButton

        # Texte Règlements
        reglement = """ 
                          • Un damier de 8 cases par 8 contient 24 pièces (12 blanches, 12 noires);
                          • Le joueur avec les pièces blanches commence en premier ;
                          • Une pièce de départ est appelée un pion et peut se déplacer en diagonale vers l’avant
                            (vers le haut pour les blancs, vers le bas pour les noirs). Une case doit être libre pour
                            pouvoir s’y déplacer ;
                          • Lorsqu’un pion atteint le côté opposé du plateau, il devient une dame. Cette action se
                            nomme la promotion. Une dame possède aussi la particularité de se déplacer vers l’arrière
                            (toujours en diagonale) ;
                          • Une prise est l’action de « manger » une pièce adverse. Elle est effectuée en sautant
                            par-dessus la pièce adverse, toujours en diagonale, vers l’avant ou l’arrière. On ne
                            peut sauter par-dessus qu’une pièce adverse à la fois : la case d’arrivée doit donc être
                            libre ;
                          • Après une prise, le joueur courant peut effectuer une (ou plusieurs) prise(s) 
                            supplémentaire(s) en utilisant la même pièce ;
                          • Lors du tour d’un joueur, si celui-ci peut prendre une pièce ennemie, il doit absolument
                            le faire (on ne peut pas déplacer une pièce s’il était possible d’effectuer une prise) ;
                          • Lorsqu’un joueur commence son tour et prend une pièce adverse, s’il peut continuer son tour 
                            en continuant de prendre des pièces adverses avec la même pièce, il doit le faire.
                          """

        # Label titre règlements
        self.label2 = Label(self.frame4, text=reglement, fg=self.color[0], bg=self.color[1], justify=LEFT)
        self.label2.grid(row=1, padx=10, pady=10)
        self.label2['font'] = myFontTexte

        # Bouton retour à la configuration
        self.bouton1 = Button(self.frame4, text='Retour', highlightthickness=1, bd=3, relief=GROOVE, width=20,
                              command=lambda: controller.montrer_fenetre(FenetreConfiguration))
        self.bouton1.grid(row=2, padx=10, pady=10)

        # Truc pour le redimensionnement automatique des éléments de la fenêtre.
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Truc pour le redimensionnement automatique des éléments de la fenêtre.
        self.frame4.grid_columnconfigure(0, weight=1)
        self.frame4.grid_rowconfigure(0, weight=1)


class FenetreConfiguration(FBase):
    """ Interface graphique de la classe FenetreConfiguration.

    Description:
        Fenêtre permettant la configuration du jeu avant ou pendant la partie.

    Attributs:
         op1 (OptionMenu) : Widget pour la selection d'un thème de couleurs.
         choix_theme (str) : Variable pour contenir la sélection du thème choisi. Thème Base par défaut.
         entrer_nom_joueur_un (Entry) : Widget pour la saisie du nom. La valeur par défaut est Joueur 1.
         nom_joueur_un (str) : Variable pour contenir la saisie du nom du joueur 1.
         entrer_nom_joueur_un (Entry) : Widget pour la saisie du nom. La valeur par défaut est Joueur 2.
         nom_joueur_deux (str) : Variable pour contenir la saisie du nom du joueur 2.
         boutonJouer (Button) : Permet d'accéder et d'afficher la fenêtre FenetrePartie
                                ainsi que de démarrer la partie.

    """

    def __init__(self, parent, controller):
        """ Constructeur de la classe FenetreConfiguration. On initialise les paramètres de configuration et
        on dispose les «widgets» dans la fenêtre.
        """
        FBase.__init__(self, parent, controller)

        self.choix_theme = StringVar()

        # Cadre principal
        self.frame2 = Frame(self.frame0, borderwidth=0, background=self.color[1], width=HEIGHT, height=HEIGHT)
        self.frame2.grid(row=0, padx=1, pady=1)

        # Partie Titre
        self.titre = Label(self.frame2, fg=self.color[0], bg=self.color[1], text=TITREJEU, font=myFontIcone)
        self.titre.grid(columnspan=2, row=0, padx=5, pady=5)

        # Cadre sélection de thème
        self.frame3 = Frame(self.frame2, bg=self.color[1], bd=2)
        self.frame3.grid(row=1, columnspan=2, pady=(10, 5))

        # Label sélection de thème
        self.label1 = Label(self.frame3, fg=self.color[0], bg=self.color[1], text="Sélection de thème", width=20)
        self.label1.grid(column=0, row=0, padx=0)

        # Menu sélection du thème de couleurs
        self.choix_theme.set(self.themes[0])
        self.op1 = OptionMenu(self.frame3, self.choix_theme, *self.themes, command=self.recuperer_theme)
        self.op1.config(highlightthickness=1, relief=RAISED, width=20)
        self.op1.grid(column=1, row=0, padx=(0, 40))

        # Section des noms des joueurs. Permet une entrée optionnelle des noms des joueurs.

        # Variables d'interface
        entryWidth = 28
        entryPadx = 14

        # Joueur un
        self.cadreJoueur1 = Frame(self.frame3, bg=self.color[1], bd=2)
        self.cadreJoueur1.grid(row=3, column=0, padx=(30, 0), pady=(0, 20))

        # Couleur du joueur un
        self.label1_joueur_un = Label(self.cadreJoueur1, bg=self.color[1], fg='white', text="BLANC")
        self.label1_joueur_un.grid(row=1, column=0, padx=10, pady=10, sticky='WE')
        self.label2_joueur_un = Label(self.cadreJoueur1, bg=self.color[1], fg='white', text="Nom:")
        self.label2_joueur_un.grid(row=2, column=0, padx=entryPadx, pady=1, sticky='W')

        # Entrée du joueur un
        self.entrer_nom_joueur_un = Entry(self.cadreJoueur1, width=entryWidth,
                                          textvariable=self.controller.nom_joueur_un)
        self.entrer_nom_joueur_un.grid(row=3, column=0, padx=10, pady=1)

        # Joueur deux
        self.cadreJoueur2 = Frame(self.frame3, bg=self.color[1])
        self.cadreJoueur2.grid(row=3, column=1, padx=(0, 30), pady=(0, 20))

        # Couleur du joueur deux
        self.label1_joueur_deux = Label(self.cadreJoueur2, bg=self.color[1], fg='white', text="NOIR")
        self.label1_joueur_deux.grid(row=1, column=0, padx=10, pady=10, sticky='WE')
        self.label2_joueur_deux = Label(self.cadreJoueur2, bg=self.color[1], fg='white', text="Nom:")
        self.label2_joueur_deux.grid(row=2, column=0, padx=10, pady=1, sticky='W')

        # Entrée du joueur deux
        self.entrer_nom_joueur_deux = Entry(self.cadreJoueur2, width=entryWidth,
                                            textvariable=self.controller.nom_joueur_deux)
        self.entrer_nom_joueur_deux.grid(row=3, column=0, padx=entryPadx, pady=1)

        # Bouton Jouer pour lancer la partie
        self.boutonJouer = Button(self.frame3, highlightthickness=1, bd=3, relief=GROOVE,
                                  text=">>>>>>>>>>>  JOUER  <<<<<<<<<<<", font=('Arial', 12), height=1, width=41,
                                  command=self.demarrer_partie)
        self.boutonJouer.grid(row=4, columnspan=2, pady=10)

        # Règlement ou quitter
        self.cadreMenu = Frame(self.frame3, bg=self.color[1])
        self.cadreMenu.grid(row=5, columnspan=2, padx=10, pady=10)

        # Lire règlements
        self.boutonInfo = Button(self.cadreMenu, text='Réglements',
                                 font=('Arial', 10), relief=GROOVE,
                                 width=20, command=lambda: controller.montrer_fenetre(FenetreReglements))
        self.boutonInfo.grid(row=1, column=0, padx=20, pady=20)

        # Quitter
        self.boutonQuitter = Button(self.cadreMenu, highlightthickness=1, bd=3, text='Quitter', font=('Arial', 10),
                                    relief=GROOVE,
                                    width=20, command=self.quitter_la_partie)
        self.boutonQuitter.grid(row=1, column=1, padx=20, pady=20)

        # Truc pour le redimensionnement automatique des éléments de la fenêtre.
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def demarrer_partie(self):
        """ Méthode qui permet le démarrage de la partie.

        """

        # Affichage de la FenetrePartie
        self.controller.nom_joueur_courant.set(self.controller.nom_joueur_un.get().capitalize())
        self.controller.montrer_fenetre(FenetrePartie)

    def recuperer_theme(self, event):
        """ Méthode qui permet de récupérer le thème courant choisi et la liste de couleurs associées.
           De plus, les couleurs de l'objet de cette classe seront actualisées et seront assignées à une variable
           globale.

        Args:
            event (tkinter.Event): Objet décrivant l'évènement qui a causé l'appel de la méthode.

        Attributes:
            theme_courant (str): Le thème choisi par l'utilisateur. Thème Base par défaut
            color (list): Liste de couleurs associées au thème courant

        """

        global theme_courant
        global color

        # Récupérer le thème courant
        self.theme_courant = self.choix_theme.get()

        # Assignation à la variable globale
        theme_courant = self.theme_courant
        color = self.choix_de_theme()

        # Actualiser la fenêtre
        self.actualiser_couleurs()

    def actualiser_couleurs(self):
        """ Méthode qui permet d'actualiser la couleur des différents widget de la classe en fonction du thème choisi.
           L'actualisation de cette fenêtre (classe FenetreConfiguration) se fait au moment de la selection d'un thème.

        Attributs:
            color (list): Liste de couleurs correspondant au thème courant

        """

        # Liste de couleurs
        c1 = self.color[1]

        # Widgets à actualiser
        self.frame3["background"] = c1
        self.frame2["background"] = c1
        self.titre["background"] = c1
        self.frame3["background"] = c1
        self.frame3["background"] = c1
        self.label1["background"] = c1
        self.cadreJoueur1["background"] = c1
        self.label1_joueur_un["background"] = c1
        self.label2_joueur_un["background"] = c1
        self.cadreJoueur2["background"] = c1
        self.label1_joueur_deux["background"] = c1
        self.label2_joueur_deux["background"] = c1
        self.cadreMenu["background"] = c1
        self.frame0["background"] = c1

    def quitter_la_partie(self):
        """ Méthode qui permet de quitter la partie en supprimant le fichier temporaire d'historique de partie:
           PartieCourante_FichierTemporaire.txt

        """

        # Gestion d'erreur si le fichier est absent.
        try:
            # Supprimer le fichier temporaire
            os.remove('PartieCourante_FichierTemporaire.txt')
        except IOError:
            pass
        quit()


class FenetrePartie(FBase):
    """ Interface graphique du jeu de dames.

    Attributs:
        controller (): Permet l'affichage de la fenêtre.
        partie (Partie): Le gestionnaire de la partie de dame.
        canvas_damier (CanvasDamier): Le «widget» gérant l'affichage du damier à l'écran.
        messages (Label): Un «widget» affichant des messages à l'utilisateur du programme.
        couleur_joueur_courant (str): La couleur du joueur devant effectuer le prochain mouvement.
        position (Position): Les coordonnées de la case sélectionnée.
        position_source (Position): Les coordonnées de la position source sélectionnée.
        position_cible (Position): Les coordonnées de la position cible sélectionnée.
        doit_prendre (bool): Un booléen indiquant si le joueur actif doit absolument effectuer une prise
            de pièce. True s'il doit en prendre une, False autrement.
        position_source_forcee (Position): Coordonnées de la pièce devant continuer son mouvement après une prise.
        sauvegarde_source_forcee (Position): Sauvegarde en mémoire de la dernière position source forcée pour la
            réassigner lors de l'annulation du dernier mouvement.
        derniere_position_source (Position): Sauvegarde en mémoire de la dernière position source pour la
            réassigner lors de l'annulation du dernier mouvement.
        derniere_position_cible (Position): Sauvegarde en mémoire de la dernière position cible pour la
            réassigner lors de  l'annulation du dernier mouvement.
        derniere_position_piece_prise (Position): Sauvegarde en mémoire de la dernière position d'une pièce prise
            pour la réassigner lors de l'annulation du dernier mouvement.
        derniere_piece_position_source (Piece): Sauvegarde en mémoire de la dernière pièce d'une position source
            pour la réassigner lors de l'annulation du dernier mouvement.
        derniere_piece_position_cible (Piece): Sauvegarde en mémoire de la dernière pièce d'une position cible
            pour la réassigner lors de l'annulation du dernier mouvement.
        derniere_piece_prise (Piece): Sauvegarde en mémoire de la dernière pièce prise pour la réassigner lors
            de l'annulation du dernier mouvement.
        dernier_message (str): Sauvegarde en mémoire du dernier message pour le réassigner lors
            de l'annulation du dernier mouvement.
        pieces_prises_blanches (int): Le nombre de pièces noires prises par le joueur blanc.
        pieces_prises_noires (int): Le nombre de pièces blanches prises par le joueur noir.
        pieces_restantes_blanches (int): Le nombre de pièces blanches restantes sur le jeu.
        pieces_restantes_noires (int): Le nombre de pièces noires restantes sur le jeu.
        montrer_positions_sources (bool): Un booléen indiquant si l'utilisateur a choisi d'activer l'option
            affichant les positions sources valides. True si elle est activée, False autrement.
        liste_positions (list): Une liste de déplacements (Position) permettant l'affichage d’un
            historique de la partie courante.
        liste_couleur_joueur_courant (list): Une liste de la couleur (str) du joueur courant pour
            l'associer la valeur d'une position source et cible courante.

    """

    def __init__(self, parent, controller):
        """ Constructeur de la classe FenetrePartie. On initialise une partie en utilisant la classe Partie du TP3 et
        on dispose les «widgets» dans la fenêtre. Initialise les attributs à leur valeur par défaut.

        """
        FBase.__init__(self, parent, controller)

        # La partie
        self.partie = Partie()

        # Création du canvas damier.
        self.canvas_damier = CanvasDamier(self.frame0, self.partie.damier, 60)
        self.canvas_damier.grid(column=0, padx=(10, 0), pady=10, row=0, sticky=NSEW)
        self.canvas_damier.bind('<Button-1>', self.selectionner)

        # Couleur joueur courant
        self.couleur_joueur_courant = "blanc"

        # Attributs de départ du jeu
        self.position = None
        self.position_source = None
        self.position_cible = None
        self.doit_prendre = False
        self.position_source_forcee = None
        self.sauvegarde_source_forcee = None
        self.derniere_position_source = None
        self.derniere_position_cible = None
        self.derniere_piece_position_source = None
        self.derniere_piece_position_cible = None
        self.derniere_piece_prise = None
        self.derniere_position_piece_prise = None
        self.dernier_message = None
        self.pieces_prises_blanches = 0
        self.pieces_prises_noires = 0
        self.pieces_restantes_blanches = 12
        self.pieces_restantes_noires = 12
        self.montrer_positions_sources = False

        # Listes utilisées pour la sauvegarde de l'historique
        self.liste_positions = []
        self.liste_couleur_joueur_courant = []

        # Truc pour le redimensionnement automatique des éléments de la fenêtre.
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Colonne d'informations à droite

        # Attributs d'interface
        messages_label_width = 48
        action_button_width = 30
        WrapLength = 280
        points_padx = 20
        points_pady = 2
        points_font = ('Arial', 10)
        w = 4
        pd = 5
        bdw = 3
        pad = 0

        # Cadre colonne
        self.cadre_informations = Frame(self.frame0, bg=self.color[1])
        self.cadre_informations.grid(column=1, row=0, padx=(0, 10), pady=0, sticky=NSEW)

        # Titre
        self.tour_joueur = Label(self.cadre_informations, bg=self.color[1], fg=self.color[0], text="Tour du joueur",
                                 font=('Arial', 30), width=15)
        self.tour_joueur.grid(column=0, row=0, padx=10, pady=0)

        # Cadre tour du joueur
        self.jouer_cadre = Frame(self.cadre_informations, bg=self.color[1])
        self.jouer_cadre.grid(row=1)

        # Étiquette indiquant la couleur du joueur courant
        self.joueur = Label(self.jouer_cadre, fg=self.color[0], bg=self.color[1], text='Blanc', width=16)
        self.joueur.grid(column=0, row=0, padx=pad * 1.5, pady=pad)

        # Étiquette nom du joueur courant
        self.label_nom_joueur_courant = Label(self.jouer_cadre, fg=self.color[0], bg=self.color[1],
                                              textvariable=self.controller.nom_joueur_courant, width=16)
        self.label_nom_joueur_courant.grid(column=1, row=0, padx=pad * 1.5, pady=pad)

        # Cadre messages
        self.cadre_messages = Frame(self.cadre_informations, bg='white', relief=SUNKEN, bd=3, height=110, width=300)
        self.cadre_messages.grid(column=0, row=2, padx=10, pady=10, sticky=NSEW)
        self.cadre_messages.grid_propagate(False)

        # Ajout d'une étiquette informant le joueur des actions à effectuer et des erreurs.
        self.message_jeu = Label(self.cadre_messages, bg='white', width=messages_label_width,
                                 wraplength=WrapLength, anchor=W, justify=LEFT)
        self.message_jeu.grid(column=0, row=0, padx=10)

        # Ajout d'une étiquette affichant les messages relatifs aux positions sources
        self.message_position_source = Label(self.cadre_messages, bg='white',
                                             text='Veuillez sélectionner la pièce à déplacer.',
                                             width=messages_label_width, wraplength=WrapLength, anchor=W, justify=LEFT)
        self.message_position_source.grid(column=0, row=1, padx=10)

        # Ajout d'une étiquette affichant les messages relatifs aux positions cibles
        self.message_position_cible = Label(self.cadre_messages, bg='white', width=messages_label_width,
                                            wraplength=WrapLength, anchor=W, justify=LEFT)
        self.message_position_cible.grid(column=0, row=2, padx=10)

        # Cadre des statistiques de la partie
        self.cadre_points = Frame(self.cadre_informations, bg=self.color[1])
        self.cadre_points.grid(column=0, row=4)

        # Section pièces blanches
        self.blanc1 = Frame(self.cadre_points, bg=self.color[1])
        self.blanc1.grid(column=0, row=0)

        # Pièces blanches restantes
        self.stat1 = Label(self.blanc1, text='Blanc', bg=self.color[1], fg=self.color[0])
        self.stat1.grid(columnspan=2, row=0)
        self.stat2 = Label(self.blanc1, text='Pièce(s):', bg=self.color[1], fg=self.color[0])
        self.stat2.grid(column=0, row=1)
        self.blanches_restantes = Label(self.blanc1, bg='#D1DFEB', width=w,
                                        text='{:2}'.format(self.pieces_restantes_blanches), font=points_font, bd=2,
                                        relief=SUNKEN)
        self.blanches_restantes.grid(column=1, row=1, padx=points_padx, pady=points_pady)

        # Pièces blanches prises
        self.stat3 = Label(self.blanc1, text='Prise(s):', bg=self.color[1], fg=self.color[0])
        self.stat3.grid(column=0, row=2)
        self.blanches_prises = Label(self.blanc1, bg='#D1DFEB', width=w,
                                     text='{:2}'.format(self.pieces_prises_blanches), font=points_font, bd=2,
                                     relief=SUNKEN)
        self.blanches_prises.grid(column=1, row=2, padx=points_padx, pady=points_pady)

        # Section pièces noires
        self.noir1 = Frame(self.cadre_points, bg=self.color[1])
        self.noir1.grid(column=1, row=0)

        # Pièces noires restantes
        self.stat4 = Label(self.noir1, text='Noir', bg=self.color[1], fg=self.color[0])
        self.stat4.grid(columnspan=2, row=0)
        self.stat5 = Label(self.noir1, text='Pièce(s):', bg=self.color[1], fg=self.color[0])
        self.stat5.grid(column=0, row=1)
        self.noires_restantes = Label(self.noir1, bg='#D1DFEB', width=w,
                                      text='{:2}'.format(self.pieces_restantes_noires), font=points_font, bd=2,
                                      relief=SUNKEN)
        self.noires_restantes.grid(column=1, row=1, padx=points_padx, pady=points_pady)

        # Pièces noires prises
        self.stat6 = Label(self.noir1, text='Prise(s):', bg=self.color[1], fg=self.color[0])
        self.stat6.grid(column=0, row=2)
        self.noires_prises = Label(self.noir1, bg='#D1DFEB', width=w,
                                   text='{:2}'.format(self.pieces_prises_noires), font=points_font, bd=2, relief=SUNKEN)
        self.noires_prises.grid(column=1, row=2, padx=points_padx, pady=points_pady)

        # Truc pour le redimensionnement automatique des éléments de la fenêtre.
        self.cadre_points.grid_columnconfigure(0, weight=1)
        self.cadre_points.grid_rowconfigure(0, weight=1)

        # Cadre section des boutons
        self.cadre_boutons = Frame(self.cadre_informations, bg=self.color[1])
        self.cadre_boutons.grid(column=0, row=5, padx=20, pady=20, sticky=NSEW)

        # Bouton Afficher positions sources possibles
        self.afficher_positions_sources = Button(self.cadre_boutons, text='Afficher positions sources possibles',
                                                 relief=GROOVE, bd=bdw, width=action_button_width)
        self.afficher_positions_sources.grid(row=0, padx=pd, pady=pd)
        self.afficher_positions_sources.bind('<Button-1>', self.depart_positions_sources)
        self.afficher_positions_sources.bind('<Double-Button-1>', self.cacher_depart_positions_sources)

        # Bouton Annuler le dernier déplacement
        self.annuler_mouvement = Button(self.cadre_boutons, text='Annuler le dernier mouvement', relief=GROOVE,
                                        bd=bdw, width=action_button_width, state='disable')
        self.annuler_mouvement.grid(row=1, padx=pd, pady=pd)
        self.annuler_mouvement.bind('<Button-1>', self.annuler_dernier_mouvement)

        # Bouton Afficher l'historique
        self.afficher_historique = Button(self.cadre_boutons, text="Afficher l'historique", state='disable',
                                          relief=GROOVE, bd=bdw, width=action_button_width,
                                          command=lambda: controller.afficher_historique())
        self.afficher_historique.grid(row=2, padx=pd, pady=pd)
        self.afficher_historique.bind('<Button-1>', self.enregistrer_liste_deplacements)

        # Bouton Réglages
        self.bouton_configuration = Button(self.cadre_boutons, text='Réglages',
                                           relief=GROOVE, bd=bdw, width=action_button_width,
                                           command=lambda: controller.montrer_fenetre(FenetreConfiguration))
        self.bouton_configuration.grid(row=3, padx=pd, pady=pd)

        # Bouton Nouvelle partie
        self.nouvelle_partie = Button(self.cadre_boutons, text='Nouvelle partie',
                                      relief=GROOVE, bd=bdw, width=action_button_width)  # ,
        # command=lambda: controller.montrer_fenetre(FenetreConfiguration))
        self.nouvelle_partie.grid(row=4, padx=pd, pady=pd)

        # Mise à zéro des attributs
        self.nouvelle_partie.bind('<Button-1>', self.recharge_nouvelle_partie)

        # Bouton Quitter
        self.quitter = Button(self.cadre_boutons, text='Quitter', relief=GROOVE, bd=bdw,
                              width=action_button_width, command=self.quitter_la_partie)
        self.quitter.grid(row=5, padx=pd, pady=pd)

        # Truc pour le redimensionnement automatique des éléments de la fenêtre.
        self.cadre_boutons.grid_columnconfigure(0, weight=1)
        self.cadre_boutons.grid_rowconfigure(0, weight=1)

    def selectionner(self, event):
        """ Méthode qui gère le clic de souris sur le damier. Met aussi à jour les différentes étiquettes
        informant le joueur du déroulement du jeu.

        Args:
            event (tkinter.Event): Objet décrivant l'évènement qui a causé l'appel de la méthode.

        """

        # On trouve le numéro de ligne/colonne en divisant les positions en y/x par le nombre de pixels par case.
        ligne = event.y // self.canvas_damier.n_pixels_par_case
        colonne = event.x // self.canvas_damier.n_pixels_par_case
        self.position = Position(ligne, colonne)


        # Activer les boutons Annuler le dernier mouvement et Afficher l'historique
        if self.position is None:
            pass
        else:
            self.annuler_mouvement['state'] = 'normal'
            self.afficher_historique['state'] = 'normal'

        # On récupère l'information sur la pièce à l'endroit choisi.
        piece = self.partie.damier.recuperer_piece_a_position(self.position)

        # Sauvegarde de la couleur du joueur courant dans une liste pour l'historique.
        self.liste_couleur_joueur_courant.append(self.couleur_joueur_courant)

        # Si la partie est terminée.
        if self.message_jeu['text'] == "Partie terminée! Pour rejouer, appuyer sur Nouvelle partie.":
            self.message_position_source['text'] = 'La partie est terminée. Veuillez appuyer sur Nouvelle partie ' \
                                                   'pour rejouer.'
            self.message_position_source['fg'] = 'red'

        else:
            # Si aucune position source n'a encore été sélectionnée.
            if self.position_source is None:

                # Vérifie si la position source sélectionnée est valide.
                if self.position_source_valide(self.position)[0] is True:

                    # Sauvegarde des positions dans une liste pour l'historique.
                    self.liste_positions.append(self.position)

                    # Mise à jour des étiquettes d'informations sur le jeu.
                    self.message_position_source['text'] = 'Position source: {}.'.format(self.position)
                    self.message_position_source['fg'] = 'black'
                    self.message_position_cible['text'] = 'Veuillez sélectionner la case cible.'
                    self.message_position_cible['fg'] = 'black'

                    # Mise à jour des variables membres
                    self.position_source = self.position
                    self.derniere_position_source = self.position
                    self.derniere_piece_position_source = self.partie.damier.recuperer_piece_a_position(self.position)

                    # Indicateur utilisé dans la méthode afficher_positions_cibles de la classe CanvasDamier pour
                    # indiquer si la pièce doit faire une prise ou non.
                    if not self.doit_prendre:
                        indicateur = 1
                    else:
                        indicateur = 2

                    self.canvas_damier.afficher_positions_cibles(self.position, indicateur)

                # Si la position source n'est pas valide.
                else:
                    self.message_position_source['text'] = \
                        'Position invalide. {} Sélectionnez une nouvelle case.'.format(
                            self.position_source_valide(self.position)[1])
                    self.message_position_source['fg'] = 'red'

            # Si la position sélectionnée correspond à la position cible.
            else:

                # Vérifie si la position cible est valide. Si c'est le cas, met à jour les étiquettes d'informations
                # et les variables membres avant d'effectuer le mouvement.
                if self.position_cible_valide(self.position)[0] is True:
                    self.message_position_cible['text'] = 'Position source: {}.'.format(self.position)
                    self.message_position_cible['fg'] = 'black'
                    self.position_cible = self.position
                    self.derniere_position_cible = self.position
                    self.derniere_piece_position_cible = self.partie.damier.recuperer_piece_a_position(self.position)
                    self.dernier_message = self.message_jeu['text']
                    self.tour()

                # Si la position cible n'est pas valide.
                else:
                    self.message_position_source['text'] = \
                        'Position invalide. {} Sélectionnez une nouvelle case.'.format(
                            self.position_source_valide(self.position)[1])
                    self.message_position_source['fg'] = 'red'

                # Sauvegarde dans une liste des positions pour l'historique.
                self.liste_positions.append(self.position)

    def position_source_valide(self, position_source):
        """ Vérifie la validité de la position source, notamment:
            - Est-ce que la position contient une pièce?
            - Est-ce que cette pièce est de la couleur du joueur actif?
            - Si le joueur doit absolument continuer son mouvement avec une prise supplémentaire, a-t-il choisi la
              bonne pièce?

        Cette méthode retourne deux valeurs. La première valeur est Booléenne (True ou False), et la seconde valeur est
        un message d'erreur indiquant la raison pourquoi la position n'est pas valide (ou une chaîne vide s'il n'y a pas
        d'erreur).

        Args:
            position_source (Position): La position source à valider.

        Returns:
            bool, str: Un couple où le premier élément représente la validité de la position (True ou False), et le
                 deuxième élément est un message d'erreur (ou une chaîne vide s'il n'y a pas d'erreur).

        """

        # Valider si la position contient une pièce.
        if self.partie.damier.recuperer_piece_a_position(position_source) is not None:

            # Valider si la pièce est de la couleur du joueur actif.
            if self.partie.damier.recuperer_piece_a_position(position_source).couleur == self.couleur_joueur_courant:
                position_valide = True
                message = ""

                # Si la pièce ne peut pas se déplacer.
                if self.partie.damier.piece_peut_se_deplacer(position_source) == False and \
                        self.partie.damier.piece_peut_faire_une_prise(position_source) == False:
                    position_valide = False
                    message = "Erreur, la pièce sélectionnée ne peut pas se déplacer."

                # Si la pièce peut se déplacer.
                else:

                    # Si le joueur n'a pas à continuer son mouvement avec une prise supplémentaire,
                    # vérifie si le joueur doit faire une prise.
                    if self.position_source_forcee is None:

                        # Si le joueur doit absolument prendre une prise et que la position entrée est bonne.
                        if self.partie.damier.piece_peut_faire_une_prise(position_source) and self.doit_prendre == True:
                            position_valide = True
                            message = ""

                        # Si le joueur doit absolument prendre une prise et que la position entrée ne le permet pas.
                        elif self.partie.damier.piece_peut_faire_une_prise(position_source) == False \
                                and self.doit_prendre == True:
                            position_valide = False
                            message = "La pièce sélectionnée ne peut pas prendre la prise obligatoire."

                        # Si le joueur n'a pas de prise obligatoire à faire.
                        else:
                            position_valide = True
                            message = ""

                    # Si le joueur doit continuer son mouvement avec une prise supplémentaire.
                    else:
                        # Si la pièce sélectionnée correspond bien à la pièce ayant fait une prise le tour précédent.
                        if position_source == self.position_source_forcee:
                            position_valide = True
                            message = ""

                        # Si la pièce sélectionnée ne correspond pas à la pièce ayant fait une prise le tour précédent.
                        else:
                            position_valide = False
                            message = "Erreur, la pièce sélectionnée doit être " \
                                      "en position {}.".format(self.position_source_forcee)

            # Si la couleur de la pièce ne correspond pas à celle du joueur actif.
            else:
                position_valide = False
                message = "Erreur, la pièce sélectionnée n'est pas de la bonne couleur."

        # Si la position source ne contient pas de pièce.
        else:
            position_valide = False
            message = "Erreur, la case sélectionnée ne contient pas de pièce."

        return position_valide, message

    def position_cible_valide(self, position_cible):
        """ Vérifie si la position cible est valide (en fonction de la position source sélectionnée). Doit non seulement
        vérifier si le déplacement serait valide, mais également si le joueur a respecté la contrainte de
        prise obligatoire.

        Returns:
            bool, str: Deux valeurs, la première étant Booléenne et indiquant si la position cible est valide, et la
                seconde valeur est une chaîne de caractères indiquant un message d'erreur (ou une chaîne vide s'il n'y
                a pas d'erreur).

        """

        # Si la pièce entrée peut effectuer le déplacement.
        if self.partie.damier.piece_peut_se_deplacer_vers(self.position_source, position_cible) or \
                self.partie.damier.piece_peut_sauter_vers(self.position_source, position_cible):

            # Vérifie s'il existe une prise obligatoire.
            if self.partie.damier.piece_peut_faire_une_prise(self.position_source) and self.doit_prendre == True:
                if self.partie.damier.piece_peut_sauter_vers(self.position_source, position_cible):
                    position_valide = True
                    message = ""
                else:
                    position_valide = False
                    message = "La case sélectionnée ne peut pas faire la prise obligatoire."

            # Si le joueur doit absolument faire une prise et que la position entrée ne le permet pas.
            elif self.partie.damier.piece_peut_faire_une_prise(self.position_source) == False \
                    and self.doit_prendre == True:
                position_valide = False
                message = "La case sélectionnée ne peut pas faire la prise obligatoire."

            # Si le joueur n'a pas de prise obligatoire à faire.
            else:
                position_valide = True
                message = ""

        # Si le déplacement n'est pas valide.
        else:
            position_valide = False
            message = "Erreur, la position n'est pas valide."

        return position_valide, message

    def tour(self):
        """ Cette méthode effectue le tour d'un joueur en réalisant les actions suivantes:
            - Met à jour l'attribut self.doit_prendre
            - Affiche l'état du jeu
            - Effectue le déplacement

        """

        # Vérifie si la pièce a effectué une prise. Si oui, met à jour les attributs utiles pour
        # annuler le dernier déplacement
        if int((self.position_source.ligne + self.position_cible.ligne) / 2) not in [self.position_source.ligne,
                                                                                     self.position_cible.ligne]:

            self.derniere_position_piece_prise = Position((self.derniere_position_source.ligne
                                                           + self.derniere_position_cible.ligne) / 2,
                                                          (self.derniere_position_source.colonne +
                                                           self.derniere_position_cible.colonne) / 2)
            self.derniere_piece_prise = \
                self.partie.damier.recuperer_piece_a_position(self.derniere_position_piece_prise)

        # Si la pièce n'a pas effectué de prise, met à jour les attributs en conséquence.
        else:
            self.derniere_position_piece_prise = None
            self.derniere_piece_prise = None

        # Effectue le déplacement
        self.partie.damier.deplacer(self.position_source, self.position_cible)

        # Si une pièce adverse a été prise.
        if int((self.position_source.ligne + self.position_cible.ligne) / 2) not in [self.position_source.ligne,
                                                                                     self.position_cible.ligne]:

            # Si la dernière pièce prise est blanche, met à jour les statistiques de jeu en conséquence.
            if self.derniere_piece_prise.est_blanche():
                self.pieces_prises_blanches += 1
                self.blanches_prises['text'] = '{}'.format(self.pieces_prises_blanches)
                self.pieces_restantes_blanches -= 1
                self.blanches_restantes['text'] = '{}'.format(self.pieces_restantes_blanches)

            # Si la dernière pièce prise est noire, met à jour les statistiques de jeu en conséquence.
            else:
                self.pieces_prises_noires += 1
                self.noires_prises['text'] = '{}'.format(self.pieces_prises_noires)
                self.pieces_restantes_noires -= 1
                self.noires_restantes['text'] = '{}'.format(self.pieces_restantes_noires)

            # Si la pièce doit prendre une autre pièce et continuer son mouvement.
            if self.partie.damier.piece_peut_faire_une_prise(self.position_cible):
                self.position_source_forcee = self.position_cible
                self.sauvegarde_source_forcee = self.position_source_forcee

            # Si la pièce ne peut pas faire une autre prise et continuer son mouvement.
            else:
                self.position_source_forcee = None
                self.doit_prendre = False

                # Pour changer la couleur du joueur courant: devient noir si elle était blanc.
                if self.couleur_joueur_courant == "blanc":
                    self.couleur_joueur_courant = "noir"
                    self.joueur['text'] = 'Noir'
                    self.controller.nom_joueur_courant.set(self.controller.nom_joueur_deux.get().capitalize())

                # La couleur du joueur courant devient blanc si elle était noir.
                else:
                    self.couleur_joueur_courant = "blanc"
                    self.joueur['text'] = 'Blanc'
                    self.controller.nom_joueur_courant.set(self.controller.nom_joueur_un.get().capitalize())

        # Si aucun autre déplacement n'est requis.
        else:
            self.position_source_forcee = None
            self.doit_prendre = False

            # Pour changer la couleur du joueur courant: devient noir si elle était blanc.
            if self.couleur_joueur_courant == "blanc":
                self.couleur_joueur_courant = "noir"
                self.joueur['text'] = 'Noir'
                self.controller.nom_joueur_courant.set(self.controller.nom_joueur_deux.get().capitalize())

            # La couleur du joueur courant devient blanc si elle était noir.
            else:
                self.couleur_joueur_courant = "blanc"
                self.joueur['text'] = 'Blanc'
                self.controller.nom_joueur_courant.set(self.controller.nom_joueur_un.get().capitalize())

        # Détermine si le joueur courant a la possibilité de prendre une pièce adverse.
        if self.partie.damier.piece_de_couleur_peut_faire_une_prise(self.couleur_joueur_courant):
            self.doit_prendre = True

        # Affiche l'état du jeu

        # Met à jour les messages du jeu selon l'obligation de prendre une pièce ou non.
        if self.doit_prendre:
            if self.position_source_forcee is None:
                self.message_jeu['text'] = " Doit prendre une pièce."
            else:
                self.message_jeu['text'] = " Doit prendre avec " \
                                           "la pièce en position {}.".format(self.position_source_forcee)
        else:
            self.message_jeu['text'] = ""

        # Si aucun autre mouvement n'est possible, détermine le joueur gagnant et met à jour les attributs.
        if self.partie.damier.piece_de_couleur_peut_se_deplacer(self.couleur_joueur_courant) == False and \
                self.partie.damier.piece_de_couleur_peut_faire_une_prise(self.couleur_joueur_courant) == False:
            if self.couleur_joueur_courant == "blanc":
                gagnant = "noir"
            else:
                gagnant = "blanc"

            self.position_source = None
            self.position_cible = None
            self.canvas_damier.actualiser()
            self.message_jeu['text'] = "Partie terminée! Pour rejouer, appuyer sur Nouvelle partie."

            # Utilisé pour l'animation gagnant
            if gagnant == 'noir':
                nom = self.controller.nom_joueur_deux.get().capitalize()
            else:
                nom = self.controller.nom_joueur_un.get().capitalize()

            # Animation qui 'couronne' le joueur gagnant
            activer_animation = True
            while activer_animation:
                try:
                    AnimationGagnant(True, nom, color)

                except Exception:
                    activer_animation = False
                    pass

        # Met à jour les atttributs pour le nouveau tour à jouer.
        self.position_source = None
        self.position_cible = None
        self.message_position_source['text'] = 'Veuillez sélectionner la pièce à déplacer.'
        self.message_position_source['fg'] = 'black'
        self.message_position_cible['text'] = ''

        if self.partie.damier.piece_de_couleur_peut_se_deplacer(self.couleur_joueur_courant) == False and \
                self.partie.damier.piece_de_couleur_peut_faire_une_prise(self.couleur_joueur_courant) == False:
            self.message_position_source['text'] = ''

        # Si le joueur veut afficher les positions sources possibles.
        if self.montrer_positions_sources == True:
            self.afficher_positions_source()

        self.canvas_damier.actualiser()

    def depart_positions_sources(self, event):
        """ Méthode qui active la méthode self.afficher_position_source. Met à jour la variable
            membre self.montrer_positions_sources.

        Args:
            event (tkinter.Event): Objet décrivant l'évènement qui a causé l'appel de la méthode.

        """

        # Attribution d'une valeur booléenne
        self.montrer_positions_sources = True

        # Appel de la méthode
        self.afficher_positions_source()

        # Actualiser le damier
        self.canvas_damier.actualiser()

        # Actualiser les widgets
        self.afficher_positions_sources['relief'] = SUNKEN
        self.afficher_positions_sources['text'] = 'Double clic pour désactiver'

    def cacher_depart_positions_sources(self, event):
        """ Méthode qui désactive la méthode self.afficher_position_source. Met à jour la variable
        membre self.montrer_positions_sources.

        Args:
            event (tkinter.Event): Objet décrivant l'évènement qui a causé l'appel de la méthode.

        """

        # Attribution d'une valeur booléenne
        self.montrer_positions_sources = False

        # Actualiser le damier
        self.canvas_damier.actualiser()

        # Actualiser les widgets
        self.afficher_positions_sources['text'] = 'Afficher positions sources possibles'
        self.afficher_positions_sources['relief'] = GROOVE

    def afficher_positions_source(self):
        """ Méthode qui permet d'afficher les positions sources en fonction de la couleur du joueur courant.

        Args:
            event (tkinter.Event): Objet décrivant l'évènement qui a causé l'appel de la méthode.

        """

        # Si le joueur courant doit prendre une pièce.
        if self.position_source_forcee is not None:
            self.canvas_damier.afficher_position_source_forcee(self.position_source_forcee)

        # Si le joueur courant est noir.
        elif self.couleur_joueur_courant == "noir" and self.position_source_forcee is None:
            self.canvas_damier.afficher_positions_sources_noir()

        # Si le joueur courant est blanc.
        elif self.couleur_joueur_courant == "blanc" and self.position_source_forcee is None:
            self.canvas_damier.afficher_positions_sources_blanc()

    def annuler_dernier_mouvement(self, event):
        """ Méthode qui permet d'annuler le dernier mouvement effectué.

        Args:
            event (tkinter.Event): Objet décrivant l'évènement qui a causé l'appel de la méthode.

        """

        # Si aucun mouvement n'a encore été effectué.
        if self.derniere_position_cible is None and self.derniere_position_source is None:
            self.message_jeu['text'] = "Impossible d'annuler le dernier mouvement: " \
                                       "aucune pièce n'a encore été déplacée."

        else:

            # Vérifie qu'aucun mouvement n'a encore été annulé dans le tour courant. Si ce n'est pas le cas,
            # replace la pièce à sa position précédente.
            if self.derniere_position_cible is None or \
                    self.partie.damier.recuperer_piece_a_position(self.derniere_position_source) is None:

                self.partie.damier.cases[self.derniere_position_source] = self.derniere_piece_position_source
                del self.partie.damier.cases[self.derniere_position_cible]

                # Si une pièce a été prise, actualise le damier et met les variables membres des statistiques à jour.
                if int((self.derniere_position_source.ligne + self.derniere_position_cible.ligne) / 2) not in \
                        [self.derniere_position_source.ligne, self.derniere_position_cible.ligne]:
                    self.partie.damier.cases[self.derniere_position_piece_prise] = self.derniere_piece_prise
                    if self.derniere_piece_prise.est_blanche:
                        self.pieces_prises_blanches -= 1
                        self.pieces_restantes_noires += 1
                    else:
                        self.pieces_prises_noires -= 1
                        self.pieces_restantes_blanches += 1

                    # Si la pièce doit prendre une autre pièce et continuer son mouvement.
                    if self.position_source_forcee is not None:
                        self.position_source_forcee = self.sauvegarde_source_forcee

                    # Si la pièce ne peut pas faire une autre prise et continuer son mouvement.
                    else:
                        self.position_source_forcee = None
                        self.doit_prendre = False

                self.canvas_damier.actualiser()

                # Actualise les étiquettes et le joueur courant.
                if self.couleur_joueur_courant == "blanc":
                    self.couleur_joueur_courant = "noir"
                    self.joueur['text'] = 'noir'
                    self.controller.nom_joueur_courant.set(self.controller.nom_joueur_deux.get())

                # La couleur du joueur courant devient blanc si elle était noir.
                else:
                    self.couleur_joueur_courant = "blanc"
                    self.joueur['text'] = 'blanc'
                    self.controller.nom_joueur_courant.set(self.controller.nom_joueur_un.get())

                # Détermine si le joueur courant a la possibilité de prendre une pièce adverse.
                if self.partie.damier.piece_de_couleur_peut_faire_une_prise(self.couleur_joueur_courant):
                    self.doit_prendre = True
                else:
                    self.doit_prendre = False

                # Affiche l'état du jeu
                if self.doit_prendre:
                    if self.position_source_forcee is None:
                        self.message_jeu['text'] = " Doit prendre une pièce."
                    else:
                        self.message_jeu['text'] = " Doit prendre avec " \
                                                   "la pièce en position {}.".format(self.position_source_forcee)
                else:
                    self.message_jeu['text'] = ""

                self.position_source = None
                self.position_cible = None
                self.message_position_source['text'] = 'Veuillez sélectionner la pièce à déplacer.'
                self.message_position_cible['text'] = ''

            else:
                self.message_jeu['text'] = "Seul le dernier mouvement peut être annulé."
                self.message_jeu['fg'] = "red"

            self.effacer_le_dernier_deplacement_liste_deplacement()
            self.liste_positions = self.liste_positions[:-2]
            self.liste_couleur_joueur_courant = self.liste_couleur_joueur_courant[:-2]

            # Si le joueur veut afficher les positions sources possibles.
            if self.montrer_positions_sources == True:
                self.afficher_positions_source()
            self.canvas_damier.actualiser()

    def recharge_nouvelle_partie(self, event):
        """ Méthode qui permet d'initialiser les attributs à leur valeur par défaut. Le damier est construit
            avec les pièces à leurs positions initiales, le joueur actif est le joueur blanc, et celui-ci n'est pas
            forcé de prendre une pièce adverse. Aucune position source n'est sélectionnée, et aucune position source
            n'est forcée. Le thème courant ainsi que le nom des joueurs seront conservés.

        Args:
            event (tkinter.Event): Objet décrivant l'évènement qui a causé l'appel de la méthode.

        """

        # Réinitialiser tous les attributs.
        self.position = None
        self.position_source = None
        self.position_cible = None
        self.doit_prendre = False
        self.couleur_joueur_courant = "blanc"
        self.position_source_forcee = None
        self.sauvegarde_source_forcee = None
        self.derniere_position_source = None
        self.derniere_position_cible = None
        self.derniere_piece_position_source = None
        self.derniere_piece_position_cible = None
        self.derniere_piece_prise = None
        self.derniere_position_piece_prise = None
        self.dernier_message = None
        self.pieces_prises_blanches = 0
        self.pieces_prises_noires = 0
        self.pieces_restantes_blanches = 12
        self.pieces_restantes_noires = 12
        self.montrer_positions_sources = False

        self.position_source_selectionnee = None

        self.joueur['text'] = 'Blanc'
        self.controller.nom_joueur_courant.set(self.controller.nom_joueur_un.get())
        self.noires_prises['text'] = '{}'.format(self.pieces_prises_noires)
        self.noires_restantes['text'] = '{}'.format(self.pieces_restantes_noires)
        self.blanches_prises['text'] = '{}'.format(self.pieces_prises_blanches)
        self.blanches_restantes['text'] = '{}'.format(self.pieces_restantes_blanches)
        self.message_position_source['text'] = 'Veuillez sélectionner la case source.'
        self.message_position_source['fg'] = "black"
        self.message_jeu['text'] = ""

        # Liste pour l'affichage d'historique.
        self.liste_couleur_joueur_courant = []
        self.liste_positions = []

        # Réinitilaliser le dictionnaire de cases du damier.
        self.canvas_damier.damier.cases = {
            Position(7, 0): Piece("blanc", "pion"),
            Position(7, 2): Piece("blanc", "pion"),
            Position(7, 4): Piece("blanc", "pion"),
            Position(7, 6): Piece("blanc", "pion"),
            Position(6, 1): Piece("blanc", "pion"),
            Position(6, 3): Piece("blanc", "pion"),
            Position(6, 5): Piece("blanc", "pion"),
            Position(6, 7): Piece("blanc", "pion"),
            Position(5, 0): Piece("blanc", "pion"),
            Position(5, 2): Piece("blanc", "pion"),
            Position(5, 4): Piece("blanc", "pion"),
            Position(5, 6): Piece("blanc", "pion"),
            Position(2, 1): Piece("noir", "pion"),
            Position(2, 3): Piece("noir", "pion"),
            Position(2, 5): Piece("noir", "pion"),
            Position(2, 7): Piece("noir", "pion"),
            Position(1, 0): Piece("noir", "pion"),
            Position(1, 2): Piece("noir", "pion"),
            Position(1, 4): Piece("noir", "pion"),
            Position(1, 6): Piece("noir", "pion"),
            Position(0, 1): Piece("noir", "pion"),
            Position(0, 3): Piece("noir", "pion"),
            Position(0, 5): Piece("noir", "pion"),
            Position(0, 7): Piece("noir", "pion"),
        }

        # Actualiser le damier
        self.canvas_damier.actualiser()

        # Boîte de messages
        self.afficher_positions_sources['text'] = 'Afficher positions sources possibles'
        self.afficher_positions_sources['relief'] = GROOVE
        #
        self.annuler_mouvement['state'] = 'disable'
        self.afficher_historique['state'] = 'disable'

    def enregistrer_liste_deplacements(self, event):
        """ Méthode permettant d'enregistrer dans un fichier temporaire la liste de déplacements pour la partie
            courante. Le fichier en question sera récupéré par le un widget (Text) pour l'affichage de
            l'historique du jeu.

        Args:
            event (tkinter.Event): Objet décrivant l'évènement qui a causé l'appel de la méthode.

        """

        liste_positions = self.liste_positions
        liste_couleur_joueur_courant = self.liste_couleur_joueur_courant
        nom_joueur_un = self.controller.nom_joueur_un.get().capitalize()
        nom_joueur_deux = self.controller.nom_joueur_deux.get().capitalize()


        x = 1
        po = open("PartieCourante_FichierTemporaire.txt", 'w')

        # Écriture de tous les déplacements et du joueur les ayant effectué.
        while len(liste_positions) > 0:
            po.write('-' * 56 + '\n')
            deplacement_source = liste_positions[0]
            deplacement_cible = liste_positions[1]
            couleur_joueur_courant = liste_couleur_joueur_courant[0]

            if couleur_joueur_courant == 'blanc':
                po.write(f'{x}: Déplacement: {couleur_joueur_courant}         Nom du joueur: {nom_joueur_un}  \n')
                po.write(f'\n   Position source: {deplacement_source}    Position cible: {deplacement_cible}   \n')
            else:
                po.write(f'{x}: Déplacement: {couleur_joueur_courant}          Nom du joueur: {nom_joueur_deux}  \n')
                po.write(f'\n   Position source: {deplacement_source}    Position cible: {deplacement_cible}   \n')

            liste_positions = liste_positions[2:]
            liste_couleur_joueur_courant = liste_couleur_joueur_courant[2:]
            x = x + 1

            if (int(str(deplacement_source)[1])) - (int(str(deplacement_cible)[1])) == 1 \
                    or (int(str(deplacement_source)[1])) - (int(str(deplacement_cible)[1])) == -1:
                po.write('\n   Déplacement simple.\n')
            elif (int(str(deplacement_source)[1])) - (int(str(deplacement_cible)[1])) == 2 \
                    or (int(str(deplacement_source)[1])) - (int(str(deplacement_cible)[1])) == -2:
                po.write('\n   Déplacement avec prise.\n')
            else:
                pass

        po.write('-' * 56 + '\n')
        po.write('\n')
        po.close()

    def effacer_le_dernier_deplacement_liste_deplacement(self):
        """ Méthode qui permet d'effacer le dernier déplacement du fichier PartieCourante_FichierTemporaire.txt.

        """

        try:
            po = open("PartieCourante_FichierTemporaire.txt", 'r')
            lines = po.readlines()
            po.close()
            po = open("PartieCourante_FichierTemporaire.txt", 'w')
            lines = lines[:-6]
            for i in lines:
                po.write(i)
            po.close()
            self.canvas_damier.actualiser()

        except FileNotFoundError:
            pass

    def quitter_la_partie(self):
        """ Méthode qui permet de quitter la partie en supprimant le fichier temporaire d'historique de partie :
           PartieCourante_FichierTemporaire.txt.

         """

        # Gestion d'erreur si le fichier est absent.
        try:
            # Supprimer le fichier temporaire
            os.remove('PartieCourante_FichierTemporaire.txt')
        except IOError:
            pass
        quit()


if __name__ == '__main__':
    # Point d'entrée du programme
    app = JeuDames()
    app.mainloop()

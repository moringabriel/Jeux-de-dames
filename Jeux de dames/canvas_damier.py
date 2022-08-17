# Auteurs: Jean-Francis Roy, Pascal Germain, Sarah Lemieux-Montminy et Gabriel Morin

from tkinter import Tk, Canvas
from position import Position
from piece import Piece
from damier import Damier


class CanvasDamier(Canvas):
    """ Interface graphique de la partie de dames.

    Attributes:
        damier (Damier): L'objet qui contient les informations sur le damier à dessiner
        n_pixels_par_case (int): Nombre de pixels par case.

    """

    def __init__(self, parent, damier, n_pixels_par_case=60):
        """ Constructeur de la classe CanvasDamier. Initialise les deux attributs de la classe.

        Args:
            parent (tkinter.Widget): Le «widget» parent sur lequel sera ajouté le nouveau CanvasDamier
            damier (Damier): L'objet qui contient les informations sur le damier à dessiner
            n_pixels_par_case (int): Nombre de pixels par case. Ceci peut varier selon la taille de l'affichage

        """
        self.damier = damier

        # Nombre de pixels par case, variable.
        self.n_pixels_par_case = n_pixels_par_case
        self.liste_positions_source = []
        self.liste_positions_cibles = []

        # Appel du constructeur de la classe de base (Canvas).
        largeur = self.damier.n_lignes * n_pixels_par_case
        hauteur = self.damier.n_colonnes * n_pixels_par_case
        super().__init__(parent, width=largeur, height=hauteur,  highlightthickness=0)

        # On fait en sorte que le redimensionnement du canvas redimensionne son contenu. Cet événement étant également
        # généré lors de la création de la fenêtre, nous n'avons pas à dessiner les cases et les pièces dans le
        # constructeur.
        self.bind('<Configure>', self.redimensionner)

    def dessiner_cases(self):
        """ Méthode qui dessine les cases du damier sur le canvas (sans les pièces). Permet aussi de dessiner les cases
            des positions sources possibles et des positions cibles.

        """

        for i in range(self.damier.n_lignes):
            for j in range(self.damier.n_colonnes):
                position = Position(i, j)

                # Si les cases sont des positions sources possibles devant être affichées.
                if position in self.liste_positions_source:
                    debut_ligne = position.ligne * self.n_pixels_par_case
                    fin_ligne = debut_ligne + self.n_pixels_par_case
                    debut_colonne = position.colonne * self.n_pixels_par_case
                    fin_colonne = debut_colonne + self.n_pixels_par_case

                    couleur = '#DA9C57'
                    self.create_rectangle(debut_colonne, debut_ligne, fin_colonne, fin_ligne,
                                          fill=couleur , tags='positions sources')

                # Si les cases sont des positions cibles.
                elif position in self.liste_positions_cibles:
                    debut_ligne = position.ligne * self.n_pixels_par_case
                    fin_ligne = debut_ligne + self.n_pixels_par_case
                    debut_colonne = position.colonne * self.n_pixels_par_case
                    fin_colonne = debut_colonne + self.n_pixels_par_case

                    couleur = '#71A16C'
                    self.create_rectangle(debut_colonne, debut_ligne, fin_colonne, fin_ligne,
                                          fill=couleur, tags='positions cibles')

                # Si les cases correspondent aux cases de damier régulières.
                else:
                    debut_ligne = i * self.n_pixels_par_case
                    fin_ligne = debut_ligne + self.n_pixels_par_case
                    debut_colonne = j * self.n_pixels_par_case
                    fin_colonne = debut_colonne + self.n_pixels_par_case
    
                    # On détermine la couleur.
                    if (i + j) % 2 == 0:
                        couleur = '#394B5D'
                    else:
                        couleur = '#D1DFEB'
    
                    # On dessine le rectangle. On utilise l'attribut "tags" pour être en mesure de récupérer
                    # les éléments par la suite.
                    self.create_rectangle(debut_colonne, debut_ligne, fin_colonne, fin_ligne
                                          , fill=couleur, tags='case')

    def dessiner_pieces(self):
        """ Méthode qui dessine les pièces sur le canvas.

        """

        # Pour toute paire de position, pièce:
        for position, piece in self.damier.cases.items():
            # On dessine la pièce dans le canvas, au centre de la case. On utilise l'attribut "tags" pour être en
            # mesure de récupérer les éléments dans le canvas.
            coordonnee_y = position.ligne * self.n_pixels_par_case + self.n_pixels_par_case // 2
            coordonnee_x = position.colonne * self.n_pixels_par_case + self.n_pixels_par_case // 2

            # On utilise des caractères unicodes représentant des pièces.
            if piece.est_blanche() and piece.est_pion():
                icone = "\u26C0"
            elif piece.est_blanche() and piece.est_dame():
                icone = "\u26C1"
            elif piece.est_noire() and piece.est_pion():
                icone = "\u26C2"
            else:
                icone = "\u26C3"

            police_de_caractere = ('Deja Vu', self.n_pixels_par_case//2)
            self.create_text(coordonnee_x, coordonnee_y, text=icone, font=police_de_caractere, tags='piece')

    def redimensionner(self, event):
        """ Méthode qui est est appelée automatiquement lorsque le canvas est redimensionné.

        Args:
            event (tkinter.Event): Objet décrivant l'évènement qui a causé l'appel de la méthode.

        """

        # Nous recevons dans le "event" la nouvelle dimension dans les attributs width et height. On veut un damier
        # carré, alors on ne conserve que la plus petite de ces deux valeurs.
        nouvelle_taille = min(event.width, event.height)

        # Calcul de la nouvelle dimension des cases.
        self.n_pixels_par_case = nouvelle_taille // self.damier.n_lignes

        self.actualiser()

    def actualiser(self):
        """ Méthode qui redessinne le canvas (mets à jour l'affichage du damier).

        """

        # On supprime les anciennes cases et on ajoute les nouvelles.
        self.delete('case')
        self.dessiner_cases()
        self.liste_positions_source = []
        self.liste_positions_cibles = []

        # On supprime les anciennes pièces et on ajoute les nouvelles.
        self.delete('piece')
        self.dessiner_pieces()

    def afficher_positions_cibles(self, position_source, indicateur):
        """ Méthode qui détermine toutes les cases des positions cibles possibles pour une pièce sélectionnée et les
            place dans une liste dédiée à cet effet (self.liste_positions_cibles).

        Args:
            - position_source (Position): La position source de la case sélectionnée.
            - indicateur (int): Chiffre indiquant si la pièce sélectionnée doit prendre une prise.
            1 si elle ne doit pas en prendre, 2 autrement.

        """

        # Création d'une liste contenant toutes les positions des déplacements à vérifier.
        liste_cases_deplacements = position_source.quatre_positions_diagonales() + \
                                   position_source.quatre_positions_sauts()

        # Si la pièce sélectionnée ne doit pas faire de prise.
        if indicateur is 1:

            # Ajoute toutes les cases des déplacements possibles dans la liste dédiée à cet effet.
            for case in liste_cases_deplacements:
                if self.damier.piece_peut_se_deplacer_vers(position_source, case) or \
                        self.damier.piece_peut_sauter_vers(position_source, case):
                    self.liste_positions_cibles.append(case)

        # Si la pièce sélectionnée doit faire une prise.
        else:
            # Ajoute toutes les cases des déplacements possibles dans la liste dédiée à cet effet.
            for case in liste_cases_deplacements:
                if self.damier.piece_peut_sauter_vers(position_source, case):
                    self.liste_positions_cibles.append(case)
         
        self.actualiser()

    def afficher_positions_sources_blanc(self):
        """ Méthode qui détermine toutes les cases des positions sources possibles pour les pièces de couleur blanche
            et les place dans une liste dédiée à cet effet (self.liste_positions_source).

        """

        # Parcours toutes les cases du damier pour vérifier si une ou plusieurs pièce(s) peut(vent) faire une prise.
        ligne = 0
        while ligne < 8:
            colonne = 0
            while colonne < 8:
                case = Position(ligne, colonne)
                piece_case = self.damier.recuperer_piece_a_position(case)

                # S'il existe une pièce sur la case, qu'elle est blanche et qu'elle peut faire une prise,
                # ajoute sa position à la liste dédiée à cet effet.
                if piece_case is None:
                    pass
                else:
                    if piece_case.est_blanche() and self.damier.piece_peut_faire_une_prise(case):
                        self.liste_positions_source.append(case)
                colonne += 1
            ligne += 1

        # Si aucune pièce ne peut faire de prise, parcours toutes les cases du damier pour vérifier quelle(s) pièce(s)
        # peuvent se déplacer.
        if self.liste_positions_source == []:
            ligne = 0
            while ligne < 8:
                colonne = 0
                while colonne < 8:
                    case = Position(ligne, colonne)
                    piece_case = self.damier.recuperer_piece_a_position(case)

                    # S'il existe une pièce sur la case, qu'elle est blanche et qu'elle peut se déplacer,
                    # ajoute sa position à la liste dédiée à cet effet.
                    if piece_case is None:
                        pass
                    else:
                        if piece_case.est_blanche() and self.damier.piece_peut_se_deplacer(case):
                            self.liste_positions_source.append(case)
                    colonne += 1
                ligne += 1

    def afficher_positions_sources_noir(self):
        """ Méthode qui détermine toutes les cases des positions sources possibles pour les pièces de couleur noire
            et les place dans une liste dédiée à cet effet (self.liste_positions_source).

        """

        # Parcours toutes les cases du damier pour vérifier si une ou plusieurs pièce(s) peut(vent) faire une prise.
        ligne = 0
        while ligne < 8:
            colonne = 0
            while colonne < 8:
                case = Position(ligne, colonne)
                piece_case = self.damier.recuperer_piece_a_position(case)

                # S'il existe une pièce sur la case, qu'elle est blanche et qu'elle peut faire une prise,
                # ajoute sa position à la liste dédiée à cet effet.
                if piece_case is None:
                    pass
                else:
                    if piece_case.est_noire() and self.damier.piece_peut_faire_une_prise(case):
                        self.liste_positions_source.append(case)
                colonne += 1
            ligne += 1

        # Si aucune pièce ne peut faire de prise, parcours toutes les cases du damier pour vérifier quelle(s) pièce(s)
        # peuvent se déplacer.
        if self.liste_positions_source == []:
            ligne = 0
            while ligne < 8:
                colonne = 0
                while colonne < 8:
                    case = Position(ligne, colonne)
                    piece_case = self.damier.recuperer_piece_a_position(case)

                    # S'il existe une pièce sur la case, qu'elle est blanche et qu'elle peut se déplacer,
                    # ajoute sa position à la liste dédiée à cet effet.
                    if piece_case is None:
                        pass
                    else:
                        if piece_case.est_noire() and self.damier.piece_peut_se_deplacer(case):
                            self.liste_positions_source.append(case)
                    colonne += 1
                ligne += 1
    
    def afficher_position_source_forcee(self, position_source_forcee):
        """ Méthode permettant d'ajouter la position source obligatoire à une liste dédiée à cet effet.

        Args:
            - position_source_forcee (Position): La position source devant obligatoirement être sélectionnée.

        """

        self.liste_positions_source = [position_source_forcee]
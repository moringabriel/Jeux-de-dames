# Auteurs: Sarah Lemieux-Montminy, Gabriel Morin

from position import Position
from piece import Piece



class Damier:
    """Plateau de jeu d'un jeu de dames. Contient un ensemble de pièces positionnées à une certaine position
    sur le plateau.

    Attributes:
        cases (dict): Dictionnaire dont une clé représente une Position, et une valeur correspond à la Piece
            positionnée à cet endroit sur le plateau. Notez bien qu'une case vide (sans pièce blanche ou noire)
            correspond à l'absence de clé la position de cette case dans le dictionnaire.

        n_lignes (int): Le nombre de lignes du plateau. La valeur est 8 (constante).
        n_colonnes (int): Le nombre de colonnes du plateau. La valeur est 8 (constante).

    """

    def __init__(self):
        """Constructeur du Damier. Initialise un damier initial de 8 lignes par 8 colonnes.

        """
        self.n_lignes = 8
        self.n_colonnes = 8

        self.cases = {
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



    def recuperer_piece_a_position(self, position):
        """Récupère une pièce dans le damier à partir d'une position.

        Args:
            position (Position): La position où récupérer la pièce.

        Returns:
            La pièce (de type Piece) à la position reçue en argument, ou None si aucune pièce n'était à cette position.

        """
        if position not in self.cases:
            return None

        return self.cases[position]

    def position_est_dans_damier(self, position):
        """Vérifie si les coordonnées d'une position sont dans les bornes du damier (entre 0 inclusivement et le nombre
        de lignes/colonnes, exclusement.

        Args:
            position (Position): La position à valider.

        Returns:
            bool: True si la position est dans les bornes, False autrement.

        """

        ligne = 0
        liste_cases = []

        # Parcours chaque case du damier et les ajoute à une liste dédiée à cet effet.
        while ligne < 8:
            colonne = 0
            while colonne < 8:
                case = Position(ligne, colonne)
                liste_cases.append(case)
                colonne += 1
            ligne += 1

        # Si la position entrée correspond à l'une des cases de la liste créée précédemment, retourne True.
        if position in liste_cases:
            return True
        # Sinon, retourne False.
        else:
            return False


    def piece_peut_se_deplacer_vers(self, position_piece, position_cible):
        """Cette méthode détermine si une pièce (à la position reçue) peut se déplacer à une certaine position cible.
        On parle ici d'un déplacement standard (et non une prise).

        Une pièce doit être positionnée à la position_piece reçue en argument (retourner False autrement).

        Une pièce de type pion ne peut qu'avancer en diagonale (vers le haut pour une pièce blanche, vers le bas pour
        une pièce noire). Une pièce de type dame peut avancer sur n'importe quelle diagonale, peu importe sa couleur.
        Une pièce ne peut pas se déplacer sur une case déjà occupée par une autre pièce. Une pièce ne peut pas se
        déplacer à l'extérieur du damier.

        Args:
            position_piece (Position): La position de la pièce source du déplacement.
            position_cible (Position): La position cible du déplacement.

        Returns:
            bool: True si la pièce peut se déplacer à la position cible, False autrement.

        """

        # Vérifie d'abord si une pièce est positionnée à la position de départ
        # et si la position cible est bien dans le damier.
        # Si ce n'est pas le cas, False sera retourné.
        if self.recuperer_piece_a_position(position_piece) == None \
                or self.position_est_dans_damier(position_cible) == False:
            possibilite_deplacement = False

        # S'exécute si une pièce est bel et bien positionnée à la position de départ.
        else:
            # Vérifie si la pièce est une dame. Si oui, vérifie si elle peut se déplacer vers la position cible.
            if self.recuperer_piece_a_position(position_piece).est_dame():
                deplacements_possibles = position_piece.quatre_positions_diagonales()

                # Vérifie si la position cible se trouve dans les déplacements possibles de la pièce.
                if position_cible in deplacements_possibles:

                    # Si la case est vide, le déplacement est possible.
                    if self.recuperer_piece_a_position(position_cible) == None:
                        possibilite_deplacement = True

                    # Sinon, le déplacement n'est pas possible.
                    else:
                        possibilite_deplacement = False

                # Sinon, le déplacement n'est pas possible.
                else:
                    possibilite_deplacement = False

            # Si la pièce est un pion, vérifie sa couleur.
            else:
                # Si le pion est noir, vérifie si les déplacements selon les diagonales du bas sont possibles.
                if self.recuperer_piece_a_position(position_piece).est_noire():
                    deplacements_possibles = position_piece.positions_diagonales_bas()

                    # Vérifie si la position cible est un déplacement possible pour la pièce.
                    # Si oui, vérifie si la case de la position cible est vide.
                    if position_cible in deplacements_possibles:

                        # Si la case est vide, le déplacement est possible.
                        if self.recuperer_piece_a_position(position_cible) == None:
                            possibilite_deplacement = True

                        # Sinon, le déplacement n'est pas possible.
                        else:
                            possibilite_deplacement = False

                    # Si la position cible n'est pas comprise dans les déplacements possibles du pion,
                    # le retour sera False.
                    else:
                        possibilite_deplacement = False

                # Si le pion est blanc, vérifie si les déplacements selon les diagonales du haut sont possibles.
                else:
                    deplacements_possibles = position_piece.positions_diagonales_haut()

                    # Vérifie si la position cible est un déplacement possible pour la pièce.
                    # Si oui, vérifie si la case de la position cible est vide.
                    if position_cible in deplacements_possibles:

                        # Si la case est vide, le déplacement est possible.
                        if self.recuperer_piece_a_position(position_cible) == None:
                            possibilite_deplacement = True

                        # Sinon, le déplacement n'est pas possible.
                        else:
                            possibilite_deplacement = False

                    # Si la position cible n'est pas comprise dans les déplacements possibles du pion,
                    # le retour sera False.
                    else:
                        possibilite_deplacement = False

        return possibilite_deplacement


    def piece_peut_sauter_vers(self, position_piece, position_cible):
        """Cette méthode détermine si une pièce (à la position reçue) peut sauter vers une certaine position cible.
        On parle ici d'un déplacement qui "mange" une pièce adverse.

        Une pièce doit être positionnée à la position_piece reçue en argument (retourner False autrement).

        Une pièce ne peut que sauter de deux cases en diagonale. N'importe quel type de pièce (pion ou dame) peut sauter
        vers l'avant ou vers l'arrière. Une pièce ne peut pas sauter vers une case qui est déjà occupée par une autre
        pièce. Une pièce ne peut faire un saut que si elle saute par dessus une pièce de couleur adverse.

        Args:
            position_piece (Position): La position de la pièce source du saut.
            position_cible (Position): La position cible du saut.

        Returns:
            bool: True si la pièce peut sauter vers la position cible, False autrement.

        """

        # Vérifie d'abord si une pièce est positionnée à la position de départ
        # et si la position cible est bien dans le damier.
        # Si ce n'est pas le cas, False sera retourné.
        if self.recuperer_piece_a_position(position_piece) == None \
                or self.position_est_dans_damier(position_cible) == False:
            possibilite_saut = False
            return possibilite_saut

        # S'exécute si une pièce est bel et bien positionnée à la position de départ.
        else:

            # Vérifie que la position cible est dans les sauts possibles de la pièce de départ.
            if position_cible in position_piece.quatre_positions_sauts():

                # Vérifie que la case de la position cible est vide.
                if self.recuperer_piece_a_position(position_cible) == None:
                    position_case_sautee = Position((position_piece.ligne + position_cible.ligne) / 2,
                                                    (position_piece.colonne + position_cible.colonne) / 2)

                    # Vérifie s'il existe une pièce sur l'une des cases par dessus laquelle
                    # un saut peut être effectué.
                    if self.recuperer_piece_a_position(position_case_sautee) != None:

                        # Exécute cette partie si la pièce de départ est noire.
                        if self.cases[position_piece].est_noire():

                            # Si la pièce à prendre est noire, une prise ne pourra pas être effectuée.
                            if self.cases[position_case_sautee].est_noire():
                                possibilite_saut = False

                            # Si au contraire la pièce à prendre est blanche, une prise pourra être effectuée
                            # et le saut devient donc valide.
                            else:
                                possibilite_saut = True

                        # Exécute cette partie si la pièce de départ est blanche.
                        else:

                            # Si la piece à prendre est blanche , une prise ne pourra pas être effectuée.
                            if self.cases[position_case_sautee].est_blanche():
                                possibilite_saut = False

                            # Si au contraire la pièce à prendre est noire, une prise pourra être effectuée
                            # et le saut devient donc valide.
                            else:
                                possibilite_saut = True

                    # S'il n'existe pas de pièce sur l'une des cases par dessus laquelle
                    # un saut peut être effectué.
                    else:
                        possibilite_saut = False

                # Si la case de la position cible est occupée.
                else:
                    possibilite_saut = False

            # Si la position cible n'est pas dans les sauts possibles de la pièce de départ.
            else:
                possibilite_saut = False

        return possibilite_saut


    def piece_peut_se_deplacer(self, position_piece):
        """Vérifie si une pièce à une certaine position a la possibilité de se déplacer (sans faire de saut).

        ATTENTION: N'oubliez pas qu'étant donné une position, il existe une méthode dans la classe Position retournant
        les positions des quatre déplacements possibles.

        Args:
            position_piece (Position): La position source.

        Returns:
            bool: True si une pièce est à la position reçue et celle-ci peut se déplacer, False autrement.

        """

        possibilite_deplacement = False

        # S'assure d'abord qu'il existe une pièce sur la position entrée.
        if self.recuperer_piece_a_position(position_piece) != None:

            # Vérifie si la pièce est une dame. Si oui, détermine ses déplacements possibles selon les 4 diagonales.
            if self.recuperer_piece_a_position(position_piece).est_dame():
                deplacements_possibles = position_piece.quatre_positions_diagonales()

                # Effectue les opérations suivantes pour chaque déplacement possible de la dame
                # jusqu'à ce que l'un d'entre eux respecte toutes les conditions pour être réalisable, s'il y a lieu.
                for deplacement in deplacements_possibles:

                    # S'il n'y a pas de pièce sur la case où le déplacement est envisageable.
                    if self.recuperer_piece_a_position(deplacement) == None:

                        # Vérifie si la position cible est bien dans le damier.
                        # Si ce n'est pas le cas, False sera retourné.
                        if self.position_est_dans_damier(deplacement) == False:
                            possibilite_deplacement = False

                        # Si au contraire la position est dans le damier, True sera retourné.
                        else:
                            possibilite_deplacement = True
                            break

                    # S'il y a une pièce sur la case où le déplacement est envisageable.
                    else:
                        possibilite_deplacement = False

            # Si la pièce est un pion, vérifie sa couleur.
            else:

                # Si le pion est noir, détermine ses déplacements possibles selon les diagonales du bas.
                if self.recuperer_piece_a_position(position_piece).est_noire():
                    deplacements_possibles = position_piece.positions_diagonales_bas()

                    # Effectue les opérations suivantes pour chaque déplacement possible du pion
                    # jusqu'à ce que l'un d'entre eux respecte toutes les conditions pour être réalisable, s'il y a lieu.
                    for deplacement in deplacements_possibles:

                        # S'il n'y a pas de pièce sur la case où le déplacement est envisageable.
                        if self.recuperer_piece_a_position(deplacement) == None:

                            # Vérifie si la position cible est bien dans le damier.
                            # Si ce n'est pas le cas, False sera retourné.
                            if self.position_est_dans_damier(deplacement) == False:
                                possibilite_deplacement = False

                            # Si au contraire la position est dans le damier, True sera retourné.
                            else:
                                possibilite_deplacement = True
                                break

                # Si le pion est blanc, détermine ses déplacements possibles selon les diagonales du haut.
                else:
                    deplacements_possibles = position_piece.positions_diagonales_haut()

                    # Effectue les opérations suivantes pour chaque déplacement possible du pion
                    # jusqu'à ce que l'un d'entre eux respecte toutes les conditions pour être réalisable, s'il y a lieu.
                    for deplacement in deplacements_possibles:

                        # S'il n'y a pas de pièce sur la case où le déplacement est envisageable.
                        if self.recuperer_piece_a_position(deplacement) == None:

                            # Vérifie si la position cible est bien dans le damier.
                            # Si ce n'est pas le cas, False sera retourné.
                            if self.position_est_dans_damier(deplacement) == False:
                                possibilite_deplacement = False

                            # Si au contraire la position est dans le damier, True sera retourné.
                            else:
                                possibilite_deplacement = True
                                break

        # S'il n'existe pas de pièce à la position entrée.
        else:
            possibilite_deplacement = False

        return possibilite_deplacement


    def piece_peut_faire_une_prise(self, position_piece):
        """Vérifie si une pièce à une certaine position a la possibilité de faire une prise.

        Warning:
            N'oubliez pas qu'étant donné une position, il existe une méthode dans la classe Position retournant
            les positions des quatre sauts possibles.

        Args:
            position_piece (Position): La position source.

        Returns:
            bool: True si une pièce est à la position reçue et celle-ci peut faire une prise. False autrement.

        """

        # Détermine les 4 sauts possibles.
        deplacements_possibles = position_piece.quatre_positions_sauts()
        position_cases_libres = []

        # Vérifie s'il existe une pièce sur l'une des cases où un saut est possible.
        for deplacement in deplacements_possibles:

            # Si la case est libre, garde sa position dans la liste dédiée à cet effet.
            if self.recuperer_piece_a_position(deplacement) == None and self.position_est_dans_damier(deplacement):
                position_cases_libres += [deplacement]

        # Si une case pour un saut est libre,
        # détermine s'il existe une pièce pouvant être prise sur la case sautée.
        if position_cases_libres != []:

            # Vérifie s'il existe une pièce sur l'une des cases par dessus laquelle un saut peut être effectué.
            for position in position_cases_libres:
                position_case_sautee = Position((position_piece.ligne + position.ligne) / 2,
                                                (position_piece.colonne + position.colonne) / 2)

                # S'il n'existe pas de pièce sur la case sautée, poursuit la boucle.
                if self.recuperer_piece_a_position(position_case_sautee) is None:
                    possibilite_prise = False

                # Exécute cette partie si au contraire il existe une pièce sur la case sautée.
                else:

                    # Exécute cette partie si la pièce de départ est noire.
                    if self.recuperer_piece_a_position(position_piece).est_noire():

                        # Si la pièce sur la case sautée est noire, une prise ne pourra pas être effectuée
                        # et la boucle se poursuit.
                        if self.recuperer_piece_a_position(position_case_sautee).est_noire():
                            possibilite_prise = False

                        # Si la pièce sur la case sautée est blanche,
                        # une prise pourra être effectuée et la boucle s'arrête.
                        else:
                            possibilite_prise = True
                            break

                    # Exécute cette partie si la pièce de départ est blanche.
                    else:

                        # Si la pièce sur la case sautée est noire,
                        # une prise pourra être effectuée et la boucle s'arrête.
                        if self.recuperer_piece_a_position(position_case_sautee).est_noire():
                            possibilite_prise = True
                            break

                        # Si la pièce sur la case sautée est blanche, une prise ne pourra pas être effectuée
                        # et la boucle se poursuit.
                        else:
                            possibilite_prise = False

        # Si aucune case de saut n'est disponible, aucune prise ne sera possible.
        else:
            possibilite_prise = False

        return possibilite_prise


    def piece_de_couleur_peut_se_deplacer(self, couleur):
        """Vérifie si n'importe quelle pièce d'une certaine couleur reçue en argument a la possibilité de se déplacer
        vers une case adjacente (sans saut).

        ATTENTION: Réutilisez les méthodes déjà programmées!

        Args:
            couleur (str): La couleur à vérifier.

        Returns:
            bool: True si une pièce de la couleur reçue peut faire un déplacement standard, False autrement.
        """

        ligne = 0
        colonne = 0
        possibilite_deplacement = False

        # Vérifie à chaque case du damier s'il y a une pièce en passant une ligne à la fois tant qu'aucune possibilité
        # de déplacement n'a été trouvée.
        while ligne < 8 and possibilite_deplacement == False:
            case = Position(ligne, colonne)

            # Vérifie chaque colonne de la ligne, soit chaque case de celle-ci.
            while colonne < 8:
                case = Position(ligne, colonne)

                # S'il n'y a pas de pièce sur la case, passe à la suivante.
                if self.recuperer_piece_a_position(case) == None:
                    pass

                # S'il y a une pièce noire sur la case et qu'elle peut se déplacer, quitte la boucle.
                elif couleur.upper() == "NOIR" and self.recuperer_piece_a_position(case).est_noire() and\
                    self.piece_peut_se_deplacer(case):
                    possibilite_deplacement = True
                    break

                # S'il y a une pièce blanche sur la case et qu'elle peut se déplacer, quitte la boucle.
                elif couleur.upper() == "BLANC" and self.recuperer_piece_a_position(case).est_blanche() and\
                    self.piece_peut_se_deplacer(case):
                    possibilite_deplacement = True
                    break

                else:
                    possibilite_deplacement = False

                colonne += 1

            ligne += 1
            colonne = 0

        return possibilite_deplacement


    def piece_de_couleur_peut_faire_une_prise(self, couleur):
        """Vérifie si n'importe quelle pièce d'une certaine couleur reçue en argument a la possibilité de faire un
        saut, c'est à dire vérifie s'il existe une pièce d'une certaine couleur qui a la possibilité de prendre une
        pièce adverse.

        ATTENTION: Réutilisez les méthodes déjà programmées!

        Args:
            couleur (str): La couleur à vérifier.

        Returns:
            bool: True si une pièce de la couleur reçue peut faire un saut (une prise), False autrement.
        """

        ligne = 0
        colonne = 0
        possibilite_prise = False

        # Vérifie à chaque case du damier s'il y a une pièce en passant une ligne à la fois tant qu'aucune possibilité
        # de prise n'a été trouvée.
        while ligne < 8 and possibilite_prise == False:
            case = Position(ligne, colonne)

            # Vérifie chaque colonne de la ligne, soit chaque case de celle-ci.
            while colonne < 8:
                case = Position(ligne, colonne)

                # S'il n'y a pas de pièce sur la case, passe à la suivante.
                if self.recuperer_piece_a_position(case) == None:
                    pass

                # S'il y a une pièce noire sur la case et qu'elle peut se déplacer, quitte la boucle.
                elif couleur.upper() == "NOIR" and self.recuperer_piece_a_position(case).est_noire() and\
                    self.piece_peut_faire_une_prise(case):
                    possibilite_prise = True
                    break

                # S'il y a une pièce blanche sur la case et qu'elle peut se déplacer, quitte la boucle.
                elif couleur.upper() == "BLANC" and self.recuperer_piece_a_position(case).est_blanche() and\
                    self.piece_peut_faire_une_prise(case):
                    possibilite_prise = True
                    break

                else:
                    possibilite_prise = False

                colonne += 1

            ligne += 1
            colonne = 0

        return possibilite_prise


    def deplacer(self, position_source, position_cible):
        """Effectue le déplacement sur le damier. Si le déplacement est valide, on doit mettre à jour le dictionnaire
        self.cases, en déplaçant la pièce à sa nouvelle position (et possiblement en supprimant une pièce adverse qui a
        été prise).

        Cette méthode doit également:
        - Promouvoir un pion en dame si celui-ci atteint l'autre extrémité du plateau.
        - Retourner un message indiquant "ok", "prise" ou "erreur".

        ATTENTION: Si le déplacement est effectué, cette méthode doit retourner "ok" si aucune prise n'a été faite,
            et "prise" si une pièce a été prise.
        ATTENTION: Ne dupliquez pas de code! Vous avez déjà programmé (ou allez programmer) des méthodes permettant
            de valider si une pièce peut se déplacer vers un certain endroit ou non.

        Args:
            position_source (Position): La position source du déplacement.
            position_cible (Position): La position cible du déplacement.

        Returns:
            str: "ok" si le déplacement a été effectué sans prise, "prise" si une pièce adverse a été prise, et
                "erreur" autrement.

        """

        liste_promotion_noir = [Position(7, 0), Position(7, 2), Position(7, 4), Position(7, 6)]
        liste_promotion_blanc = [Position(0, 1), Position(0, 3), Position(0, 5), Position(0, 7)]

        # Vérifie d'abord si le déplacement est possible.
        if self.piece_peut_se_deplacer_vers(position_source, position_cible):

            # Vérifie si la pièce est noire et si elle peut devenir une dame.
            # Si oui, exécute sa promotion et le déplacement.
            if self.recuperer_piece_a_position(position_source).est_noire() and \
                    position_cible in liste_promotion_noir:
                self.cases[position_cible] = Piece("noir", "pion")
                self.cases[position_cible].promouvoir()
                #self.cases[position_cible] = Piece("noir", "dame")
            # Vérifie si la pièce est blanche et si elle peut devenir une dame.
            # Si oui, exécute sa promotion et le déplacement.
            elif self.recuperer_piece_a_position(position_source).est_blanche() and \
                    position_cible in liste_promotion_blanc:
                #self.cases[position_cible].promouvoir()
                self.cases[position_cible] = Piece("blanc", "pion")
                self.cases[position_cible].promouvoir()

            # Si la pièce ne peut pas devenir une dame, déplace le pion à la position cible.
            else:
                self.cases[position_cible] = self.cases[position_source]

            # Supprime la pièce de la case de départ et retourne ok.
            del self.cases[position_source]
            retour = 'ok'

        # Vérifie si la pièce peut faire un déplacement diagonal avec prise.
        elif self.piece_peut_sauter_vers(position_source, position_cible):

            # Vérifie si la pièce est noire et si elle peut devenir une dame.
            # Si oui, exécute sa promotion et le déplacement
            if self.recuperer_piece_a_position(position_source).est_noire() and \
                    position_cible in liste_promotion_noir:
                #self.cases[position_cible].promouvoir()
                self.cases[position_cible] = Piece("noir", "pion")
                self.cases[position_cible].promouvoir()

            # Vérifie si la pièce est blanche et si elle peut devenir une dame.
            # Si oui, exécute sa promotion et le déplacement
            elif self.recuperer_piece_a_position(position_source).est_blanche() and \
                    position_cible in liste_promotion_blanc:
                #self.cases[position_cible].promouvoir()
                self.cases[position_cible] = Piece("blanc", "pion")
                self.cases[position_cible].promouvoir()

            # Si la pièce ne peut pas devenir une dame, déplace le pion à la position cible.
            else:
                self.cases[position_cible] = self.recuperer_piece_a_position(position_source)

            # Supprime la pièce de la case de départ et celle de la case sautée.
            # Retourne prise.
            del self.cases[position_source]
            position_case_sautee = Position((position_cible.ligne + position_source.ligne) / 2,
                                            (position_cible.colonne + position_source.colonne) / 2)
            del self.cases[position_case_sautee]
            retour = 'prise'

        # Si la pièce ne peut pas faire le déplacement demandé, retourne un message d'erreur.
        else:
            retour = 'erreur'

        return retour


    def __repr__(self):
        """Cette méthode spéciale permet de modifier le comportement d'une instance de la classe Damier pour
        l'affichage. Faire un print(un_damier) affichera le damier à l'écran.

        """
        s = " +-0-+-1-+-2-+-3-+-4-+-5-+-6-+-7-+\n"
        for i in range(0, 8):
            s += str(i)+"| "
            for j in range(0, 8):
                if Position(i, j) in self.cases:
                    s += str(self.cases[Position(i, j)])+" | "
                else:
                    s += "  | "
            s += "\n +---+---+---+---+---+---+---+---+\n"

        return s


if __name__ == "__main__":
    print('Test unitaires de la classe "Damier"...')

    un_damier = Damier()

    # position_est_dans_damier

    assert un_damier.position_est_dans_damier(Position(7, 0)) == True
    assert un_damier.position_est_dans_damier(Position(7, 1)) == True
    assert un_damier.position_est_dans_damier(Position(-1, -1)) == False
    assert un_damier.position_est_dans_damier(Position(0, 0)) == True
    assert un_damier.position_est_dans_damier(Position(20, 10)) == False


    # piece_peut_se_deplacer_vers

    # Pièces blanches
    assert un_damier.piece_peut_se_deplacer_vers(Position(7, 0), Position(6, 0)) == False
    assert un_damier.piece_peut_se_deplacer_vers(Position(5, 2), Position(4, 3)) == True
    assert un_damier.piece_peut_se_deplacer_vers(Position(6, 3), Position(5, 2)) == False
    assert un_damier.piece_peut_se_deplacer_vers(Position(6, 7), Position(5, 8)) == False

    un_damier.cases[Position(3, 4)] = Piece("blanc", "pion")
    del un_damier.cases[Position(5, 4)]

    assert un_damier.piece_peut_se_deplacer_vers(Position(3, 4), Position(4, 3)) == False
    assert un_damier.piece_peut_se_deplacer_vers(Position(3, 4), Position(2, 3)) == False

    un_damier.recuperer_piece_a_position(Position(3, 4)).promouvoir()

    assert un_damier.piece_peut_se_deplacer_vers(Position(3, 4), Position(4, 3)) == True

    # Pièces noires
    assert un_damier.piece_peut_se_deplacer_vers(Position(0, 7), Position(0, 8)) == False
    assert un_damier.piece_peut_se_deplacer_vers(Position(2, 1), Position(3, 2)) == True
    assert un_damier.piece_peut_se_deplacer_vers(Position(2, 1), Position(1, 2)) == False
    assert un_damier.piece_peut_se_deplacer_vers(Position(2, 7), Position(3, 8)) == False

    un_damier.cases[Position(4, 1)] = Piece("noir", "pion")
    del un_damier.cases[Position(2, 1)]

    assert un_damier.piece_peut_se_deplacer_vers(Position(4, 1), Position(5, 0)) == False
    assert un_damier.piece_peut_se_deplacer_vers(Position(4, 1), Position(3, 0)) == False

    un_damier.recuperer_piece_a_position(Position(4, 1)).promouvoir()

    assert un_damier.piece_peut_se_deplacer_vers(Position(4, 1), Position(3, 0)) == True


    # piece_peut_sauter_vers

    assert un_damier.piece_peut_sauter_vers(Position(0, 0), Position(0, 0)) == False
    assert un_damier.piece_peut_sauter_vers(Position(0, 0), Position(-1, -1)) == False
    assert un_damier.piece_peut_sauter_vers(Position(2, 3), Position(4, 5)) == True
    assert un_damier.piece_peut_sauter_vers(Position(5, 2), Position(3, 4)) == False
    assert un_damier.piece_peut_sauter_vers(Position(6, 3), Position(4, 5)) == False

    un_damier.cases[Position(3, 0)] = Piece("blanc", "pion")
    del un_damier.cases[Position(5, 2)]

    assert un_damier.piece_peut_sauter_vers(Position(3, 0), Position(5, 2)) == True
    assert un_damier.piece_peut_sauter_vers(Position(4, 1), Position(2, -1)) == False
    assert un_damier.piece_peut_sauter_vers(Position(5, 6), Position(3, 4)) == False


    # piece_peut_se_deplacer

    assert un_damier.piece_peut_se_deplacer(Position(1, 0)) == True
    assert un_damier.piece_peut_se_deplacer(Position(0, 3)) == False
    assert un_damier.piece_peut_se_deplacer(Position(7, 0)) == False
    assert un_damier.piece_peut_se_deplacer(Position(3, 4)) == True
    assert un_damier.piece_peut_se_deplacer(Position(7, 1)) == False


    # piece_peut_faire_une_prise

    # Pièces blanches
    assert un_damier.piece_peut_faire_une_prise(Position(3, 0)) == True
    assert un_damier.piece_peut_faire_une_prise(Position(5, 0)) == True
    assert un_damier.piece_peut_faire_une_prise(Position(6, 3)) == False
    assert un_damier.piece_peut_faire_une_prise(Position(7, 6)) == False

    # Pièces noires
    assert un_damier.piece_peut_faire_une_prise(Position(0, 1)) == False
    assert un_damier.piece_peut_faire_une_prise(Position(2, 5)) == True
    assert un_damier.piece_peut_faire_une_prise(Position(7, 1)) == False
    assert un_damier.piece_peut_faire_une_prise(Position(3, 8)) == False
    assert un_damier.piece_peut_faire_une_prise(Position(4, 1)) == False


    # piece_de_couleur_peut_se_deplacer

    damier_test_blanc = Damier()
    del damier_test_blanc.cases[Position(0, 1)]
    del damier_test_blanc.cases[Position(0, 3)]
    del damier_test_blanc.cases[Position(0, 5)]
    del damier_test_blanc.cases[Position(0, 7)]
    del damier_test_blanc.cases[Position(1, 0)]
    del damier_test_blanc.cases[Position(1, 2)]
    del damier_test_blanc.cases[Position(1, 4)]
    del damier_test_blanc.cases[Position(1, 6)]
    del damier_test_blanc.cases[Position(2, 1)]
    del damier_test_blanc.cases[Position(2, 3)]
    del damier_test_blanc.cases[Position(2, 5)]
    del damier_test_blanc.cases[Position(2, 7)]

    assert un_damier.piece_de_couleur_peut_se_deplacer("noir") == True
    assert un_damier.piece_de_couleur_peut_se_deplacer("Blanc") == True
    assert damier_test_blanc.piece_de_couleur_peut_se_deplacer("Blanc") == True
    assert damier_test_blanc.piece_de_couleur_peut_se_deplacer("Noir") == False


    # piece_de_couleur_peut_faire_une_prise

    assert un_damier.piece_de_couleur_peut_faire_une_prise("noir") == True
    assert un_damier.piece_de_couleur_peut_faire_une_prise("blanc") == True
    del un_damier.cases[Position(4, 1)]
    assert un_damier.piece_de_couleur_peut_faire_une_prise("blanc") == False
    assert damier_test_blanc.piece_de_couleur_peut_faire_une_prise("noir") == False


    # deplacer

    assert un_damier.deplacer(Position(6, 3), Position(5, 2)) == "ok"
    assert un_damier.deplacer(Position(2, 3), Position(4, 5)) == "prise"
    assert un_damier.deplacer(Position(5, 6), Position(3, 4)) == "prise"
    assert un_damier.deplacer(Position(7, 0), Position(4, 5)) == "erreur"

    del un_damier.cases[Position(7, 6)]
    del un_damier.cases[Position(6, 5)]
    un_damier.cases[Position(6, 5)] = Piece("noir", "pion")
    print(un_damier)

    assert un_damier.deplacer(Position(6, 5), Position(7, 6)) == 'ok'
    assert un_damier.deplacer(Position(7, 6), Position(6, 5)) == "ok"
    assert un_damier.deplacer(Position(6, 7), Position(7, 6)) == "erreur"

    del un_damier.cases[Position(0, 1)]
    del un_damier.cases[Position(1, 2)]
    un_damier.cases[Position(1, 2)] = Piece("blanc", "pion")

    #assert un_damier.deplacer(Position(1, 2), Position(0, 1)) == "ok"
    #assert un_damier.deplacer(Position(0, 1), Position(1, 2)) == "ok"

    print('Tests unitaires passés avec succès!')

    # NOTEZ BIEN: Pour vous aider lors du développement, affichez le damier!
    print(un_damier)

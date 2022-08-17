# Auteurs: Sarah Lemieux-Montminy, Gabriel Morin

from damier import Damier
from position import Position


class Partie():
    """Gestionnaire de partie de dames.

    Attributes:
        damier (Damier): Le damier de la partie, contenant notamment les pièces.
        couleur_joueur_courant (str): Le joueur à qui c'est le tour de jouer.
        doit_prendre (bool): Un booléen représentant si le joueur actif doit absolument effectuer une prise
            de pièce. Sera utile pour valider les mouvements et pour gérer les prises multiples.
        position_source_selectionnee (Position): La position source qui a été sélectionnée. Utile pour sauvegarder
            cette information avant de poursuivre. Contient None si aucune pièce n'est sélectionnée.
        position_source_forcee (Position): Une position avec laquelle le joueur actif doit absolument jouer. Le
            seul moment où cette position est utilisée est après une prise: si le joueur peut encore prendre
            d'autres pièces adverses, il doit absolument le faire. Ce membre contient None si aucune position n'est
            forcée.

    """

    def __init__(self):


        """Constructeur de la classe Partie. Initialise les attributs à leur valeur par défaut. Le damier est construit
        avec les pièces à leurs valeurs initiales, le joueur actif est le joueur blanc, et celui-ci n'est pas forcé
        de prendre une pièce adverse. Aucune position source n'est sélectionnée, et aucune position source n'est forcée.

        """
        self.s = 1
        self.c = 2




        self.damier = Damier()
        self.couleur_joueur_courant = "blanc"
        self.doit_prendre = False
        self.position_source_selectionnee = None
        self.position_source_forcee = None

    def position_source_valide(self, position_source):
        """Vérifie la validité de la position source, notamment:
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
        if self.damier.recuperer_piece_a_position(position_source) != None:

            # Valider si la pièce est de la couleur du joueur actif.
            if (self.damier.recuperer_piece_a_position(position_source).couleur) == self.couleur_joueur_courant:
                position_valide = True
                message = ""

                # Si la pièce ne peut pas se déplacer.
                if self.damier.piece_peut_se_deplacer(position_source) == False and \
                        self.damier.piece_peut_faire_une_prise(position_source) == False:
                    position_valide = False
                    message = "Erreur, la pièce sélectionnée ne peut pas se déplacer."

                # Si la pièce peut se déplacer.
                else:

                    # Si le joueur n'a pas à continuer son mouvement avec une prise supplémentaire,
                    # vérifie si le joueur doit faire une prise.
                    if self.position_source_forcee is None:

                        # Si le joueur doit absolument prendre une prise et que la position entrée est bonne.
                        if self.damier.piece_peut_faire_une_prise(position_source) and self.doit_prendre == True:
                            position_valide = True
                            message = ""

                        # Si le joueur doit absolument prendre une prise et que la position entrée ne le permet pas.
                        elif self.damier.piece_peut_faire_une_prise(position_source) == False \
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
        """Vérifie si la position cible est valide (en fonction de la position source sélectionnée). Doit non seulement
        vérifier si le déplacement serait valide (utilisez les méthodes que vous avez programmées dans le Damier!), mais
        également si le joueur a respecté la contrainte de prise obligatoire.

        Returns:
            bool, str: Deux valeurs, la première étant Booléenne et indiquant si la position cible est valide, et la
                seconde valeur est une chaîne de caractères indiquant un message d'erreur (ou une chaîne vide s'il n'y
                a pas d'erreur).

        """

        # Si la pièce entrée peut effectuer le déplacement.
        if self.damier.piece_peut_se_deplacer_vers(self.position_source_selectionnee, position_cible) or \
                self.damier.piece_peut_sauter_vers(self.position_source_selectionnee, position_cible):

            # Vérifie s'il existe une prise obligatoire.
            if self.damier.piece_peut_faire_une_prise(self.position_source_selectionnee) and self.doit_prendre == True:
                if self.damier.piece_peut_sauter_vers(self.position_source_selectionnee, position_cible):
                    position_valide = True
                    message = ""
                else:
                    position_valide = False
                    message = "La case sélectionnée ne peut pas faire la prise obligatoire."

            # Si le joueur doit absolument faire une prise et que la position entrée ne le permet pas.
            elif self.damier.piece_peut_faire_une_prise(self.position_source_selectionnee) == False \
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

    def demander_positions_deplacement(self):
        """Demande à l'utilisateur les positions sources et cible, et valide ces positions. Cette méthode doit demander
        les positions à l'utilisateur tant que celles-ci sont invalides.

        Cette méthode ne doit jamais planter, peu importe ce que l'utilisateur entre.

        Returns:
            Position, Position: Un couple de deux positions (source et cible).

        """

        positions_valides = False
        while not positions_valides:

            input('')
            print("allo")
            print(self.position_source)
            # print(type(self.position_source))
            # print(type(self.position_source[1]))
            # print(self.position_source[1])
            print(self.ps)
            self.ps = Position(5, 0)
            print(self.ps)

            source_ligne = (str(self.ps))[1]
            source_colonne = (str(self.ps))[4]
            print(
                f"(Position source) Numéro de ligne : {source_ligne}\n(Position source) Numéro de colonne : {source_colonne}")
            print(self.ps)
            input('')

            position_valide, message = self.position_source_valide(Position(source_ligne, source_colonne))
            print("bb")

            if not position_valide:
                print("Erreur: {}.\n".format(message))
                continue

            position_source = Position(source_ligne, source_colonne)

            self.position_source_selectionnee = (position_source)

            self.pc = Position(4, 1)
            print(self.pc)

            # input('')
            cible_ligne = (str(self.pc))[1]
            cible_colonne = (str(self.pc))[4]
            print(
                f"(Position cible) Numéro de ligne : {cible_ligne}\n(Position cible) Numéro de colonne : {cible_colonne}")
            input('')

            position_cible = Position(cible_ligne, cible_colonne)

            position_valide, message = self.position_cible_valide(position_cible)

            if not position_valide:
                print(message + "\n")
                continue

            self.position_source_selectionnee = None

            positions_valides = True

        return position_source, position_cible

    def tour(self):
        """Cette méthode effectue le tour d'un joueur, et doit effectuer les actions suivantes:
        - Assigne self.doit_prendre à True si le joueur courant a la possibilité de prendre une pièce adverse.
        - Affiche l'état du jeu
        - Demander les positions source et cible (utilisez self.demander_positions_deplacement!)
        - Effectuer le déplacement (à l'aide de la méthode du damier appropriée)
        - Si une pièce a été prise lors du déplacement, c'est encore au tour du même joueur si celui-ci peut encore
          prendre une pièce adverse en continuant son mouvement. Utilisez les membres self.doit_prendre et
          self.position_source_forcee pour forcer ce prochain tour!
        - Si aucune pièce n'a été prise ou qu'aucun coup supplémentaire peut être fait avec la même pièce, c'est le
          tour du joueur adverse. Mettez à jour les attributs de la classe en conséquence.

        """

        # Détermine si le joueur courant a la possibilité de prendre une pièce adverse.
        if self.damier.piece_de_couleur_peut_faire_une_prise(self.couleur_joueur_courant):
            self.doit_prendre = True

        # Affiche l'état du jeu
        print(self.damier)
        print("")
        print("Tour du joueur", self.couleur_joueur_courant, end=".")
        if self.doit_prendre:
            if self.position_source_forcee is None:
                print(" Doit prendre une pièce.")
            else:
                print(" Doit prendre avec la pièce en position {}.".format(self.position_source_forcee))
        else:
            print("")

        # Demander les positions
        positions_demandees = self.demander_positions_deplacement()
        self.position_source_selectionnee = positions_demandees[0]

        # Effectuer le déplacement (à l'aide de la méthode du damier appropriée)

        print(self.damier.deplacer(positions_demandees[0], positions_demandees[1]))

        # Mettre à jour les attributs de la classe

        # Si une pièce adverse a été prise.
        if int((positions_demandees[0].ligne + positions_demandees[1].ligne) / 2) not in [positions_demandees[0].ligne,
                                                                                          positions_demandees[1].ligne]:

            # Si la pièce doit prendre une autre pièce et continuer son mouvement.
            if self.damier.piece_peut_faire_une_prise(positions_demandees[1]):
                self.position_source_forcee = positions_demandees[1]

            # Si la pièce ne peut pas faire une autre prise et continuer son mouvement.
            else:
                self.position_source_forcee = None
                self.doit_prendre = False

                # Pour changer la couleur du joueur courant: devient noir, si elle était blanc.
                if self.couleur_joueur_courant == "blanc":
                    self.couleur_joueur_courant = "noir"

                # La couleur du joueur courant devient blanc si elle était noir.
                else:
                    self.couleur_joueur_courant = "blanc"

        # Si aucun autre déplacement n'est requis.
        else:
            self.position_source_forcee = None
            self.doit_prendre = False

            # Pour changer la couleur du joueur courant: devient noir, si elle était blanc.
            if self.couleur_joueur_courant == "blanc":
                self.couleur_joueur_courant = "noir"

            # La couleur du joueur courant devient blanc si elle était noir.
            else:
                self.couleur_joueur_courant = "blanc"

    def jouer(self):
        """Démarre une partie. Tant que le joueur courant a des déplacements possibles (utilisez les méthodes
        appriopriées!), un nouveau tour est joué.

        Returns:
            str: La couleur du joueur gagnant.
        """

        while self.damier.piece_de_couleur_peut_se_deplacer(self.couleur_joueur_courant) or \
                self.damier.piece_de_couleur_peut_faire_une_prise(self.couleur_joueur_courant):
            self.tour()

        if self.couleur_joueur_courant == "blanc":
            return "noir"
        else:
            return "blanc"


if __name__ == "__main__":
    # Point d'entrée du programme. On initialise une nouvelle partie, et on appelle la méthode jouer().
    partie = Partie()
    damier = Damier()

    gagnant = partie.jouer()

    print("------------------------------------------------------")
    print("Partie terminée! Le joueur gagnant est le joueur", gagnant)


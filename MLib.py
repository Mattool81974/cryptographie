#Importation des bibliothèques nécessaires (pygame pour le fenêtre et sys pour le contrôle de l'application)
from math import *
import os
from pygame import *
from sys import *
from time import time_ns
import pygame
pygame.init()

class MWidget: #Définition d'une classe représentant tout les widgets dans la GUI
    def __init__(self, taille, position, parent = None, arrierePlanCouleur = (255, 255, 255, 1), curseurSurvol = SYSTEM_CURSOR_ARROW): #Constructeur d'un widget avec comme paramètre la taille
        self.arrierePlanCouleur = arrierePlanCouleur
        self.curseurSurvol = curseurSurvol
        self.enfant = [] #Attributs de type liste comprenant tout les enfants de la fenêtre
        self.fenetrePrincipale = self #Variable contenant la fenêtre principale
        self.globalPosition = position #Variable contenant la position par rapport à la fenêtre principale
        self.parent = parent #Parent du widget (si None, alors le widget est une fenêtre de base)
        self.position = position
        self.taille = taille
        if self.type == None:
            self.type = "Widget" #Variable contenant le type de widget
        
        if parent != None:
            self.parent.__nouveauEnfant(self) #Rajouter un enfant au widget parent

        fenetreBuff = self #Variable temporaire pour chercher la fenêtre principale
        while True: #Chercher la fenêtre principale
            if fenetreBuff.type != "Fenetre": #Si le widget anbalysé n'est pas la fenêtre principale
                if fenetreBuff.parent != None: #Si l'objet à un parent
                    fenetreBuff = fenetreBuff.parent #Mettre le widget analysée au parent du widget analysé
                    self.globalPosition = (self.globalPosition[0] + fenetreBuff.position[0], self.globalPosition[1] + fenetreBuff.position[1]) #Changer le position globale de l'objet
                else:
                    break #Quitter la boucle
            else:
                self.fenetrePrincipale = fenetreBuff #Mettre la fenêtre principale au widget analysé
                break #Quitter la boucle
        
    def __enleverEnfant(self, enfant): #Enlever un enfant à ce widget (fonction privée)
        if self.enfant.count(enfant) > 0:
            self.enfant.remove(enfant)

    def get_parent(self): #Retourne le parent du widget
        return self.parent

    def get_position(self): #Retourne la position du widget
        return self.position

    def get_rect(self):
        return self.position + self.taille

    def get_survol(self): #Retourne si le widget est survolé par le curseur ou pas
        positionSouris = mouse.get_pos()
        if positionSouris[0] > self.globalPosition[0] and positionSouris[0] < self.globalPosition[0] + self.taille[0] and positionSouris[1] > self.globalPosition[1] and positionSouris[1] < self.globalPosition[1] + self.taille[1]:
            return True
        return False

    def get_taille(self): #Retourne la taille du widget
        return self.taille

    def __nouveauEnfant(self, enfant): #Ajouter un enfant à ce widget (fonction privée)
        if self.enfant.count(enfant) > 0:
            self.enfant.remove(enfant)
        self.enfant.append(enfant)

    def _render(self): #Méthode permettant de renvoyer une image de la fenêtre
        retour = Surface(self.taille, SRCALPHA).convert_alpha() #Création de l'image qui sera retourné à la fin
        retour.fill(self.arrierePlanCouleur)
        if self.get_survol():
            self.fenetrePrincipale.set_cursor(self.curseurSurvol)
        retour = self._renderBeforeHierarchy(retour) #Appel de la fonction pour appliquer un render avec celle des widgets enfants
        for surface in self.enfant: #Application des render des enfants
            img = surface._render()
            retour.blit(img, surface.get_rect())
        retour = self._renderAfterHierarchy(retour) #Appel de la fonction pour appliquer un render après celle des widgets enfants
        return retour

    def _renderAfterHierarchy(self, surface): #Méthode permettant de modifier le rendu de render() avant que la hiérarchie soit appliqué, à ré-implémenter
        return surface

    def _renderBeforeHierarchy(self, surface): #Méthode permettant de modifier le rendu de render() avant que la hiérarchie soit appliqué, à ré-implémenter
        return surface

    def set_parent(self, parent): #Retourne le parent du widget
        if self.parent != None:
            self.parent.__enleverEnfant(self)
        self.parent = parent

    def set_taille(self, taille): #Change la taille du widget
        self.taille = taille



class MFenetre(MWidget): #Définition d'une classe représentant la fenêtre principale
    def __init__(self, fenetre, titre = "Fenêtre MGui", arrierePlanImage="", arrierePlanImageAlignement="GH", arrierePlanImageParSeconde=24, arrierePlanCouleur = (255, 255, 255, 1), curseurSurvol = SYSTEM_CURSOR_ARROW): #Constructeur qui prend la taille en paramètre
        self.type = "Fenetre"
        MWidget.__init__(self, fenetre.get_size(), (0, 0), None, arrierePlanCouleur, curseurSurvol) #Constructeur parent
        self.arrierePlanImage = None
        self.arrierePlanImageAlignement = arrierePlanImageAlignement
        self.actuelFrameGif = 0 #Frame du gif actuel
        if os.path.exists(arrierePlanImage): #Charger l'image de l'arrière plan
            self.arrierePlanImage = image.load(arrierePlanImage)
        else:
            sep = arrierePlanImage.split(".")
            if sep[-1] == "gif": #Fichier gif split
                self.arrierePlanImage = ""
                for i in range(len(sep) - 1):
                    self.arrierePlanImage += sep[i]
                self.actuelFrameGif = 0
            else: #Le fichier n'existe pas
                self.arrierePlanImage = None
        self.arrierePlanImageParSeconde = arrierePlanImageParSeconde #Vitesse du gif d'arrière plan en images par secondes
        self.arrierePlanImageParSecondeEcoule = 0 #Temps écoulé depuis la dernière update du gif
        self.curseur = SYSTEM_CURSOR_ARROW #Curseur de l'application
        self._deltaTime = time_ns() #Variable tampon pour deltaTime
        self.deltaTime = 0 #Temps entre 2 frames
        self.fenetre = fenetre
        self.fps = 0 #Nombre de frames par secondes
        self.fpsMoyen = 0 #Nombre de frames par secondes en moyenne
        self.fpsNb = 0 #Nombre d'actualisation des fps
        self.fpsNbFrame = 0 #Nombre de frame entre 2 actualisations de fps
        self.set_titreFenetre(titre)
        self.tempsDExecution = 0 #Temps d'éxécution depuis le dernier comptage des fps

    def _renderBeforeHierarchy(self, surface): #Ré-implémentation de la fonction pour afficher l'image d'arrière plan
        img = None #Création de la variable avec l'image a appliquer
        if self.arrierePlanImage != None: #Le fichier est un gif ou n'existe pas
            if type(self.arrierePlanImage) == str: #Le fichier existe
                if os.path.exists(self.arrierePlanImage):
                    fichiers = os.listdir(self.arrierePlanImage)
                    img = image.load(self.arrierePlanImage + "/" + fichiers[self.actuelFrameGif]) #Image a affiché lors de cette frame
                    self.arrierePlanImageParSecondeEcoule += self.deltaTime
                    if self.arrierePlanImageParSecondeEcoule >= 1/(self.arrierePlanImageParSeconde):
                        self.actuelFrameGif += 1 #Changer l'imageu du gif
                        self.arrierePlanImageParSecondeEcoule = 0
                    if self.actuelFrameGif >= len(fichiers): #Actualiser l'image du gif en cas de problème
                        self.actuelFrameGif = 0
            else: #Le fichier est une fichier image normal
                img = self.arrierePlanImage
        if img != None:
            xImg = 0
            yImg = 0
            if self.arrierePlanImageAlignement[0] == "J": #En cas de justification de l'image
                xQuotient = self.taille[0] / img.get_size()[0]
                img = transform.scale(img, (xQuotient * img.get_width(), xQuotient * img.get_height()))
            elif self.arrierePlanImageAlignement[1] == "J":
                yQuotient = self.taille[1] / img.get_size()[1]
                img = transform.scale(img, (yQuotient * img.get_width(), yQuotient * img.get_height()))
                
            if self.arrierePlanImageAlignement[0] == "C": #Gérer selon l'alignement de l'image
                xImg = self.taille[0] / 2 - img.get_size()[0] / 2
            elif self.arrierePlanImageAlignement[0] == "G":
                xImg = self.taille[0] - img.get_size()[0]
            if self.arrierePlanImageAlignement[1] == "C":
                yImg = self.taille[1] / 2 - img.get_size()[1] / 2
            elif self.arrierePlanImageAlignement[0] == "B":
                yImg = self.taille[1] - img.get_size()[1]
            surface.blit(img, (xImg, yImg, 0, 0))
        return surface

    def frame(self): #Actualise une frame de la fenêtre
        self.deltaTime = (time_ns() - self._deltaTime)/pow(10, 9) #Actualiser le delta time en secondes
        self.tempsDExecution += self.deltaTime #Actualiser le temps d'éxécution
        self.fpsNbFrame += 1

        if self.tempsDExecution >= 1: #Actualisation des fps
            self.tempsDExecution -= floor(self.tempsDExecution)
            self.fpsNb += 1
            self.fps = self.fpsNbFrame
            self.fpsNbFrame = 0
            self.fpsMoyen = (self.fpsMoyen + self.fps) / (2)
            print(self.fps)
        
        self._deltaTime = time_ns() #Préparer le delta time pour le prochain affichage en utilisant _deltaTime

        self.set_cursor(SYSTEM_CURSOR_ARROW) #Initialiser le curseur à une valeur par défaut
        img = self._render()
        self.fenetre.blit(img, self.get_rect())
        mouse.set_cursor(self.curseur)

    def get_cursor(self): #Retourne le curseur de la fenêtre
        return self.curseur

    def get_titreFenetre(self): #Retourne le titre de la fenêtre
        return display.get_caption()
    
    def set_cursor(self, curseur): #Changer le curseur de la fenêtre
        self.curseur = curseur

    def set_titreFenetre(self, titre): #Actualiser le titre de la fenêtre
        self.titre = titre
        display.set_caption(titre)



class MBordure(MWidget): #Définition d'une représentant un widget avec une bordure
    def __init__(self, position, taille, parent, bordureLargeur = 2, bordureCouleur = (0, 0, 0), bordureRayon = 0, arrierPlanCouleur=(0, 0, 0, 0), bordureLargeurGauche = None, bordureLargeurDroite = None, bordureLargeurBas = None, bordureLargeurHaut = None, bordureRayonGH = None, bordureRayonDH = None, bordureRayonGB = None, bordureRayonDB = None): #Constructeur de la classe
        self.type = "Bordure"
        MWidget.__init__(self, taille, position, parent, arrierPlanCouleur) #Appeler le constructeur de la classe MWidget
        if bordureLargeurGauche != None: #Calculer les différentes largeur
            self.bordureLargeurGauche = bordureLargeurGauche
        else:
            self.bordureLargeurGauche = bordureLargeur
        if bordureLargeurDroite != None: #Calculer les différentes largeur
            self.bordureLargeurDroite = bordureLargeurDroite
        else:
            self.bordureLargeurDroite = bordureLargeur
        if bordureLargeurBas != None: #Calculer les différentes largeur
            self.bordureLargeurBas = bordureLargeurBas
        else:
            self.bordureLargeurBas = bordureLargeur
        if bordureLargeurHaut != None: #Calculer les différentes largeur
            self.bordureLargeurHaut = bordureLargeurHaut
        else:
            self.bordureLargeurHaut = bordureLargeur
        if bordureLargeurGauche != None: #Calculer les différentes largeur
            self.bordureLargeurGauche = bordureLargeurGauche
        else:
            self.bordureLargeurGauche = bordureLargeur
        if bordureRayonGH != None: #Calculer les différents rayons
            self.bordureRayonGH = bordureRayonGH
        else:
            self.bordureRayonGH = bordureRayon
        if bordureRayonDH != None: #Calculer les différents rayons
            self.bordureRayonDH = bordureRayonDH
        else:
            self.bordureRayonDH = bordureRayon
        if bordureRayonGB != None: #Calculer les différents rayons
            self.bordureRayonGB = bordureRayonGB
        else:
            self.bordureRayonGB = bordureRayon
        if bordureRayonDB != None: #Calculer les différents rayons
            self.bordureRayonDB = bordureRayonDB
        else:
            self.bordureRayonDB = bordureRayon
        self.bordureCouleur = bordureCouleur
    def _renderBeforeHierarchy(self, surface): #Ré-implémentation de la fonction pour afficher la bordure
        surface.fill((0, 0, 0, 0))
        draw.rect(surface, self.bordureCouleur, (0, 0, self.taille[0], self.taille[1]), border_bottom_left_radius=self.bordureRayonGB, border_top_left_radius=self.bordureRayonGH, border_bottom_right_radius=self.bordureRayonDB, border_top_right_radius=self.bordureRayonDH) #Dessiner la bordure
        draw.rect(surface, self.arrierePlanCouleur, (self.bordureLargeurGauche, self.bordureLargeurHaut, self.taille[0] - (self.bordureLargeurGauche + self.bordureLargeurDroite), self.taille[1] - (self.bordureLargeurBas + self.bordureLargeurDroite)), border_bottom_left_radius=self.bordureRayonGB, border_top_left_radius=self.bordureRayonGH, border_bottom_right_radius=self.bordureRayonDB, border_top_right_radius=self.bordureRayonDH) #Dessiner l'intèrieur de la bordure
        return surface



class MTexte(MBordure): #Définition d'une classe représentant un texte graphique
    def __init__(self, texte, taille, position, policeTaille=12, policeType = "Ariel", texteAlignement = "GH", texteCouleur=(0, 0, 0), parent=None, bordureCouleur = (0, 0, 0), bordureLargeur = None, bordureRayon = 0, couleur=(0, 0, 0, 0)): #Constructeur
        self.type="Texte"
        MBordure.__init__(self, taille, position, parent, bordureLargeur, bordureCouleur, bordureRayon, couleur) #Appel du constructeur parent
        self.policeTaille = policeTaille #Affectation des variables de la classe
        self.policeType = policeType
        self.texte = texte
        self.texteAlignement = texteAlignement
        self.texteCouleur = texteCouleur
    def _renderBeforeHierarchy(self, surfaceF): #Ré-implémentation de la fonction pour afficher la bordure
        surfaceF = MBordure._renderBeforeHierarchy(self, surfaceF) #Appel de la fonction de bordure
        if font.get_fonts().count(self.policeType) <= 0: #Vérification de la police
            self.policeType = "Arial"
        police = font.SysFont(self.policeType, self.policeTaille) #Création de la police
        imageTexte = police.render(self.texte, True, (self.texteCouleur)) #Rendu du texte
        xTexte = 0
        yTexte = 0
        if self.texteAlignement[0] == "C":
            xTexte = (self.taille[0]/2)-(imageTexte.get_size()[0]/2)
        elif self.texteAlignement[0] == "G":
            xTexte = self.bordureLargeurGauche
        elif self.texteAlignement[0] == "D":
            xTexte = self.taille[0] - (self.bordureLargeurDroite + imageTexte.get_size()[0])

        if self.texteAlignement[1] == "C":
            yTexte = self.taille[1]/2-imageTexte.get_size()[1]/2
        elif self.texteAlignement[1] == "H":
            yTexte = self.bordureLargeurHaut
        elif self.texteAlignement[1] == "B":
            yTexte = self.taille[1] - (self.bordureLargeurBas + imageTexte.get_size()[1])

        surfaceF.blit(imageTexte, (xTexte, yTexte, imageTexte.get_size()[0], imageTexte.get_size()[1])) #Affichage du texte
        return surfaceF



class MEntreeTexte(MWidget): #Définition d'une classe représentant une entrée classe
    def __init__(self, position, taille, parent, texte = "", bordureCouleur = (0, 0, 0), bordureRayon = 10, bordureTaille = 5, couleur = (255, 255, 255), tempsDAffichageCurseur = 0.4): #Constructeur d'une entrée texte grâce à la taille, la position, et toutes les variables secondaires
        self.type = "EntreeTexte"
        MWidget.__init__(self, taille, position, parent, arrierePlanCouleur=(0, 0, 0, 0), curseurSurvol=SYSTEM_CURSOR_HAND) #Appelle du constructeur de MWidget
        self.bordureCouleur = bordureCouleur #Affectation des variables de base pour l'entrée
        self.bordureRayon = bordureRayon
        self.bordureTaille = bordureTaille
        self.couleur = couleur
        self.focus = False
        self.survol = False
        self.tempsDAffichageCurseur = tempsDAffichageCurseur
        self.texte = texte
    def _renderBeforeHierarchy(self, surface): #Ré-implémentation de la fonction pour afficher l'entrée
        draw.rect(surface, self.bordureCouleur, (0, 0, self.taille[0], self.taille[1]), 0, self.bordureRayon) #Affichage de l'entrée
        draw.rect(surface, self.couleur, (self.bordureTaille, self.bordureTaille, self.taille[0] - self.bordureTaille * 2, self.taille[1] - self.bordureTaille * 2), 0, self.bordureRayon)
        
        return surface
#Importation des bibliothèques nécessaires (pygame pour le fenêtre et sys pour le contrôle de l'application)
from math import *
from pygame import *
from sys import *
from time import time_ns
import pygame
pygame.init()

class MWidget: #Définition d'une classe représentant tout les widgets dans la GUI
    def __init__(self, taille, position, parent = None, arrierePlanCouleur = (255, 255, 255, 1), curseurSurvol = SYSTEM_CURSOR_ARROW): #Constructeur d'un widget avec comme paramètre la taille
        self.arrierPlanCouleur = arrierePlanCouleur
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
        retour = Surface(self.taille).convert_alpha() #Création de l'image qui sera retourné à la fin
        retour.fill(self.arrierPlanCouleur)
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
    def __init__(self, fenetre, titre = "Fenêtre MGui", arrierePlanCouleur = (255, 255, 255, 1), curseurSurvol = SYSTEM_CURSOR_ARROW): #Constructeur qui prend la taille en paramètre
        self.type = "Fenetre"
        MWidget.__init__(self, fenetre.get_size(), (0, 0), arrierePlanCouleur=arrierePlanCouleur, curseurSurvol=curseurSurvol)
        self.curseur = SYSTEM_CURSOR_ARROW #Curseur de l'application
        self.deltaTime = 0 #Temps entre 2 frames
        self.fenetre = fenetre
        self.fps = 0 #Nombre de frames par secondes
        self.fpsMoyen = 0 #Nombre de frames par secondes en moyenne
        self.fpsNb = 0 #Nombre d'actualisation des fps
        self.fpsNbFrame = 0 #Nombre de frame entre 2 actualisations de fps
        self.set_titreFenetre(titre)
        self.tempsDExecution = 0 #Temps d'éxécution depuis le dernier comptage des fps

    def frame(self): #Actualise une frame de la fenêtre
        self.deltaTime = (time_ns() - self.deltaTime)/pow(10, 9) #Actualiser le delta time en secondes
        self.tempsDExecution += self.deltaTime #Actualiser le temps d'éxécution
        self.fpsNbFrame += 1

        if self.tempsDExecution >= 1: #Actualisation des fps
            self.tempsDExecution -= floor(self.tempsDExecution)
            self.fpsNb += 1
            self.fps = self.fpsNbFrame
            self.fpsNbFrame = 0
            self.fpsMoyen = (self.fpsMoyen + self.fps) / (2)
            print(self.fps)
        
        self.deltaTime = time_ns() #Préparer le delta time pour le prochain affichage

        self.set_cursor(SYSTEM_CURSOR_ARROW) #Initialiser le curseur à une valeur par défaut
        img = self._render()
        self.fenetre.blit(img, self.get_rect())
        mouse.set_cursor(self.curseur)

    def get_cursor(self): #Retourne le curseur de la fenêtre
        return self.curseur

    def set_cursor(self, curseur): #Changer le curseur de la fenêtre
        self.curseur = curseur

    def set_titreFenetre(self): #Retourne le titre de la fenêtre
        return display.get_caption()

    def set_titreFenetre(self, titre): #Actualiser le titre de la fenêtre
        self.titre = titre
        display.set_caption(titre)



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
    def _renderAfterHierarchy(self, surface): #Ré-implémentation de la fonction pour afficher l'entrée
        draw.rect(surface, self.bordureCouleur, (0, 0, self.taille[0], self.taille[1]), 0, self.bordureRayon) #Affichage de l'entrée
        draw.rect(surface, self.couleur, (self.bordureTaille, self.bordureTaille, self.taille[0] - self.bordureTaille * 2, self.taille[1] - self.bordureTaille * 2), 0, self.bordureRayon)
        
        return surface
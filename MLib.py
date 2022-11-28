#Importation des bibliothèques nécessaires (pygame pour le fenêtre et sys pour le contrôle de l'application)
from math import *
import os
from pygame import *
from sys import *
from time import time_ns
import pygame
pygame.init()

class MWidget: #Définition d'une classe représentant tout les widgets dans la GUI
    def __init__(self, position, taille, parent = None, arrierePlanCouleur = (255, 255, 255, 1), curseurSurvol = SYSTEM_CURSOR_ARROW): #Constructeur d'un widget avec comme paramètre la taille
        self.arrierePlanCouleur = arrierePlanCouleur
        self.curseurSurvol = curseurSurvol
        self.enfant = [] #Attributs de type liste comprenant tout les enfants de la fenêtre
        self.fenetrePrincipale = self #Variable contenant la fenêtre principale
        self.focus = False
        self.globalPosition = position #Variable contenant la position par rapport à la fenêtre principale
        self.parent = parent #Parent du widget (si None, alors le widget est une fenêtre de base)
        self.position = position
        self.taille = taille
        self.visible = True #Est ce que le widget est visible
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
                self.fenetrePrincipale._nouvelleElement(self) #Dire à la fenêtre que cette éléments existe
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

    def get_visible(self): #Retourne si le widget est visible
        return self.visible

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
            if surface.visible: #Si l'enfant est visible
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

    def set_visible(self, visible): #Change la visibilité du widget
        self.visible = visible



class MFenetre(MWidget): #Définition d'une classe représentant la fenêtre principale
    def __init__(self, fenetre, titre = "Fenêtre MGui", arrierePlanImage="", arrierePlanImageAlignement="GH", arrierePlanImageParSeconde=24, arrierePlanCouleur = (255, 255, 255, 1), curseurSurvol = SYSTEM_CURSOR_ARROW): #Constructeur qui prend la taille en paramètre
        self.toutLesElements = [] #Liste de tout les éléments de la fenêtre
        self.type = "Fenetre"
        MWidget.__init__(self, (0, 0), fenetre.get_size(), None, arrierePlanCouleur, curseurSurvol) #Constructeur parent
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
        self.caplockPressee = False #Savoir si le bouton pour bloquer les majuscule est pressé
        self.curseur = SYSTEM_CURSOR_ARROW #Curseur de l'application
        self._deltaTime = time_ns() #Variable tampon pour deltaTime
        self.deltaTime = 0 #Temps entre 2 frames
        self.fenetre = fenetre
        self.fps = 0 #Nombre de frames par secondes
        self.fpsMoyen = 0 #Nombre de frames par secondes en moyenne
        self.fpsNb = 0 #Nombre d'actualisation des fps
        self.fpsNbFrame = 0 #Nombre de frame entre 2 actualisations de fps
        self.set_titreFenetre(titre)
        self.shiftPressee = False #Savoir si le bouton pour les majuscule est pressé
        self.tempsDExecution = 0 #Temps d'éxécution depuis le dernier comptage des fps

    def _nouvelleElement(self, element): #Ajouter un élément à la fenêtre
        self.toutLesElements.append(element)
    
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

        self.positionSouris = mouse.get_pos() #Stocker la position de la souris dans une variable
        
        self.evenement = event.get() #Obtenir tout les évènements
        for evnt in self.evenement: #Chercher dans tout les évènements
            if evnt.type == QUIT: exit() #Si évènement quitter appeler alors quitter
            elif evnt.type == MOUSEBUTTONDOWN: #Si un bouton est clické
                for i in self.toutLesElements: #Ré-initialiser le focus de chaque éléments
                    i.focus = False
                focus = self
                for i in focus.enfant: #Chercher le widget focus
                    if i.get_position()[0] < self.positionSouris[0] and self.positionSouris[0] < i.get_position()[0] + i.get_taille()[0] and i.get_position()[1] < self.positionSouris[1] and self.positionSouris[1] < i.get_position()[1] + i.get_taille()[1]:
                        focus = i
                focus.focus = True
                self.evenement.remove(evnt)
            elif evnt.type == KEYDOWN:
                if evnt.key == K_LSHIFT: #Si la touche pour les majuscules est pressée
                    self.shiftPressee = True
                    self.evenement.remove(evnt)
                elif evnt.key == K_CAPSLOCK: #Si la touche pour bloquer les majuscule est pressé
                    if self.caplockPressee:
                        self.caplockPressee = False
                    else:
                        self.caplockPressee = True
                    self.evenement.remove(evnt)
            elif evnt.type == KEYUP:
                if evnt.key == K_LSHIFT: #Si la touche pour les majuscules n'est plus pressé
                    self.shiftPressee = False
                    self.evenement.remove(evnt)

        self.set_cursor(self.curseurSurvol) #Initialiser le curseur à une valeur par défaut
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
    def __init__(self, position, taille, parent, bordureLargeur = 2, bordureCouleur = (0, 0, 0), bordureRayon = 0, bordureLargeurGauche = None, bordureLargeurDroite = None, bordureLargeurBas = None, bordureLargeurHaut = None, bordureRayonGH = None, bordureRayonDH = None, bordureRayonGB = None, bordureRayonDB = None, arrierePlanCouleur=(0, 0, 0, 0), curseurSurvol=SYSTEM_CURSOR_ARROW): #Constructeur de la classe
        self.type = "Bordure"
        MWidget.__init__(self, position, taille, parent, arrierePlanCouleur, curseurSurvol) #Appeler le constructeur de la classe MWidget
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
    def __init__(self, texte, position, taille, parent=None, curseur = False, curseurLargeur=2,  curseurTempsDAffichage = 0.4, ligneLongueurMax = -1, ligneMax = 1, longueurMax = 32, policeTaille=12, policeType = "Ariel", texteAlignement = "GH", texteCouleur=(0, 0, 0), bordureCouleur = (0, 0, 0), bordureLargeur = 0, bordureRayon = 0, bordureLargeurGauche = None, bordureLargeurDroite = None, bordureLargeurBas = None, bordureLargeurHaut = None, bordureRayonGH = None, bordureRayonDH = None, bordureRayonGB = None, bordureRayonDB = None, arrierePlanCouleur=(0, 0, 0, 0), curseurSurvol=SYSTEM_CURSOR_ARROW): #Constructeur
        self.type="Texte"
        MBordure.__init__(self, position, taille, parent, bordureLargeur, bordureCouleur, bordureRayon, bordureLargeurGauche, bordureLargeurDroite, bordureLargeurBas, bordureLargeurHaut, bordureRayonGH, bordureRayonDH, bordureRayonGB, bordureRayonDB, arrierePlanCouleur, curseurSurvol) #Appel du constructeur parent
        self.curseur = curseur
        self.curseurLargeur = curseurLargeur
        self.curseurPosition = 0 #Défini la position du curseur dans le texte
        self.curseurTempsDAffichage = curseurTempsDAffichage
        self.curseurTempsDAffichageAffiche = True
        self.curseurTempsDAffichageEcoule = 0 #Temps écoulé depuis le changement de curseur
        if ligneLongueurMax < 0:
            self.ligneLongueurMax = taille[0]
        else:
            self.ligneLongueurMax = ligneLongueurMax
        self.ligneMax = ligneMax
        self.longueurMax = longueurMax
        self.policeTaille = policeTaille #Affectation des variables de la classe
        self.policeType = policeType
        if policeType == "defaut":
            policeType = font.get_default_font()
        self.texte = texte
        self.textes = texte.split("\n") #Texte split selon les sauts de lignes
        self.texteAlignement = texteAlignement
        self.texteCouleur = texteCouleur
        self.texteRect = [(0, 0, 0, 0)]
    def _renderBeforeHierarchy(self, surfaceF): #Ré-implémentation de la fonction pour afficher la bordure
        if self.focus and self.curseur:
            if self.curseurTempsDAffichageEcoule == -1: #Calculer le temps restant à afficher ou non le curseur
                self.curseurTempsDAffichageEcoule = 0
                self.curseurTempsDAffichageAffiche = True
            if self.curseurTempsDAffichageEcoule >= self.curseurTempsDAffichage:
                    while self.curseurTempsDAffichageEcoule >= self.curseurTempsDAffichage:
                        self.curseurTempsDAffichageEcoule -= self.curseurTempsDAffichage
                    if self.curseurTempsDAffichageAffiche:
                        self.curseurTempsDAffichageAffiche = False
                    else:
                        self.curseurTempsDAffichageAffiche = True
                    
        if self.curseurPosition < 0:
            self.curseurPosition = 0
        elif self.curseurPosition >= len(self.texte):
            self.curseurPosition = len(self.texte)
            
        #print("A", self.ligneLongueurMax)
        
        xCurseur = 0
        yCurseur = 0
        hCurseur = 0
        
        surfaceF = MBordure._renderBeforeHierarchy(self, surfaceF) #Appel de la fonction de bordure
        if font.get_fonts().count(self.policeType) <= 0: #Vérification de la police
            self.policeType = "Arial"
        police = font.SysFont(self.policeType, self.policeTaille) #Création de la police
        texteFinal  = self.texte
        
        offsetCurseur = 0 #Savoir à quel point le curseur devra être avancer selon les modifications apportées
        if self.ligneLongueurMax != -1:
            ligneTaille = 0 #Variable qui contient la taile de chaque lignes
            nombreLigne = 0
            self.texte = "" #Ré-initialisation pour préparer une modification potentielle
            tailleTotal = 0 #Variable qui contient la taile total du texte
            for c in enumerate(texteFinal): #Gérer la taille du texte
                self.texte += c[1]
                tailleTotal += 1
                if c[1] == "\n":
                    if nombreLigne < self.ligneMax - 1:
                        ligneTaille = 0
                        nombreLigne += 1
                    else: #Si il y a trop de ligne
                        self.texte = self.texte[0:len(self.texte) - 1]
                        texteFinal = texteFinal[0:tailleTotal - 1]
                        if self.curseurPosition > len(texteFinal) - (offsetCurseur):
                            self.curseurPosition = len(texteFinal) - (offsetCurseur)
                        break
                else:
                    ligneTaille += police.size(c[1])[0]
                    if ligneTaille > self.ligneLongueurMax: #Si un saut de ligne est nécessaire
                        if nombreLigne < self.ligneMax - 1:
                            texteFinal = (texteFinal[0:tailleTotal-1] + "\n" + texteFinal[tailleTotal-1:len(texteFinal)])
                            nombreLigne += 1
                            tailleTotal += 1
                            if c[0] <= self.curseurPosition:
                                offsetCurseur += 1
                            ligneTaille = 0
                        else: #Si il y a trop de ligne
                            self.texte = self.texte[0:len(self.texte) - 1]
                            texteFinal = texteFinal[0:tailleTotal - 1]
                            if self.curseurPosition > len(texteFinal) - (offsetCurseur):
                                self.curseurPosition = len(texteFinal) - (offsetCurseur)
                            break
        self.textes = texteFinal.split("\n")
        
        buff = 0 #Variable temporaire pour placer le curseur
        ligneCurseur = 0 #Variable qui stocke la ligne du curseur
        tailleImageTexte = (0, 0)
        texteSurface = [] #Variable qui contient toutes les surfaces du texte
        tailleY = 0 #Variable qui contient la taille de tous les textes
        for c in enumerate(self.textes): #Générer les surfaces pour les textes avec le curseur
            if buff != -1:
                    buff += len(c[1])
            if self.curseurPosition <= buff:
                i = 0 #Variable temporaire pour éviter des erreurs out of range
                if c[0] > 0:
                    i = buff - len(c[1])
                posCurseur = (buff - i) - (buff-(self.curseurPosition+offsetCurseur))
                imageTexte = police.render(c[1][0:posCurseur], True, (self.texteCouleur)) #Rendu du texte avec le curseur
                xCurseur = imageTexte.get_size()[0]
                imageTexte = police.render(c[1], True, (self.texteCouleur)) #Rendu du texte
                texteSurface.append(imageTexte)
                tailleY += imageTexte.get_size()[1]
                buff = -1
            else:
                imageTexte = police.render(c[1], True, (self.texteCouleur)) #Rendu du texte
                texteSurface.append(imageTexte)
                tailleY += imageTexte.get_size()[1]
                if buff != -1:
                    ligneCurseur += 1
            if buff != -1:
                    buff += 1
            
        multiplier = 1
        xTexte = self.bordureLargeurGauche
        yTexte = self.bordureLargeurHaut
        
        if self.texteAlignement[1] == "C": #Calculer l'alignement y du 1er texte
            yTexte = self.taille[1]/2-tailleY/2
        elif self.texteAlignement[1] == "B":
                yTexte = self.taille[1] - (self.bordureLargeurBas + c.get_size[1])
                multiplier = -1
            
        self.texteRect.clear() #Vider les coordonnées des textes
        buff = 0 #Réutilisation de la variable buff
        for c in texteSurface: #Calculer les tailles de chaques texte
            if self.texteAlignement[0] == "C":
                xTexte = self.taille[0]/2 - c.get_size()[0]/2
            elif self.texteAlignement[0] == "D":
                xTexte = self.taille[0] - (self.bordureLargeurDroite + c.get_size()[0])
             
            if buff == ligneCurseur:
                xCurseur += xTexte
                yCurseur = yTexte
                hCurseur = c.get_size()[1]
            buff += 1
                
            surfaceF.blit(c, (xTexte, yTexte, c.get_size()[0], c.get_size()[1]))
            self.texteRect.append((xTexte, yTexte, c.get_size()[0], c.get_size()[1])) #Ajoute des coordonnées aux coordonnées de textes
            yTexte += c.get_size()[1] * multiplier
            
        if self.curseur and self.focus: #Afficher le curseur si nécessaire
            if self.curseurTempsDAffichageAffiche:
                draw.line(surfaceF, (self.texteCouleur), (xCurseur, yCurseur), (xCurseur, yCurseur + hCurseur), self.curseurLargeur)
            self.curseurTempsDAffichageEcoule += self.fenetrePrincipale.deltaTime
        else:
            self.curseurTempsDAffichageEcoule = -1
            
        return surfaceF
    
    def get_texte(self):
        return self.texte
    
    def set_texte(self, texte):
        self.texte = texte



class MBouton(MTexte): #Définition d'une classe représentant un bouton
    def __init__(self, position, taille, parent, actionAuSurvol = "", texte = "", curseur = False, curseurLargeur=2,  curseurTempsDAffichage = 0.4, ligneLongueurMax = -1, ligneMax = 1, longueurMax = 32, policeTaille=12, policeType = "Ariel", texteAlignement = "GH", texteCouleur=(0, 0, 0), bordureCouleur = (0, 0, 0), bordureLargeur=5, bordureRayon = 0, bordureLargeurGauche = None, bordureLargeurDroite = None, bordureLargeurBas = None, bordureLargeurHaut = None, bordureRayonGH = None, bordureRayonDH = None, bordureRayonGB = None, bordureRayonDB = None, arrierePlanCouleur = (255, 255, 255)):
        self.type = "Bouton"
        MTexte.__init__(self, texte, position, taille, parent, curseur, curseurLargeur, curseurTempsDAffichage, ligneLongueurMax, ligneMax, longueurMax, policeTaille, policeType, texteAlignement, texteCouleur, bordureCouleur, bordureLargeur, bordureRayon, bordureLargeurGauche, bordureLargeurDroite, bordureLargeurBas, bordureLargeurHaut, bordureRayonGH, bordureRayonDH, bordureRayonGB, bordureRayonDB, arrierePlanCouleur, SYSTEM_CURSOR_HAND)
        self.actionAuSurvol = actionAuSurvol
        self.click = False #Savoir si l'objet est clické
    def _renderBeforeHierarchy(self, surfaceF):
        self.click = False
        taillePolice = self.policeTaille #Plein de variables temporaires pour pouvoir bien utiliser le survol
        texte = self.texte
        if self.get_survol():
            actions = self.actionAuSurvol.split("-")
            for c in actions:
                action = c.split("=")[0]
                if action == "policeTaille":
                    self.policeTaille = int(self.actionAuSurvol.split("=")[1])
                if action == "texte":
                    self.texte = self.actionAuSurvol[len(self.actionAuSurvol.split("=")[1]):len(self.actionAuSurvol)]
        if self.focus: #Si l'objet est clické
            self.click = True
            self.focus = False
        surfaceF = super()._renderBeforeHierarchy(surfaceF)
        self.policeTaille = taillePolice
        self.texte = texte
        return surfaceF
    def get_clicke(self):
        return self.click


class MEntreeTexte(MTexte): #Définition d'une classe représentant une entrée classe
    def __init__(self, position, taille, parent, texte = "", caracteresAuthorises = "all", curseur = True, curseurLargeur=2,  curseurTempsDAffichage = 0.4, ligneLongueurMax = -1, ligneMax = 1, longueurMax = 32, policeTaille=12, policeType = "Ariel", texteAlignement = "GH", texteCouleur=(0, 0, 0), bordureCouleur = (0, 0, 0), bordureLargeur=5, bordureRayon = 0, bordureLargeurGauche = None, bordureLargeurDroite = None, bordureLargeurBas = None, bordureLargeurHaut = None, bordureRayonGH = None, bordureRayonDH = None, bordureRayonGB = None, bordureRayonDB = None, arrierePlanCouleur = (255, 255, 255)): #Constructeur d'une entrée texte grâce à la taille, la position, et toutes les variables secondaires
        self.type = "EntreeTexte"
        MTexte.__init__(self, texte, position, taille, parent, curseur, curseurLargeur, curseurTempsDAffichage, ligneLongueurMax, ligneMax, longueurMax, policeTaille, policeType, texteAlignement, texteCouleur, bordureCouleur, bordureLargeur, bordureRayon, bordureLargeurGauche, bordureLargeurDroite, bordureLargeurBas, bordureLargeurHaut, bordureRayonGH, bordureRayonDH, bordureRayonGB, bordureRayonDB, arrierePlanCouleur, SYSTEM_CURSOR_HAND) #Appelle du constructeur de MWidget
        self.caracteresAuthorises = caracteresAuthorises
    def _renderBeforeHierarchy(self, surface): #Ré-implémentation de la fonction pour afficher l'entrée
        if self.focus: #Si le widget est focus
            for evnt in self.fenetrePrincipale.evenement: #Chercher les évènements du clavier
                if evnt.type == KEYDOWN:
                    caractere = evnt.unicode #Obtenir le code unicode de la touche
                    if evnt.key == K_BACKSPACE:
                        caractere = ""
                        if self.curseurPosition > 0:
                            self.texte = self.texte[0:self.curseurPosition-1] + self.texte[self.curseurPosition:len(self.texte)]
                            self.curseurPosition -= 1
                    elif evnt.key == K_TAB:
                        caractere = "   "
                    elif evnt.key == K_RETURN:
                        caractere = "\n"
                    elif evnt.key == K_LEFT:
                        caractere = ""
                        self.curseurPosition -= 1
                    elif evnt.key == K_RIGHT:
                        caractere = ""
                        self.curseurPosition += 1
                    if self.caracteresAuthorises == "all" or self.caracteresAuthorises.count(code) > 0: #Si le caractère est authorisé
                        self.texte = self.texte[0:self.curseurPosition] + caractere + self.texte[self.curseurPosition:len(self.texte)] #Ajouter le caractère au texte
                        self.curseurPosition += len(caractere)
                    self.fenetrePrincipale.evenement.remove(evnt)
        else:
            curseurTempsDAffichageEcoule = -1
        super()._renderBeforeHierarchy(surface)
        return surface
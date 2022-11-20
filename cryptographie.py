from pygame import * #Import de tout les éléments de pygame
from sys import * #Importer tout les éléments de sys
import pygame #Import de pygame
pygame.init() #Lancement de pygame
from MLib import *

TAILLE=(500, 500) #Taille de la fenêtre

fenetre=display.set_mode(TAILLE) #Création de l'instance d'une fenêtre
app = MFenetre(fenetre, "Cryptographie", arrierePlanImage="assets/fond.gif") #Création d'un objet app pour mieux gérer la fenêtre

titre = MTexte("Chiffrage", (100, 5), (300, 90), parent=app, bordureCouleur=(0, 0, 0), bordureLargeur=3, bordureRayon=25, couleur=(255, 255, 255, 0.2), policeTaille=50, texteAlignement="CC")
texteDecrypter = MEntreeTexte((100, 100), (300, 100), app)

while True: #Boucle infini tant que l'évènement "quitter" n'est pas vue
    for evenement in event.get(): #Chercher dans tout les évènements
        if evenement.type == QUIT: exit() #Si évènement quitter appeler alors quitter
        
    app.frame()
    
    display.flip()


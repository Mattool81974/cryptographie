from pygame import * #Import de tout les éléments de pygame
from sys import * #Importer tout les éléments de sys
import pygame #Import de pygame
pygame.init() #Lancement de pygame
from MLib import *

TAILLE=(500, 500) #Taille de la fenêtre

fenetre=display.set_mode(TAILLE) #Création de l'instance d'une fenêtre
app = MFenetre(fenetre, "Cryptographie", arrierePlanImage="assets/fond.gif", arrierePlanImageAlignement="CJ", arrierePlanImageParSeconde=48) #Création d'un objet app pour mieux gérer la fenêtre

titre = MTexte("Chiffrage", (100, 5), (300, 90), parent=app, bordureCouleur=(0, 0, 0), bordureLargeur=3, bordureRayon=25, arrierePlanCouleur=(255, 255, 255, 255*0.75), policeTaille=65, texteAlignement="CC")
texteDecrypter = MEntreeTexte((100, 100), (300, 90), app, ligneLongueurMax=280, ligneMax=3, bordureRayon=15, policeTaille=22, policeType="defaut", texteAlignement="GH")
boutonCrypter = MBouton((10, 210), (150, 60), app, actionAuSurvol="policeTaille=32", texte="Chiffrer", texteAlignement="CC", policeTaille=24, policeType="defaut", bordureLargeur=2, bordureRayon=5)
boutonDecrypter = MBouton((340, 210), (150, 60), app, actionAuSurvol="policeTaille=32", texte="Déchiffrer", texteAlignement="CC", policeTaille=24, bordureLargeur=2, bordureRayon=5)
texteCrypter = MEntreeTexte((100, 290), (300, 90), app, ligneLongueurMax=280, ligneMax=3, bordureRayon=15, policeTaille=22, texteAlignement="GH")

while True: #Boucle infini tant que l'évènement "quitter" n'est pas vue
    app.frame()
    
    if boutonCrypter.get_clicke():
        texte = texteDecrypter.get_texte()
        resultat = ""
        for c in texte:
            if strAlpha(c):
                entier = ord(c) + 13
                if strAlphaLower(c):
                    if entier > 122:
                        entier -= 25
                elif strAlphaUpper(c):
                    if entier > 91:
                        entier -= 25
                resultat += chr(entier)
            else:
                resultat += c
        texteCrypter.set_texte(resultat)
    elif boutonDecrypter.get_clicke():
        texte = texteCrypter.get_texte()
        resultat = ""
        for c in texte:
            if strAlpha(c):
                entier = ord(c) - 13
                if strAlphaLower(c):
                    if entier < 97:
                        entier += 25
                elif strAlphaUpper(c):
                    if entier < 65:
                        entier += 25
                resultat += chr(entier)
            else:
                resultat += c
        texteDecrypter.set_texte(resultat)
    
    display.flip()


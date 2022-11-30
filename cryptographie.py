#Par Mattéo Menou
from pygame import * #Import de tout les éléments de pygame
from sys import * #Importer tout les éléments de sys
import pygame #Import de pygame
pygame.init() #Lancement de pygame
from MLib import *
from cryptage_ROT13 import * #Importer le code ROT13 fait par Alexis Bergère
from cryptage_VIGENERE import * #Importer le code Vigenère fait par Illiam Pont Layus

TAILLE=(500, 500) #Taille de la fenêtre

fenetre=display.set_mode(TAILLE) #Création de l'instance d'une fenêtre
app = MFenetre(fenetre, "Chiffrage", arrierePlanImage="assets/fond.gif", arrierePlanImageAlignement="CJ", arrierePlanImageParSeconde=48) #Création d'un objet app pour mieux gérer la fenêtre

titre = MTexte(texte="Chiffrage", position=(100, 5), taille=(300, 90), parent=app, bordureCouleur=(0, 0, 0), bordureLargeur=3, bordureRayon=25, arrierePlanCouleur=(255, 255, 255, 255*0.75), policeTaille=65, texteAlignement="CC") #Titre de la fenêtre
texteDechiffrer = MEntreeTexte(position=(100, 100), taille=(300, 90), parent=app, ligneLongueurMax=280, ligneMax=3, bordureRayon=15, policeTaille=22, policeType="defaut", texteAlignement="GH") #Entrée du texte déchiffré
boutonChiffrer = MBouton(position=(10, 210), taille=(150, 60), parent=app, actionAuSurvol="policeTaille=32", texte="Chiffrer", texteAlignement="CC", policeTaille=24, policeType="defaut", bordureLargeur=2, bordureRayon=5) #Bouton pour mettre le texte déchiffré dans l'entrée du texte chiffré après chiffrage
boutonDechiffrer = MBouton(position=(340, 210), taille=(150, 60), parent=app, actionAuSurvol="policeTaille=32", texte="Déchiffrer", texteAlignement="CC", policeTaille=24, bordureLargeur=2, bordureRayon=5) #Bouton pour mettre le texte chiffré dans l'entrée du texte déchiffré après déchiffrage
bordureChoixBouton = MTexte(texte="Rot13", position=(170, 195), taille=(160, 80), parent=app, arrierePlanCouleur=(255, 255, 255, 255*0.75), bordureLargeur=2, bordureRayon=15, policeTaille=24, texteAlignement="GC") #Texte qui contient le nom du chiffrage utilisé
boutonGaucheChoixBouton = MBouton(position=(87, 20), taille=(35, 40), parent=bordureChoixBouton, actionAuSurvol="", texte="<", bordureLargeur=2, policeTaille=30, texteAlignement="CC") #Bouton pour changer le chiffrage
boutonDroiteChoixBouton = MBouton(position=(122, 20), taille=(35, 40), parent=bordureChoixBouton, actionAuSurvol="", texte=">", bordureLargeur=2, policeTaille=30, texteAlignement="CC") #Bouton pour changer le chiffrage
texteCle = MEntreeTexte(position=(170, 280), taille=(160, 35), parent=app, texte="CLE", bordureLargeur=4, caracteresAutorises=(ALPHA_UPPER), policeTaille=20, texteAlignement="CC") #Clé de Vigenère (disponible que quand le chiffrage est à Vigenère)
texteChiffrer = MEntreeTexte(position=(100, 320), taille=(300, 90), parent=app, ligneLongueurMax=280, ligneMax=3, bordureRayon=15, policeTaille=22, texteAlignement="GH") #Entrée du texte chiffré

while True: #Boucle infini tant que l'évènement "quitter" n'est pas vue
    app.frame()

    if boutonDroiteChoixBouton.get_clicke() or boutonGaucheChoixBouton.get_clicke():
        if bordureChoixBouton.get_texte() == "Rot13":
            bordureChoixBouton.set_texte("Vigenère")
            texteCle.set_texte("CLE")
            texteCle.set_curseurPosition(3)
        else:
            bordureChoixBouton.set_texte("Rot13")

    if bordureChoixBouton.get_texte() == "Rot13":
        texteCle.set_visible(False)
    else:
        texteCle.set_visible(True)
    
    if boutonChiffrer.get_clicke(): #Chiffrer le texte
        if bordureChoixBouton.get_texte() == "Rot13": #Avec rot13
            texte = texteDechiffrer.get_texte() #Obtention du texte à chiffrer
            resultat = rot13(texte) #Chiffrage grâce au code de cryptage_ROT13
            texteChiffrer.set_texte(resultat) #Appliquage du résultat final
        else: #Avec Vigenère
            texteBrut = texteDechiffrer.get_texte() #Obtention du texte à chiffrer
            texte = ""
            cle = texteCle.get_texte() #Obtention de la clé
            majuscules = [] #Liste de tous les index où se trouvent des majuscules dans le texte
            for c in enumerate(texteBrut): #Convertir le texte en majuscule en gardant la position des majuscules
                cFinal = c[1]
                if strAlpha(c[1]):
                    if strAlphaUpper(c[1]):
                        majuscules.append(c[0])
                    cFinal = c[1].upper()
                texte += cFinal
            resultatBrut = vigenere(cle, texte) #Chiffrage du texte grâce au code de cryptage_VIGENERE
            resultat = ""
            for c in enumerate(resultatBrut): #Convertir le texte en minuscule et en majuscule
                cFinal = c[1]
                if strAlpha(c[1]):
                    if majuscules.count(c[0]) <= 0:
                        cFinal = c[1].lower()
                resultat += cFinal
            texteChiffrer.set_texte(resultat)
    elif boutonDechiffrer.get_clicke(): #Déchiffrer le texte
        if bordureChoixBouton.get_texte() == "Rot13": #Avec rot13
            texte = texteChiffrer.get_texte() #Obtention du texte à chiffrer
            resultat = rot13Dechiffrage(texte) #Déchiffrage grâce au code de cryptage_ROT13
            texteDechiffrer.set_texte(resultat) #Appliquage du résultat final
        else: #Avec Vigenère
            texteBrut = texteChiffrer.get_texte() #Obtention du texte à chiffrer
            texte = ""
            cle = texteCle.get_texte() #Obtention de la clé
            majuscules = [] #Liste de tous les index où se trouvent des majuscules dans le texte
            for c in enumerate(texteBrut): #Convertir le texte en majuscule en gardant la position des majuscules
                cFinal = c[1]
                if strAlpha(c[1]):
                    if strAlphaUpper(c[1]):
                        majuscules.append(c[0])
                    cFinal = c[1].upper()
                texte += cFinal
            resultatBrut = decode_vigenere(cle, texte) #Déchiffrage du texte grâce au code de cryptage_VIGENERE
            resultat = ""
            for c in enumerate(resultatBrut): #Convertir le texte en minuscule et en majuscule
                cFinal = c[1]
                if strAlpha(c[1]):
                    if majuscules.count(c[0]) <= 0:
                        cFinal = c[1].lower()
                resultat += cFinal
            texteDechiffrer.set_texte(resultat)
    
    display.flip()


#Par Mattéo Menou
from pygame import * #Import de tout les éléments de pygame
from sys import * #Importer tout les éléments de sys
import pygame #Import de pygame
pygame.init() #Lancement de pygame
from MLib import *
from cryptage_ROT13 import * #Imporer le code ROT13 fait par Alexis Bergère

TAILLE=(500, 500) #Taille de la fenêtre

fenetre=display.set_mode(TAILLE) #Création de l'instance d'une fenêtre
app = MFenetre(fenetre, "Cryptographie", arrierePlanImage="assets/fond.gif", arrierePlanImageAlignement="CJ", arrierePlanImageParSeconde=48) #Création d'un objet app pour mieux gérer la fenêtre

titre = MTexte(texte="Chiffrage", position=(100, 5), taille=(300, 90), parent=app, bordureCouleur=(0, 0, 0), bordureLargeur=3, bordureRayon=25, arrierePlanCouleur=(255, 255, 255, 255*0.75), policeTaille=65, texteAlignement="CC") #Titre de la fenêtre
texteDecrypter = MEntreeTexte(position=(100, 100), taille=(300, 90), parent=app, ligneLongueurMax=280, ligneMax=3, bordureRayon=15, policeTaille=22, policeType="defaut", texteAlignement="GH") #Entrée du texte déchiffré
boutonCrypter = MBouton(position=(10, 210), taille=(150, 60), parent=app, actionAuSurvol="policeTaille=32", texte="Chiffrer", texteAlignement="CC", policeTaille=24, policeType="defaut", bordureLargeur=2, bordureRayon=5) #Bouton pour mettre le texte déchiffré dans l'entrée du texte chiffré après chiffrage
boutonDecrypter = MBouton(position=(340, 210), taille=(150, 60), parent=app, actionAuSurvol="policeTaille=32", texte="Déchiffrer", texteAlignement="CC", policeTaille=24, bordureLargeur=2, bordureRayon=5) #Bouton pour mettre le texte chiffré dans l'entrée du texte déchiffré après déchiffrage
bordureChoixBouton = MTexte(texte="Rot13", position=(170, 195), taille=(160, 80), parent=app, arrierePlanCouleur=(255, 255, 255, 255*0.75), bordureLargeur=2, bordureRayon=15, policeTaille=24, texteAlignement="GC") #Texte qui contient le nom du chiffrage utilisé
boutonGaucheChoixBouton = MBouton(position=(87, 20), taille=(35, 40), parent=bordureChoixBouton, actionAuSurvol="", texte="<", bordureLargeur=2, policeTaille=30, texteAlignement="CC") #Bouton pour changer le chiffrage
boutonDroiteChoixBouton = MBouton(position=(122, 20), taille=(35, 40), parent=bordureChoixBouton, actionAuSurvol="", texte=">", bordureLargeur=2, policeTaille=30, texteAlignement="CC") #Bouton pour changer le chiffrage
texteCleVigenere = MEntreeTexte(position=(170, 280), taille=(160, 35), parent=app, bordureLargeur=4, caracteresAuthorises=(ALPHA_UPPER), policeTaille=20, texteAlignement="CC") #Clé de Vigenère (disponible que quand le chiffrage est à Vigenère)
texteCrypter = MEntreeTexte(position=(100, 320), taille=(300, 90), parent=app, ligneLongueurMax=280, ligneMax=3, bordureRayon=15, policeTaille=22, texteAlignement="GH") #Entrée du texte chiffré

while True: #Boucle infini tant que l'évènement "quitter" n'est pas vue
    app.frame()

    if boutonDroiteChoixBouton.get_clicke() or boutonGaucheChoixBouton.get_clicke():
        if bordureChoixBouton.get_texte() == "Rot13":
            bordureChoixBouton.set_texte("Vigenère")
        else:
            bordureChoixBouton.set_texte("Rot13")

    if bordureChoixBouton.get_texte() == "Rot13":
        texteCleVigenere.set_visible(False)
    else:
        texteCleVigenere.set_visible(True)
    
    if boutonCrypter.get_clicke(): #Crypter le texte
        if bordureChoixBouton.get_texte() == "Rot13": #Avec rot13
            texte = texteDecrypter.get_texte() #Obtention du texte à crypter
            resultat = rot13(texte)
            texteCrypter.set_texte(resultat) #Appliquage du résultat final
        else: #Avec Vigenère
            texte = texteDecrypter.get_texte() #Obtention du texte à crypter
            cle = texteCleVigenere.get_texte() #Obtention de la clé Vigenère
            clePosition = 0 #Position du caractère dans la clé lors de l'analyse
            resultat = ""
            for c in texte: #Analyse de chaque caractères
                if strAlpha(c): #Si le caractère est dans l'alphabet
                    cleNombre = ord(cle[clePosition]) - 65 #Calcul du caractère de la clé
                    texteNombre = ord(c) + cleNombre #Appliquation du déchiffrage
                    if strAlphaLower(c): #Ajuster le caractère
                        if texteNombre > 122:
                            texteNombre -= 26
                    elif strAlphaUpper(c): #Ajuster le caractère
                        if texteNombre > 91:
                            texteNombre -= 26
                    resultat += chr(texteNombre)
                    clePosition += 1
                    if clePosition >= len(cle):
                        clePosition = 0
                else: #Si il n'est pas dans l'alphabet
                    resultat += c
            texteCrypter.set_texte(resultat)
    elif boutonDecrypter.get_clicke(): #Décrypter le texte
        if bordureChoixBouton.get_texte() == "Rot13": #Avec rot13
            texte = texteCrypter.get_texte() #Obtention du texte à crypter
            resultat = rot13Dechiffrage(texte)
            texteDecrypter.set_texte(resultat) #Appliquage du résultat final
        else: #Avec Vigenère
            texte = texteCrypter.get_texte() #Obtention du texte à crypter
            cle = texteCleVigenere.get_texte() #Obtention de la clé Vigenère
            clePosition = 0 #Position du caractère dans la clé lors de l'analyse
            resultat = ""
            for c in texte: #Analyse de chaque caractères
                if strAlpha(c): #Si le caractère est dans l'alphabet
                    cleNombre = ord(cle[clePosition]) - 65 #Calcul du caractère de la clé
                    texteNombre = ord(c) - cleNombre #Appliquation du déchiffrage
                    if strAlphaLower(c): #Ajuster le caractère
                        if texteNombre < 97:
                            texteNombre += 26
                    elif strAlphaUpper(c): #Ajuster le caractère
                        if texteNombre < 65:
                            texteNombre += 26
                    resultat += chr(texteNombre)
                    clePosition += 1
                    if clePosition >= len(cle):
                        clePosition = 0
                else: #Si il n'est pas dans l'alphabet
                    resultat += c
            texteDecrypter.set_texte(resultat)
    
    display.flip()


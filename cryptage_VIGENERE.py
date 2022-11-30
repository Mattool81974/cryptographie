#Par Illiam Pont Layus
def vigenere(cle, message):

 # La fonction d'encodage se base sur :
 # message : le message à chiffrer en  chaine de caractères
# cle : la clé à utiliser en   chaine de caractères
 # Elle retourne le message chiffré en  chaine  caractères

    indice_cle = 0
    msg_code = ""

    for i in range(0, len(message)):
        if 'A' <= message[i] <= 'Z':
            msg_code +=  chr((((ord(message[i]) - ord('A')) + (ord(cle[indice_cle]) - ord('A'))) % 26) + ord('A'))# on met en chaine de caractéres le calcul du rang dees lettres

            indice_cle =  (indice_cle + 1) % len(cle) #on incremente 1 et le divise par la longueur de la clé qui nous renvera le reste de la division
        else:
            msg_code +=  message[i]  # on ajoute le tous les index de message au  message codé
    return msg_code # on retourne en programme le messsage codé

def decode_vigenere(cle,message):
# cette fois si le programme sera  quasiment  pareille à un détaille près
# La fonction de décodage se base sur :
# message : le message chiffré enchaine de caractères
# cle : la clé à utiliser en chaine dee caractères
# Elle retourne le message en  chaine de caractères

    indice_cle = 0
    msg_code = ""

    for i in range(0, len(message)):
        if 'A' <= message[i] <= 'Z':
            msg_code +=  chr((((ord(message[i]) - ord('A')) - (ord(cle[indice_cle]) - ord('A'))) % 26) + ord('A')) #dans ce calcul on va faire la différence entre le code asscii des index de la variable message avec le code asscii de l'index de clé  qui à contrario dans le programme de chiffrement on fessait l'addtion
            indice_cle =  (indice_cle + 1) % len(cle)
        else:
            msg_code +=  message[i]
    return msg_code
#Par Alexis Bergère
def decale(lettre,n):
    s=ord(lettre)
    #si s est dans l'alphabet
    if (s >= 65 and s <= 90) or (s >= 97 and s <= 122):
        s=s+n
        if (s>90 and (ord(lettre) >= 65 and ord(lettre) <= 90)) or (s > 122 and (ord(lettre) >= 97 and ord(lettre) <= 122)):
            s=s-26
        elif (s < 65 and (ord(lettre) >= 65 and ord(lettre) <= 90)) or (s < 97 and (ord(lettre) >= 97 and ord(lettre) <= 122)):
            s=s+26
    return chr(s) 

def rot(phrase,n):
    #variable qui contiendras le texte finale 
    ss=""
    #decalage de chaque caractère de phrase
    for k in phrase:
        ss=ss+decale(k,n)
    #retour du resultat
    return (ss)

def rot13(phrase):
    return rot(phrase, 13)

def rot13Dechiffrage(phrase):
    return rot(phrase, -13)
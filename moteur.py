#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
Gérer les photos à répartir équitablement entre les articles

voir les lignes vides en trop (y'a une option dans jinja)
"""

import jinja2
import os
import imghdr
import argparse

def list_images(path=''):
    """
    Retourne la liste des fichier jpeg dans path
    """
    images = [f for f in os.listdir(path) if os.path.isfile(''.join([path, f]))]
    # on vérifie que ce sont des fichiers jpeg
    for fichier in images:
        if imghdr.what(''.join([path, fichier])) != "jpeg":
            images.remove(fichier)

    images.sort()
    return images

if __name__ == '__main__':
    """
    Création automatique de site photo
    """

    parser = argparse.ArgumentParser(description='Générateur de page web')

    args = parser.parse_args()

    # creation du jeux de données
    # ce sera un tableau d'élément pour chaque article
    # nom du fichier - nom reduit - titre

    articles = list_images('./site/asptthb/images/articles/')
    photos = list_images('./site/asptthb/images/photos/')

    # on construit le jeux de donnees avec les articles
    jeux = []
    path_file = 'images/articles/'
    for fichier in articles:
        court = os.path.splitext(fichier)
        reduit = court[0] + '_reduit' + court[1]
        jeux.append((''.join([path_file, fichier]), ''.join([path_file, 'reduit/', reduit]), 'Titre'))

    # on ajoute les photos aux jeux de données
    # => utiliser la fonction list.insert
    compteur = len(jeux) / len(photos)
    place = compteur
    path_file = 'images/photos/'
    for indice in range(len(photos)):
        court = os.path.splitext(photos[indice])
        reduit = court[0] + '_reduit' + court[1]
        jeux.insert(place, (''.join([path_file, photos[indice]]), ''.join([path_file, 'reduit/', reduit]), 'Photos Christian Kruppa'))
        place = place + compteur

    # application du template
    templateLoader = jinja2.FileSystemLoader(searchpath="./template/asptthb/")
    templateEnv = jinja2.Environment(loader=templateLoader)

    template = templateEnv.get_template("index.jinja")

    templateVars = {"jeux": jeux}

    outputText = template.render(templateVars)

    # création du fichier html
    fd = os.open('./site/asptthb/index.html', os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
    os.write(fd, outputText.encode('UTF-8'))
    os.close(fd)

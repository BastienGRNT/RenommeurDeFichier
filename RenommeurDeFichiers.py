#Warning ce Script à était fait à l'aide d'une IA (principalement pour l'utilisation du module Tkinter)

import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class RenommeurFichiersApp:
    def __init__(self, racine):
        #Initialisation de la fenêtre principale et des widgets
        self.racine = racine
        self.racine.title("Renommeur de Fichiers")
        self.index_fichier = 0  #Index du fichier actuel
        self.fichiers = []  #Liste des fichiers dans le dossier

        #Bouton pour choisir un dossier
        self.bouton_choisir_dossier = tk.Button(racine, text="Choisir un dossier", command=self.choisir_dossier)
        self.bouton_choisir_dossier.pack(pady=20)

        #Cadre pour afficher les informations de fichier et le bouton de renommage
        self.cadre = tk.Frame(racine)
        self.cadre.pack(pady=20)

        #Label pour indiquer l'endroit où renommer le fichier
        self.etiquette_instruction_renommage = tk.Label(self.cadre, text="Renommer le fichier ici :")
        self.etiquette_instruction_renommage.pack(pady=5)

        #Entrée pour saisir le nouveau nom du fichier
        self.entree_nouveau_nom = tk.Entry(self.cadre, width=50)
        self.entree_nouveau_nom.pack(pady=10)

        #Label pour afficher l'aperçu du fichier
        self.etiquette_apercu = tk.Label(self.cadre)
        self.etiquette_apercu.pack(pady=10)

        #Bouton pour valider le renommage et passer au fichier suivant
        self.bouton_renommer = tk.Button(self.cadre, text="Renommer", command=self.renommer_fichier)
        self.bouton_renommer.pack(pady=20)

    def choisir_dossier(self):
        #Fonction pour choisir un dossier et lister les fichiers
        self.dossier = filedialog.askdirectory()
        if self.dossier:
            #Lister tous les fichiers dans le dossier sélectionné
            self.fichiers = [f for f in os.listdir(self.dossier) if os.path.isfile(os.path.join(self.dossier, f))]
            if self.fichiers:
                #Afficher le premier fichier
                self.afficher_fichier()
            else:
                #Afficher un message si le dossier est vide
                messagebox.showinfo("Information", "Le dossier sélectionné est vide.")

    def afficher_fichier(self):
        #Fonction pour afficher le fichier actuel et son aperçu
        if self.index_fichier < len(self.fichiers):
            chemin_fichier = os.path.join(self.dossier, self.fichiers[self.index_fichier])
            self.entree_nouveau_nom.delete(0, tk.END)
            self.entree_nouveau_nom.insert(0, self.fichiers[self.index_fichier])

            try:
                #Tenter d'afficher un aperçu si c'est une image
                img = Image.open(chemin_fichier)
                img.thumbnail((200, 200))
                img = ImageTk.PhotoImage(img)
                self.etiquette_apercu.config(image=img)
                self.etiquette_apercu.image = img
            except Exception as e:
                #Afficher un message si l'aperçu n'est pas disponible
                self.etiquette_apercu.config(image='', text=f"Pas d'aperçu disponible pour {self.fichiers[self.index_fichier]}")

    def renommer_fichier(self):
        #Fonction pour renommer le fichier et passer au suivant
        nouveau_nom = self.entree_nouveau_nom.get()
        if nouveau_nom:
            ancien_chemin_fichier = os.path.join(self.dossier, self.fichiers[self.index_fichier])
            nouveau_chemin_fichier = os.path.join(self.dossier, nouveau_nom)
            os.rename(ancien_chemin_fichier, nouveau_chemin_fichier)
            self.fichiers[self.index_fichier] = nouveau_nom
        self.index_fichier += 1
        if self.index_fichier < len(self.fichiers):
            #Afficher le fichier suivant
            self.afficher_fichier()
        else:
            #Afficher un message et fermer la fenêtre une fois tous les fichiers traités
            messagebox.showinfo("Information", "Tous les fichiers ont été renommés.")
            self.racine.quit()


if __name__ == "__main__":
    racine = tk.Tk()
    app = RenommeurFichiersApp(racine)
    racine.mainloop()
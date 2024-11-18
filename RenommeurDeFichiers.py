import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class RenommeurFichiersApp:
    def __init__(self, racine):
        self.racine = racine
        self.racine.title("Renommeur de Fichiers")
        self.index_fichier = 0 
        self.fichiers = []

        self.bouton_choisir_dossier = tk.Button(racine, text="Choisir un dossier", command=self.choisir_dossier)
        self.bouton_choisir_dossier.pack(pady=20)

        self.cadre = tk.Frame(racine)
        self.cadre.pack(pady=20)

        self.etiquette_instruction_renommage = tk.Label(self.cadre, text="Renommer le fichier ici :")
        self.etiquette_instruction_renommage.pack(pady=5)

        self.entree_nouveau_nom = tk.Entry(self.cadre, width=50)
        self.entree_nouveau_nom.pack(pady=10)

        self.etiquette_apercu = tk.Label(self.cadre)
        self.etiquette_apercu.pack(pady=10)

        self.bouton_renommer = tk.Button(self.cadre, text="Renommer", command=self.renommer_fichier)
        self.bouton_renommer.pack(pady=20)

    def choisir_dossier(self):
        self.dossier = filedialog.askdirectory()
        if self.dossier:
            self.fichiers = [f for f in os.listdir(self.dossier) if os.path.isfile(os.path.join(self.dossier, f))]
            if self.fichiers:
                self.afficher_fichier()
            else:
                messagebox.showinfo("Information", "Le dossier sélectionné est vide.")

    def afficher_fichier(self):
        if self.index_fichier < len(self.fichiers):
            chemin_fichier = os.path.join(self.dossier, self.fichiers[self.index_fichier])
            self.entree_nouveau_nom.delete(0, tk.END)
            self.entree_nouveau_nom.insert(0, self.fichiers[self.index_fichier])

            try:
                img = Image.open(chemin_fichier)
                img.thumbnail((200, 200))
                img = ImageTk.PhotoImage(img)
                self.etiquette_apercu.config(image=img)
                self.etiquette_apercu.image = img
            except Exception as e:
                self.etiquette_apercu.config(image='', text=f"Pas d'aperçu disponible pour {self.fichiers[self.index_fichier]}")

    def renommer_fichier(self):
        nouveau_nom = self.entree_nouveau_nom.get()
        if nouveau_nom:
            ancien_chemin_fichier = os.path.join(self.dossier, self.fichiers[self.index_fichier])
            nouveau_chemin_fichier = os.path.join(self.dossier, nouveau_nom)
            os.rename(ancien_chemin_fichier, nouveau_chemin_fichier)
            self.fichiers[self.index_fichier] = nouveau_nom
        self.index_fichier += 1
        if self.index_fichier < len(self.fichiers):
            self.afficher_fichier()
        else:
            messagebox.showinfo("Information", "Tous les fichiers ont été renommés.")
            self.racine.quit()


if __name__ == "__main__":
    racine = tk.Tk()
    app = RenommeurFichiersApp(racine)
    racine.mainloop()

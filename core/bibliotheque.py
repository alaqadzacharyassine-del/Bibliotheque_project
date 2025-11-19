from typing import List, Dict
from collections import Counter
import matplotlib.pyplot as plt
from bibliotheque_project.models.livre import Livre
from bibliotheque_project.models.utilisateur import Utilisateur

class Bibliotheque:
    """
    Représente la bibliothèque et gère les livres, utilisateurs et emprunts.
    """

    def __init__(self) -> None:
        """
        Initialise la bibliothèque avec des dictionnaires pour les livres et utilisateurs.

        Args:
            Aucun

        Returns:
            None
        """
        self._livres: Dict[int, Livre] = {}
        self._utilisateurs: Dict[int, Utilisateur] = {}

    # ---------- Gestion livres ----------
    def ajouter_livre(self, titre: str, auteur: str) -> Livre:
        """
        Ajoute un nouveau livre à la bibliothèque et le retourne.

        Args:
            titre (str) : Titre du livre.
            auteur (str) : Auteur du livre.

        Returns:
            Livre: L'objet Livre ajouté a la bibliothèque
        """
        livre = Livre(titre, auteur)
        self._livres[livre.id] = livre
        return livre

    def supprimer_livre(self, livre_id: int) -> bool:
        """
        Supprime un livre uniquement s'il est disponible.
        Retourne True si le livre a bien été supprimé.

        Args:
            livre_id (int) : ID du livre a supprimer.

        Raises:
            KeyError : Si le livre n'existe pas.
            ValueError : Si le livre est actuellement emprunté.

        Returns:
            bool : True si le livre a bien été supprimé.
        """
        livre = self._livres.get(livre_id)
        if livre is None:
            raise KeyError(f"Aucun livre avec id={livre_id}.")
        if not livre.est_disponible():
            raise ValueError("Impossible de supprimer un livre emprunté.")
        del self._livres[livre_id]
        return True

    def modifier_status(self, livre_id: int, status: str) -> None:
        """
        Modifie le statut du livre (disponible/emprunté).

        Args:
            livre_id (int) : ID du livre dont on doit modifier le statut.
            status (str) : Nouveaux statut du livre ('disponible' ou 'emprunté').

        Raises:
            KeyError: Si le livre n'existe pas.
            ValueError: Si le statut fourni est invalide.

        Returns:
            None
        """
        if status not in ("disponible", "emprunté"):
            raise ValueError("Status invalide. Utilisez 'disponible' ou 'emprunté'.")
        livre = self._livres.get(livre_id)
        if livre is None:
            raise KeyError(f"Aucun livre avec id={livre_id}.")
        livre.status = status

    def lister_tous_les_livres(self) -> List[Livre]:
        """
        Retourne la liste de tous les livres de la bibliothèque.
        Args:
            Aucun

        Returns:
            List[Livre]: Liste de tous les livres dans la bibliothèque.
        """
        return list(self._livres.values())

    def lister_livres_disponibles(self) -> List[Livre]:
        """
        Retourne la liste des livres disponibles, c'est a dire non emprunté.
        Args:
            Aucun

        Returns:
            List[Livre]: Liste de tous les livres disponibles a l'emprunt.
        """
        return [livre for livre in self._livres.values() if livre.est_disponible()]

    def rechercher_par_titre(self, query: str) -> List[Livre]:
        """
        Recherche des livres dont le titre contient la chaine fournie (insensible à la casse).

        Args:
            query (str) : Chaine de recherche qui se retrouve dans le titre

        Returns:
            List[Livre]: Liste des livres correspondant, c'est a dire retrouvant la chaine fournie dans leurs titres.
        """
        q = query.lower() #Convertie la chaine de caractère en minuscule
        return [livre for livre in self._livres.values() if q in livre.titre.lower()]

    def rechercher_par_auteur(self, query: str) -> List[Livre]:
        """
        Recherche des livres dont l'auteur contient la chaine fournie (insensible à la casse).

        Args:
            query (str): Chaine de recherche qui se retrouve dans l'auteur

        Returns:
            List[Livre]: Liste des livres correspondant, c'est a dire retrouvant la chaine fournie dans l'auteur.
        """
        q = query.lower()
        return [livre for livre in self._livres.values() if q in livre.auteur.lower()]

    def rechercher_par_mot_clef(self, query: str) -> List[Livre]:
        """
        Recherche des livres dont le titre ou l'auteur contient la chaine fournie (insensible a la casse).

        Args:
            query (str): Chaîne de recherche contenant les mots clés souhaités.

        Returns:
            List[Livre]: Liste des livres correspondants, c'est a dire ou les mots clé apparaissent dans l'auteur ou le titre du livre.
        """
        q = query.lower()
        return [livre for livre in self._livres.values() if q in livre.titre.lower() or q in livre.auteur.lower()]

    # ---------- Gestion utilisateurs ----------
    def creer_utilisateur(self, nom: str) -> Utilisateur:
        """
        Crée un nouvel utilisateur et l'ajoute à la bibliothèque.

        Args:
            nom (str): Nom de l'utilisateur.

        Returns:
            Utilisateur: L'objet Utilisateur créé.
        """
        u = Utilisateur(nom)
        self._utilisateurs[u.id] = u
        return u

    def supprimer_utilisateur(self, utilisateur_id: int) -> bool:
        """
        Supprime un utilisateur uniquement s'il n'a aucun livre emprunté et qu'il existe.

        Args:
            utilisateur_id (int): ID de l'utilisateur.

        Raises:
            KeyError: Si l'utilisateur n'existe pas.
            ValueError: Si l'utilisateur a encore des livres empruntés.

        Returns:
            bool: True si la suppression a réussi.
        """
        u = self._utilisateurs.get(utilisateur_id)
        if u is None:
            raise KeyError(f"Aucun utilisateur avec id={utilisateur_id}.")
        if u.livres_empruntes:
            raise ValueError("Impossible de supprimer un utilisateur qui a des livres empruntés.")
        del self._utilisateurs[utilisateur_id]
        return True

    def lister_utilisateurs(self) -> List[Utilisateur]:
        """
        Retourne la liste de tous les utilisateurs.

        Args:
            Aucun

        Returns:
            List[Utilisateur]: Liste des utilisateurs.
        """
        return list(self._utilisateurs.values())

    # ---------- Emprunts / Retours ----------
    def emprunter(self, utilisateur_id: int, livre_id: int) -> None:
        """
        Permet à un utilisateur si il existe d'emprunter un livre si ce dernier est disponible et existe
        Met à jour le statut du livre et la liste d'emprunts de l'utilisateur.

        Args:
            utilisateur_id (int): ID de l'utilisateur.
            livre_id (int): ID du livre à emprunter.

        Raises:
            KeyError: Si l'utilisateur ou le livre n'existe pas.
            ValueError: Si le livre n'est pas disponible.

        Returns:
            None
        """
        u = self._utilisateurs.get(utilisateur_id)
        livre = self._livres.get(livre_id)
        if u is None:
            raise KeyError(f"Aucun utilisateur avec id={utilisateur_id}.")
        if livre is None:
            raise KeyError(f"Aucun livre avec id={livre_id}.")
        if not livre.est_disponible():
            raise ValueError("Le livre n'est pas disponible pour emprunt.")
        livre.emprunter()
        u.emprunter_livre(livre_id)

    def rendre(self, utilisateur_id: int, livre_id: int) -> None:
        """
        Permet à un utilisateur existant de rendre un livre qui est enregistré dans la bibliothèque et qu'il a emprunté.
        Met à jour le statut du livre et retire le livre de la liste d'emprunts de l'utilisateur.

        Args:
            utilisateur_id (int): ID de l'utilisateur.
            livre_id (int): ID du livre à rendre.

        Raises:
            KeyError: Si l'utilisateur ou le livre n'existe pas.
            ValueError: Si l'utilisateur n'a pas emprunté ce livre.

        Returns:
            None
        """
        u = self._utilisateurs.get(utilisateur_id)
        livre = self._livres.get(livre_id)
        if u is None:
            raise KeyError(f"Aucun utilisateur avec id={utilisateur_id}.")
        if livre is None:
            raise KeyError(f"Aucun livre avec id={livre_id}.")
        if livre_id not in u.livres_empruntes:
            raise ValueError("Cet utilisateur n'a pas emprunté ce livre.")
        livre.rendre()
        u.rendre_livre(livre_id)

    # ---------- Statistiques ----------
    def nombre_total_livres(self) -> int:
        """
        Retourne le nombre total de livres dans la bibliothèque.

        Args:
            Aucun

        Returns:
            int: Nombre total de livres.
        """
        return len(self._livres)

    def nombre_total_utilisateurs(self) -> int:
        """
        Retourne le nombre total d'utilisateurs dans la bibliothèque.

        Args:
            Aucun

        Returns:
            int: Nombre total d'utilisateurs.
        """
        return len(self._utilisateurs)

    def distribution_emprunts_par_utilisateur(self) -> Dict[int, int]:
        """
        Retourne un dictionnaire {utilisateur_id: nombre_emprunts}.

        Args:
            Aucun

        Returns:
            Dict[int,int]: Distribution des emprunts par utilisateur.
        """
        return {u.id: u.nb_emprunts() for u in self._utilisateurs.values()}

    def histogramme_emprunts(self) -> Dict[int, int]:
        """
        Retourne un histogramme des emprunts {nombre_emprunts: nombre_utilisateurs}.

        Args:
            Aucun

        Returns:
            Dict[int,int]: Histogramme des emprunts.
        """
        counts = [u.nb_emprunts() for u in self._utilisateurs.values()]
        return dict(Counter(counts))



    def afficher_histogramme_emprunts(self) -> None:
        """
        Affiche un histogramme des emprunts par utilisateur avec matplotlib.

        Args:
            Aucun

        Returns:
            None
        """
        counts = [u.nb_emprunts() for u in self._utilisateurs.values()]
        if not counts:
            print("Aucun utilisateur pour afficher l'histogramme.")
            return

        histo = Counter(counts)
        x = list(histo.keys())
        y = list(histo.values())

        plt.bar(x, y, color='skyblue')
        plt.xlabel("Nombre d'emprunts")
        plt.ylabel("Nombre d'utilisateurs")
        plt.title("Histogramme des emprunts par utilisateur")
        plt.xticks(x)  # pour afficher chaque nombre d'emprunts
        plt.show()
    # ---------- Utilitaires pour affichage ----------
    def affiche_livres(self) -> None:
        """
        Affiche tous les livres dans la console.

        Args:
            Aucun

        Returns:
            None
        """
        if not self._livres:
            print("Aucun livre en base.")
            return
        for livre in sorted(self._livres.values(), key=lambda x: x.id):
            print(f"ID : {livre.id} | Titre : {livre.titre} | Auteur :  {livre.auteur} | Status : {livre.status}")

    def affiche_utilisateurs(self) -> None:
        """
        Affiche tous les utilisateurs dans la console.

        Args:
            Aucun

        Returns:
            None
        """
        if not self._utilisateurs:
            print("Aucun utilisateur enregistré.")
            return
        for u in sorted(self._utilisateurs.values(), key=lambda x: x.id):
            print(f"ID : {u.id} | Nom : {u.nom} | emprunts: {u.livres_empruntes}")

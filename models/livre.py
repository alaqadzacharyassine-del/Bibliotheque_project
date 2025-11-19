from typing import Literal


class Livre:
    """
    Représente un livre dans la bibliothèque caractérisé par un ID unique automatique, un titre, un auteur et un statut.
    """

    _next_id = 1 #On auto-incrémente l'ID pour qu'il soit unique

    def __init__(self, titre: str, auteur: str, status: Literal["disponible", "emprunté"] = "disponible")->None:
        """
        Crée un nouveau livre caractérisé par un ID unique automatique, un titre, un auteur et un status (disponible par défaut).

        Args:
            titre (str): Le titre du livre.
            auteur (str): L'auteur du livre.
            status (str, optionnel): 'disponible' ou 'emprunté'. Par défaut 'disponible'.

        Returns:
            None
        """
        self.id: int = Livre._next_id
        Livre._next_id += 1
        self.titre: str = titre
        self.auteur: str = auteur
        self.status: Literal["disponible", "emprunté"] = status

    def est_disponible(self) -> bool:
        """
        Vérifie si le livre est disponible a l'emprunt.

        Args:
            Aucun

        Returns:
            bool : True si le livre est disponible, False sinon.
        """
        return self.status == "disponible"

    def emprunter(self) -> None:
        """
        Change de statut du livre lorsqu'il est emprunté quand il est disponible.
        Renvoie une erreur si un livre non disponible tente d'etre emprunter

        Args:
            Aucun

        Returns:
            None
        """
        if not self.est_disponible():
            raise ValueError(f"Le livre '{self.titre}' (id={self.id}) n'est pas disponible.")
        self.status = "emprunté"

    def rendre(self) -> None:
        """
        Permet de rendre le livre et donc de re mettre son statut disponible.

        Args:
            Aucun

        Returns:
            None
        """
        self.status = "disponible"

    def __repr__(self) -> str:
        """"
        Renvoie une représentation textuelle du livre pour le débogage.

        Args:
            Aucun

        Returns:
            str: Représentation textuelle du livre avec l'ID, le titre, l'auteur et le statut.
        """""
        return f"<Livre id={self.id} titre={self.titre!r} auteur={self.auteur!r} status={self.status}>"

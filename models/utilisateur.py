from typing import List

class Utilisateur:
    """
    Représente un utilisateur de la bibliothèque caractérisé par un ID unique, un nom et une liste de livres empruntés
    """

    _next_id = 1 #Auto-incrémente l'ID pour qu'il soit unique

    def __init__(self, nom: str)->None:
        """
        Crée un nouvel utilisateur avec un ID unique attribué automatiquement, un nom et
        une liste de livre emprunté qui est vide au départ car il a emprunté aucun livre avant d'etre créer.

        Args:
            nom (str): Nom de l'utilisateur.

        Returns:
            None
        """
        self.id: int = Utilisateur._next_id
        Utilisateur._next_id += 1
        self.nom: str = nom
        self.livres_empruntes: List[int] = []

    def emprunter_livre(self, livre_id: int) -> None:
        """
        Permet d'emprunter un livre en l'ajoutant à la liste des emprunts de l'utilisateur.
        Renvoie une erreur si le livre est déjà emprunté.

        Args:
            livre_id (int): L'identifiant du livre a emprunter.

        Raises:
            ValueError: Si le livre est déja emprunté.

        Returns:
            None
        """
        if livre_id in self.livres_empruntes:
            raise ValueError(f"L'utilisateur {self.nom} (id={self.id}) a déjà le livre id={livre_id}.")
        self.livres_empruntes.append(livre_id)

    def rendre_livre(self, livre_id: int) -> None:
        """
        Permet de rendre un livre en le retirant de la liste des emprunts de l'utilisateur.
        Renvoie une erreur si le livre n'était pas emprunté.

        Args:
            livre_id (int): L'identifiant du livre à rendre.

        Raises:
            ValueError: Si le livre n'est pas dans la liste des emprunts.

        Returns:
            None
        """
        try:
            self.livres_empruntes.remove(livre_id)
        except ValueError:
            raise ValueError(f"Le livre id={livre_id} n'est pas dans la liste d'emprunts de {self.nom} (id={self.id}).")

    def nb_emprunts(self) -> int:
        """
        Retourne le nombre de livres actuellement empruntés par l'utilisateur.

        Args:
            Aucun

        Returns:
            int: Le nombre de livre emprunté par l'utilisateur.
        """
        return len(self.livres_empruntes)

    def __repr__(self) -> str:
        """
        Fournit une représentation textuelle de l'utilisateur pour le débogage.

        Args:
            Aucun

        Returns:
            str: Représentation de l'utilisateur avec l'ID, le nom et la liste des emprunts.
        """
        return f"<Utilisateur id={self.id} nom={self.nom!r} emprunts={self.livres_empruntes}>"

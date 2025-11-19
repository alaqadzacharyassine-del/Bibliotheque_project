import pytest
from bibliotheque_project.models.utilisateur import Utilisateur

def test_emprunter_livre():
    """
    Vérifie que la méthode emprunter_livre ajoute correctement un livre à la liste d'emprunts de l'utilisateur concerné
    et renvoie une erreur si l'utilisateur tente d'emprunter un livre non disponible.
    """
    u = Utilisateur("Alice")

    # Cas 1 : emprunt normal
    u.emprunter_livre(1)
    assert 1 in u.livres_empruntes

    # Cas 2 : emprunt du même livre à nouveau → erreur
    with pytest.raises(ValueError):
        u.emprunter_livre(1)

def test_rendre_livre():
    """
    Vérifie que la méthode rendre_livre retire correctement un livre de la liste d'emprunts de l'utilisateur concerné
    et renvoie une erreur si le livre n'était pas emprunté par l'utilisateur.
    """
    u = Utilisateur("Alice")

    # Cas 1 : livre emprunté → on peut le rendre
    u.emprunter_livre(1)
    u.rendre_livre(1)
    assert 1 not in u.livres_empruntes

    # Cas 2 : livre non emprunté → erreur
    with pytest.raises(ValueError):
        u.rendre_livre(2)

def test_nb_emprunts():
    """
    Vérifie que la méthode nb_emprunts retourne correctement
    le nombre de livres actuellement empruntés par l'utilisateur.
    """
    u = Utilisateur("Alice")

    # Cas 1 : aucun emprunt
    assert u.nb_emprunts() == 0

    # Cas 2 : emprunt de livres
    u.emprunter_livre(1)
    u.emprunter_livre(2)
    assert u.nb_emprunts() == 2

    # Cas 3 : rendre un livre
    u.rendre_livre(1)
    assert u.nb_emprunts() == 1

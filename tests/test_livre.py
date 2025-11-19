import pytest
from bibliotheque_project.models.livre import Livre

def test_est_disponible():
    """
    Vérifie que la méthode est_disponible retourne True si le livre
    est disponible et False si le livre est emprunté.
    """
    # Livre disponible
    livre1 = Livre("1984", "George Orwell")
    livre1.status = "disponible"
    assert livre1.est_disponible() is True

    # Livre emprunté
    livre2 = Livre("Harry Potter", "J.K. Rowling")
    livre2.status = "emprunté"
    assert livre2.est_disponible() is False

def test_emprunter():
    """
    Vérifie que la méthode emprunter change le statut du livre
    de 'disponible' à 'emprunté' et renvoie une erreur si le livre
    est déjà emprunté.
    """
    # Cas 1 : livre disponible
    livre = Livre("1984", "George Orwell")
    livre.status = "disponible"
    livre.emprunter()
    assert livre.status == "emprunté"

    # Cas 2 : livre déjà emprunté
    livre2 = Livre("Harry Potter", "J.K. Rowling")
    livre2.status = "emprunté"
    with pytest.raises(ValueError) as excinfo:
        livre2.emprunter()
    assert "n'est pas disponible" in str(excinfo.value)

def test_rendre():
    """
    Vérifie que la méthode rendre change le statut du livre
    de 'emprunté' à 'disponible'. Si le livre est déjà disponible,
    le statut reste inchangé.
    """
    # Cas 1 : livre emprunté
    livre = Livre("1984", "George Orwell")
    livre.status = "emprunté"
    livre.rendre()
    assert livre.status == "disponible"

    # Cas 2 : livre déjà disponible
    livre2 = Livre("Harry Potter", "J.K. Rowling")
    livre2.status = "disponible"
    livre2.rendre()
    assert livre2.status == "disponible"


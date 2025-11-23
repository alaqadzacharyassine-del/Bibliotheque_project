import pytest
from bibliotheque_project.models.livre import Livre, StatusLivre

def test_est_disponible():
    """
    Vérifie que la méthode est_disponible retourne True si le livre
    est disponible et False si le livre est emprunté.
    """
    # Livre disponible
    livre1 = Livre("1984", "George Orwell", status=StatusLivre.DISPONIBLE)
    assert livre1.est_disponible() is True

    # Livre emprunté
    livre2 = Livre("Harry Potter", "J.K. Rowling", status=StatusLivre.EMPRUNTE)
    assert livre2.est_disponible() is False

def test_emprunter():
    """
    Vérifie que la méthode emprunter change le statut du livre
    de 'disponible' à 'emprunté' et renvoie une erreur si le livre
    est déjà emprunté.
    """
    # Cas 1 : livre disponible
    livre = Livre("1984", "George Orwell", status=StatusLivre.DISPONIBLE)
    livre.emprunter()
    assert livre.status == StatusLivre.EMPRUNTE

    # Cas 2 : livre déjà emprunté
    livre2 = Livre("Harry Potter", "J.K. Rowling", status=StatusLivre.EMPRUNTE)
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
    livre = Livre("1984", "George Orwell", status=StatusLivre.EMPRUNTE)
    livre.rendre()
    assert livre.status == StatusLivre.DISPONIBLE

    # Cas 2 : livre déjà disponible
    livre2 = Livre("Harry Potter", "J.K. Rowling", status=StatusLivre.DISPONIBLE)
    livre2.rendre()
    assert livre2.status == StatusLivre.DISPONIBLE

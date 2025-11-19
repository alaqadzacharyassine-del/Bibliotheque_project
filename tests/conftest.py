# tests/conftest.py
import pytest
from bibliotheque_project.models.livre import Livre
from bibliotheque_project.models.utilisateur import Utilisateur

@pytest.fixture(autouse=True)
def reset_ids():
    # réinitialise les compteurs d'IDs pour chaque test
    Livre._next_id = 1
    Utilisateur._next_id = 1
    yield

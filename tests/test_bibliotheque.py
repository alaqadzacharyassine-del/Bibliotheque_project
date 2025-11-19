import pytest
from collections import Counter
from bibliotheque_project.core.bibliotheque import Bibliotheque
from bibliotheque_project.models.livre import Livre
from unittest.mock import patch

def test_ajouter_livre():
    """
    Vérifie qu'un livre ajouté à la bibliothèque est correctement enregistré
    avec les attributs titre et auteur et présent dans le dictionnaire interne de la bibliotheque.
    """
    biblio = Bibliotheque()
    livre = biblio.ajouter_livre("1984", "George Orwell")

    # Vérifie que le livre est bien ajouté
    assert livre.id in biblio._livres
    assert biblio._livres[livre.id].titre == "1984"
    assert biblio._livres[livre.id].auteur == "George Orwell"


def test_supprimer_livre_disponible():
    """
    Vérifie que la suppression d'un livre disponible fonctionne
    et que le livre est retiré du dictionnaire interne de la bibliotheque.
    """
    biblio = Bibliotheque()
    livre = biblio.ajouter_livre("1984", "George Orwell")

    # Suppression d'un livre disponible
    result = biblio.supprimer_livre(livre.id)
    assert result is True
    assert livre.id not in biblio._livres


def test_supprimer_livre_emprunte():
    """
    Vérifie que la suppression d'un livre emprunté renvoie une ValueError.
    """
    biblio = Bibliotheque()
    livre = biblio.ajouter_livre("1984", "George Orwell")
    livre.emprunter()  # le livre n'est plus disponible

    # Doit renvoyer une ValueError
    with pytest.raises(ValueError, match="Impossible de supprimer un livre emprunté."):
        biblio.supprimer_livre(livre.id)


def test_supprimer_livre_inexistant():
    """
    Vérifie que la suppression d'un livre inexistant renvoie un KeyError.
    """
    biblio = Bibliotheque()

    # Doit renvoyer un KeyError
    with pytest.raises(KeyError, match="Aucun livre avec id=999."):
        biblio.supprimer_livre(999)


def test_modifier_status_valide():
    """
    Vérifie que le statut d'un livre peut être modifié correctement
    en 'disponible' ou 'emprunté'.
    """
    biblio = Bibliotheque()
    livre = biblio.ajouter_livre("1984", "George Orwell")

    # Modifier le statut en "emprunté"
    biblio.modifier_status(livre.id, "emprunté")
    assert biblio._livres[livre.id].status == "emprunté"

    # Modifier le statut en "disponible"
    biblio.modifier_status(livre.id, "disponible")
    assert biblio._livres[livre.id].status == "disponible"

def test_modifier_status_invalide():
    """
    Vérifie qu'un statut invalide renvoie une ValueError.
    """
    biblio = Bibliotheque()
    livre = biblio.ajouter_livre("1984", "George Orwell")

    # Statut invalide doit renvoyer une ValueError
    with pytest.raises(ValueError, match="Status invalide. Utilisez 'disponible' ou 'emprunté'."):
        biblio.modifier_status(livre.id, "perdu")

def test_modifier_status_livre_inexistant():
    """
    Vérifie qu'un livre inexistant renvoie un KeyError lors de la modification du statut.
    """
    biblio = Bibliotheque()

    # Livre inexistant doit renvoyer un  KeyError
    with pytest.raises(KeyError, match="Aucun livre avec id=999."):
        biblio.modifier_status(999, "disponible")

def test_lister_tous_les_livres():
    """
    Vérifie que la liste de tous les livres retourne correctement tous les objets Livre
    ajoutés à la bibliothèque.
    """
    biblio = Bibliotheque()

    # Au départ, la bibliothèque est vide
    assert biblio.lister_tous_les_livres() == []

    # Ajouter quelques livres
    livre1 = biblio.ajouter_livre("1984", "George Orwell")
    livre2 = biblio.ajouter_livre("Le Petit Prince", "Antoine de Saint-Exupéry")
    livre3 = biblio.ajouter_livre("Harry Potter", "J.K. Rowling")

    # Vérifie que la liste contient tous les livres ajoutés
    livres = biblio.lister_tous_les_livres()
    assert len(livres) == 3
    assert livre1 in livres
    assert livre2 in livres
    assert livre3 in livres

    # Vérifie que ce sont bien des objets Livre
    assert all(isinstance(lv, Livre) for lv in livres)


def test_lister_livres_disponibles():
    """
    Vérifie que lister_livres_disponibles retourne uniquement les livres disponibles
    et que les livres empruntés sont exclus.
    """
    biblio = Bibliotheque()

    # Ajouter plusieurs livres
    livre1 = biblio.ajouter_livre("1984", "George Orwell")
    livre2 = biblio.ajouter_livre("Le Petit Prince", "Antoine de Saint-Exupéry")
    livre3 = biblio.ajouter_livre("Harry Potter", "J.K. Rowling")

    # Emprunter certains livres
    livre2.emprunter()  # maintenant indisponible

    # Récupérer la liste des livres disponibles
    disponibles = biblio.lister_livres_disponibles()

    # Vérifie que le livre emprunté n'est pas dans la liste
    ids_disponibles = [livre.id for livre in disponibles]
    assert livre1.id in ids_disponibles
    assert livre2.id not in ids_disponibles
    assert livre3.id in ids_disponibles

    # Vérifie le nombre de livres disponibles
    assert len(disponibles) == 2

    # Vérifie que tous les éléments ont les attributs attendus (évite problème isinstance)
    assert all(hasattr(livre, "id") and hasattr(livre, "titre") and hasattr(livre, "auteur") for livre in disponibles)

def test_rechercher_par_titre():
    """
    Vérifie que la recherche par titre fonctionne correctement.
    Teste la recherche insensible à la casse, la recherche partielle et la recherche sans résultat.
    """
    biblio = Bibliotheque()

    # Ajouter quelques livres
    livre1 = biblio.ajouter_livre("1984", "George Orwell")
    livre2 = biblio.ajouter_livre("Le Petit Prince", "Antoine de Saint-Exupéry")
    livre3 = biblio.ajouter_livre("Harry Potter et la Chambre des Secrets", "J.K. Rowling")

    # Recherche insensible à la casse
    result = biblio.rechercher_par_titre("petit")
    ids_result = [livre.id for livre in result]
    assert livre2.id in ids_result
    assert livre1.id not in ids_result
    assert livre3.id not in ids_result

    # Recherche partielle
    result = biblio.rechercher_par_titre("harry")
    ids_result = [livre.id for livre in result]
    assert livre3.id in ids_result
    assert len(result) == 1

    # Recherche sans résultat
    result = biblio.rechercher_par_titre("inexistant")
    assert result == []

def test_rechercher_par_auteur():
    """
    Vérifie que la recherche par auteur fonctionne correctement.
    Teste la recherche insensible à la casse, la recherche partielle et la recherche sans résultat.
    """
    biblio = Bibliotheque()

    # Ajouter quelques livres
    livre1 = biblio.ajouter_livre("1984", "George Orwell")
    livre2 = biblio.ajouter_livre("Le Petit Prince", "Antoine de Saint-Exupéry")
    livre3 = biblio.ajouter_livre("Harry Potter et la Chambre des Secrets", "J.K. Rowling")

    # Recherche insensible à la casse
    result = biblio.rechercher_par_auteur("rowling")
    ids_result = [livre.id for livre in result]
    assert livre3.id in ids_result
    assert livre1.id not in ids_result
    assert livre2.id not in ids_result

    # Recherche partielle
    result = biblio.rechercher_par_auteur("george")
    ids_result = [livre.id for livre in result]
    assert livre1.id in ids_result
    assert len(result) == 1

    # Recherche sans résultat
    result = biblio.rechercher_par_auteur("inconnu")
    assert result == []

def test_rechercher_par_mot_clef():
    """
    Vérifie que la recherche par mot-clé fonctionne correctement.
    Teste la recherche sur titre, auteur, recherche partielle et recherche sans résultat.
    """
    biblio = Bibliotheque()

    # Ajouter quelques livres
    livre1 = biblio.ajouter_livre("1984", "George Orwell")
    livre2 = biblio.ajouter_livre("Le Petit Prince", "Antoine de Saint-Exupéry")
    livre3 = biblio.ajouter_livre("Harry Potter et la Chambre des Secrets", "J.K. Rowling")

    # Recherche par mot clé dans le titre
    result = biblio.rechercher_par_mot_clef("petit")
    ids_result = [livre.id for livre in result]
    assert livre2.id in ids_result
    assert livre1.id not in ids_result
    assert livre3.id not in ids_result

    # Recherche par mot clé dans l'auteur
    result = biblio.rechercher_par_mot_clef("rowling")
    ids_result = [livre.id for livre in result]
    assert livre3.id in ids_result
    assert livre1.id not in ids_result
    assert livre2.id not in ids_result

    # Recherche partielle sur titre ou auteur
    result = biblio.rechercher_par_mot_clef("george")
    ids_result = [livre.id for livre in result]
    assert livre1.id in ids_result
    assert len(result) == 1

    # Recherche sans résultat
    result = biblio.rechercher_par_mot_clef("inconnu")
    assert result == []

def test_creer_utilisateur():
    """
    Vérifie la création d'un utilisateur et son enregistrement dans la bibliothèque.
    """
    biblio = Bibliotheque()

    # Créer un utilisateur
    utilisateur = biblio.creer_utilisateur("Alice")

    # Vérifie que l'objet retourné a le bon nom
    assert utilisateur.nom == "Alice"

    # Vérifie que l'utilisateur est bien enregistré dans la bibliothèque
    assert utilisateur.id in biblio._utilisateurs
    assert biblio._utilisateurs[utilisateur.id] == utilisateur

def test_supprimer_utilisateur():
    """
    Vérifie la suppression d'utilisateurs.
    Cas testés : suppression normale, suppression avec livres empruntés et suppression d'un utilisateur inexistant.
    """
    biblio = Bibliotheque()

    # Créer des utilisateurs
    u1 = biblio.creer_utilisateur("Alice")
    u2 = biblio.creer_utilisateur("Bob")

    # Cas 1 : supprimer un utilisateur sans livre emprunté
    assert biblio.supprimer_utilisateur(u1.id) is True
    assert u1.id not in biblio._utilisateurs

    # Cas 2 : essayer de supprimer un utilisateur avec livre emprunté
    livre = biblio.ajouter_livre("1984", "George Orwell")
    u2.emprunter_livre(livre)  # Assure-toi que cette méthode existe
    with pytest.raises(ValueError):
        biblio.supprimer_utilisateur(u2.id)

    # Cas 3 : essayer de supprimer un utilisateur inexistant
    with pytest.raises(KeyError):
        biblio.supprimer_utilisateur(999)

def test_lister_utilisateurs():
    """
    Vérifie que lister_utilisateurs retourne correctement tous les utilisateurs.
    """
    biblio = Bibliotheque()

    # Au départ, la liste est vide
    assert biblio.lister_utilisateurs() == []

    # Ajouter quelques utilisateurs
    u1 = biblio.creer_utilisateur("Alice")
    u2 = biblio.creer_utilisateur("Bob")
    u3 = biblio.creer_utilisateur("Charlie")

    # Récupérer la liste
    utilisateurs = biblio.lister_utilisateurs()

    # Vérifie le nombre d'utilisateurs
    assert len(utilisateurs) == 3

    # Vérifie que tous les IDs sont présents
    ids_utilisateurs = [u.id for u in utilisateurs]
    assert u1.id in ids_utilisateurs
    assert u2.id in ids_utilisateurs
    assert u3.id in ids_utilisateurs

    # Vérifie que les objets récupérés sont bien les mêmes
    assert u1 in utilisateurs
    assert u2 in utilisateurs
    assert u3 in utilisateurs

def test_emprunter():
    """
    Vérifie le fonctionnement de l'emprunt de livres.
    Cas testés : emprunt réussi, livre déjà emprunté, livre inexistant, utilisateur inexistant.
    """
    biblio = Bibliotheque()

    # Créer utilisateur et livres
    u1 = biblio.creer_utilisateur("Alice")
    livre1 = biblio.ajouter_livre("1984", "George Orwell")
    livre2 = biblio.ajouter_livre("Le Petit Prince", "Antoine de Saint-Exupéry")

    # Cas 1 : emprunt réussi
    biblio.emprunter(u1.id, livre1.id)
    assert livre1.status == "emprunté"
    assert livre1.id in u1.livres_empruntes

    # Cas 2 : emprunter un livre déjà emprunté
    with pytest.raises(ValueError):
        biblio.emprunter(u1.id, livre1.id)

    # Cas 3 : emprunter un livre inexistant
    with pytest.raises(KeyError):
        biblio.emprunter(u1.id, 999)

    # Cas 4 : emprunter par un utilisateur inexistant
    with pytest.raises(KeyError):
        biblio.emprunter(999, livre2.id)

def test_rendre():
    """
    Vérifie le fonctionnement du retour de livres.
    Cas testés : rendu normal, livre non emprunté par l'utilisateur, livre inexistant, utilisateur inexistant.
    """
    biblio = Bibliotheque()

    # Créer utilisateur et livres
    u1 = biblio.creer_utilisateur("Alice")
    livre1 = biblio.ajouter_livre("1984", "George Orwell")
    livre2 = biblio.ajouter_livre("Le Petit Prince", "Antoine de Saint-Exupéry")

    # Emprunter un livre pour tester le rendu
    biblio.emprunter(u1.id, livre1.id)

    # Cas 1 : rendre le livre correctement
    biblio.rendre(u1.id, livre1.id)
    assert livre1.status == "disponible"
    assert livre1.id not in u1.livres_empruntes

    # Cas 2 : tenter de rendre un livre non emprunté par l'utilisateur
    with pytest.raises(ValueError):
        biblio.rendre(u1.id, livre2.id)

    # Cas 3 : livre inexistant
    with pytest.raises(KeyError):
        biblio.rendre(u1.id, 999)

    # Cas 4 : utilisateur inexistant
    with pytest.raises(KeyError):
        biblio.rendre(999, livre1.id)

def test_nombre_total_livres():
    """
    Vérifie que la méthode nombre_total_livres() retourne le nombre correct
    de livres dans la bibliothèque.
    Cas testés :
    - Bibliothèque vide au départ
    - Ajout de plusieurs livres et vérification du compteur
    """
    biblio = Bibliotheque()

    # Au départ, il n'y a aucun livre
    assert biblio.nombre_total_livres() == 0

    # Ajouter des livres
    biblio.ajouter_livre("1984", "George Orwell")
    biblio.ajouter_livre("Le Petit Prince", "Antoine de Saint-Exupéry")
    biblio.ajouter_livre("Harry Potter", "J.K. Rowling")

    # Vérifie le nombre total
    assert biblio.nombre_total_livres() == 3

def test_nombre_total_utilisateurs():
    """
    Vérifie que la méthode nombre_total_utilisateurs() retourne le nombre correct
    d'utilisateurs dans la bibliothèque.
    Cas testés :
    - Bibliothèque vide au départ
    - Ajout de plusieurs utilisateurs et vérification du compteur
    """
    biblio = Bibliotheque()

    # Au départ, aucun utilisateur
    assert biblio.nombre_total_utilisateurs() == 0

    # Ajouter des utilisateurs
    u1 = biblio.creer_utilisateur("Alice")
    u2 = biblio.creer_utilisateur("Bob")
    u3 = biblio.creer_utilisateur("Charlie")

    # Vérifie le nombre total
    assert biblio.nombre_total_utilisateurs() == 3



def test_distribution_emprunts_par_utilisateur():
    """
    Vérifie la distribution des emprunts par utilisateur.
    Cas testés :
    - Utilisateurs n'ayant rien emprunté
    - Utilisateurs ayant emprunté un ou plusieurs livres
    """
    biblio = Bibliotheque()

    # Créer utilisateurs et livres
    u1 = biblio.creer_utilisateur("Alice")
    u2 = biblio.creer_utilisateur("Bob")
    livre1 = biblio.ajouter_livre("1984", "George Orwell")
    livre2 = biblio.ajouter_livre("Le Petit Prince", "Antoine de Saint-Exupéry")
    livre3 = biblio.ajouter_livre("Harry Potter", "J.K. Rowling")

    # Au départ, tous les utilisateurs n'ont rien emprunté
    dist = biblio.distribution_emprunts_par_utilisateur()
    assert dist[u1.id] == 0
    assert dist[u2.id] == 0

    # Alice emprunte 2 livres
    biblio.emprunter(u1.id, livre1.id)
    biblio.emprunter(u1.id, livre2.id)

    # Bob emprunte 1 livre
    biblio.emprunter(u2.id, livre3.id)

    # Vérifie la distribution
    dist = biblio.distribution_emprunts_par_utilisateur()
    assert dist[u1.id] == 2
    assert dist[u2.id] == 1

def test_histogramme_emprunts():
    """
    Vérifie la création de l'histogramme des emprunts.
    Cas testés :
    - Aucun emprunt pour tous les utilisateurs
    - Emprunts variés par plusieurs utilisateurs
    - Vérifie la correspondance avec l'histogramme attendu
    """
    biblio = Bibliotheque()

    # Créer utilisateurs et livres
    u1 = biblio.creer_utilisateur("Alice")
    u2 = biblio.creer_utilisateur("Bob")
    u3 = biblio.creer_utilisateur("Charlie")
    livre1 = biblio.ajouter_livre("1984", "George Orwell")
    livre2 = biblio.ajouter_livre("Le Petit Prince", "Antoine de Saint-Exupéry")
    livre3 = biblio.ajouter_livre("Harry Potter", "J.K. Rowling")

    # Au départ, tous ont 0 emprunt
    hist = biblio.histogramme_emprunts()
    assert hist == {0: 3}

    # Alice emprunte 2 livres
    biblio.emprunter(u1.id, livre1.id)
    biblio.emprunter(u1.id, livre2.id)

    # Bob emprunte 1 livre
    biblio.emprunter(u2.id, livre3.id)

    # Charlie n'a rien emprunté
    hist = biblio.histogramme_emprunts()

    # Vérifie histogramme
    resultat = Counter({2: 1, 1: 1, 0: 1})
    assert hist == dict(resultat)

def test_afficher_histogramme_emprunts():
    """
    Vérifie la méthode afficher_histogramme_emprunts().

    Cas testés :
    - Aucun utilisateur : doit afficher un message d'avertissement
    - Plusieurs utilisateurs avec différents nombres d'emprunts :
      plt.show() doit être appelé pour afficher l'histogramme
    """
    biblio = Bibliotheque()

    # Cas 1 : aucun utilisateur
    with patch("builtins.print") as mock_print:
        biblio.afficher_histogramme_emprunts()
        mock_print.assert_called_once_with("Aucun utilisateur pour afficher l'histogramme.")

    # Cas 2 : utilisateurs avec emprunts
    u1 = biblio.creer_utilisateur("Alice")
    u2 = biblio.creer_utilisateur("Bob")
    livre1 = biblio.ajouter_livre("1984", "George Orwell")
    livre2 = biblio.ajouter_livre("Le Petit Prince", "Antoine de Saint-Exupéry")
    livre3 = biblio.ajouter_livre("Harry Potter", "J.K. Rowling")

    biblio.emprunter(u1.id, livre1.id)
    biblio.emprunter(u1.id, livre2.id)
    biblio.emprunter(u2.id, livre3.id)

    # Patch de plt.show pour éviter l'ouverture de la fenêtre graphique
    with patch("matplotlib.pyplot.show") as mock_show:
        biblio.afficher_histogramme_emprunts()
        mock_show.assert_called_once()

def test_affiche_livres(capsys):
    """
    Vérifie la méthode affiche_livres() en capturant la sortie console.
    Cas testés :
    - Bibliothèque vide
    - Bibliothèque avec plusieurs livres
    - Vérifie que les informations affichées contiennent titre, ID et status
    """
    biblio = Bibliotheque()

    # Cas 1 : bibliothèque vide
    biblio.affiche_livres()
    capture = capsys.readouterr()
    assert "Aucun livre en base." in capture.out

    # Cas 2 : ajouter quelques livres
    livre1 = biblio.ajouter_livre("1984", "George Orwell")
    livre2 = biblio.ajouter_livre("Le Petit Prince", "Antoine de Saint-Exupéry")

    biblio.affiche_livres()
    capture = capsys.readouterr()

    # Vérifie que les informations des livres sont dans la sortie
    assert f"ID : {livre1.id} | Titre : {livre1.titre}" in capture.out
    assert f"ID : {livre2.id} | Titre : {livre2.titre}" in capture.out
    assert "Status : disponible" in capture.out


def test_affiche_utilisateurs(capsys):
    """
    Vérifie la méthode affiche_utilisateurs() en capturant la sortie console.
    Cas testés :
    - Aucun utilisateur
    - Plusieurs utilisateurs ajoutés
    - Vérifie que les informations affichées contiennent ID, nom et emprunts
    """
    biblio = Bibliotheque()

    # Cas 1 : aucun utilisateur
    biblio.affiche_utilisateurs()
    captured = capsys.readouterr()
    assert "Aucun utilisateur enregistré." in captured.out

    # Cas 2 : ajouter quelques utilisateurs
    u1 = biblio.creer_utilisateur("Alice")
    u2 = biblio.creer_utilisateur("Bob")

    biblio.affiche_utilisateurs()
    captured = capsys.readouterr()

    # Vérifie que les informations des utilisateurs sont dans la sortie
    assert f"ID : {u1.id} | Nom : {u1.nom}" in captured.out
    assert f"ID : {u2.id} | Nom : {u2.nom}" in captured.out
    # Vérifie la présence de la liste des emprunts (vide au départ)
    assert "emprunts: []" in captured.out

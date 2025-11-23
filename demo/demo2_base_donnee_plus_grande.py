"""
Ce script illustre toutes les fonctions de la bibliothèque dans des cas possibles et impossibles
avec un peu plus de livres et utlisateurs.

- 50 livres définis manuellement
- 10 utilisateurs définis manuellement
- Emprunts choisis précisément (pas de random)
- Même forme que la version précédente (docstrings, variables explicites)

"""

from bibliotheque_project.core.bibliotheque import Bibliotheque
from bibliotheque_project.models.livre import StatusLivre


def sep(title: str) -> None:
    """"
    Creé des séparateur afin de garantir un meilleur affichage lors de la démonstration ci dessous

    Args:
        title (str):Chaine de caractère qu'on souhaite mettre en valeur

    Returns:
        None
    """
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60 + "\n")


def generate_books(biblio: Bibliotheque):
    """
    Génère 50 livres manuellement et les ajoute à la bibliothèque.

    Args:
        biblio (Bibliotheque): Instance de la bibliothèque.

    Returns:
        List[Livre]: Liste des livres ajoutés.
    """
    livres = []
    for i in range(1, 51):
        titre = f"Livre Exemple {i}"
        auteur = f"Auteur {chr(65 + (i - 1) % 26)}"
        livre = biblio.ajouter_livre(titre, auteur)
        livres.append(livre)
    return livres


def generate_users(biblio: Bibliotheque):
    """
    Génère 10 utilisateurs manuellement et les ajoute à la bibliothèque.

    Args:
        biblio (Bibliotheque): Instance de la bibliothèque.

    Returns:
        List[Utilisateur]: Liste des utilisateurs ajoutés.
    """
    utilisateurs = []
    for i in range(1, 11):
        utilisateur = biblio.creer_utilisateur(f"Utilisateur_{i}")
        utilisateurs.append(utilisateur)
    return utilisateurs


def simu_emprunts(biblio: Bibliotheque, utilisateurs, livres):
    """
    Effectue des emprunts manuels précis, pas de random.

    Args:
        biblio (Bibliotheque): Instance de la bibliothèque.
        utilisateurs (List[Utilisateur]): Liste d'utilisateurs.
        livres (List[Livre]): Liste de livres.

    Returns:
        None
    """
    # utilisateur_1 : livres 1,2,3
    biblio.emprunter(utilisateurs[0].id, livres[0].id)
    biblio.emprunter(utilisateurs[0].id, livres[1].id)
    biblio.emprunter(utilisateurs[0].id, livres[2].id)

    # utilisateur_2 : livres 4,5
    biblio.emprunter(utilisateurs[1].id, livres[3].id)
    biblio.emprunter(utilisateurs[1].id, livres[4].id)

    # utilisateur_3 : livre 6
    biblio.emprunter(utilisateurs[2].id, livres[5].id)

    # utilisateur_4 : livres 7,8,9,10
    for i in range(6, 10):
        biblio.emprunter(utilisateurs[3].id, livres[i].id)

    # utilisateur_5 : aucun
    # utilisateur_6 : livre 11
    biblio.emprunter(utilisateurs[5].id, livres[10].id)

    # utilisateur_7 : livres 12,13
    biblio.emprunter(utilisateurs[6].id, livres[11].id)
    biblio.emprunter(utilisateurs[6].id, livres[12].id)

    # utilisateur_8 : aucun
    # utilisateur_9 : livres 14,15,16
    biblio.emprunter(utilisateurs[8].id, livres[13].id)
    biblio.emprunter(utilisateurs[8].id, livres[14].id)
    biblio.emprunter(utilisateurs[8].id, livres[15].id)

    # utilisateur_10 : livre 17
    biblio.emprunter(utilisateurs[9].id, livres[16].id)


def run_demo():
    """
    Démonstration complète de la bibliothèque avec :
    - 50 livres, 10 utilisateurs
    - ajout / suppression de livres (possible et impossible)
    - création / suppression d'utilisateurs (possible et impossible)
    - emprunts / retours (réussis et cas d'erreur)
    - recherches (titre, auteur, mot-clé)
    - modification de statut
    - statistiques et affichage d'un histogramme (matplotlib)

    Args:
        Aucun

    Returns:
        None
    """
    biblio = Bibliotheque()

    sep("1. Génération de 50 livres")
    livres = generate_books(biblio)
    print("50 livres ajoutés.")
    for livre in livres[:]:
        print(livre)

    sep("2. Création des 10 utilisateurs")
    utilisateurs = generate_users(biblio)
    for utilisateur in utilisateurs[:]:
        print(utilisateur)

    sep("3a. Livres disponibles avant emprunt")
    disponibles = biblio.lister_livres_disponibles()
    if not disponibles:
        print("Aucun livre disponible.")
    else:
        print("Livres disponibles :")
        for livre in disponibles:
            print(f"ID : {livre.id} | Titre : {livre.titre} | Auteur : {livre.auteur} | Status : {livre.status.name}")

    sep("3b. Emprunts définis manuellement")
    simu_emprunts(biblio, utilisateurs, livres)
    biblio.affiche_livres()
    biblio.affiche_utilisateurs()

    sep("3c. Livres disponibles après emprunt")
    disponibles = biblio.lister_livres_disponibles()
    if not disponibles:
        print("Aucun livre disponible.")
    else:
        print("Livres disponibles :")
        for livre in disponibles:
            print(f"ID : {livre.id} | Titre : {livre.titre} | Auteur : {livre.auteur} | Status : {livre.status.name}")

    sep("4. Tentative d'emprunt impossible : livre déjà emprunté")
    try:
        biblio.emprunter(utilisateurs[4].id, livres[0].id)
    except Exception as e:
        print("Livre déja emprunté :", type(e).__name__, str(e))

    sep("5. Emprunt impossible : utilisateur ou livre inexistant")
    try:
        biblio.emprunter(999, livres[0].id)
    except Exception as e:
        print("Utilisateur inexistant :", type(e).__name__, str(e))

    try:
        biblio.emprunter(utilisateurs[0].id, 99999)
    except Exception as e:
        print("Livre inexistant :", type(e).__name__, str(e))

    sep("6. Rendre un livre + erreur")
    print(f"{utilisateurs[0].nom} rend le livre 1")
    biblio.rendre(utilisateurs[0].id, livres[0].id)
    print("Retour effectué")

    try:
        biblio.rendre(utilisateurs[0].id, 99999)
    except Exception as e:
        print("Erreur attendue:", type(e).__name__, str(e))

    sep("7. Suppression livre (bloqué si emprunté)")
    try:
        biblio.supprimer_livre(livres[1].id)
    except Exception as e:
        print("Attention — suppression interdite :", type(e).__name__, str(e))

    sep("8. Suppression utilisateur (bloqué s'il a des emprunts)")
    try:
        biblio.supprimer_utilisateur(utilisateurs[1].id)
    except Exception as e:
        print("Attention — suppression interdite :", type(e).__name__, str(e))

    sep("9. Recherches")
    print("Recherche 'Exemple 1' :")
    for livre in biblio.rechercher_par_titre("Exemple 1"):
        print(livre)

    print("Recherche Auteur A :")
    for livre in biblio.rechercher_par_auteur("Auteur A"):
        print(livre)

    sep("10. Statut forcé")
    biblio.modifier_status(livres[20].id, StatusLivre.EMPRUNTE)
    print(biblio._livres[livres[20].id])
    biblio.modifier_status(livres[20].id, StatusLivre.DISPONIBLE)
    print(biblio._livres[livres[20].id])

    sep("11. Statistiques")
    print("Total livres:", biblio.nombre_total_livres())
    print("Total utilisateurs:", biblio.nombre_total_utilisateurs())
    print("Distribution:", biblio.distribution_emprunts_par_utilisateur())
    print("Histogramme:", biblio.histogramme_emprunts())

    print("Affichage de l'histogramme via matplotlib (fermez la fenêtre pour continuer)")
    try:
        biblio.afficher_histogramme_emprunts()
    except Exception as e:
        print("Impossible d'afficher l'histogramme (environnement headless?) :", e)

    sep("Fin de la démo")


if __name__ == "__main__":
    run_demo()

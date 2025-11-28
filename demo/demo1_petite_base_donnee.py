"""
Ce script illustre toutes les fonctions de la bibliothèque dans des cas possibles et impossibles dans un cas très simple.

Scénarios couverts :
- ajout / suppression de livres (possible et impossible)
- création / suppression d'utilisateurs (possible et impossible)
- emprunts / retours (réussis et cas d'erreur)
- recherches (par titre, auteur, mot-clé)
- affichage des utilisateurs, livre et livres disponible
- modification de statut
- statistiques et affichage d'un histogramme via matplotlib

"""
from bibliotheque_project.core.bibliotheque import Bibliotheque
from bibliotheque_project.models.livre import StatusLivre


def sep(title: str) -> None:
    """
    Crée des séparateurs afin de garantir un meilleur affichage lors de la démonstration ci-dessous

    Args:
        title (str):Chaîne de caractère qu'on souhaite mettre en valeur

    Returns:
        None
    """
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60 + "\n")


def run_demo()->None:
    """"
    Génère la demonstration de la gestion de notre bibliothèque avec toutes les fonctionnalités possibles et impossibles:
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

    sep("1. Ajout de livres")
    livre_1 = biblio.ajouter_livre("Le Petit Prince", "Antoine de Saint-Exupéry")
    livre_2 = biblio.ajouter_livre("1984", "George Orwell")
    livre_3 = biblio.ajouter_livre("Clean Code", "Robert C. Martin")
    print("Livres ajoutés :")
    biblio.affiche_livres() #On regarde si les livres ont bien été ajoutés.

    sep("2. Création d'utilisateurs")
    utilisateur_1 = biblio.creer_utilisateur("Alice")
    utilisateur_2 = biblio.creer_utilisateur("Bob")
    print("Utilisateurs :")
    biblio.affiche_utilisateurs() #On regarde si les utilisateurs ont bien été ajoutés.

    sep("3a. Livres disponibles avant emprunt")
    disponibles = biblio.lister_livres_disponibles()
    if not disponibles:
        print("Aucun livre disponible.")
    else:
        print("Livres disponibles :")
        for livre in disponibles:
            print(f"ID : {livre.id} | Titre : {livre.titre} | Auteur : {livre.auteur} | Status : {livre.status.name}")


    sep("3b. Emprunt réussi")
    try:
        print(f"Alice (id={utilisateur_1.id}) emprunte {livre_1.titre} (id={livre_1.id})")
        biblio.emprunter(utilisateur_1.id, livre_1.id)
        print("Emprunt effectué")
    except Exception as e:
        print("Erreur inattendue :", e)
    biblio.affiche_livres() #On regarde les livres et remarque que le statut du livre 1 est bien "emprunté".
    biblio.affiche_utilisateurs() #Alice a bien le livre 1 dans sa liste d'emprunts.

    sep("3c. Livres disponibles après emprunt")
    disponibles = biblio.lister_livres_disponibles()
    if not disponibles:
        print("Aucun livre disponible.")
    else:
        print("Livres disponibles :")
        for livre in disponibles:
            print(f"ID : {livre.id} | Titre : {livre.titre} | Auteur : {livre.auteur} | Status : {livre.status.name}")


    sep("4. Emprunt impossible : livre déjà emprunté")
    try:
        print(f"Bob (id={utilisateur_2.id}) tente d'emprunter {livre_1.titre} (id={livre_1.id})")
        biblio.emprunter(utilisateur_2.id, livre_1.id)
    except Exception as e:
        print("Livre déja emprunté :", type(e).__name__, str(e)) #Erreur car le livre est déja emprunté

    sep("5. Emprunt impossible : utilisateur ou livre non existant")
    try:
        biblio.emprunter(999, livre_2.id)  # utilisateur inexistant
    except Exception as e:
        print("Utilisateur inexistant :", type(e).__name__, str(e))

    try:
        biblio.emprunter(utilisateur_2.id, 999)  # livre inexistant
    except Exception as e:
        print("Livre inexistant :", type(e).__name__, str(e))

    sep("6. Rendre un livre (réussi) et cas d'erreur")
    try:
        print(f"Alice rend {livre_1.titre} (id={livre_1.id})")
        biblio.rendre(utilisateur_1.id, livre_1.id)
        print("Retour effectué")
    except Exception as e:
        print("Erreur attendue :", e)

    # Essayer de rendre un livre que l'utilisateur n'a pas
    try:
        print(f"Bob tente de rendre {livre_2.titre} (id={livre_2.id}) qu'il n'a pas")
        biblio.rendre(utilisateur_2.id, livre_2.id)
    except Exception as e:
        print("Erreur :", type(e).__name__, str(e))

    sep("7. Suppression livre (impossible si emprunté)")
    # Empruntons un livre puis tentons de le supprimer
    biblio.emprunter(utilisateur_2.id, livre_2.id)
    try:
        print(f"Tentative de suppression de {livre_2.titre} (id={livre_2.id}) alors qu'il est emprunté")
        biblio.supprimer_livre(livre_2.id)
    except Exception as e:
        print("Attention — suppression interdite :", type(e).__name__, str(e))

    # Rendre puis supprimer
    biblio.rendre(utilisateur_2.id, livre_2.id)
    try:
        print(f"Suppression de {livre_2.titre} (id={livre_2.id}) après retour")
        ok = biblio.supprimer_livre(livre_2.id)
        print("Suppression effectué ->", ok)
    except Exception as e:
        print("Erreur inattendue lors de la suppression :", e)

    sep("8. Suppression utilisateur (impossible s'il a des emprunts)")
    # Donnons un livre à Alice et tentons de supprimer
    biblio.emprunter(utilisateur_1.id, livre_3.id)
    try:
        print(f"Suppression de l'utilisateur Alice (id={utilisateur_1.id}) qui a des emprunts")
        biblio.supprimer_utilisateur(utilisateur_1.id)
    except Exception as e:
        print("Attention— suppression interdite :", type(e).__name__, str(e))

    # Rendre puis supprimer
    biblio.rendre(utilisateur_1.id, livre_3.id)
    try:
        print(f"Suppression de l'utilisateur Alice (id={utilisateur_1.id}) après retour")
        ok = biblio.supprimer_utilisateur(utilisateur_1.id)
        print("Suppression effectué ->", ok)
    except Exception as e:
        print("Erreur inattendue :", e)

    sep("9. Recherches")
    biblio.ajouter_livre("Le Prince", "Niccolo Machiavelli")
    biblio.ajouter_livre("Princesse Maléfique", "Auteur X")
    print("Recherche par titre contenant 'prince' :")
    for livre in biblio.rechercher_par_titre("prince"):
        print(livre)

    print("Recherche par auteur 'martin' :")
    for livre in biblio.rechercher_par_auteur("martin"):
        print(livre)

    print("Recherche par mot-clé 'prin' :")
    for livre in biblio.rechercher_par_mot_clef("prin"):
        print(livre)

    sep("10. Modification de statut")
    # Forcer changement de statut
    all_books = biblio.lister_tous_les_livres()
    if all_books: #Si il existe au moins un livre
        premier_livre = all_books[0]
        print(f"Statut avant: {premier_livre}")
        biblio.modifier_status(premier_livre.id, StatusLivre.EMPRUNTE)
        print("Statut forcé à 'EMPRUNTE' ->", biblio._livres[premier_livre.id])
        # Remettre à dispo
        biblio.modifier_status(premier_livre.id, StatusLivre.DISPONIBLE)
        print("Statut remis à 'DISPONIBLE' ->", biblio._livres[premier_livre.id])

    sep("11. Statistiques")
    print("Nombre total de livres:", biblio.nombre_total_livres())
    print("Nombre total d'utilisateurs:", biblio.nombre_total_utilisateurs())
    print("Distribution emprunts par utilisateur:", biblio.distribution_emprunts_par_utilisateur())
    print("Histogramme des emprunts (dict):", biblio.histogramme_emprunts())

    print("Affichage de l'histogramme via matplotlib")
    try:
        biblio.afficher_histogramme_emprunts()
    except Exception as e:
        print("Impossible d'afficher l'histogramme (environnement headless?) :", e)

    sep("Fin de la démo")


if __name__ == "__main__":
    run_demo()

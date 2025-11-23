"""
Ce script illustre toutes les fonctions de la bibliothèque dans des cas possibles et impossibles
via une simulation "aléatoire" (avec un seed) d'emprunts.

Scénario couvert:
- crée 50 livres et 10 utilisateurs
- distribue des emprunts aléatoires (répétables via seed)
- applique toutes les fonctions de base (ajout, suppression, modification de statut, emprunt, retour)
- vérifie et illustre les conditions empêchant certaines suppressions (livre emprunté / utilisateur avec emprunts)
- affiche les erreurs attendues et les succès
"""

from bibliotheque_project.core.bibliotheque import Bibliotheque
from bibliotheque_project.models.livre import StatusLivre
import random


def sep(title: str) -> None:
    """
    Creé des séparateur afin de garantir un meilleur affichage lors de la démonstration ci dessous

    Args:
        title (str):Chaine de caractère qu'on souhaite mettre en valeur

    Returns:
        None
    """
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80 + "\n")


def generate_books(biblio: Bibliotheque):
    """
    Génère 50 livres et les ajoute à la bibliothèque.

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
    Génère 10 utilisateurs et les ajoute à la bibliothèque.

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


def random_emprunts(biblio: Bibliotheque, utilisateurs, livres, max_per_user=6, seed: int = 42):
    """
    Distribue des emprunts aléatoires mais reproductibles via seed.

    Args:
        biblio (Bibliotheque): Instance de la bibliothèque.
        utilisateurs (List[Utilisateur]): Liste des utilisateurs.
        livres (List[Livre]): Liste des livres.
        max_per_user (int): Nombre maximum de livres par utilisateur.
        seed (int): Seed pour reproductibilité.

    Returns:
        None
    """
    rnd = random.Random(seed)
    for utilisateur in utilisateurs:
        nb = rnd.randint(0, max_per_user)
        candidate_ids = [livre.id for livre in livres]
        rnd.shuffle(candidate_ids)
        for lid in candidate_ids:
            if nb <= 0:
                break
            livre = biblio._livres.get(lid)
            if livre and livre.status == StatusLivre.DISPONIBLE:
                try:
                    biblio.emprunter(utilisateur.id, lid)
                    nb -= 1
                except Exception:
                    pass


def run_demo():
    """
    Démonstration complète avec 50 livres, 10 utilisateurs et emprunts aléatoires.
    Illustre toutes les vérifications (ajout, suppression, modification de statut, emprunt, retour).

    Args:
        Aucun

    Returns:
        None
    """
    sep("1. Initialisation : création des livres et utilisateurs")
    biblio = Bibliotheque()
    livres = generate_books(biblio)
    utilisateurs = generate_users(biblio)

    print("Livres :")
    for livre in livres:
        print(livre)

    print("Utilisateurs :")
    for utilisateur in utilisateurs:
        print(utilisateur)

    sep("2. Distribution ALÉATOIRE des emprunts")
    seed = 2025
    print(f"Seed utilisée : {seed}")
    random_emprunts(biblio, utilisateurs, livres, max_per_user=5, seed=seed)

    sep("3. Vérification post-emprunts")
    for utilisateur in biblio.lister_utilisateurs():
        print(f"{utilisateur.nom} (id={utilisateur.id}) -> emprunts: {utilisateur.livres_empruntes}")

    livre_emprunte = next((livre for livre in livres if livre.status == StatusLivre.EMPRUNTE), None)
    livre_disponible = next((livre for livre in livres if livre.status == StatusLivre.DISPONIBLE), None)

    sep("4. Tentative de suppression d'un livre emprunté (doit échouer)")
    if livre_emprunte:
        try:
            print(f"Tentative suppression livre emprunté id={livre_emprunte.id}")
            biblio.supprimer_livre(livre_emprunte.id)
        except Exception as e:
            print("Livre déja emprunté:", type(e).__name__, str(e))
    else:
        print("Aucun livre emprunté trouvé pour ce test")

    sep("5. Suppression d'un livre disponible (doit réussir)")
    if livre_disponible:
        try:
            print(f"Suppression livre disponible id={livre_disponible.id}")
            ok = biblio.supprimer_livre(livre_disponible.id)
            print("Suppression réussite:", ok)
        except Exception as e:
            print("Erreur inattendue lors de la suppression d'un livre disponible:", e)
    else:
        print("Aucun livre disponible trouvé pour ce test")

    sep("6. Tentative de suppression d'un utilisateur qui a des emprunts (doit échouer)")
    utilisateur_avec_emprunt = next((utilisateur for utilisateur in utilisateurs if utilisateur.livres_empruntes), None)
    if utilisateur_avec_emprunt:
        try:
            print(f"Tentative suppression utilisateur id={utilisateur_avec_emprunt.id}")
            biblio.supprimer_utilisateur(utilisateur_avec_emprunt.id)
        except Exception as e:
            print("Attention — suppression interdite :", type(e).__name__, str(e))
    else:
        print("Aucun utilisateur avec emprunts trouvé")

    sep("7. Rendre tous les emprunts d'un utilisateur puis le supprimer (doit réussir)")
    if utilisateur_avec_emprunt:
        emprunts = list(utilisateur_avec_emprunt.livres_empruntes)
        for lid in emprunts:
            try:
                print(f"Rendu du livre id={lid} par utilisateur id={utilisateur_avec_emprunt.id}")
                biblio.rendre(utilisateur_avec_emprunt.id, lid)
            except Exception as e:
                print("Erreur inattendue lors du rendu :", e)
        try:
            ok = biblio.supprimer_utilisateur(utilisateur_avec_emprunt.id)
            print("Suppression utilisateur après rendu ->", ok)
        except Exception as e:
            print("Erreur inattendue lors de la suppression utilisateur :", e)

    sep("8. Tentative d'emprunt invalide (utilisateur ou livre inexistant)")
    try:
        biblio.emprunter(999999, livres[0].id)
    except Exception as e:
        print("Utilisateur inexistant :", type(e).__name__, str(e))
    try:
        biblio.emprunter(utilisateurs[0].id, 9999999)
    except Exception as e:
        print("Livre inexistant :", type(e).__name__, str(e))

    sep("9. Modification forcée de statut et vérification")
    remaining = next(iter(biblio.lister_tous_les_livres()), None)
    if remaining:
        print("Avant:", remaining)
        biblio.modifier_status(remaining.id, StatusLivre.EMPRUNTE)
        print("Après forçage à emprunté:", biblio._livres[remaining.id])
        biblio.modifier_status(remaining.id, StatusLivre.DISPONIBLE)
        print("Après remise à disponible:", biblio._livres[remaining.id])

    sep("10. Recherches exemples")
    print("Recherche titre 'Exemple 1' :")
    for livre in biblio.rechercher_par_titre('Exemple 1'):
        print(livre)

    print("Recherche auteur 'Auteur A' :")
    for livre in biblio.rechercher_par_auteur('Auteur A'):
        print(livre)

    sep("11. Statistiques")
    print("Nombre total de livres:", biblio.nombre_total_livres())
    print("Nombre total d'utilisateurs:", biblio.nombre_total_utilisateurs())
    print("Distribution emprunts par utilisateur:", biblio.distribution_emprunts_par_utilisateur())
    print("Histogramme des emprunts:", biblio.histogramme_emprunts())

    print("Affichage histogramme via matplotlib")
    try:
        biblio.afficher_histogramme_emprunts()
    except Exception as e:
        print("Impossible d'afficher (headless) :", e)

    sep("Fin de la démo ALÉATOIRE avec vérifications")


if __name__ == '__main__':
    run_demo()

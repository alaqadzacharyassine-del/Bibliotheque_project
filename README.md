 📚 Gestion d'une Librairie
---
## 🎯 Objectif
- Ce projet consiste à concevoir un programme Python simulant la gestion d'une bibliothèque de manière bien typé. C'est a dire qu'on veut toutes les docstrings ainsi que tester ce qu'on code via pytest.  
Le programme modélise les **livres**, les **utilisateurs**, et leurs interactions : emprunts, retours.
---
## 🧩 Description générale
Ce programme s'articule autour de deux entités principales :  

- 📘 **Les livres**  
- 👤 **Les utilisateurs**  

Et leurs interactions : **emprunter et rendre des livres**.

---

## 📂 Arborescence du projet
Voici l'arborescence de notre projet Python :
```
│ 
│ ── core/                   # Logique métier principale
│   ├── __init__.py
│   └── bibliotheque.py     # Classe Bibliotheque
│
├── demo/                   # Script de démonstration
│   ├──__init__.py
│   ├── demo1_petite_base_donnee.py
│   ├── demo2_base_donnee_plus_grande.py
│   └── demo3_emprunt_aleatoire.py

├── models/                 # Modèles de données
│   ├── __init__.py
│   ├── livre.py            # Classe Livre
│   └── utilisateur.py      # Classe Utilisateur
│
│
├── tests/                  # Tests unitaires pytest
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_bibliotheque.py
│   ├── test_livre.py
│   └── test_utilisateur.py
│
└── README.md
```

---

## 1. 📘 Gestion des Livres

### Attributs d'un livre
- **id** : Identifiant unique du livre  
- **titre** : Titre du livre  
- **auteur** : Auteur du livre  
- **status** : État du livre (`disponible` / `emprunté`)  

### Fonctionnalités
- ➕ Ajouter un livre  
- 🗑️ Supprimer un livre (uniquement s'il n'est pas emprunté)  
- 🔁 Modifier le statut d'un livre (`disponible ↔ emprunté`)  
- 📜 Lister tous les livres disponibles  
- 🔍 Rechercher un livre par :  
  - titre  
  - auteur  
  - mot-clé  

---

## 2. 👤 Gestion des Utilisateurs

### Attributs d'un utilisateur
- **id** : Identifiant unique de l'utilisateur  
- **nom** : Nom de l'utilisateur  
- **livres_empruntés** : Liste des identifiants de livres empruntés  

### Fonctionnalités
- 🆕 Créer un utilisateur  
- 🗑️ Supprimer un utilisateur (uniquement s'il n'a aucun livre emprunté)  
- 📜 Lister tous les utilisateurs enregistrés  

---

## 3. 🔄 Gestion des Emprunts et Retours

### Fonctionnalités
- 📥 **Emprunter un livre** (si disponible) :  
  - Mettre à jour le statut du livre  
  - Ajouter l'identifiant du livre à la liste de l'utilisateur  

- 📤 **Rendre un livre** :  
  - Remettre le statut du livre à `disponible`  
  - Supprimer l'identifiant du livre de la liste de l'utilisateur  

---

## 4. 📊 Statistiques

Le programme peut afficher des statistiques globales :  

- 📚 Nombre total de livres  
- 👥 Nombre total d'utilisateurs  
- 📈 Distribution du nombre de livres empruntés par utilisateur  

---

## 🧪 Remarques générales
- Vous pouvez générer des données "fake" pour vos tests à l'aide de GPT ou d'un script Python.  
- Le code est fait pour rester **maintenable, efficace et intuitif**.


---

## ⚙️ Pré-requis
- Python 3.8 ou supérieur  
- Bibliothèques Python standard (pas de dépendances externes nécessaires)  
- Pytest
---

## 📚 Guide d'utilisation
- Suivre les instructions affichées dans le terminal pour ajouter des livres, créer des utilisateurs, emprunter ou rendre des livres.
- Les fonctions principales sont documentées dans le code avec des docstrings pour faciliter leur compréhension.
---
## ⭐ Remerciements
- Nous souhaitons remercier notre enseignant en python qui nous à proposé ce projet : Baptiste Gauthier

---
## 👥 Contributeurs
- Développeur principal : Alaqad Zachary, Sabi Yanis et Michon Louis
- Contact : alaqadzacharyassine@gmail.com
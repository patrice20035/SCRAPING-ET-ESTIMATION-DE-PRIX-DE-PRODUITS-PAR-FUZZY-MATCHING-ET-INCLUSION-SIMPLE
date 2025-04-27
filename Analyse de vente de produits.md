# ANALYSE DE VENTES DE PRODUITS CARREFOUR

### Scraping et estimation par fuzzing matching pour les 5 premières pages
Auteurs : **KAMEDA PATRICE THOMAS -KABORE JULIEN -MAMADOU GIULIANO** 
Date : 28/04/2025

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://github.com/patrice20035/Analyse-de-vente-de-produits/blob/main/ESTIMATION%20PAR%20FUZZY%20MATCHING)


## Sommaire
    1. Introduction
    2. Installation des bibliothèques
    3. Importation des modules
    4. Définition des catégories Carrefour
    5. Création du dossier de sortie
    6. Choix du mode utilisateur
    7. Fonction de scraping
    8. Modes de fonctionnement
        8.1 Scraping des promotions ou produits
        8.2 Estimation de prix par fuzzing
    9. Résultat final
    10. Améliorations possibles

# 1. Introduction

Ce projet a pour but de :
- Scraper des produits ou promotions sur le site Carrefour.
- Estimer le prix d'un produit par correspondance floue (fuzzy matching).
- Générer des fichiers CSV pour analyses ultérieures.

# 2. Installation des bibliothèques

Bibliothèques utilisées :
    selenium pour piloter le navigateur
    pandas pour manipuler les données
    matplotlib pour générer d’éventuels graphiques
    openpyxl pour la gestion d’Excel
    rapidfuzz pour la recherche de similarité de textes

```bash
!pip install selenium pandas matplotlib openpyxl rapidfuzz
```

# 3. Importation des modules

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import os
import time
import re
from rapidfuzz import fuzz
```

# 4. Définition des catégories Carrefour

Une liste fixe de 29 catégories est créée pour permettre à l'utilisateur de sélectionner facilement ce qu’il souhaite scraper.

```python
CATEGORIES = [
    'bio-et-ecologie', 'fruits-et-legumes', 'viandes-et-poissons', 'pains-et-patisseries',
    'cremerie-et-produits-laitiers', 'charcuterie-et-traiteur', 'surgeles', 'epicerie-salee',
    'epicerie-sucree', 'beaute-et-sante', 'boissons', 'nutrition-et-vegetale', 'hygiene-et-beaute',
    'entretien-et-nettoyage', 'animalerie', 'bebe', 'jardin', 'entretien-de-la-maison',
    'maison-et-decoration', 'cuisine', 'gros-electromenager', 'bricolage',
    'velo-trotinettes-et-loisirs', 'smartphones-et-objets-connectes', 'image-et-son',
    'informatique-et-bureau', 'jeux-videos', 'jeux-et-jouets', 'mode-et-bagagerie'
]
```

# 5. Création du dossier de sortie

```python
OUTPUT_FOLDER = r"icloud drive/Output"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
```

# 6. Choix du mode utilisateur

À l'exécution, l'utilisateur choisit un des modes suivants :
    products : Scraping de produits normaux
    promotions : Scraping de promotions
    estimate : Estimation de prix par correspondance floue
Saisie contrôlée avec validation.

```python
mode = input("Souhaitez-vous scraper des promotions, des produits, ou estimer un prix ? [promotions/products/estimate] : ").strip().lower()
while mode not in ["promotions", "products", "estimate"]:
    mode = input("Veuillez entrer 'promotions', 'products', ou 'estimate' : ").strip().lower()

if mode in ["products", "estimate"]:
    print("\nCatégories disponibles :")
    for idx, cat in enumerate(CATEGORIES, 1):
        print(f" {idx}. {cat}")
    while True:
        try:
            cat_choice = int(input("Choisissez le numéro de la catégorie : ").strip())
            if 1 <= cat_choice <= len(CATEGORIES):
                categorie = CATEGORIES[cat_choice - 1]
                break
            else:
                print("Numéro invalide. Réessayez.")
        except ValueError:
            print("Veuillez entrer un numéro valide.")
else:
    categorie = None
```

# 7. Fonction de scraping

Utilisation de Selenium pour ouvrir 5 pages successives
    Récupération :
        du nom du produit
        du prix proprement nettoyé
    Sauvegarde temporaire dans un DataFrame

```python
def scrap_pages(url_base):
    driver = webdriver.Chrome()
    all_data = []
    for page in range(5):
        driver.get(f"{url_base}&page={page}")
        time.sleep(5)
        products = driver.find_elements(By.CLASS_NAME, "product-list-grid__item")
        print(f"Scraping page {page + 1} : {len(products)} produits")

        for p in products:
            try:
                name = p.find_element(By.CSS_SELECTOR, "a.product-card-title").text
            except:
                name = None

            try:
                price_block = p.find_element(By.CSS_SELECTOR, "div.product-price__amount--main")
                price_text = price_block.text
                clean_price = re.sub(r'[^\d,\.]', '', price_text)
                price = float(clean_price.replace(',', '.'))
            except:
                price = None

            all_data.append({
                "product_name": name,
                "price": price,
                "page": page + 1
            })

    driver.quit()
    return pd.DataFrame(all_data)
```

# 8. Modes de fonctionnement
## 8.1 Scraping des promotions ou produits
Si l’utilisateur choisit promotions ou products :
    Construction de l'URL
    Scraping des produits
    Sauvegarde en CSV (carrefour_promotions_5pages.csv ou carrefour_products_<catégorie>_5pages.csv)

```python
if mode in ["promotions", "products"]:
    if mode == "promotions":
        base_url = "https://www.carrefour.fr/promotions?noRedirect=1"
        df = scrap_pages(base_url)
        filename = "carrefour_promotions_5pages.csv"
    else:
        base_url = f"https://www.carrefour.fr/r/{categorie}?noRedirect=1"
        df = scrap_pages(base_url)
        filename = f"carrefour_products_{categorie}_5pages.csv"

    csv_path = os.path.join(OUTPUT_FOLDER, filename)
    df.to_csv(csv_path, index=False)
    print(f"\u2705 Fichier CSV enregistré : {csv_path}")
    print(df.head())
```

## Resultat du scraping promotions carrefour
Voici un aperçu du scraping realise sur la categorie bebe

![Résultat du scraping](//icloud-drive/output_![Capture d’écran 2025-04-27 à 03.46.51.png](40d256ee-4ad7-4861-aa43-48eb0f92f38d.png).png)

## Résultat du scraping des produits Carrefour

Voici un aperçu du scraping realise sur la catégorie cuisine (5 pages) :

![Résultat du scraping](/icloud-drive/output_![Capture d’écran 2025-04-27 à 03.49.42.png](7b8e2431-da5e-46d5-9518-bc75bb69adb1.png)

## 8.2 Estimation de prix par fuzzing
Si l’utilisateur choisit estimate :
    Scraping des produits dans la catégorie choisie
    Saisie du nom du produit cible
    Utilisation de rapidfuzz pour calculer la similarité
    Sélection des produits similaires (score > 60%)
    Calcul :
        Prix moyen
        Prix minimum
        Prix maximum
    Affichage des résultats

    ```python
elif mode == "estimate":
    produit_cible = input("Saisissez le nom du produit à estimer : ").strip().lower()
    base_url = f"https://www.carrefour.fr/r/{categorie}?noRedirect=1"
    df = scrap_pages(base_url)

    if df.empty:
        print("\u26a0\ufe0f Aucun produit trouvé dans cette catégorie.")
    else:
        df['similarity'] = df['product_name'].apply(lambda x: fuzz.partial_ratio(produit_cible, x.lower()) if pd.notnull(x) else 0)
        similaires = df[df['similarity'] >= 60]

        if similaires.empty:
            print("\u26a0\ufe0f Aucun produit similaire trouvé.")
        else:
            prix_moyen = similaires['price'].mean()
            prix_min = similaires['price'].min()
            prix_max = similaires['price'].max()
            print("\nProduits similaires trouvés :")
            print(similaires[['product_name', 'price']])
            print(f"\nNombre de produits similaires : {len(similaires)}")
            print(f"Prix estimé moyen : {prix_moyen:.2f} €")
            print(f"Prix minimum : {prix_min:.2f} €, Prix maximum : {prix_max:.2f} €")
```

## Résultat du scraping des produits Carrefour
Voici un aperçu realisé sur l-estimation des prix sur la categorie 20 (produit estimé cuisine)
![Résultat du scraping](/icloud-drive/output_![Capture d’écran 2025-04-27 à 03.32.58.png](0f8168f5-19cd-47f6-a6fb-2ecce7f53d20.png)

# 9. Résultat final

À la fin du script, nous avons réussi à automatiser le scraping de produits et promotions du site Carrefour et à sauvegarder les données sous format CSV.
L'outil permet également d'estimer un prix moyen pour un produit spécifique grâce à une approche de fuzzy matching.
Les résultats sont affichés directement dans le notebook, rendant l'analyse rapide, claire et exploitable pour des traitements ultérieurs.

# 10. Améliorations possibles

Ajout automatique du format Excel (.xlsx) avec plusieurs feuilles (ex: produits + promotions)

     .Visualisation graphique des prix (histogrammes, boxplots)
     .Scraping infini (au lieu de 5 pages fixes)
     .Optimisation du scraping (headless mode pour Selenium)
     .Comparaison automatique entre prix promotionnels et prix standards
     .Scraping multi-catégories en une seule exécution
     .Nettoyage automatique des textes (stopwords, homogénéisation)




```python

```

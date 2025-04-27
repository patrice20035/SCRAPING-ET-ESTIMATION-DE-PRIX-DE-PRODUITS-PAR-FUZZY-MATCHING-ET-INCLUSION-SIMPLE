# Scraping et Analyse-de-vente-de-produits

# Web Scraping Tool for Carrefour Products and Promotions

This project is a Python-based web scraping tool designed to extract product and promotion data from the Carrefour website. It allows users to scrape promotions, scrape products from specific categories, or estimate the price of a product based on similar items.

## Features

- **Scrape Promotions**: Extract promotional product data, including current price, old price, discount percentage, and more.
- **Scrape Products**: Extract product data from a specific category, including product name, price, and unit price.
- **Estimate Product Prices**: Estimate the price of a product by finding similar items in a category using fuzzy matching.
- **Export Data**: Save the scraped data as CSV and Excel files,.

## Requirements

Before running the script, ensure you have the following installed:

- Python 3.7 or higher
- Required Python libraries:
  ```bash
  pip install selenium pandas matplotlib openpyxl rapidfuzz

Voici une **explication claire et détaillée** pour notre projet Carrefour Scraper :

---

```markdown
# 🛒 Carrefour Web Scraper

## 📋 Objectif

Ce projet a pour but de **scraper les produits et promotions** du site **Carrefour.fr** afin de :
- **Récupérer les produits** d'une catégorie spécifique.
- **Collecter les promotions** (avec anciens et nouveaux prix).
- **Estimer le prix d'un produit** en fonction de son nom via des produits similaires.
- **Analyser les données** (prix moyens, top 5  des réductions) et **exporter** les résultats en **CSV** et **Excel**.

---

## ⚙️ Fonctionnalités principales

### 1. Modes disponibles
- **Products** : Scrape les **produits d'une catégorie** au choix.
- **Promotions** : Scrape toutes les **promotions en cours** avec détails (prix avant/après réduction, % réduction, description promo).
- **Estimate** : Estime en **temps réel** le prix moyen d’un **produit saisi par l'utilisateur**, en fonction des produits similaires scrapés.

### 2. Scraping multi-pages
- Le scraper **parcourt automatiquement toutes les pages** d'une catégorie ou des promotions jusqu'à **épuisement des produits**.

### 3. Analyses et exportation
- Les données sont **exportées en CSV** (brut) et en **Excel** (avec analyses supplémentaires).
- Analyses incluses dans le fichier Excel (pour promotions) :
  - **Moyenne de la différence de prix** par catégorie.


### 4. Estimation en temps réel
- **Saisie d’un nom de produit**.
- Scraping en **temps réel** de la catégorie sélectionnée.
- Recherche de produits **similaires** par **inclusion directe de texte**.
- Affichage :
  - **Liste des produits similaires**.
  - **Prix moyen, minimum, maximum**.


---

## 🖥️ Technologies utilisées

- **Python**
- **Selenium** : pour le scraping web.
- **Pandas** : pour la gestion et l’analyse des données.
- **Matplotlib** : pour générer des graphiques (distribution des prix).
- **Rapidfuzz** (optionnel) : pour du fuzzy matching (remplacé ici par une recherche directe).

---

## 🚀 Comment utiliser

1. **Installer les dépendances** :
   ```bash
   pip install selenium pandas matplotlib
   ```

2. **Télécharger le WebDriver** :
   - Télécharger **ChromeDriver** compatible avec ta version de Chrome : [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads).
   - Ajouter **chromedriver.exe** au même dossier que le script ou dans ton PATH système.

3. **Lancer le script** :
   ```bash
   python carrefour_scraper.py
   ```

4. **Choisir un mode** :
   - `promotions` : scrape toutes les promotions.
   - `products` : scrape les produits d'une catégorie (choix par numéro).
   - `estimate` : estimer le prix d'un produit saisi.

---

## 📂 Fichiers générés

- **CSV** : contient les données brutes.
- **Excel** : contient :
  - Feuille **Données**.
  - Feuille **Moyenne différences** (promotions).
  - Feuille **Nombre promotions** (promotions).


---

## 🛠️ Possibilités d’amélioration

- Ajouter la gestion **des erreurs réseau** ou des **timeouts**.
- Supporter **d’autres sites marchands**.
- Ajouter un **mode graphique (interface utilisateur)**.
- Automatiser l’**envoi par email** des résultats.

---

## 👨‍💻 Auteurs

Projet développé par 

-**KAMEDA PATRICE THOMAS**

-**KABORE JULIEN**

-**JULIANO**

dans le cadre du cours de **Programmation Python**.

```



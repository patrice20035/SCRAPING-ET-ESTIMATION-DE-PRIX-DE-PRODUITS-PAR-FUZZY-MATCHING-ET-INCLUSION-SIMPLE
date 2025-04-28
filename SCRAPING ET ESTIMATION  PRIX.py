from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import os
import time
import re
import matplotlib.pyplot as plt

# Liste des catégories disponibles
CATEGORIES = [
    'bio-et-ecologie', 'fruits-et-legumes', 'viandes-et-poissons', 'pains-et-patisseries',
    'cremerie-et-produits-laitiers', 'charcuterie-et-traiteur', 'surgeles', 'epicerie-salee',
    'epicerie-sucree', 'beaute-et-sante', 'boissons', 'nutrition-et-vegetale', 'hygiene-et-beaute',
    'entretien-et-nettoyage', 'animalerie', 'bebe', 'jardin', 'entretien-de-la-maison',
    'maison-et-decoration', 'cuisine', 'gros-electromenager', 'bricolage',
    'velo-trotinettes-et-loisirs', 'smartphones-et-objets-connectes', 'image-et-son',
    'informatique-et-bureau', 'jeux-videos', 'jeux-et-jouets', 'mode-et-bagagerie'
]

# Dossier de sortie
OUTPUT_FOLDER = r"C:/Users/DELL/OneDrive - etu.unistra.fr/Bureau/cours fac/PROGRAMMATION PYTHON/PROJET/Output"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Demander à l'utilisateur ce qu'il veut scraper
mode = input("Souhaitez-vous scraper des promotions, des produits, ou estimer un prix ? [promotions/products/estimate] : ").strip().lower()
while mode not in ["promotions", "products", "estimate"]:
    mode = input("Veuillez entrer 'promotions', 'products', ou 'estimate' : ").strip().lower()

# S'il s'agit de produits, demander la catégorie
if mode == "products":
    print("Voici les catégories disponibles :")
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

# Scraping des pages de promotions
def scrap_single_page_promotions():
    driver = webdriver.Chrome()
    page = 0
    all_data = []
    while True:
        driver.get(f"https://www.carrefour.fr/promotions?noRedirect=1&page={page}")
        time.sleep(5)
        products = driver.find_elements(By.CLASS_NAME, "product-list-grid__item")
        if not products:  # Break the loop if no products are found
            break

        data = []
        for p in products:
            try:
                name = p.find_element(By.CSS_SELECTOR, "a.product-card-title").text
            except:
                name = None

            price = None
            old_price = None
            try:
                price_block = p.find_element(By.CSS_SELECTOR, "div.product-price__amount--main")
                price_text = price_block.text
                clean_price = re.sub(r'[^\d,\.]', '', price_text)
                price = float(clean_price.replace(',', '.'))
            except:
                pass

            try:
                old_price_block = p.find_element(By.CSS_SELECTOR, "div.product-price__amount--old")
                old_price_text = old_price_block.text
                clean_old_price = re.sub(r'[^\d,\.]', '', old_price_text)
                old_price = float(clean_old_price.replace(',', '.'))
            except:
                pass

            try:
                unit = p.find_element(By.CSS_SELECTOR, "span.product-list-card-plp-grid__per-unit-label").text
            except:
                unit = None

            try:
                promo_description = p.find_element(By.CSS_SELECTOR, "span.promotion-label-refonte__label").text
            except:
                promo_description = None

            try:
                category = p.find_element(By.CSS_SELECTOR, "span.product-card-category").text
            except:
                category = None

            if (price and old_price and price != old_price) or promo_description:
                data.append({
                    "product_name": name,
                    "price": price,
                    "old_price": old_price,
                    "difference": round(old_price - price, 2) if price and old_price else None,
                    "percentage_difference": round(((old_price - price) / old_price) * 100, 2) if price and old_price else None,
                    "price_per_unit": unit,
                    "promo_description": promo_description,
                    "category": category,
                    "purchasable": True,
                    "page": page
                })

        all_data.extend(data)
        page += 1
    driver.quit()
    return pd.DataFrame(all_data)

# Scraping des pages de produits
def scrap_single_page_products(categorie):
    driver = webdriver.Chrome()
    page = 0
    all_data = []
    while True:
        driver.get(f"https://www.carrefour.fr/r/{categorie}?noRedirect=1&page={page}")
        time.sleep(5)
        products = driver.find_elements(By.CLASS_NAME, "product-list-grid__item")
        if not products:  # Break the loop if no products are found
            break

        data = []
        for p in products:
            try:
                name = p.find_element(By.CSS_SELECTOR, "a.product-card-title").text
            except:
                name = None

            try:
                price_block = p.find_element(By.CSS_SELECTOR, "div.product-price__amount--main")
                parts = price_block.find_elements(By.CSS_SELECTOR, "p.product-price__content")
                price_text = ''.join([part.text for part in parts])
                price = float(price_text.replace(',', '.').replace('€', '').strip())
            except:
                price = None

            try:
                unit = p.find_element(By.CSS_SELECTOR, "span.product-list-card-plp-grid__per-unit-label").text
            except:
                unit = None

            data.append({
                "product_name": name,
                "price": price,
                "price_per_unit": unit,
                "category": categorie.replace('-', ' ').title(),
                "purchasable": True,
                "page": page
            })

        all_data.extend(data)
        page += 1
    driver.quit()
    return pd.DataFrame(all_data)

# Fonction pour estimer le prix d'un produit en temps réel
def estimate_price():
    print("Voici les catégories disponibles :")
    for idx, cat in enumerate(CATEGORIES, 1):
        print(f" {idx}. {cat}")
    while True:
        try:
            cat_choice = int(input("Choisissez le numéro de la catégorie pour l'estimation : ").strip())
            if 1 <= cat_choice <= len(CATEGORIES):
                categorie = CATEGORIES[cat_choice - 1]
                break
            else:
                print("Numéro invalide. Réessayez.")
        except ValueError:
            print("Veuillez entrer un numéro valide.")

    produit_cible = input("Saisissez le nom du produit à estimer : ").strip().lower()
    df = scrap_single_page_products(categorie)
    if df.empty:
        print("⚠️ Aucun produit trouvé dans cette catégorie.")
        return

    df['similarity'] = df['product_name'].apply(lambda x: produit_cible in x.lower() if pd.notnull(x) else False)
    similaires = df[df['similarity']]

    if similaires.empty:
        print("⚠️ Aucun produit similaire trouvé.")
    else:
        prix_moyen = similaires['price'].mean()
        prix_min = similaires['price'].min()
        prix_max = similaires['price'].max()
        print("Produits similaires trouvés :")
        print(similaires[['product_name', 'price']])
        print(f"Nombre de produits similaires : {len(similaires)}")
        print(f"Prix estimé moyen : {prix_moyen:.2f} €")
        print(f"Prix minimum : {prix_min:.2f} €, Prix maximum : {prix_max:.2f} €")


# Exécution et sauvegarde CSV
if mode == "estimate":
    estimate_price()
elif mode == "promotions":
    df = scrap_single_page_promotions()
    filename = "carrefour_promotions_page0.csv"
else:
    df = scrap_single_page_products(categorie)
    filename = f"carrefour_products_{categorie}_page0.csv"

if mode in ["promotions", "products"]:
    csv_path = os.path.join(OUTPUT_FOLDER, filename)
    if not df.empty:
        df.to_csv(csv_path, index=False)
        print(f"✅ Fichier CSV enregistré : {csv_path}")

        # Exporter vers Excel avec analyses
        excel_path = csv_path.replace('.csv', '.xlsx')
        with pd.ExcelWriter(excel_path) as writer:
            df.to_excel(writer, sheet_name='Données', index=False)
            if mode == "promotions":
                # Ajouter analyse moyenne différence par catégorie
                if 'category' in df.columns and 'difference' in df.columns:
                    mean_diff = df[df['old_price'].notna()].groupby('category')['difference'].mean().reset_index()
                    mean_diff.to_excel(writer, sheet_name='Moyenne différences', index=False)
                # Ajouter nombre de promotions par catégorie
                if 'category' in df.columns:
                    count_promos = df.groupby('category').size().reset_index(name='count_promotions')
                    count_promos.to_excel(writer, sheet_name='Nombre promotions', index=False)
        print(f"📊 Fichier Excel avec analyses enregistré : {excel_path}")
        print(df.head())
    else:
        print("⚠️ Aucun produit correspondant aux critères n'a été trouvé.")

    # Analyse pour promotions uniquement
    if mode == "promotions":
        pass
else:
    print("⚠️ Aucun produit correspondant aux critères n'a été trouvé.")

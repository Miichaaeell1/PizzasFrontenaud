import streamlit as st

def calculer_quantites(pizza, nombre):
    """Calcule les quantités nécessaires pour un certain nombre de pizzas."""
    return [
        (i + 1, nom, f"{round(quantite_par_pizza * nombre, 2)} {unite}")
        for i, (nom, quantite_par_pizza, unite) in enumerate(pizza)
    ]

def calculer_totaux(nombres_pizzas, pizzas):
    """Calcule les totaux des ingrédients pour plusieurs types de pizzas."""
    totaux, unites = {}, {}

    for pizza, nombre in zip(pizzas, nombres_pizzas):
        for _, ingredient, quantite_unite in calculer_quantites(pizza, nombre):
            quantite, unite = quantite_unite.split()
            totaux[ingredient] = totaux.get(ingredient, 0) + float(quantite)
            unites[ingredient] = unite

    ajustements_specifiques(totaux, unites)
    return organiser_resultats(totaux, unites)

def ajustements_specifiques(totaux, unites):
    """Applique des ajustements spécifiques à certains ingrédients."""
    if "Olives noires dénoyautées" in totaux:
        totaux["Olives noires dénoyautées"] *= 0.003
        unites["Olives noires dénoyautées"] = "Kg (poids net égoutté)"

    if "Boîte à pizza" in totaux:
        totaux["Boîte à pizza"] = int(totaux["Boîte à pizza"])

def organiser_resultats(totaux, unites):
    """Organise les résultats pour l'affichage."""
    boite_a_pizza = totaux.pop("Boîte à pizza", None)
    result = [(
        f"{ing} : {round(qte, 2)} {unites[ing]}" if ing != "Boîte à pizza" else
        f"{ing} : {int(qte)} Unités"
    ) for ing, qte in totaux.items()]
    if boite_a_pizza is not None:
        result.append(f"Boîte à pizza : {boite_a_pizza} Unités")
    return result

# Définition des recettes de pizzas
pizzas = {
    "Pizz'Adagio": [
        ["Purée de tomate", 0.1, "Kg"],
        ["Mozzarella en cossettes", 0.1, "Kg"],
        ["Chiffonade de jambon", 0.05, "Kg"],
        ["Emmental râpé", 0.1, "Kg"],
        ["Olives noires dénoyautées", 5, "Unités"],
        ["Boîte à pizza", 1, "Unités"]
    ],
    "Trio de fromages": [
        ["Purée de tomate", 0.1, "Kg"],
        ["Mozzarella en cossettes", 0.1, "Kg"],
        ["Fromage bleu", 0.08, "Kg"],
        ["Emmental râpé", 0.1, "Kg"],
        ["Olives noires dénoyautées", 5, "Unités"],
        ["Boîte à pizza", 1, "Unités"]
    ],
    "Ballade Bressane": [
        ["Poulet rôti émincé", 0.09, "Kg"],
        ["Crème fraîche", 0.1, "Kg"],
        ["Mozzarella en cossettes", 0.1, "Kg"],
        ["Lardons", 0.05, "Kg"],
        ["Oignons émincés", 0.03, "Kg"],
        ["Emmental râpé", 0.1, "Kg"],
        ["Olives noires dénoyautées", 5, "Unités"],
        ["Boîte à pizza", 1, "Unités"]
    ]
}

# Configuration de la page Streamlit
st.set_page_config(page_title="Calcul des ingrédients à commander pour les pizzas 🍕", layout="wide")
st.title("Calcul des ingrédients à commander pour les pizzas 🍕")

# CSS pour masquer les deux premières colonnes et la première ligne des trois premiers tableaux
st.markdown(
    """
    <style>
    /* Masquer les deux premières colonnes */
    table tr th:nth-child(1),
    table tr th:nth-child(2),
    table tr td:nth-child(1),
    table tr td:nth-child(2) {
        display: none;
    }
    /* Masquer la première ligne */
    table tr:first-child {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Interface utilisateur
cols = st.columns(3)
nombres_pizzas = [cols[i].number_input(nom, min_value=0, step=1, value=1) for i, nom in enumerate(pizzas)]

if st.button("Calculer les Ingrédients"):
    for nom, nombre, pizza in zip(pizzas, nombres_pizzas, pizzas.values()):
        st.markdown(f'<h2 class="pizza-title">Ingrédients pour {nom} ({nombre} pizzas)</h2>', unsafe_allow_html=True)
        st.table([("#", "Ingrédient", "Qté totale")] + calculer_quantites(pizza, nombre))

    st.subheader("Récapitulatif des Totaux")
    st.table([("Ingrédients à acheter", "Qté à acheter")] + calculer_totaux(nombres_pizzas, list(pizzas.values())))

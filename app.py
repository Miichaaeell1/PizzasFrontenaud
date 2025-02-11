import streamlit as st

def calculer_quantites(pizza, nombre):
    """Calcule les quantités nécessaires pour un certain nombre de pizzas."""
    return [
        (i + 1, nom, f"{round(quantite_par_pizza * nombre, 2)} {unite}")
        for i, (nom, quantite_par_pizza, unite) in enumerate(pizza)
    ]

def calculer_totaux(nombres_pizzas, pizzas):
    """Calcule les totaux des ingrédients pour plusieurs types de pizzas."""
    totaux = {}
    unites = {}

    for pizza, nombre in zip(pizzas, nombres_pizzas):
        for _, ingredient, quantite_unite in calculer_quantites(pizza, nombre):
            quantite_str, unite = quantite_unite.split()
            quantite = float(quantite_str)
            if ingredient in totaux:
                totaux[ingredient] += quantite
            else:
                totaux[ingredient] = quantite
                unites[ingredient] = unite

    # Ajustements spécifiques pour certains ingrédients
    ajustements_specifiques(totaux, unites)

    # Mettre "Boîte à pizza" en dernière ligne
    result = organiser_resultats(totaux, unites)

    return result

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
    boite_a_pizza_unite = unites.pop("Boîte à pizza", "Unités")

    result = [
        (ingredient, f"{round(qte, 2)} {unites[ingredient]}")
        for ingredient, qte in totaux.items()
    ]

    if boite_a_pizza is not None:
        result.append(("Boîte à pizza", f"{boite_a_pizza} {boite_a_pizza_unite}"))

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
        ["Emmental râpé", 0.1, "Kg"],  # Ajout de la ligne Emmental râpé
        ["Olives noires dénoyautées", 5, "Unités"],
        ["Boîte à pizza", 1, "Unités"]
    ]
}

# Configuration de la page Streamlit
st.set_page_config(page_title="Calcul des Ingrédients pour Pizzas", layout="wide")

st.title("Calcul des Ingrédients pour Pizzas")

st.markdown(
    """
    <style>
    .main {
        padding: 2rem;
        background-color: #F6F6F6;
    }
    .stButton>button {
        background-color: #F6F6F6;
        color: black;
        font-weight: bold;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        border: 2px solid #FFFFFF;
    }
    .stButton>button:hover {
        background-color: #F6F6F6;
        color: black;
    }
    table {
        border-collapse: collapse;
        width: 100%;
        margin-bottom: 2rem;
        background-color: #F6F6F6;
        table-layout: auto;
        word-wrap: break-word;
    }
    th, td {
        border: 2px solid #FFFFFF;
        padding: 8px;
        text-align: left;
        white-space: normal;
    }
    th {
        background-color: #FACE38;
        color: white;
    }
    h1, h2 {
        color: #036093;
    }
    /* Hide first column and first row */
    table tr:first-child,
    table tr td:first-child,
    table tr th:first-child {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Interface utilisateur
col1, col2, col3 = st.columns(3)

with col1:
    nombre_pizzas_1 = st.number_input("Nombre de Pizz'Adagio", min_value=0, step=1, value=1)
with col2:
    nombre_pizzas_2 = st.number_input("Nombre de Trio de fromages", min_value=0, step=1, value=1)
with col3:
    nombre_pizzas_3 = st.number_input("Nombre de Ballade Bressane", min_value=0, step=1, value=1)

if st.button("Calculer les Ingrédients"):
    nombres_pizzas = [nombre_pizzas_1, nombre_pizzas_2, nombre_pizzas_3]

    for nom_pizza, nombre, pizza in zip(pizzas.keys(), nombres_pizzas, pizzas.values()):
        st.subheader(f"Ingrédients pour {nom_pizza} ({nombre} pizzas)")
        st.table(
            [("#", "Ingrédient", "Qté totale")] + calculer_quantites(pizza, nombre)
        )

    st.subheader("Récapitulatif des Totaux")
    st.table(
        [("Ingrédients à acheter", "Qté à acheter")] + calculer_totaux(nombres_pizzas, list(pizzas.values()))
    )

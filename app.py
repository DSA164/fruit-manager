import streamlit as st
from fruit_manager import *

st.title("🍇 Dashboard de la Plantation")

inventaire = ouvrir_inventaire()
prix = ouvrir_prix()
tresorerie = ouvrir_tresorerie()

with st.sidebar:
    st.header("🛒 Vendre des Fruits")
    fruit_vendre = st.selectbox("Choisir un fruit", list(inventaire.keys()))
    quantite_vendre = st.number_input("Quantité a vendre", min_value=1, step=1)

    if st.button("Vendre"):
        inventaire, tresorerie = vendre(inventaire, fruit_vendre, quantite_vendre, tresorerie, prix)

    st.header("🌱 Récolter des Fruits")
    fruit_recolter = st.selectbox("Choisir un fruit à récolter", list(inventaire.keys()), key="recolte_individuelle")
    quantite_recolter = st.number_input("Quantité à récolter", min_value=1, step=1, key="quantite_recolte")

    if st.button("Récolter"):
        inventaire = recolter(inventaire, fruit_recolter, quantite_recolter)


st.header("💰 Trésorerie")
st.metric(label="Montant disponible", value=f"{tresorerie:.2f} $")

st.header("📦 Inventaire")
st.table(inventaire)


ecrire_inventaire(inventaire)
ecrire_tresorerie(tresorerie)
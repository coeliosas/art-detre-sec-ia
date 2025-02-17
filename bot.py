import streamlit as st
import openai
import os
from dotenv import load_dotenv
from fpdf import FPDF
import time

# Charger la clé API OpenAI
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if api_key is None:
    raise ValueError("Clé API OpenAI non trouvée. Vérifie tes secrets Streamlit Cloud.")

client = openai.OpenAI(api_key=api_key)

# Initialiser OpenAI
client = openai.OpenAI(api_key=api_key)

def sanitize_text(text):
    replacements = {
        "’": "'", "“": '"', "”": '"', "é": "e", "è": "e", "à": "a", "ç": "c", "ê": "e", "ô": "o"
    }
    for key, val in replacements.items():
        text = text.replace(key, val)
    return text

def calculer_metabolisme_basal(poids, taille, age, sexe):
    if sexe == "Homme":
        return 10 * poids + 6.25 * taille - 5 * age + 5
    else:
        return 10 * poids + 6.25 * taille - 5 * age - 161

def calculer_macronutriments(masse_maigre, metabolisme_basal):
    proteines = masse_maigre * 1.8
    lipides = masse_maigre * 0.8
    glucides = (metabolisme_basal - (proteines * 4 + lipides * 9)) / 4
    fibres = (metabolisme_basal / 1000) * 15
    return proteines, lipides, glucides, fibres

st.set_page_config(page_title="L'Art d'Être Sec IA", page_icon="🖤👑", layout="wide")
st.markdown("""
    <style>
        .main {background-color: #000000;}
        .stButton button {background-color: #FF0000; color: white; font-size: 18px; border-radius: 10px;}
        .stDownloadButton button {background-color: #FF0000; color: white; font-size: 18px; border-radius: 10px;}
        h1, h2, h3, h4, h5, h6, p {color: #FFFFFF;}
    </style>
""", unsafe_allow_html=True)

st.title("AI Program by L’Art d’Être Sec")
st.subheader("Ton programme de perte de poids automatisé !")
st.progress(0)

st.markdown("---")

preparation = st.radio("Quelle est votre moyenne de pas par jour sur le dernier mois ?", ["Moins de 10.000", "Plus de 10.000"], horizontal=True)
besoin_preparation = preparation == "Moins de 10.000"
st.session_state["besoin_preparation"] = besoin_preparation

st.subheader("⚖️ Calcul du métabolisme basal")
col1, col2, col3 = st.columns(3)

with col1:
    poids = st.number_input("Poids actuel (kg)", min_value=30, max_value=200, step=1, key="poids")
with col2:
    taille = st.number_input("Taille (cm)", min_value=120, max_value=220, step=1, key="taille")
with col3:
    age = st.number_input("Âge (années)", min_value=10, max_value=100, step=1, key="age")

sexe = st.radio("Sexe", ["Homme", "Femme"], horizontal=True, key="sexe")

if poids and taille and age:
    metabolisme_basal = calculer_metabolisme_basal(poids, taille, age, sexe)
    st.info(f"📊 Métabolisme basal estimé : **{int(metabolisme_basal)} kcal/jour**")

st.subheader("📉 Estimation du taux de masse grasse")
st.image("bodyfathomme.jpg", caption="Sélectionnez votre taux de masse grasse.", use_container_width=True)
bodyfat = st.slider("Sélectionnez votre taux de bodyfat (%)", min_value=8, max_value=40, step=1, key="bodyfat_slider")

affirmation = st.radio("As-tu été vraiment honnête avec toi-même ??", ["Oui", "Non"], horizontal=True, key="honnetete")
if affirmation == "Non":
    bodyfat = st.slider("Rechoisissez votre taux de bodyfat (%)", min_value=8, max_value=40, step=1, key="bodyfat_corrected")

masse_maigre = poids * (1 - (bodyfat / 100))
proteines, lipides, glucides, fibres = calculer_macronutriments(masse_maigre, metabolisme_basal)

from datetime import datetime, timedelta

st.subheader("📅 Sélectionne la date de début du programme")
date_debut = st.date_input("Date de début", datetime.today(), key="date_debut")
date_formatee = date_debut.strftime("%d/%m/%Y")

generate_button = st.button("🚀 Générer mon programme", key="generate_button")

if generate_button:
    with st.spinner("Génération du programme..."):
        time.sleep(2)
    
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_fill_color(0, 0, 0)  # Ajout d'un fond noir après l'image
    pdf.set_fill_color(0, 0, 0)
    pdf.rect(0, 0, 210, 297, 'F')  # Ajout d'un logo en haut du document
    pdf.set_fill_color(0, 0, 0)  # Fond noir  # Fond noir
    pdf.rect(0, 0, 210, 297, 'F')  # Remplissage du fond
    pdf.ln(5)
    pdf.set_text_color(255, 215, 0)  # Texte en doré
    pdf.set_font("Arial", size=50)
    pdf.set_text_color(255, 215, 0)
    pdf.rotate(45, x=50, y=150)
    pdf.text(50, 150, sanitize_text("AI Program by L’Art d’Être Sec"))
    pdf.rotate(0)  # Réinitialisation de la rotation
    pdf.set_fill_color(0, 0, 0)  # Fond noir
    pdf.rect(0, 0, 210, 297, 'F')  # Remplissage du fond
    pdf.set_text_color(255, 215, 0)  # Texte en doré
    pdf.set_font("Arial", style='B', size=16)
    pdf.set_font("Helvetica", style='B', size=22)
    pdf.cell(200, 15, sanitize_text("AI Program by L’Art d’Être Sec"), ln=True, align='C', fill=True)
    pdf.set_text_color(255, 215, 0)  # Texte doré
    pdf.set_font("Helvetica", size=14) 
    pdf.cell(0, 10, sanitize_text("-Premium Courses-"), ln=True, align='C')
    pdf.ln(10)
    pdf.set_fill_color(255, 215, 0)  # Séparateurs dorés
    pdf.cell(0, 0.10, '', 0, 1, 'C', fill=True)
    pdf.ln(5)
    pdf.ln(10)
    if besoin_preparation:
        pdf.set_font("Arial", style='B', size=14)
        pdf.cell(0, 10, f"Semaine de Préparation - {date_formatee}", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, sanitize_text(f"Objectif : 10 000 pas/jour\nCalories/jour : {int(metabolisme_basal * 1.725)} kcal"))
        pdf.ln(5)
    
    pdf.set_font("Arial", style='B', size=12)
    
    # Ajout du tableau pour les semaines
    pdf.set_fill_color(255, 215, 0)  # Fond doré pour les en-têtes
    pdf.set_text_color(0, 0, 0)  # Texte en noir pour les en-têtes
    pdf.set_text_color(0, 0, 0)  # Texte noir
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(30, 10, "Semaine", 1, 0, 'C', fill=True)
    pdf.cell(40, 10, "Pas/jour", 1, 0, 'C', fill=True)
    pdf.cell(40, 10, "Calories/jour", 1, 0, 'C', fill=True)
    pdf.cell(30, 10, "Protéines (g)", 1, 0, 'C', fill=True)
    pdf.cell(30, 10, "Lipides (g)", 1, 0, 'C', fill=True)
    pdf.cell(30, 10, "Glucides (g)", 1, 1, 'C', fill=True)
    pdf.set_text_color(255, 255, 255)  # Texte en blanc pour le reste du tableau
    
    semaines = [(15000, 800), (15000, 600), (18000, 400), (18000, 200), (20000, 0),
                (20000, 0), (20000, 200), (20000, 400), (20000, 600), (20000, 800), (20000, 1000)]

    # Convertir la date de départ en format datetime
    date_debut = datetime.combine(date_debut, datetime.min.time())

    # Décaler la date si la semaine de préparation est nécessaire
    if besoin_preparation:
        date_debut += timedelta(days=7)

    # Créer la liste des dates pour chaque semaine
    dates_semaines = [(date_debut + timedelta(weeks=i)).strftime("%d/%m/%y") for i in range(11)]
    
    for i, (pas, surplus) in enumerate(semaines, start=1):
        calories_totales = metabolisme_basal + surplus
        proteines, lipides, glucides, fibres = calculer_macronutriments(masse_maigre, calories_totales)
        calories_totales = metabolisme_basal + surplus
        pdf.cell(30, 10, dates_semaines[i-1], 1, 0, 'C')  # Remplace le numéro de semaine par la date
        pdf.cell(40, 10, str(pas), 1, 0, 'C')
        pdf.cell(40, 10, str(int(calories_totales)), 1, 0, 'C')
        pdf.cell(30, 10, str(round(proteines, 1)), 1, 0, 'C')
        pdf.cell(30, 10, str(round(lipides, 1)), 1, 0, 'C')
        pdf.cell(30, 10, str(round(glucides, 1)), 1, 1, 'C')
    if os.path.exists("icons/calories.png"):
        pdf.image("icons/calories.png", x=10, y=pdf.get_y() + 5, w=8)
    if os.path.exists("icons/proteins.png"):
        pdf.image("icons/proteins.png", x=50, y=pdf.get_y() + 5, w=8)
    if os.path.exists("icons/fats.png"):
        pdf.image("icons/fats.png", x=90, y=pdf.get_y() + 5, w=8)
    if os.path.exists("icons/carbs.png"):
        pdf.image("icons/carbs.png", x=130, y=pdf.get_y() + 5, w=8)
    if os.path.exists("icons/steps.png"):
        pdf.image("icons/steps.png", x=170, y=pdf.get_y() + 5, w=8)

    # Ajouter un espace après le tableau
    pdf.ln(10)

    # Définir la couleur et le style de la note
    pdf.set_text_color(255, 215, 0)  # Texte doré
    pdf.set_font("Arial", style='B', size=14)
    pdf.cell(0, 10, "Note Importante", ln=True, align='L')

    # Texte explicatif
    pdf.set_text_color(255, 255, 255)  # Texte blanc
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 8, "Pour ne pas être ballonné et paraître plus gros que ce que tu ne l'es, consomme 15g de fibres par 1000 calories ingérées. C'est le secrêt d'un bon transit !", align='L')

    # Ajouter un espace avant la fin du PDF
    pdf.ln(10)
    
    pdf_path = "ai_program_by_Lartdetresec.pdf"
    pdf.output(pdf_path)
    
    st.success("📄 Programme généré avec succès !")
    st.download_button(label="📥 Télécharge ton programme en PDF", data=open(pdf_path, "rb").read(), file_name="ai_program_by_Lartdetresec.pdf", mime="application/pdf")

st.markdown("---")
st.subheader("📌 Et après ?")
st.markdown("**Si tu es satisfait de ton physique à la fin de la 11e semaine :**")
st.markdown("- Reste avec ton nouveau maintien calorique que tu devras calculer toi-même en choisissant ‘très actif’.")
st.markdown("- Garde soit 15 000 pas par jour, ou choisis 10 000 pas par jour et recalcule ton maintien en choisissant ‘actif’.")
st.markdown("**Si tu n'es pas satisfait :**")
st.markdown("- Tu peux recommencer un cycle avec tes nouvelles données corporelles.")

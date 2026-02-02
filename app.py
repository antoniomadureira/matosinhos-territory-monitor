import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os

# --- 1. CONFIGURAÇÃO E CARREGAMENTO DE DADOS ---
st.set_page_config(page_title="Matosinhos em Dados", page_icon="🇵🇹", layout="wide")

# Função para carregar dados do JSON (Gerado pelo ETL)
def load_data():
    file_path = "dados.json"
    # Se o ficheiro JSON não existir (ainda não correu o ETL), usa defaults
    if not os.path.exists(file_path):
        return {
            "populacao": {"valor": "179 558", "ano": "2023"},
            "ganho_medio": {"valor": "1 424", "ano": "2021"},
            "empresas": {"valor": "23 152", "ano": "2022"},
            "medicos": {"valor": "9,9", "ano": "2022"}
        }
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

# Carregar dados dinâmicos
DADOS = load_data()

# --- 2. SISTEMA DE DESIGN ---
COLORS = {"Gov": "#00538B", "Amb": "#3F7E44", "Mob": "#766C9F", "Vida": "#D68E2C", "Eco": "#C04E38", "Soc": "#A67C52", "AMP": "#9CA3AF"}

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    .stApp {background-color: #F9FAFB; font-family: 'Inter', sans-serif; color: #1F2937;}
    .macro-card {background: white; padding: 20px; border-radius: 12px; text-align: center; border-bottom: 4px solid #00538B; box-shadow: 0 4px 6px rgba(0,0,0,0.05);}
    .macro-val {font-size: 28px; font-weight: 800; color: #00538B;}
    .macro-lbl {font-size: 12px; font-weight: 600; color: #6B7280; text-transform: uppercase;}
    .macro-yr {font-size: 10px; color: #9CA3AF; margin-top: 5px;}
    div.stButton > button {width: 100%; height: 100px; border-radius: 10px; border: none; color: white; font-weight: 700; text-transform: uppercase;}
    div[data-testid="stHorizontalBlock"] > div:nth-child(1) button {background-color: #00538B;}
    div[data-testid="stHorizontalBlock"] > div:nth-child(2) button {background-color: #3F7E44;}
    div[data-testid="stHorizontalBlock"] > div:nth-child(3) button {background-color: #766C9F;}
    div[data-testid="stHorizontalBlock"] > div:nth-child(4) button {background-color: #D68E2C;}
    div[data-testid="stHorizontalBlock"] > div:nth-child(5) button {background-color: #C04E38;}
    div[data-testid="stHorizontalBlock"] > div:nth-child(6) button {background-color: #A67C52;}
    </style>
""", unsafe_allow_html=True)

# --- 3. DASHBOARD ---

# Header
c1, c2 = st.columns([1, 8])
with c1: st.image("https://www.cm-matosinhos.pt/cmmatosinhos/uploads/writer_file/document/2179/logo_cmm.png", width=90)
with c2: 
    st.title("Matosinhos em Números")
    st.markdown("**Monitor Territorial Inteligente** | Dados Oficiais (Atualização Automática)")

st.markdown("---")

# MACRO CARDS (Dados lidos do JSON)
cols = st.columns(4)
stats = [
    {"l": "População", "v": DADOS['populacao']['valor'], "y": DADOS['populacao']['ano']},
    {"l": "Ganho Médio (€)", "v": DADOS['ganho_medio']['valor'], "y": DADOS['ganho_medio']['ano']},
    {"l": "Empresas", "v": DADOS['empresas']['valor'], "y": DADOS['empresas']['ano']},
    {"l": "Médicos/1k Hab", "v": DADOS['medicos']['valor'], "y": DADOS['medicos']['ano']}
]

for i, stat in enumerate(stats):
    with cols[i]:
        st.markdown(f"""
        <div class="macro-card">
            <div class="macro-val">{stat['v']}</div>
            <div class="macro-lbl">{stat['l']}</div>
            <div class="macro-yr">Fonte: INE {stat['y']}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br><h4 style='text-align:center; color:#6B7280;'>SELECIONE UMA DIMENSÃO</h4><br>", unsafe_allow_html=True)

# Menu de Navegação
c1, c2, c3, c4, c5, c6 = st.columns(6)
with c1: st.button("GOVERNANÇA")
with c2: st.button("AMBIENTE")
with c3: st.button("MOBILIDADE")
with c4: st.button("MODOS DE VIDA")
with c5: st.button("ECONOMIA")
with c6: st.button("SOCIEDADE")

# (Aqui entra a lógica de renderização detalhada das páginas, mantida da versão anterior...)
if 'page' not in st.session_state: st.session_state.page = 'home'
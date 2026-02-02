import streamlit as st
import pandas as pd
import requests
import folium
from streamlit_folium import st_folium
import plotly.express as px

# --- 1. CONFIGURAÇÃO VISUAL (ODS STYLE) ---
st.set_page_config(
    page_title="Matosinhos ODS 2030",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS para o estilo "Clean White" e cores dos ODS
st.markdown("""
    <style>
    .stApp {background-color: #ffffff;}
    .css-1r6slb0 {background-color: white; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.04); border: 1px solid #f3f4f6;}
    h1, h2, h3 {font-family: 'Helvetica Neue', sans-serif; color: #111827;}
    div[data-testid="stMetricValue"] {font-size: 24px; color: #1f2937; font-weight: 700;}
    .ods-badge {
        display: inline-block;
        padding: 4px 8px;
        border-radius: 4px;
        color: white;
        font-weight: bold;
        font-size: 0.8rem;
        margin-bottom: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DADOS E CONSTANTES ---
CODIGO_MATOSINHOS = "1308"
MATOSINHOS_COORDS = [[41.22, -8.71], [41.24, -8.66], [41.21, -8.62], [41.17, -8.65], [41.17, -8.70], [41.22, -8.71]]

# Estrutura de Dados com Metadados ODS
# Inclui IDs da API (para tentar o real-time) e Dados de Backup (Reais 2022/23)
CATALOGO = {
    "Demografia": {
        "População Residente": {"id": "0011609", "ods": "11", "color": "#FD9D24", "backup": { "2011": 175478, "2021": 173842, "2023": 179558}},
        "Nados-Vivos": {"id": "0011802", "ods": "3", "color": "#4C9F38", "backup": {"2020": 1289, "2021": 1315, "2022": 1290}},
        "Índice Envelhecimento": {"id": "0010003", "ods": "10", "color": "#DD1367", "backup": {"2019": 160.1, "2021": 170.5, "2022": 182.3}}
    },
    "Economia": {
        "Poder de Compra": {"id": "0005512", "ods": "8", "color": "#A21942", "backup": {"2017": 112.4, "2019": 115.4, "2021": 118.2}},
        "Ganho Médio Mensal (€)": {"id": "0011388", "ods": "8", "color": "#A21942", "backup": {"2019": 1250, "2020": 1390, "2021": 1420}},
        "Volume Negócios (Mil Milhões €)": {"id": "0008827", "ods": "9", "color": "#FD6925", "backup": {"2019": 7.9, "2020": 8.13, "2021": 9.2}}
    },
    "Ambiente": {
        "Água Segura (%)": {"id": "0009891", "ods": "6", "color": "#26BDE2", "backup": {"2020": 99.5, "2021": 99.65, "2022": 99.8}},
        "Perdas de Água (%)": {"id": "0000000", "ods": "6", "color": "#26BDE2", "backup": {"2013": 22.0, "2022": 10.8, "2023": 9.1}}, # Líder nacional
        "Recolha Seletiva (Ton)": {"id": "0009890", "ods": "12", "color": "#BF8B2E", "backup": {"2020": 14500, "2021": 15200, "2022": 15800}}
    },
    "Sociedade": {
        "Despesa Cultura (€/hab)": {"id": "0000000", "ods": "11", "color": "#FD9D24", "backup": {"2020": 95.2, "2021": 105.4, "2022": 117.4}},
        "Crimes Registados (‰)": {"id": "0004245", "ods": "16", "color": "#00689D", "backup": {"2021": 22.1, "2022": 23.5, "2023": 24.1}}
    }
}

# --- 3. MOTOR DE DADOS ---
@st.cache_data(ttl=3600)
def get_data(categoria, indicador):
    meta = CATALOGO[categoria][indicador]
    api_id = meta["id"]
    
    # URL Tática: Tenta sempre o geocódigo direto
    url = f"https://www.ine.pt/ine/json_indicador/pindica.jsp?op=2&varcd={api_id}&lang=PT&geocod={CODIGO_MATOSINHOS}&Dim1=T"
    
    records = []
    source = "api"
    
    # Tenta API apenas se tivermos um ID válido (diferente de 0000000)
    if api_id != "0000000":
        try:
            r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=3)
            if r.status_code == 200:
                data = r.json()
                if data and 'Dados' in data[0]:
                    dados_dict = data[0]['Dados']
                    for ano, lista in dados_dict.items():
                        if len(str(ano)) == 4 and str(ano).isdigit():
                            if isinstance(lista, list):
                                # Regra do Máximo (para evitar duplicados de sexo/idade)
                                max_val = 0.0
                                found = False
                                for item in lista:
                                    geo = str(item.get('geocod') or item.get('geocodigo'))
                                    if geo == CODIGO_MATOSINHOS:
                                        try:
                                            v = float(str(item.get('valor')).replace(',', '.'))
                                            if v > max_val:
                                                max_val = v
                                                found = True
                                        except: pass
                                if found:
                                    records.append({"Ano": ano, "Valor": max_val})
        except: pass

    # Se a API falhar ou não tiver ID, usa o Backup (Dados Reais inseridos manualmente)
    if not records:
        source = "backup"
        records = [{"Ano": k, "Valor": v} for k, v in meta["backup"].items()]
    
    df = pd.DataFrame(records)
    if not df.empty:
        df = df.sort_values('Ano')
        
    return df, source, meta

# --- 4. WIDGETS ---
def ods_badge(ods_num, color):
    return f'<div class="ods-badge" style="background-color: {color};">ODS {ods_num}</div>'

def render_chart(df, title, color):
    fig = px.bar(df, x="Ano", y="Valor", text="Valor") if len(df) < 5 else px.area(df, x="Ano", y="Valor")
    fig.update_traces(marker_color=color, textposition='outside')
    fig.update_layout(
        title=None,
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=250,
        margin=dict(l=20, r=20, t=10, b=20),
        yaxis=dict(showgrid=True, gridcolor='#f3f4f6'),
        xaxis=dict(showgrid=False)
    )
    st.plotly_chart(fig, use_container_width=True)

# --- 5. DASHBOARD ---
c1, c2 = st.columns([1, 6])
with c1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Matosinhos_coat_of_arms.png/170px-Matosinhos_coat_of_arms.png", width=80)
with c2:
    st.title("Matosinhos 2030: Monitor ODS")
    st.markdown("Monitorização de metas de sustentabilidade, economia e qualidade de vida.")

st.markdown("---")

# Abas por Área Temática
tabs = st.tabs(["🌍 Visão Geral", "👥 Sociedade", "💰 Economia", "🌿 Ambiente"])

# --- ABA 1: VISÃO GERAL ---
with tabs[0]:
    st.subheader("Destaques do Território")
    c1, c2, c3, c4 = st.columns(4)
    
    # KPI 1: População
    df_pop, src, meta = get_data("Demografia", "População Residente")
    with c1:
        curr = df_pop.iloc[-1]['Valor']
        st.metric("População", f"{curr:,.0f}", delta=f"{curr - df_pop.iloc[-2]['Valor']:,.0f}")
        st.caption(f"ODS {meta['ods']} | {src.upper()}")

    # KPI 2: Poder de Compra
    df_pib, src, meta = get_data("Economia", "Poder de Compra")
    with c2:
        curr = df_pib.iloc[-1]['Valor']
        st.metric("Poder Compra", f"{curr:.1f}", delta="Index 100")
        st.caption(f"ODS {meta['ods']} | {src.upper()}")
        
    # KPI 3: Água (Eficiência)
    df_agua, src, meta = get_data("Ambiente", "Perdas de Água (%)")
    with c3:
        curr = df_agua.iloc[-1]['Valor']
        st.metric("Perdas Água", f"{curr:.1f}%", delta="-1.7%", delta_color="inverse") # Inverso porque descer é bom
        st.caption(f"ODS {meta['ods']} | {src.upper()}")

    # KPI 4: Cultura
    df_cult, src, meta = get_data("Sociedade", "Despesa Cultura (€/hab)")
    with c4:
        curr = df_cult.iloc[-1]['Valor']
        st.metric("Inv. Cultura", f"€ {curr:.1f}", delta="+12.0")
        st.caption(f"ODS {meta['ods']} | {src.upper()}")

    st.markdown("---")
    cm, ci = st.columns([2, 1])
    with cm:
        st.markdown("##### 📍 Localização ODS Local")
        m = folium.Map(location=[41.20, -8.66], zoom_start=12, tiles="cartodbpositron")
        folium.Polygon(MATOSINHOS_COORDS, color="#3b82f6", fill=True, fill_opacity=0.1).add_to(m)
        st_folium(m, height=350, use_container_width=True)
    with ci:
        st.info("**Nota Técnica:** Este painel prioriza dados da API do INE. Quando indisponível, utiliza dados validados dos Relatórios de Gestão Municipal 2022/2023.")

# --- GERADOR DE ABAS AUTOMÁTICO ---
# Cria as outras abas dinamicamente baseadas no CATALOGO
areas_map = {"Sociedade": 1, "Economia": 2, "Ambiente": 3}

for area, tab_idx in areas_map.items():
    with tabs[tab_idx]:
        st.subheader(f"Indicadores de {area}")
        cols = st.columns(2)
        
        # Itera pelos indicadores da área
        for idx, (ind_nome, _) in enumerate(CATALOGO[area].items()):
            # Alterna colunas (Grid 2 colunas)
            with cols[idx % 2]:
                df, src, meta = get_data(area, ind_nome)
                
                # Card Visual
                with st.container():
                    st.markdown(f"**{ind_nome}** " + ods_badge(meta['ods'], meta['color']), unsafe_allow_html=True)
                    render_chart(df, ind_nome, meta['color'])
                    
                    # Tabela expansível
                    with st.expander(f"Ver dados ({src})"):
                        st.dataframe(df, use_container_width=True)
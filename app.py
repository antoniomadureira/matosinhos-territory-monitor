import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- 1. CONFIGURAÇÃO GERAL ---
st.set_page_config(
    page_title="Matosinhos em Dados",
    page_icon="🇵🇹",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Gestão de Estado
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'cluster' not in st.session_state:
    st.session_state.cluster = None

# --- 2. SISTEMA DE DESIGN ---
COLORS = {
    "Gov": "#00538B",   "Amb": "#3F7E44",   "Mob": "#766C9F",
    "Vida": "#D68E2C",  "Eco": "#C04E38",   "Soc": "#A67C52",
    "AMP": "#9CA3AF",   "Mat": "#00538B"
}

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap');
    .stApp {background-color: #F9FAFB; color: #1F2937; font-family: 'Inter', sans-serif;}
    h1, h2, h3, h4 {color: #111827 !important; font-weight: 700 !important;}
    p {color: #4B5563 !important;}

    /* MACRO CARDS */
    .macro-card {
        background: white; padding: 24px; border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); text-align: center;
        border-bottom: 4px solid #00538B; height: 100%; transition: transform 0.2s;
    }
    .macro-card:hover {transform: translateY(-4px);}
    .macro-val {font-size: 28px; font-weight: 800; color: #00538B;}
    .macro-lbl {font-size: 11px; font-weight: 700; color: #6B7280; text-transform: uppercase; margin-top: 10px;}
    .macro-yr {font-size: 10px; color: #9CA3AF; margin-top: 4px; font-weight: 600;}

    /* BOTÕES MENU */
    div.stButton > button {
        width: 100%; height: 100px; border: none; border-radius: 12px;
        color: white !important; font-size: 14px; font-weight: 700;
        text-transform: uppercase; letter-spacing: 0.5px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05); transition: all 0.2s;
    }
    div.stButton > button:hover {transform: scale(1.02); filter: brightness(110%);}

    /* Cores das Colunas */
    div[data-testid="stHorizontalBlock"] > div:nth-child(1) div.stButton > button {background-color: #00538B !important;}
    div[data-testid="stHorizontalBlock"] > div:nth-child(2) div.stButton > button {background-color: #3F7E44 !important;}
    div[data-testid="stHorizontalBlock"] > div:nth-child(3) div.stButton > button {background-color: #766C9F !important;}
    div[data-testid="stHorizontalBlock"] > div:nth-child(4) div.stButton > button {background-color: #D68E2C !important;}
    div[data-testid="stHorizontalBlock"] > div:nth-child(5) div.stButton > button {background-color: #C04E38 !important;}
    div[data-testid="stHorizontalBlock"] > div:nth-child(6) div.stButton > button {background-color: #A67C52 !important;}

    /* Botão Voltar */
    button[kind="secondary"] {background: white !important; color: #374151 !important; border: 1px solid #D1D5DB !important;}
    
    /* KPI Sidebar */
    .kpi-box {background: white; padding: 20px; border-radius: 10px; border-left: 4px solid #ccc; margin-bottom: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.02);}
    .kpi-num {font-size: 22px; font-weight: 800; color: #1F2937;}
    .kpi-tit {font-size: 11px; font-weight: 600; color: #6B7280; text-transform: uppercase;}
    .kpi-sub {font-size: 11px; color: #059669;}
    .kpi-date {font-size: 10px; color: #9CA3AF; margin-top: 2px;}
    </style>
""", unsafe_allow_html=True)

# --- 3. DADOS REAIS INE (COM DATAS EXPLÍCITAS) ---

MACRO = [
    {"l": "População Residente", "v": "172.557", "y": "Censos 2021 (INE)"},
    {"l": "Poder de Compra", "v": "118.2", "y": "INE 2021 (PT=100)"},
    {"l": "Ganho Médio Mensal", "v": "€1.424", "y": "INE 2021"},
    {"l": "Empresas", "v": "21.771", "y": "INE 2021"}
]

# Base de Dados com referência temporal explícita
DB = {
    "Governança": {
        "color": COLORS["Gov"],
        "tabs": ["Eleições", "Transparência"],
        "kpis": [
            {"l": "Inscritos (Leg.)", "v": "150.321", "sub": "vs 1.4M (AMP)", "d": "MAI 2024"},
            {"l": "Participação", "v": "70.8%", "sub": "+3.3% vs AMP", "d": "Leg. 2024"}
        ],
        "data": {
            "Eleições": {
                "gauge": {"val": 70.8, "ref": 67.5, "tit": "Taxa de Participação (%) - 2024"},
                "bar": {"x": [29.2, 32.5], "y": ["Matosinhos", "AMP"], "tit": "Abstenção Legislativas 2024 (%)"}
            }
        }
    },
    "Modos de Vida": {
        "color": COLORS["Vida"],
        "tabs": ["Educação", "Habitação", "Segurança", "Saúde"],
        "kpis": [
            {"l": "Preço Habitação", "v": "2.450 €/m²", "sub": "+10% vs 2022", "d": "INE 2023"},
            {"l": "Ensino Superior", "v": "26.3%", "sub": "vs 24.0% (AMP)", "d": "Censos 2021"},
            {"l": "Médicos", "v": "6.5/1k", "sub": "vs 5.8 (PT)", "d": "INE 2022"}
        ],
        "data": {
            "Educação": {
                "desc": "População residente com ensino superior completo (Fonte: Censos 2021).",
                "gauge": {"val": 26.3, "ref": 24.0, "tit": "% Ensino Superior (2021)"},
                "line": {"x": [2011, 2021], "m": [21.0, 26.3], "amp": [19.5, 24.0], "tit": "Evolução da Escolaridade Superior (2011-2021)"}
            },
            "Habitação": {
                "desc": "Valor mediano das vendas de alojamentos familiares por m² (Fonte: INE).",
                "gauge": {"val": 2450, "ref": 2100, "tit": "Preço m² (2023)"},
                "line": {"x": [2020, 2021, 2022, 2023], "m": [1600, 1850, 2100, 2450], "amp": [1400, 1550, 1800, 2100], "tit": "Evolução Preço Habitação (€/m²)"}
            },
            "Segurança": {
                "desc": "Crimes registados pelas autoridades policiais por mil habitantes (Fonte: RASI/INE).",
                "gauge": {"val": 29.4, "ref": 32.1, "tit": "Crimes por 1k Hab. (2022)"},
                "bar": {"x": [29.4, 32.1], "y": ["Matosinhos", "AMP"], "tit": "Criminalidade Geral (2022)"}
            },
            "Saúde": {
                "desc": "Número de médicos por 1000 habitantes (Fonte: INE/Ordem dos Médicos).",
                "gauge": {"val": 6.5, "ref": 5.8, "tit": "Médicos / 1k Hab. (2022)"},
                "bar": {"x": [6.5, 5.8], "y": ["Matosinhos", "Média Nacional"], "tit": "Cobertura Médica (2022)"}
            }
        }
    },
    "Economia": {
        "color": COLORS["Eco"],
        "tabs": ["Tecido Empresarial", "Riqueza"],
        "kpis": [
            {"l": "Poder de Compra", "v": "118.2", "sub": "IPCr (PT=100)", "d": "INE 2021"},
            {"l": "Vol. Negócios", "v": "12.8MM", "sub": "+18% YoY", "d": "INE 2021"}
        ],
        "data": {
            "Tecido Empresarial": {
                "gauge": {"val": 56.4, "ref": 52.0, "tit": "Sobrevivência Empresas 2 Anos (2021)"},
                "line": {"x": [2019, 2020, 2021], "m": [20500, 21000, 21771], "amp": [200000, 205000, 210000], "tit": "Número de Empresas Não Financeiras"}
            },
            "Riqueza": {
                "gauge": {"val": 118.2, "ref": 105.4, "tit": "Poder de Compra Per Capita (2021)"},
                "bar": {"x": [118.2, 105.4], "y": ["Matosinhos", "AMP"], "tit": "Índice de Poder de Compra (INE 2021)"}
            }
        }
    },
    "Ambiente": {
        "color": COLORS["Amb"],
        "tabs": ["Resíduos"], 
        "kpis": [{"l": "Resíduos", "v": "541 kg", "sub": "vs 512 (AMP)", "d": "INE 2021"}], 
        "data": {"Resíduos": {"gauge": {"val": 541, "ref": 512, "tit": "Resíduos kg/hab (2021)"}}}
    },
    "Mobilidade": {
        "color": COLORS["Mob"],
        "tabs": ["Transportes"],
        "kpis": [{"l": "Carro Próprio", "v": "67.2%", "sub": "vs 62.0% (AMP)", "d": "Censos 2021"}],
        "data": {"Transportes": {"gauge": {"val": 67.2, "ref": 62.0, "tit": "% Transp. Individual (2021)"}}}
    },
    "Sociedade": {
        "color": COLORS["Soc"],
        "tabs": ["Demografia"],
        "kpis": [{"l": "Envelhecimento", "v": "189.8", "sub": "vs 175.2 (AMP)", "d": "INE 2022"}],
        "data": {"Demografia": {"gauge": {"val": 189.8, "ref": 175.0, "tit": "Índice Envelhecimento (2022)"}}}
    }
}

# --- 4. VISUALIZAÇÕES ---

def gauge_chart(val, ref, title, color):
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta", value=val,
        title={'text': title, 'font': {'size': 14, 'color': '#374151'}},
        delta={'reference': ref, 'relative': False, 'increasing': {'color': COLORS['AMP']}},
        gauge={'axis': {'range': [None, max(val, ref)*1.2]}, 'bar': {'color': color}, 'bgcolor': "white", 'bordercolor': "#E5E7EB"}
    ))
    fig.update_layout(height=200, margin=dict(t=40, b=20, l=30, r=30), paper_bgcolor='rgba(0,0,0,0)')
    return fig

def line_compare(x, m, amp, title, color):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=amp, name='AMP', line=dict(color=COLORS['AMP'], width=2, dash='dot')))
    fig.add_trace(go.Scatter(x=x, y=m, name='Matosinhos', line=dict(color=color, width=4)))
    fig.update_layout(
        title=title, height=300, plot_bgcolor='white', 
        legend=dict(orientation="h", y=1.1), xaxis=dict(showgrid=False, type='category'), yaxis=dict(showgrid=True, gridcolor='#F3F4F6')
    )
    return fig

def bar_compare(x, y, title, color):
    colors = [color if label == "Matosinhos" else COLORS["AMP"] for label in y]
    fig = px.bar(x=x, y=y, orientation='h', text=x)
    fig.update_traces(marker_color=colors, textposition='outside')
    fig.update_layout(title=title, height=250, plot_bgcolor='white', xaxis=dict(showgrid=True, gridcolor='#F3F4F6'), yaxis=dict(title=None))
    return fig

# --- 5. PÁGINAS ---

def render_home():
    c1, c2 = st.columns([1, 8])
    with c1: st.markdown('<img src="https://www.cm-matosinhos.pt/cmmatosinhos/uploads/writer_file/document/2179/logo_cmm.png" width="90">', unsafe_allow_html=True)
    with c2:
        st.markdown("# Matosinhos em Números")
        st.markdown("**Monitor Territorial Inteligente** | Dados Oficiais INE")

    st.markdown("---")
    
    # Macro Stats
    cols = st.columns(4)
    for i, m in enumerate(MACRO):
        with cols[i]:
            st.markdown(f"""
            <div class="macro-card">
                <div class="macro-val">{m['v']}</div>
                <div class="macro-lbl">{m['l']}</div>
                <div class="macro-yr">{m['y']}</div>
            </div>""", unsafe_allow_html=True)
            
    st.markdown("<br><h4 style='text-align:center; color:#6B7280;'>SELECIONE UMA DIMENSÃO</h4><br>", unsafe_allow_html=True)
    
    # Menu Colorido (CSS trata das cores)
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1: 
        if st.button("GOVERNANÇA"): st.session_state.cluster="Governança"; st.session_state.page="cluster"; st.rerun()
    with c2: 
        if st.button("AMBIENTE"): st.session_state.cluster="Ambiente"; st.session_state.page="cluster"; st.rerun()
    with c3: 
        if st.button("MOBILIDADE"): st.session_state.cluster="Mobilidade"; st.session_state.page="cluster"; st.rerun()
    with c4: 
        if st.button("MODOS DE VIDA"): st.session_state.cluster="Modos de Vida"; st.session_state.page="cluster"; st.rerun()
    with c5: 
        if st.button("ECONOMIA"): st.session_state.cluster="Economia"; st.session_state.page="cluster"; st.rerun()
    with c6: 
        if st.button("SOCIEDADE"): st.session_state.cluster="Sociedade"; st.session_state.page="cluster"; st.rerun()

def render_cluster(cluster_name):
    data = DB.get(cluster_name)
    color = data['color']
    
    if st.button("⬅ VOLTAR", type="secondary"): st.session_state.page="home"; st.rerun()
    
    st.markdown(f"""
    <div style='display:flex; align-items:center; gap:15px; margin:20px 0;'>
        <div style='background:{color}; color:white; padding:12px; border-radius:12px; width:50px; height:50px; display:flex; align-items:center; justify-content:center; font-size:24px;'>📊</div>
        <div>
            <h1 style='margin:0; color:{color} !important;'>{cluster_name}</h1>
            <p style='margin:0;'>Dados INE comparados com a Área Metropolitana do Porto (AMP)</p>
        </div>
    </div>""", unsafe_allow_html=True)
    
    col_kpi, col_main = st.columns([1, 3])
    
    with col_kpi:
        st.markdown("#### Resumo")
        for k in data['kpis']:
            st.markdown(f"""
            <div class="kpi-box" style="border-left-color: {color};">
                <div class="kpi-num">{k['v']}</div>
                <div class="kpi-tit">{k['l']}</div>
                <div class="kpi-sub">{k.get('sub','')}</div>
                <div class="kpi-date">{k.get('d','')}</div>
            </div>""", unsafe_allow_html=True)
            
    with col_main:
        tabs = st.tabs(data['tabs'])
        
        for i, tab_name in enumerate(data['tabs']):
            with tabs[i]:
                if tab_name in data['data']:
                    sub_data = data['data'][tab_name]
                    
                    if 'desc' in sub_data:
                        st.caption(sub_data['desc'])
                    
                    c1, c2 = st.columns(2)
                    with c1:
                        if 'gauge' in sub_data:
                            g = sub_data['gauge']
                            st.plotly_chart(gauge_chart(g['val'], g['ref'], g['tit'], color), use_container_width=True)
                    with c2:
                        if 'line' in sub_data:
                            l = sub_data['line']
                            st.plotly_chart(line_compare(l['x'], l['m'], l['amp'], l['tit'], color), use_container_width=True)
                        elif 'bar' in sub_data:
                            b = sub_data['bar']
                            st.plotly_chart(bar_compare(b['x'], b['y'], b['tit'], color), use_container_width=True)
                else:
                    st.info(f"Dados detalhados de {tab_name} em atualização no INE.")

# --- 6. ROUTER ---
if st.session_state.page == 'home': render_home()
elif st.session_state.page == 'cluster': render_cluster(st.session_state.cluster)
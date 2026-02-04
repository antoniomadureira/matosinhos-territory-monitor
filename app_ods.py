"""
Matosinhos Territory Monitor - Dashboard Principal
Dashboards interativos com indicadores INE mapeados para os ODS
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os
from datetime import datetime

# --- CONFIGURAÇÃO ---
st.set_page_config(
    page_title="Matosinhos Territory Monitor",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- FUNÇÕES DE CARREGAMENTO ---
@st.cache_data
def load_ods_data():
    """Carrega dados ODS extraídos do PDF."""
    file_path = "dados_ods.json"
    if not os.path.exists(file_path):
        st.warning("⚠️ Dados ODS não encontrados. Execute primeiro o ETL: `python etl_ods.py`")
        return None
    
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

# --- CORES E DESIGN ---
ODS_COLORS = {
    "ODS1": "#E5243B", "ODS2": "#DDA63A", "ODS3": "#4C9F38", "ODS4": "#C5192D",
    "ODS5": "#FF3A21", "ODS6": "#26BDE2", "ODS7": "#FCC30B", "ODS8": "#A21942",
    "ODS9": "#FD6925", "ODS10": "#DD1367", "ODS11": "#FD9D24", "ODS12": "#BF8B2E",
    "ODS13": "#3F7E44", "ODS14": "#0A97D9", "ODS15": "#56C02B", "ODS16": "#00689D",
    "ODS17": "#19486A"
}

# CSS Personalizado
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #1e3a8a;
        margin: 0;
    }
    
    .main-subtitle {
        font-size: 1.1rem;
        color: #64748b;
        margin-top: 0.5rem;
    }
    
    .kpi-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #3b82f6;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
        height: 100%;
    }
    
    .kpi-value {
        font-size: 2rem;
        font-weight: 800;
        color: #1e3a8a;
        margin: 0;
    }
    
    .kpi-label {
        font-size: 0.9rem;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
        margin-top: 0.5rem;
    }
    
    .kpi-year {
        font-size: 0.75rem;
        color: #94a3b8;
        margin-top: 0.25rem;
    }
    
    .ods-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: transform 0.2s;
        cursor: pointer;
        margin-bottom: 1rem;
    }
    
    .ods-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    .ods-number {
        font-size: 3rem;
        font-weight: 800;
        line-height: 1;
    }
    
    .ods-title {
        font-size: 1rem;
        font-weight: 700;
        margin-top: 0.5rem;
        color: #1e293b;
    }
    
    .ods-count {
        font-size: 0.85rem;
        color: #64748b;
        margin-top: 0.25rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
    }
    
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1e3a8a;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #3b82f6;
    }
    
    .info-box {
        background: #eff6ff;
        border-left: 4px solid #3b82f6;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: #fef3c7;
        border-left: 4px solid #f59e0b;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .success-box {
        background: #d1fae5;
        border-left: 4px solid #10b981;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# --- CARREGAR DADOS ---
dados = load_ods_data()

if dados is None:
    st.stop()

# --- HEADER ---
st.markdown("""
<div class="main-header">
    <h1 class="main-title">🏛️ Matosinhos Territory Monitor</h1>
    <p class="main-subtitle">Dashboard de Indicadores Territoriais alinhados com os Objetivos de Desenvolvimento Sustentável</p>
    <p style="font-size: 0.85rem; color: #94a3b8; margin-top: 0.5rem;">
        📊 Fonte: INE (Instituto Nacional de Estatística) | 
        🔄 Última atualização: {}</p>
</div>
""".format(datetime.fromisoformat(dados["metadata"]["data_extracao"]).strftime("%d/%m/%Y %H:%M")), 
unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://www.cm-matosinhos.pt/cmmatosinhos/uploads/writer_file/document/2179/logo_cmm.png", 
             use_container_width=True)
    
    st.markdown("---")
    
    st.markdown("### 🎯 Navegação")
    
    pagina = st.radio(
        "Escolha uma vista:",
        ["📊 Visão Geral", "🎯 Indicadores ODS", "📈 Análise Detalhada", "🗺️ Comparação Regional"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    st.markdown("### ℹ️ Sobre")
    st.markdown("""
    Este dashboard apresenta indicadores territoriais de Matosinhos organizados 
    segundo os 17 Objetivos de Desenvolvimento Sustentável (ODS) da ONU.
    
    **Dados:** INE  
    **Concelho:** Matosinhos  
    **Ano base:** 2022-2023
    """)
    
    st.markdown("---")
    
    # Estatísticas rápidas
    total_indicadores = len(dados["indicadores"])
    ods_com_dados = len([k for k, v in dados["ods"].items() if v["indicadores"]])
    
    st.metric("Total Indicadores", total_indicadores)
    st.metric("ODS com Dados", f"{ods_com_dados}/17")

# --- PÁGINA: VISÃO GERAL ---
if pagina == "📊 Visão Geral":
    
    # KPIs Principais
    st.markdown('<div class="section-header">📊 Indicadores Principais</div>', unsafe_allow_html=True)
    
    cols = st.columns(4)
    
    kpis_principais = [
        ("populacao", "👥 População", "#3b82f6"),
        ("ganho_medio", "💰 Ganho Médio", "#10b981"),
        ("empresas", "🏢 Empresas", "#f59e0b"),
        ("medicos_hab", "⚕️ Médicos/1000 hab", "#ef4444")
    ]
    
    for i, (key, label, color) in enumerate(kpis_principais):
        if key in dados["indicadores"]:
            ind = dados["indicadores"][key]
            with cols[i]:
                st.markdown(f"""
                <div class="kpi-card" style="border-left-color: {color};">
                    <div class="kpi-value">{ind['valor']}</div>
                    <div class="kpi-label">{label}</div>
                    <div class="kpi-year">📅 {ind['ano']} | 📏 {ind.get('unidade', '')}</div>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Mapa ODS
    st.markdown('<div class="section-header">🎯 Objetivos de Desenvolvimento Sustentável</div>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <strong>ℹ️ Sobre os ODS:</strong> Os 17 Objetivos de Desenvolvimento Sustentável são uma agenda global 
        adotada pela ONU em 2015 para erradicar a pobreza, proteger o planeta e garantir prosperidade para todos.
    </div>
    """, unsafe_allow_html=True)
    
    # Grid de ODS (4 colunas)
    ods_por_linha = 4
    ods_list = list(dados["ods"].items())
    
    for linha in range(0, len(ods_list), ods_por_linha):
        cols = st.columns(ods_por_linha)
        
        for i, (ods_code, ods_data) in enumerate(ods_list[linha:linha + ods_por_linha]):
            with cols[i]:
                num_indicadores = len(ods_data["indicadores"])
                cor = ODS_COLORS.get(ods_code, "#94a3b8")
                numero_ods = ods_code.replace("ODS", "")
                
                # Emoji por ODS
                emojis = {
                    "1": "🚫💰", "2": "🍽️", "3": "💚", "4": "📚",
                    "5": "⚖️", "6": "💧", "7": "⚡", "8": "💼",
                    "9": "🏗️", "10": "📉", "11": "🏙️", "12": "♻️",
                    "13": "🌍", "14": "🌊", "15": "🌳", "16": "⚖️",
                    "17": "🤝"
                }
                emoji = emojis.get(numero_ods, "🎯")
                
                st.markdown(f"""
                <div class="ods-card" style="border-top: 5px solid {cor};">
                    <div style="display: flex; align-items: center; gap: 1rem;">
                        <div class="ods-number" style="color: {cor};">{emoji}</div>
                        <div style="flex: 1;">
                            <div class="ods-title">{ods_data['nome']}</div>
                            <div class="ods-count">
                                {'✅ ' + str(num_indicadores) + ' indicador' + ('es' if num_indicadores != 1 else '') 
                                 if num_indicadores > 0 else '⚠️ Sem dados'}
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # Gráfico de cobertura ODS
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="section-header">📊 Cobertura de Indicadores por ODS</div>', 
                    unsafe_allow_html=True)
        
        # Preparar dados para gráfico
        ods_nomes = []
        ods_contagens = []
        ods_cores = []
        
        for ods_code, ods_data in dados["ods"].items():
            ods_nomes.append(f"{ods_code.replace('ODS', '')}. {ods_data['nome']}")
            ods_contagens.append(len(ods_data["indicadores"]))
            ods_cores.append(ODS_COLORS.get(ods_code, "#94a3b8"))
        
        fig = go.Figure(data=[
            go.Bar(
                y=ods_nomes,
                x=ods_contagens,
                orientation='h',
                marker=dict(color=ods_cores),
                text=ods_contagens,
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title="Número de Indicadores Disponíveis por ODS",
            xaxis_title="Número de Indicadores",
            yaxis_title="",
            height=600,
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown('<div class="section-header">📈 Estatísticas</div>', unsafe_allow_html=True)
        
        # Calcular estatísticas
        total_ods = 17
        ods_com_dados = len([v for v in dados["ods"].values() if v["indicadores"]])
        ods_sem_dados = total_ods - ods_com_dados
        cobertura_pct = (ods_com_dados / total_ods) * 100
        
        st.markdown(f"""
        <div class="success-box">
            <strong>✅ ODS com Dados</strong><br>
            <span style="font-size: 2rem; font-weight: 800;">{ods_com_dados}</span> / {total_ods}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="warning-box">
            <strong>⚠️ ODS sem Dados</strong><br>
            <span style="font-size: 2rem; font-weight: 800;">{ods_sem_dados}</span> / {total_ods}
        </div>
        """, unsafe_allow_html=True)
        
        # Gráfico de pizza
        fig_pie = go.Figure(data=[go.Pie(
            labels=['Com Dados', 'Sem Dados'],
            values=[ods_com_dados, ods_sem_dados],
            marker=dict(colors=['#10b981', '#f59e0b']),
            hole=0.6
        )])
        
        fig_pie.update_layout(
            height=300,
            showlegend=True,
            annotations=[dict(text=f'{cobertura_pct:.0f}%<br>Cobertura', 
                             x=0.5, y=0.5, font_size=20, showarrow=False)],
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)

# --- PÁGINA: INDICADORES ODS ---
elif pagina == "🎯 Indicadores ODS":
    
    st.markdown('<div class="section-header">🎯 Explorar Indicadores por ODS</div>', 
                unsafe_allow_html=True)
    
    # Seletor de ODS
    ods_opcoes = {f"{k} - {v['nome']}": k for k, v in dados["ods"].items() if v["indicadores"]}
    
    if not ods_opcoes:
        st.warning("⚠️ Nenhum ODS possui indicadores disponíveis.")
        st.stop()
    
    ods_selecionado_label = st.selectbox(
        "Selecione um ODS para explorar:",
        list(ods_opcoes.keys())
    )
    
    ods_selecionado = ods_opcoes[ods_selecionado_label]
    ods_info = dados["ods"][ods_selecionado]
    cor_ods = ODS_COLORS.get(ods_selecionado, "#94a3b8")
    
    # Header do ODS
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {cor_ods} 0%, {cor_ods}dd 100%); 
                padding: 2rem; border-radius: 15px; color: white; margin: 1rem 0;">
        <h2 style="margin: 0; font-size: 2rem;">{ods_selecionado_label}</h2>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.1rem; opacity: 0.9;">
            {len(ods_info['indicadores'])} indicador{'es' if len(ods_info['indicadores']) != 1 else ''} disponível{'is' if len(ods_info['indicadores']) != 1 else ''}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Mostrar indicadores
    if ods_info["indicadores"]:
        cols = st.columns(2)
        
        for i, indicador in enumerate(ods_info["indicadores"]):
            with cols[i % 2]:
                # Obter info completa do indicador
                ind_completo = dados["indicadores"].get(indicador["chave"], {})
                
                # Traduzir nome
                nomes_indicadores = {
                    "populacao": "População Residente",
                    "densidade_populacional": "Densidade Populacional",
                    "medicos_hab": "Médicos por 1000 habitantes",
                    "taxa_mortalidade_infantil": "Taxa de Mortalidade Infantil",
                    "ganho_medio": "Ganho Médio Mensal",
                    "empresas": "Total de Empresas",
                    "taxa_escolarizacao": "Taxa de Escolarização (Sec.)",
                    "taxa_criminalidade": "Taxa de Criminalidade",
                    "taxa_natalidade": "Taxa Bruta de Natalidade",
                    "despesas_cultura_desporto": "Despesas Cultura/Desporto",
                    "empresas_industria": "Empresas Indústria Transform.",
                    "exportacoes": "Exportações",
                    "populacao_65_mais": "População ≥ 65 anos"
                }
                
                nome_ind = nomes_indicadores.get(indicador["chave"], indicador["chave"])
                
                st.markdown(f"""
                <div class="kpi-card" style="border-left-color: {cor_ods};">
                    <div class="kpi-value" style="color: {cor_ods};">{indicador['valor']}</div>
                    <div class="kpi-label">{nome_ind}</div>
                    <div class="kpi-year">
                        📅 {indicador['ano']} | 
                        📏 {indicador.get('unidade', '')}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
    else:
        st.info("ℹ️ Este ODS ainda não possui indicadores mapeados.")

# --- PÁGINA: ANÁLISE DETALHADA ---
elif pagina == "📈 Análise Detalhada":
    
    st.markdown('<div class="section-header">📈 Análise Detalhada de Indicadores</div>', 
                unsafe_allow_html=True)
    
    # Tabela de todos os indicadores
    st.markdown("### 📋 Todos os Indicadores")
    
    # Preparar dados para tabela
    tabela_data = []
    
    for key, ind in dados["indicadores"].items():
        # Nome traduzido
        nomes = {
            "populacao": "População Residente",
            "densidade_populacional": "Densidade Populacional",
            "medicos_hab": "Médicos/1000 hab",
            "taxa_mortalidade_infantil": "Mortalidade Infantil",
            "ganho_medio": "Ganho Médio Mensal",
            "empresas": "Total Empresas",
            "taxa_escolarizacao": "Taxa Escolarização",
            "taxa_criminalidade": "Taxa Criminalidade",
            "taxa_natalidade": "Taxa Natalidade",
            "despesas_cultura_desporto": "Despesas Cultura/Desporto",
            "empresas_industria": "Empresas Indústria",
            "exportacoes": "Exportações",
            "populacao_65_mais": "População ≥65 anos"
        }
        
        ods_str = ", ".join(ind.get("ods", []))
        
        tabela_data.append({
            "Indicador": nomes.get(key, key),
            "Valor": ind["valor"],
            "Unidade": ind.get("unidade", "-"),
            "Ano": ind["ano"],
            "ODS": ods_str
        })
    
    df = pd.DataFrame(tabela_data)
    st.dataframe(df, use_container_width=True, height=400)
    
    # Download dos dados
    st.markdown("### 💾 Download dos Dados")
    
    col1, col2 = st.columns(2)
    
    with col1:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"matosinhos_indicadores_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    with col2:
        json_str = json.dumps(dados, ensure_ascii=False, indent=2)
        st.download_button(
            label="📥 Download JSON Completo",
            data=json_str,
            file_name=f"matosinhos_dados_completos_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json"
        )

# --- PÁGINA: COMPARAÇÃO REGIONAL ---
elif pagina == "🗺️ Comparação Regional":
    
    st.markdown('<div class="section-header">🗺️ Comparação Regional (Em Desenvolvimento)</div>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <strong>ℹ️ Funcionalidade em Desenvolvimento</strong><br>
        Esta secção permitirá comparar os indicadores de Matosinhos com outros concelhos 
        da Área Metropolitana do Porto e com as médias nacionais.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🎯 Funcionalidades Planeadas")
    
    st.markdown("""
    - 🗺️ Mapa interativo da AMP
    - 📊 Comparação de indicadores-chave
    - 📈 Ranking entre concelhos
    - 🔄 Evolução temporal
    - 📉 Análise de gaps face às metas ODS
    """)

# --- FOOTER ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #94a3b8; font-size: 0.85rem; padding: 1rem;">
    <p><strong>Matosinhos Territory Monitor</strong> | Desenvolvido com Streamlit</p>
    <p>Dados: INE (Instituto Nacional de Estatística) | ODS: Nações Unidas</p>
    <p style="margin-top: 0.5rem;">
        📧 <a href="mailto:info@cm-matosinhos.pt" style="color: #3b82f6; text-decoration: none;">Contacto</a> |
        📚 <a href="https://www.ine.pt" target="_blank" style="color: #3b82f6; text-decoration: none;">INE</a> |
        🎯 <a href="https://www.un.org/sustainabledevelopment/" target="_blank" style="color: #3b82f6; text-decoration: none;">ODS</a>
    </p>
</div>
""", unsafe_allow_html=True)

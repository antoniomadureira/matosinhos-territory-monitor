"""
Matosinhos Territory Monitor - Dashboard Avançado
Funcionalidades: Comparação AMP, Mapas, Séries Temporais, Alertas ODS
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import os
from datetime import datetime, timedelta
import numpy as np

# --- CONFIGURAÇÃO ---
st.set_page_config(
    page_title="Matosinhos Monitor Avançado",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- DADOS ---
@st.cache_data
def load_all_data():
    """Carrega todos os dados necessários."""
    data = {}
    
    # Dados ODS
    if os.path.exists("dados_ods.json"):
        with open("dados_ods.json", "r", encoding="utf-8") as f:
            data['ods'] = json.load(f)
    else:
        data['ods'] = None
    
    # Dados AMP
    if os.path.exists("data_amp.json"):
        with open("data_amp.json", "r", encoding="utf-8") as f:
            data['amp'] = json.load(f)
    else:
        data['amp'] = None
    
    # Dados temporais simulados (histórico 5 anos)
    data['temporal'] = generate_temporal_data()
    
    # Metas ODS
    data['metas_ods'] = load_ods_targets()
    
    return data

def generate_temporal_data():
    """Gera dados temporais simulados para os últimos 5 anos."""
    years = [2019, 2020, 2021, 2022, 2023]
    
    return {
        'populacao': [175000, 176200, 177800, 178900, 179558],
        'empresas': [21500, 21800, 22300, 22800, 23152],
        'ganho_medio': [1250, 1280, 1350, 1390, 1424],
        'taxa_natalidade': [8.5, 8.1, 7.8, 7.5, 7.2],
        'taxa_escolarizacao': [112.5, 114.0, 115.2, 116.5, 117.4],
        'anos': years
    }

def load_ods_targets():
    """Define metas ODS para Matosinhos."""
    return {
        'ODS3': {
            'taxa_mortalidade_infantil': {'meta': 2.0, 'atual': 2.2, 'unidade': '‰'},
            'medicos_hab': {'meta': 5.0, 'atual': 4.5, 'unidade': 'por 1000 hab'},
        },
        'ODS4': {
            'taxa_escolarizacao': {'meta': 100.0, 'atual': 117.4, 'unidade': '%'},
        },
        'ODS8': {
            'ganho_medio': {'meta': 1500, 'atual': 1424, 'unidade': '€'},
        },
        'ODS11': {
            'densidade_populacional': {'meta': 2500, 'atual': 2838, 'unidade': 'hab/km²'},
        }
    }

# --- CORES E ESTILOS ---
ODS_COLORS = {
    "ODS1": "#E5243B", "ODS3": "#4C9F38", "ODS4": "#C5192D", "ODS8": "#A21942",
    "ODS11": "#FD9D24", "ODS16": "#00689D"
}

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Inter', sans-serif;
    }
    
    .main-container {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        transition: transform 0.3s;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
        margin-top: 0.5rem;
    }
    
    .alert-success {
        background: #d1fae5;
        border-left: 4px solid #10b981;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .alert-warning {
        background: #fef3c7;
        border-left: 4px solid #f59e0b;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .alert-danger {
        background: #fee2e2;
        border-left: 4px solid #ef4444;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .section-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1e3a8a;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #667eea;
    }
    
    .ranking-card {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 5px solid #667eea;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    
    .ranking-position {
        font-size: 2rem;
        font-weight: 800;
        color: #667eea;
    }
</style>
""", unsafe_allow_html=True)

# --- CARREGAR DADOS ---
dados = load_all_data()

# --- HEADER ---
col1, col2 = st.columns([1, 4])
with col1:
    st.image("https://www.cm-matosinhos.pt/cmmatosinhos/uploads/writer_file/document/2179/logo_cmm.png", 
             width=100)
with col2:
    st.title("📊 Matosinhos Territory Monitor")
    st.markdown("**Dashboard Avançado** | Comparação AMP • Mapas • Séries Temporais • Alertas ODS")

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### 🎯 Navegação Avançada")
    
    pagina = st.radio(
        "Escolha:",
        [
            "🏆 Comparação AMP",
            "🗺️ Mapas Interativos", 
            "📈 Séries Temporais",
            "🎯 Alertas ODS",
            "📱 Dashboard Mobile"
        ],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### ⚙️ Configurações")
    
    show_portugal = st.checkbox("Comparar com Portugal", value=True)
    show_trends = st.checkbox("Mostrar tendências", value=True)
    
    st.markdown("---")
    st.markdown("### 📊 Estatísticas Rápidas")
    if dados['amp']:
        total_pop_amp = sum(v['populacao'] for v in dados['amp'].values())
        st.metric("População AMP", f"{total_pop_amp:,}".replace(',', ' '))
        st.metric("Concelhos", len(dados['amp']))

# --- PÁGINA: COMPARAÇÃO AMP ---
if pagina == "🏆 Comparação AMP":
    
    st.markdown('<div class="section-title">🏆 Comparação com a Área Metropolitana do Porto</div>', 
                unsafe_allow_html=True)
    
    if not dados['amp']:
        st.warning("⚠️ Dados AMP não disponíveis")
        st.stop()
    
    # Converter dados AMP para DataFrame
    df_amp = pd.DataFrame(dados['amp']).T
    df_amp['concelho'] = df_amp.index
    df_amp = df_amp.reset_index(drop=True)
    
    # Calcular rankings
    df_amp['rank_pop'] = df_amp['populacao'].rank(ascending=False)
    df_amp['rank_densidade'] = df_amp['densidade'].rank(ascending=False)
    df_amp['rank_empresas'] = df_amp['empresas'].rank(ascending=False)
    df_amp['rank_ganho'] = df_amp['ganho_medio'].rank(ascending=False)
    
    # Destacar Matosinhos
    matosinhos_data = df_amp[df_amp['concelho'] == 'Matosinhos'].iloc[0]
    
    # KPIs de Ranking
    st.markdown("### 🏅 Posição de Matosinhos na AMP")
    
    cols = st.columns(4)
    
    rankings = [
        ("👥 População", int(matosinhos_data['rank_pop']), "habitantes"),
        ("📊 Densidade", int(matosinhos_data['rank_densidade']), "hab/km²"),
        ("🏢 Empresas", int(matosinhos_data['rank_empresas']), "unidades"),
        ("💰 Ganho Médio", int(matosinhos_data['rank_ganho']), "euros")
    ]
    
    for i, (label, rank, unit) in enumerate(rankings):
        with cols[i]:
            # Emoji de medalha
            if rank == 1:
                emoji = "🥇"
            elif rank == 2:
                emoji = "🥈"
            elif rank == 3:
                emoji = "🥉"
            else:
                emoji = f"#{rank}"
            
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{emoji}</div>
                <div class="metric-label">{label}</div>
                <div style="font-size: 0.8rem; margin-top: 0.5rem;">{unit}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Tabs para diferentes comparações
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Gráficos", "📋 Tabela", "🗺️ Mapa", "📈 Análise"])
    
    with tab1:
        # Gráfico de barras - População
        col1, col2 = st.columns(2)
        
        with col1:
            fig_pop = px.bar(
                df_amp.sort_values('populacao', ascending=False),
                x='concelho',
                y='populacao',
                title='População por Concelho',
                color='populacao',
                color_continuous_scale='Blues'
            )
            fig_pop.update_layout(height=400, showlegend=False)
            fig_pop.update_xaxes(tickangle=45)
            # Destacar Matosinhos
            fig_pop.add_hline(y=matosinhos_data['populacao'], 
                            line_dash="dash", line_color="red",
                            annotation_text="Matosinhos")
            st.plotly_chart(fig_pop, use_container_width=True)
        
        with col2:
            fig_ganho = px.bar(
                df_amp.sort_values('ganho_medio', ascending=False),
                x='concelho',
                y='ganho_medio',
                title='Ganho Médio Mensal por Concelho',
                color='ganho_medio',
                color_continuous_scale='Greens'
            )
            fig_ganho.update_layout(height=400, showlegend=False)
            fig_ganho.update_xaxes(tickangle=45)
            fig_ganho.add_hline(y=matosinhos_data['ganho_medio'], 
                              line_dash="dash", line_color="red",
                              annotation_text="Matosinhos")
            st.plotly_chart(fig_ganho, use_container_width=True)
        
        # Scatter plot - Densidade vs Empresas
        fig_scatter = px.scatter(
            df_amp,
            x='densidade',
            y='empresas',
            size='populacao',
            color='ganho_medio',
            hover_data=['concelho'],
            title='Densidade Populacional vs. Número de Empresas',
            labels={'densidade': 'Densidade (hab/km²)', 'empresas': 'Número de Empresas'},
            color_continuous_scale='Viridis',
            size_max=60
        )
        
        # Destacar Matosinhos
        fig_scatter.add_trace(
            go.Scatter(
                x=[matosinhos_data['densidade']],
                y=[matosinhos_data['empresas']],
                mode='markers+text',
                marker=dict(size=20, color='red', symbol='star'),
                text=['MATOSINHOS'],
                textposition='top center',
                name='Matosinhos',
                showlegend=True
            )
        )
        
        fig_scatter.update_layout(height=500)
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    with tab2:
        st.markdown("### 📋 Tabela Completa AMP")
        
        # Preparar tabela formatada
        df_display = df_amp.copy()
        df_display['populacao'] = df_display['populacao'].apply(lambda x: f"{x:,}".replace(',', ' '))
        df_display['densidade'] = df_display['densidade'].apply(lambda x: f"{x:,}".replace(',', ' '))
        df_display['empresas'] = df_display['empresas'].apply(lambda x: f"{x:,}".replace(',', ' '))
        df_display['ganho_medio'] = df_display['ganho_medio'].apply(lambda x: f"{x} €")
        
        df_display = df_display[['concelho', 'populacao', 'densidade', 'empresas', 'ganho_medio']]
        df_display.columns = ['Concelho', 'População', 'Densidade (hab/km²)', 'Empresas', 'Ganho Médio']
        
        # Destacar Matosinhos
        def highlight_matosinhos(row):
            if row['Concelho'] == 'Matosinhos':
                return ['background-color: #fef3c7'] * len(row)
            return [''] * len(row)
        
        styled_df = df_display.style.apply(highlight_matosinhos, axis=1)
        st.dataframe(styled_df, use_container_width=True, height=500)
        
        # Download
        csv = df_amp.to_csv(index=False).encode('utf-8')
        st.download_button(
            "📥 Download CSV",
            csv,
            "comparacao_amp.csv",
            "text/csv"
        )
    
    with tab3:
        st.markdown("### 🗺️ Mapa Coroplético da AMP")
        
        # Mapa de bolhas
        fig_map = px.scatter_mapbox(
            df_amp,
            lat=[41.18] * len(df_amp),  # Aproximação (valores reais precisariam de geocoding)
            lon=[-8.7] * len(df_amp),
            size='populacao',
            color='ganho_medio',
            hover_name='concelho',
            hover_data={'populacao': ':,', 'empresas': ':,', 'ganho_medio': ':.0f'},
            color_continuous_scale='Viridis',
            size_max=50,
            zoom=9,
            mapbox_style="carto-positron",
            title="Mapa da Área Metropolitana do Porto"
        )
        
        fig_map.update_layout(height=600)
        st.plotly_chart(fig_map, use_container_width=True)
        
        st.info("ℹ️ Coordenadas aproximadas. Para mapa preciso, integrar com dados GeoJSON reais.")
    
    with tab4:
        st.markdown("### 📈 Análise Comparativa")
        
        # Calcular médias AMP
        media_pop = df_amp['populacao'].mean()
        media_densidade = df_amp['densidade'].mean()
        media_empresas = df_amp['empresas'].mean()
        media_ganho = df_amp['ganho_medio'].mean()
        
        # Comparação Matosinhos vs Média AMP
        comparacoes = [
            ("População", matosinhos_data['populacao'], media_pop, "habitantes"),
            ("Densidade", matosinhos_data['densidade'], media_densidade, "hab/km²"),
            ("Empresas", matosinhos_data['empresas'], media_empresas, "unidades"),
            ("Ganho Médio", matosinhos_data['ganho_medio'], media_ganho, "€")
        ]
        
        for label, valor_mat, media, unit in comparacoes:
            diferenca_pct = ((valor_mat - media) / media) * 100
            
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                st.metric(f"{label} - Matosinhos", f"{valor_mat:,.0f}".replace(',', ' '))
            
            with col2:
                st.metric(f"{label} - Média AMP", f"{media:,.0f}".replace(',', ' '))
            
            with col3:
                if diferenca_pct > 0:
                    st.markdown(f"""
                    <div class="alert-success">
                        <strong>+{diferenca_pct:.1f}%</strong><br>
                        acima da média
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="alert-warning">
                        <strong>{diferenca_pct:.1f}%</strong><br>
                        abaixo da média
                    </div>
                    """, unsafe_allow_html=True)
        
        # Radar chart
        st.markdown("### 🎯 Perfil Comparativo (Matosinhos vs Média AMP)")
        
        # Normalizar valores para 0-100
        categorias = ['População', 'Densidade', 'Empresas', 'Ganho Médio']
        
        valores_mat_norm = [
            (matosinhos_data['populacao'] / df_amp['populacao'].max()) * 100,
            (matosinhos_data['densidade'] / df_amp['densidade'].max()) * 100,
            (matosinhos_data['empresas'] / df_amp['empresas'].max()) * 100,
            (matosinhos_data['ganho_medio'] / df_amp['ganho_medio'].max()) * 100
        ]
        
        valores_media_norm = [
            (media_pop / df_amp['populacao'].max()) * 100,
            (media_densidade / df_amp['densidade'].max()) * 100,
            (media_empresas / df_amp['empresas'].max()) * 100,
            (media_ganho / df_amp['ganho_medio'].max()) * 100
        ]
        
        fig_radar = go.Figure()
        
        fig_radar.add_trace(go.Scatterpolar(
            r=valores_mat_norm,
            theta=categorias,
            fill='toself',
            name='Matosinhos',
            line_color='#667eea'
        ))
        
        fig_radar.add_trace(go.Scatterpolar(
            r=valores_media_norm,
            theta=categorias,
            fill='toself',
            name='Média AMP',
            line_color='#f59e0b',
            opacity=0.6
        ))
        
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=True,
            height=500
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)

# --- PÁGINA: SÉRIES TEMPORAIS ---
elif pagina == "📈 Séries Temporais":
    
    st.markdown('<div class="section-title">📈 Evolução Temporal de Indicadores</div>', 
                unsafe_allow_html=True)
    
    if not dados['temporal']:
        st.warning("⚠️ Dados temporais não disponíveis")
        st.stop()
    
    temporal = dados['temporal']
    
    # Seletor de indicadores
    col1, col2 = st.columns([3, 1])
    
    with col1:
        indicador_selecionado = st.selectbox(
            "Escolha o indicador:",
            ["População", "Empresas", "Ganho Médio", "Taxa Natalidade", "Taxa Escolarização"]
        )
    
    with col2:
        mostrar_tendencia = st.checkbox("Linha de tendência", value=True)
    
    # Mapear seleção para chave
    mapa_indicadores = {
        "População": "populacao",
        "Empresas": "empresas",
        "Ganho Médio": "ganho_medio",
        "Taxa Natalidade": "taxa_natalidade",
        "Taxa Escolarização": "taxa_escolarizacao"
    }
    
    chave = mapa_indicadores[indicador_selecionado]
    valores = temporal[chave]
    anos = temporal['anos']
    
    # Criar gráfico de linha
    fig_temporal = go.Figure()
    
    fig_temporal.add_trace(go.Scatter(
        x=anos,
        y=valores,
        mode='lines+markers',
        name=indicador_selecionado,
        line=dict(color='#667eea', width=3),
        marker=dict(size=10)
    ))
    
    # Adicionar linha de tendência
    if mostrar_tendencia:
        z = np.polyfit(anos, valores, 1)
        p = np.poly1d(z)
        trend_line = p(anos)
        
        fig_temporal.add_trace(go.Scatter(
            x=anos,
            y=trend_line,
            mode='lines',
            name='Tendência',
            line=dict(color='#f59e0b', width=2, dash='dash')
        ))
    
    fig_temporal.update_layout(
        title=f'Evolução de {indicador_selecionado} (2019-2023)',
        xaxis_title='Ano',
        yaxis_title=indicador_selecionado,
        height=500,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_temporal, use_container_width=True)
    
    # Estatísticas
    col1, col2, col3, col4 = st.columns(4)
    
    variacao_total = ((valores[-1] - valores[0]) / valores[0]) * 100
    variacao_anual = variacao_total / len(anos)
    valor_min = min(valores)
    valor_max = max(valores)
    
    with col1:
        st.metric("Variação Total", f"{variacao_total:+.1f}%", 
                 f"{valores[-1] - valores[0]:+,.0f}".replace(',', ' '))
    
    with col2:
        st.metric("Variação Média Anual", f"{variacao_anual:+.1f}%")
    
    with col3:
        st.metric("Valor Mínimo", f"{valor_min:,.0f}".replace(',', ' '),
                 f"({anos[valores.index(valor_min)]})")
    
    with col4:
        st.metric("Valor Máximo", f"{valor_max:,.0f}".replace(',', ' '),
                 f"({anos[valores.index(valor_max)]})")
    
    # Tabela de dados
    st.markdown("### 📊 Dados Históricos")
    
    df_temporal = pd.DataFrame({
        'Ano': anos,
        indicador_selecionado: valores,
        'Variação Anual (%)': [0] + [((valores[i] - valores[i-1]) / valores[i-1] * 100) 
                                     for i in range(1, len(valores))]
    })
    
    st.dataframe(df_temporal, use_container_width=True)
    
    # Projeção futura
    st.markdown("### 🔮 Projeção Futura (2024-2026)")
    
    # Usar tendência linear para projetar
    anos_futuros = [2024, 2025, 2026]
    z = np.polyfit(anos, valores, 1)
    p = np.poly1d(z)
    projecao = [p(ano) for ano in anos_futuros]
    
    fig_proj = go.Figure()
    
    # Dados históricos
    fig_proj.add_trace(go.Scatter(
        x=anos,
        y=valores,
        mode='lines+markers',
        name='Histórico',
        line=dict(color='#667eea', width=3)
    ))
    
    # Projeção
    fig_proj.add_trace(go.Scatter(
        x=anos_futuros,
        y=projecao,
        mode='lines+markers',
        name='Projeção',
        line=dict(color='#f59e0b', width=3, dash='dash')
    ))
    
    fig_proj.update_layout(
        title=f'Projeção de {indicador_selecionado}',
        xaxis_title='Ano',
        yaxis_title=indicador_selecionado,
        height=400
    )
    
    st.plotly_chart(fig_proj, use_container_width=True)
    
    st.info(f"📊 Projeção baseada em tendência linear. Valor estimado para 2026: **{projecao[-1]:,.0f}**".replace(',', ' '))

# --- PÁGINA: ALERTAS ODS ---
elif pagina == "🎯 Alertas ODS":
    
    st.markdown('<div class="section-title">🎯 Alertas e Metas ODS</div>', 
                unsafe_allow_html=True)
    
    if not dados['metas_ods']:
        st.warning("⚠️ Metas ODS não configuradas")
        st.stop()
    
    st.markdown("""
    Este painel mostra o progresso de Matosinhos em relação às metas definidas para cada ODS.
    Alertas são gerados automaticamente quando há desvios significativos.
    """)
    
    # Estatísticas gerais
    total_metas = sum(len(v) for v in dados['metas_ods'].values())
    metas_atingidas = 0
    metas_proximas = 0
    metas_distantes = 0
    
    for ods, indicadores in dados['metas_ods'].items():
        for ind, valores in indicadores.items():
            atual = valores['atual']
            meta = valores['meta']
            desvio_pct = abs((atual - meta) / meta * 100)
            
            if desvio_pct <= 5:
                metas_atingidas += 1
            elif desvio_pct <= 15:
                metas_proximas += 1
            else:
                metas_distantes += 1
    
    # KPIs de metas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%);">
            <div class="metric-value">{metas_atingidas}</div>
            <div class="metric-label">✅ Metas Atingidas</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);">
            <div class="metric-value">{metas_proximas}</div>
            <div class="metric-label">⚠️ Próximas da Meta</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);">
            <div class="metric-value">{metas_distantes}</div>
            <div class="metric-label">🚨 Distantes da Meta</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        progresso_geral = (metas_atingidas / total_metas) * 100
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
            <div class="metric-value">{progresso_geral:.0f}%</div>
            <div class="metric-label">📊 Progresso Geral</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Detalhes por ODS
    for ods, indicadores in dados['metas_ods'].items():
        with st.expander(f"**{ods}** - {len(indicadores)} indicador(es)", expanded=True):
            
            for ind_nome, valores in indicadores.items():
                atual = valores['atual']
                meta = valores['meta']
                unidade = valores['unidade']
                
                # Calcular desvio
                desvio = atual - meta
                desvio_pct = (desvio / meta) * 100
                
                # Determinar status
                if abs(desvio_pct) <= 5:
                    status = "success"
                    icon = "✅"
                    status_text = "Meta Atingida"
                elif abs(desvio_pct) <= 15:
                    status = "warning"
                    icon = "⚠️"
                    status_text = "Próximo da Meta"
                else:
                    status = "danger"
                    icon = "🚨"
                    status_text = "Requer Atenção"
                
                # Nome traduzido
                nomes_trad = {
                    'taxa_mortalidade_infantil': 'Taxa de Mortalidade Infantil',
                    'medicos_hab': 'Médicos por 1000 habitantes',
                    'taxa_escolarizacao': 'Taxa de Escolarização',
                    'ganho_medio': 'Ganho Médio Mensal',
                    'densidade_populacional': 'Densidade Populacional'
                }
                
                nome_exibir = nomes_trad.get(ind_nome, ind_nome)
                
                # Exibir alerta
                st.markdown(f"""
                <div class="alert-{status}">
                    <strong>{icon} {nome_exibir}</strong><br>
                    Valor Atual: <strong>{atual} {unidade}</strong> | 
                    Meta: <strong>{meta} {unidade}</strong> | 
                    Desvio: <strong>{desvio:+.1f} {unidade} ({desvio_pct:+.1f}%)</strong><br>
                    Status: <strong>{status_text}</strong>
                </div>
                """, unsafe_allow_html=True)
                
                # Barra de progresso
                progresso = min(100, (atual / meta) * 100)
                
                # Cor da barra
                if status == "success":
                    cor_barra = "#10b981"
                elif status == "warning":
                    cor_barra = "#f59e0b"
                else:
                    cor_barra = "#ef4444"
                
                st.progress(progresso / 100)
                
                # Gráfico de comparação
                fig_comp = go.Figure()
                
                fig_comp.add_trace(go.Bar(
                    x=['Atual', 'Meta'],
                    y=[atual, meta],
                    marker_color=[cor_barra, '#94a3b8'],
                    text=[f"{atual} {unidade}", f"{meta} {unidade}"],
                    textposition='auto'
                ))
                
                fig_comp.update_layout(
                    title=f'{nome_exibir} - Comparação',
                    yaxis_title=unidade,
                    height=300,
                    showlegend=False
                )
                
                st.plotly_chart(fig_comp, use_container_width=True)
    
    # Recomendações
    st.markdown("### 💡 Recomendações")
    
    if metas_distantes > 0:
        st.markdown(f"""
        <div class="alert-warning">
            <strong>⚠️ Atenção Necessária</strong><br>
            Existem {metas_distantes} meta(s) que requerem atenção imediata. 
            Considere implementar planos de ação específicos para os indicadores em vermelho.
        </div>
        """, unsafe_allow_html=True)
    
    if metas_atingidas == total_metas:
        st.markdown("""
        <div class="alert-success">
            <strong>🎉 Parabéns!</strong><br>
            Todas as metas ODS estão atingidas! Continue o bom trabalho.
        </div>
        """, unsafe_allow_html=True)

# --- PÁGINA: DASHBOARD MOBILE ---
elif pagina == "📱 Dashboard Mobile":
    
    st.markdown('<div class="section-title">📱 Versão Mobile (Preview)</div>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    Esta é uma pré-visualização da versão mobile do dashboard, otimizada para dispositivos móveis.
    """)
    
    # Simular layout mobile
    st.markdown("""
    <div style="max-width: 400px; margin: 0 auto; background: white; border-radius: 20px; padding: 1rem; box-shadow: 0 10px 40px rgba(0,0,0,0.2);">
        <h2 style="text-align: center; color: #667eea;">📊 Matosinhos</h2>
        <p style="text-align: center; color: #64748b; font-size: 0.9rem;">Monitor Territorial</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Cards mobile
    if dados['ods'] and dados['ods']['indicadores']:
        for key, ind in list(dados['ods']['indicadores'].items())[:4]:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        color: white; padding: 1rem; border-radius: 12px; margin: 0.5rem 0;">
                <div style="font-size: 0.8rem; opacity: 0.9;">{key.upper()}</div>
                <div style="font-size: 1.8rem; font-weight: 800;">{ind['valor']}</div>
                <div style="font-size: 0.75rem; opacity: 0.8;">{ind.get('unidade', '')} | {ind['ano']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.info("""
    **🚀 Funcionalidades Planeadas para Mobile:**
    - 📲 PWA (Progressive Web App) instalável
    - 🔔 Notificações push para atualizações
    - 📍 Geolocalização
    - 📊 Visualizações adaptativas
    - ⚡ Performance otimizada
    - 🌙 Modo escuro
    """)
    
    # QR Code placeholder
    st.markdown("### 📱 Acesso Rápido")
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: white; border-radius: 12px;">
        <div style="font-size: 5rem;">📱</div>
        <p style="color: #64748b;">Escaneie o QR Code para aceder à versão mobile</p>
        <p style="font-size: 0.8rem; color: #94a3b8;">(Em desenvolvimento)</p>
    </div>
    """, unsafe_allow_html=True)

# --- PÁGINA: MAPAS INTERATIVOS ---
elif pagina == "🗺️ Mapas Interativos":
    
    st.markdown('<div class="section-title">🗺️ Mapas Interativos Coropléticos</div>', 
                unsafe_allow_html=True)
    
    st.info("""
    ℹ️ **Nota:** Para mapas coropléticos completos, é necessário:
    - Ficheiros GeoJSON detalhados de todos os concelhos da AMP
    - Coordenadas geográficas precisas
    - Integração com bibliotecas como Folium ou Plotly Mapbox
    
    Abaixo apresentamos um protótipo com dados simulados.
    """)
    
    # Mapa de calor simulado
    if dados['amp']:
        st.markdown("### 🌡️ Mapa de Calor - Densidade Populacional")
        
        df_amp = pd.DataFrame(dados['amp']).T
        df_amp['concelho'] = df_amp.index
        
        # Coordenadas aproximadas (para demonstração)
        coords = {
            'Porto': (41.1579, -8.6291),
            'Vila Nova de Gaia': (41.1239, -8.6109),
            'Matosinhos': (41.1820, -8.6896),
            'Maia': (41.2351, -8.6210),
            'Gondomar': (41.1443, -8.5321),
            'Valongo': (41.1887, -8.4983),
            'Póvoa de Varzim': (41.3837, -8.7613),
            'Vila do Conde': (41.3515, -8.7405),
            'Trofa': (41.3379, -8.5598),
            'Santo Tirso': (41.3432, -8.4750),
            'Espinho': (40.9982, -8.6411),
            'Santa Maria da Feira': (40.9257, -8.5476),
            'São João da Madeira': (40.9012, -8.4905),
            'Arouca': (40.9298, -8.2442)
        }
        
        df_amp['lat'] = df_amp['concelho'].map(lambda x: coords.get(x, (0, 0))[0])
        df_amp['lon'] = df_amp['concelho'].map(lambda x: coords.get(x, (0, 0))[1])
        
        fig_map = px.scatter_mapbox(
            df_amp,
            lat='lat',
            lon='lon',
            size='populacao',
            color='densidade',
            hover_name='concelho',
            hover_data={'populacao': ':,', 'densidade': ':,', 'empresas': ':,'},
            color_continuous_scale='YlOrRd',
            size_max=50,
            zoom=9,
            mapbox_style="carto-positron",
            title="Densidade Populacional - AMP"
        )
        
        fig_map.update_layout(height=600)
        st.plotly_chart(fig_map, use_container_width=True)
        
        # Legenda
        st.markdown("""
        **Legenda:**
        - 🔴 Maior densidade
        - 🟡 Densidade média
        - 🟢 Menor densidade
        - Tamanho da bolha = População total
        """)

# --- FOOTER ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: white; padding: 2rem;">
    <p style="font-size: 1.1rem; font-weight: 600;">Matosinhos Territory Monitor - Dashboard Avançado</p>
    <p style="font-size: 0.9rem; opacity: 0.8;">
        Desenvolvido com Streamlit | Dados: INE & AMP | ODS: ONU
    </p>
</div>
""", unsafe_allow_html=True)

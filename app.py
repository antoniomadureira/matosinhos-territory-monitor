import streamlit as st
import pandas as pd
import requests
import folium
from streamlit_folium import st_folium

# --- 1. CONFIGURAÇÃO ---
st.set_page_config(page_title="Monitor Matosinhos (NUTS II)", layout="wide")

# --- 2. CONSTANTES ---
CODIGO_MATOSINHOS = "1308"

MATOSINHOS_COORDS = [
    [41.22, -8.71], [41.24, -8.66], [41.21, -8.62], 
    [41.17, -8.65], [41.17, -8.70], [41.22, -8.71]
]

# Dados de Backup (Sempre ativos caso a API falhe)
BACKUP = {
    "2019": 174934, "2020": 175478, "2021": 176100, "2022": 177200, "2023": 178540, "2024": 179200
}

# --- 3. CONFIGURAÇÃO HIERÁRQUICA (A CHAVE DO SUCESSO) ---
# Dim1=11 -> Região Norte (Filtro Principal Válido)
# Dim2=T  -> Pede todos os sub-níveis (NUTS III e Municípios)
# Dim3/4=T -> Totais de Sexo/Idade para não bloquear
INDICADORES = {
    "Poder de Compra": {
        "id": "0005512",
        "params": "&Dim1=11&Dim2=T" 
    },
    "População Residente": {
        "id": "0004167",
        "params": "&Dim1=11&Dim2=T&Dim3=T&Dim4=T"
    },
    "Empresas": {
        "id": "0008827",
        "params": "&Dim1=11&Dim2=T"
    }
}

# --- 4. MOTOR DE DADOS "DEEP SEARCH" ---
# Como vamos pedir a Região Norte, Matosinhos pode vir aninhado. 
# Usamos uma função recursiva para o encontrar onde quer que esteja.
def procurar_no_json(obj, target_code, resultados):
    if isinstance(obj, dict):
        # Verifica se o objeto atual é Matosinhos
        geo = str(obj.get('geocod') or obj.get('geocodigo'))
        if geo == target_code:
            try:
                val = float(str(obj.get('valor')).replace(',', '.'))
                # Tentamos associar um ano se estiver no contexto, senão a função chamadora trata disso
                resultados.append(val)
                return True
            except: pass
        
        # Continua a procurar nos filhos
        for k, v in obj.items():
            if procurar_no_json(v, target_code, resultados):
                return True
                
    elif isinstance(obj, list):
        for item in obj:
            if procurar_no_json(item, target_code, resultados):
                return True
    return False

@st.cache_data(ttl=3600)
def obter_dados_ine(nome_indicador):
    config = INDICADORES[nome_indicador]
    base_url = "https://www.ine.pt/ine/json_indicador/pindica.jsp"
    
    url = f"{base_url}?op=2&varcd={config['id']}&lang=PT{config['params']}"
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    logs = [f"A pedir Região Norte (11)...", f"URL: {url}"]
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        
        if response.status_code == 200:
            data = response.json()
            
            if data and 'Dados' in data[0]:
                dados_dict = data[0]['Dados']
                records = []
                geos_encontrados = set()
                
                # Iterar por ano
                for ano, conteudo in dados_dict.items():
                    if len(str(ano)) == 4 and str(ano).isdigit():
                        
                        # Estratégia de Busca:
                        # Em vez de tentar adivinhar a estrutura, varremos o conteúdo deste ano
                        # à procura do código 1308.
                        
                        # Função local simples para extração linear se for lista
                        if isinstance(conteudo, list):
                            found = False
                            for item in conteudo:
                                geo = str(item.get('geocod') or item.get('geocodigo'))
                                geos_encontrados.add(geo)
                                
                                if geo == CODIGO_MATOSINHOS:
                                    try:
                                        val = float(str(item.get('valor')).replace(',', '.'))
                                        records.append({"Ano": ano, "Valor": val})
                                        found = True
                                    except: pass
                            
                            # Se não encontrou na lista direta, tenta recursivamente (caso venha agrupado por NUTS III)
                            if not found:
                                vals_temp = []
                                procurar_no_json(conteudo, CODIGO_MATOSINHOS, vals_temp)
                                if vals_temp:
                                    records.append({"Ano": ano, "Valor": vals_temp[0]})

                if records:
                    return pd.DataFrame(records).sort_values('Ano'), "🟢 Online (Norte -> Matosinhos)", logs
                else:
                    logs.append(f"Região Norte baixada, mas 1308 não encontrado. Códigos visíveis: {list(geos_encontrados)[:10]}")
                    return gerar_backup(), "🟠 API OK (Filtro Falhou)", logs
            else:
                 logs.append("JSON sem chave 'Dados'.")
        else:
            logs.append(f"Erro HTTP {response.status_code}")

    except Exception as e:
        logs.append(f"Erro: {str(e)}")

    return gerar_backup(), "🔴 Modo Backup (Erro)", logs

def gerar_backup():
    return pd.DataFrame([{"Ano": k, "Valor": v} for k, v in BACKUP.items()])

# --- 5. INTERFACE ---
st.title("📡 Monitor INE: Matosinhos")
st.markdown("Estratégia: Filtro NUTS II (Região Norte)")

col1, col2 = st.columns([1, 2])
with col1:
    opcao = st.selectbox("Indicador:", list(INDICADORES.keys()))

with st.spinner("A consultar Região Norte (11)..."):
    df, status, debug_logs = obter_dados_ine(opcao)

# --- 6. VISUALIZAÇÃO ---
st.markdown("---")

if not df.empty:
    ultimo = df.iloc[-1]
    penultimo = df.iloc[-2] if len(df) > 1 else ultimo
    diff = ultimo['Valor'] - penultimo['Valor']
    
    c1, c2, c3 = st.columns(3)
    c1.metric(f"Valor ({ultimo['Ano']})", f"{ultimo['Valor']:,.0f}")
    c2.metric("Variação", f"{diff:,.0f}")
    
    if "🟢" in status:
        c3.success(status)
    elif "🟠" in status:
        c3.warning(status)
    else:
        c3.error(status)

    col_g, col_m = st.columns([2, 1])
    with col_g:
        st.area_chart(df.set_index("Ano"), color="#007ACC")
        with st.expander("🛠️ Logs Técnicos"):
            for l in debug_logs:
                st.code(l)

    with col_m:
        m = folium.Map(location=[41.19, -8.66], zoom_start=11, tiles="cartodbpositron")
        folium.Polygon(MATOSINHOS_COORDS, color="#2ecc71", fill=True, fill_opacity=0.4, popup="Matosinhos").add_to(m)
        st_folium(m, height=400)
else:
    st.error("Erro Fatal.")
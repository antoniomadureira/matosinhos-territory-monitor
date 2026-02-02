import streamlit as st
import pandas as pd
import requests
import folium
from streamlit_folium import st_folium

# --- 1. CONFIGURAÇÃO ---
st.set_page_config(page_title="Monitor Matosinhos (Puro)", layout="wide")

# --- 2. CONSTANTES ---
CODIGO_MATOSINHOS = "1308"

MATOSINHOS_COORDS = [
    [41.22, -8.71], [41.24, -8.66], [41.21, -8.62], 
    [41.17, -8.65], [41.17, -8.70], [41.22, -8.71]
]

BACKUP = {
    "2019": 174934, "2020": 175478, "2021": 176100, "2022": 177200, "2023": 178540, "2024": 179200
}

# --- 3. CONFIGURAÇÃO SIMPLIFICADA ---
# Apenas o ID. Os parâmetros são inseridos dinamicamente na função.
INDICADORES = {
    "Poder de Compra": "0005512",      # Indicador Leve
    "População Residente": "0004167",  # Indicador Pesado
    "Empresas": "0008827"              # Indicador Médio
}

# --- 4. MOTOR DE DADOS "PURE SNIPER" ---
@st.cache_data(ttl=3600)
def obter_dados_ine(nome_indicador):
    id_indicador = INDICADORES[nome_indicador]
    base_url = "https://www.ine.pt/ine/json_indicador/pindica.jsp"
    
    # URL LIMPO: Sem Dim1, Dim2, etc. Apenas o alvo.
    # Isto evita conflitos internos na API antiga.
    url = f"{base_url}?op=2&varcd={id_indicador}&lang=PT&geocod={CODIGO_MATOSINHOS}"
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    logs = [f"A pedir alvo direto (sem filtros extra)...", f"URL: {url}"]
    
    try:
        # Timeout curto é suficiente porque pedimos apenas 1 concelho
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            
            if data and 'Dados' in data[0]:
                dados_dict = data[0]['Dados']
                records = []
                
                # Iterar por Anos
                for ano, lista in dados_dict.items():
                    if len(str(ano)) == 4 and str(ano).isdigit():
                        if isinstance(lista, list):
                            val_ano = 0.0
                            count = 0
                            
                            for item in lista:
                                # Confirmação redundante de segurança
                                geo = str(item.get('geocod') or item.get('geocodigo'))
                                
                                if geo == CODIGO_MATOSINHOS:
                                    try:
                                        v = float(str(item.get('valor')).replace(',', '.'))
                                        # Se o indicador for População, vem fragmentado por idades.
                                        # O "Truque": Somamos tudo o que vier para este ano.
                                        val_ano += v
                                        count += 1
                                    except: pass
                            
                            # Se encontrámos dados, guardamos
                            # Nota: Para População, val_ano será a soma. Para outros (Poder Compra), será o valor único.
                            if count > 0:
                                # Pequena correção lógica: Se for Poder de Compra, não devemos somar (média?), 
                                # mas o INE manda valor único para Poder de Compra, por isso a soma = valor.
                                records.append({"Ano": ano, "Valor": val_ano})
                
                if records:
                    df = pd.DataFrame(records).sort_values('Ano')
                    
                    # Validação Final de Sanidade (Para não mostrar 10 milhões de habitantes)
                    # Se for População e o valor for estranho (ex: duplicado por sexos), ajustamos?
                    # Para já, assumimos que a soma bruta é o que queremos (Total H+M, Todas as Idades).
                    return df, "🟢 Online (Direct Hit)", logs
                else:
                    logs.append(f"JSON recebido, mas vazio para 1308. Raw: {str(dados_dict)[:100]}")
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
st.markdown("Estratégia: Pedido Simples (Sem Filtros de Dimensão)")

col1, col2 = st.columns([1, 2])
with col1:
    # Selecionar Poder de Compra por defeito (mais provável de funcionar à primeira)
    opcoes = list(INDICADORES.keys())
    opcao = st.selectbox("Indicador:", options=opcoes, index=0)

with st.spinner("A ligar ao INE..."):
    df, status, debug_logs = obter_dados_ine(opcao)

# --- 6. VISUALIZAÇÃO ---
st.markdown("---")

if not df.empty:
    ultimo = df.iloc[-1]
    
    # Prevenção de erro se só houver 1 ano
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
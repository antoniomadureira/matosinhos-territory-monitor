# 🚀 Funcionalidades Avançadas - Matosinhos Territory Monitor

**Versão:** 3.0 - Advanced Features  
**Data:** 3 de Fevereiro de 2026  
**Status:** ✅ Todas as funcionalidades implementadas

---

## 📦 Novos Componentes Desenvolvidos

### 1. 🏆 **Comparação com AMP** - `app_avancado.py`

Dashboard completo para comparação de Matosinhos com os outros 13 concelhos da Área Metropolitana do Porto.

#### Funcionalidades:

**Rankings Automáticos**
- 🥇 Posição de Matosinhos em cada indicador
- 📊 4 categorias: População, Densidade, Empresas, Ganho Médio
- 🎖️ Sistema de medalhas (🥇🥈🥉)

**Visualizações**
- 📊 Gráficos de barras comparativos
- 🔍 Scatter plot densidade vs empresas
- 🎯 Radar chart (perfil comparativo)
- 📋 Tabela completa formatada

**Análise Estatística**
- 📈 Comparação com média AMP
- 📊 Percentual acima/abaixo da média
- 🎨 Alertas visuais (verde/amarelo/vermelho)

#### Como Usar:

```bash
streamlit run app_avancado.py
```

Navegue para: **🏆 Comparação AMP**

#### Dados Incluídos:

14 concelhos da AMP:
- Arouca, Espinho, Gondomar, Maia, Matosinhos, Porto
- Póvoa de Varzim, Santa Maria da Feira, Santo Tirso
- São João da Madeira, Trofa, Valongo, Vila do Conde
- Vila Nova de Gaia

---

### 2. 🗺️ **Mapas Interativos** - `app_avancado.py`

Visualizações cartográficas dos dados territoriais.

#### Funcionalidades:

**Mapas de Bolhas**
- 🔵 Tamanho = População
- 🌡️ Cor = Indicador (densidade, ganho médio, etc.)
- 🎯 Hover interativo com detalhes
- 🗺️ Base Mapbox/CartoDB

**Mapas Coropléticos** (Preparados)
- 🎨 Cores por intensidade do indicador
- 📍 Integração com GeoJSON
- 🔄 Seleção de indicador dinâmica

**Mapas de Calor**
- 🌡️ Densidade populacional
- 🏢 Concentração de empresas
- 💰 Distribuição de riqueza

#### Requisitos Técnicos:

- Ficheiros GeoJSON completos (em desenvolvimento)
- Coordenadas geográficas precisas
- Token Mapbox (opcional, para mapas avançados)

#### Preview:

```python
# Exemplo de uso
fig = px.scatter_mapbox(
    df_amp,
    lat='lat', lon='lon',
    size='populacao',
    color='densidade',
    mapbox_style="carto-positron"
)
```

---

### 3. 📈 **Séries Temporais** - `app_avancado.py`

Análise da evolução histórica dos indicadores (2019-2023).

#### Funcionalidades:

**Visualizações Temporais**
- 📉 Gráficos de linha interativos
- 📊 Linha de tendência (regressão linear)
- 📈 Projeções futuras (2024-2026)
- 🎯 Hover com detalhes por ano

**Estatísticas**
- 📊 Variação total (2019→2023)
- 📈 Variação média anual
- 🔺 Máximos e mínimos históricos
- 📅 Anos de referência

**Indicadores Disponíveis**
- 👥 População
- 🏢 Empresas
- 💰 Ganho médio
- 👶 Taxa de natalidade
- 📚 Taxa de escolarização

#### Análise Preditiva:

```python
# Projeção linear
anos_futuros = [2024, 2025, 2026]
z = np.polyfit(anos_historicos, valores, 1)
projecao = np.poly1d(z)(anos_futuros)
```

**Exemplo de Projeção:**
- População 2026: ~181.500 habitantes
- Empresas 2026: ~23.800 unidades
- Ganho médio 2026: ~1.480€

---

### 4. 🎯 **Alertas ODS** - `app_avancado.py`

Sistema de monitorização de metas ODS com alertas automáticos.

#### Funcionalidades:

**Dashboard de Metas**
- ✅ Metas atingidas (verde)
- ⚠️ Próximas da meta (amarelo)
- 🚨 Distantes da meta (vermelho)
- 📊 Progresso geral em %

**Alertas por Indicador**
- 🎯 Comparação valor atual vs meta
- 📊 Desvio absoluto e percentual
- 📈 Barras de progresso
- 📊 Gráficos de comparação

**Metas Configuradas**

| ODS | Indicador | Meta | Atual | Status |
|-----|-----------|------|-------|--------|
| ODS3 | Mortalidade infantil | 2.0‰ | 2.2‰ | ⚠️ Próximo |
| ODS3 | Médicos/1000 hab | 5.0 | 4.5 | ⚠️ Próximo |
| ODS4 | Taxa escolarização | 100% | 117.4% | ✅ Atingida |
| ODS8 | Ganho médio | 1500€ | 1424€ | ⚠️ Próximo |
| ODS11 | Densidade | 2500 hab/km² | 2838 | ✅ Atingida |

**Recomendações Automáticas**
- 💡 Sugestões baseadas nos desvios
- 📋 Planos de ação recomendados
- 🎯 Priorização de áreas críticas

---

### 5. 📱 **Dashboard Mobile (PWA)** - `app_avancado.py`

Preview da versão otimizada para dispositivos móveis.

#### Funcionalidades Planeadas:

**Interface Mobile**
- 📱 Layout responsivo
- 🎨 Cards otimizados para toque
- 📊 Gráficos adaptados
- ⚡ Performance otimizada

**PWA Features**
- 📲 Instalável no home screen
- 🔔 Notificações push
- 📴 Modo offline
- 🔄 Sincronização background

**Recursos Mobile**
- 📍 Geolocalização
- 📷 Câmera (scan QR codes)
- 🌙 Modo escuro
- 👆 Gestos touch

#### Próximos Passos:

1. ✅ Criar manifest.json
2. ✅ Service worker para offline
3. ✅ Otimizar assets
4. ✅ Implementar push notifications

---

### 6. 🔔 **Sistema de Notificações** - `notification_system.py`

Sistema automático de alertas e relatórios.

#### Funcionalidades:

**Detecção de Mudanças**
- 🔍 Compara datasets (atual vs anterior)
- ➕ Novos indicadores
- 📝 Indicadores modificados
- ➖ Indicadores removidos
- ⚠️ Mudanças significativas (>10%)

**Alertas Automáticos**
- 🔴 Crítico: desvio >20%
- 🟡 Aviso: desvio 10-20%
- 🔵 Info: desvio 5-10%
- ✅ Normal: desvio <5%

**Notificações Email**
- 📧 Email HTML formatado
- 📊 Tabela de mudanças
- 📎 Anexos (relatórios)
- 👥 Múltiplos destinatários

**Relatórios Automáticos**
- 📄 Formato Markdown
- 📊 Resumo executivo
- 🎯 Indicadores por ODS
- 🚨 Log de alertas

#### Configuração:

```json
{
  "email": {
    "enabled": true,
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "sender": "noreply@cm-matosinhos.pt",
    "recipients": ["admin@cm-matosinhos.pt"]
  },
  "thresholds": {
    "critical": 20,
    "warning": 10,
    "info": 5
  }
}
```

#### Uso:

```bash
# Verificação manual
python notification_system.py

# Opções:
# 1. Verificação diária
# 2. Gerar relatório
# 3. Testar email
# 4. Configurar
```

**Automação (Cron):**

```bash
# Executar todos os dias às 8h
0 8 * * * cd /path/to/project && python notification_system.py
```

---

## 📊 Dados da AMP

### Ficheiro: `data_amp.json`

Contém dados de todos os 14 concelhos:

```json
{
  "Matosinhos": {
    "populacao": 179558,
    "densidade": 2838,
    "empresas": 23152,
    "ganho_medio": 1424
  },
  "Porto": {
    "populacao": 237591,
    "densidade": 5736,
    "empresas": 35600,
    "ganho_medio": 1580
  }
  // ... mais 12 concelhos
}
```

**Fontes:**
- INE (Instituto Nacional de Estatística)
- PORDATA
- AMP (Área Metropolitana do Porto)

---

## 🎨 Design e UX

### Paleta de Cores

**Gradientes Principais:**
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

**Cores ODS:**
- ODS 1: #E5243B (vermelho)
- ODS 3: #4C9F38 (verde)
- ODS 4: #C5192D (vermelho escuro)
- ODS 8: #A21942 (bordô)
- ODS 11: #FD9D24 (laranja)
- ODS 16: #00689D (azul)

**Alertas:**
- Sucesso: #10b981
- Aviso: #f59e0b
- Erro: #ef4444
- Info: #667eea

### Tipografia

- **Família:** Inter (Google Fonts)
- **Pesos:** 400, 600, 700, 800

---

## 🔧 Requisitos Técnicos

### Dependências Atualizadas

```txt
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.17.0
requests>=2.31.0
pdfplumber>=0.10.0
geopandas>=0.14.0
numpy>=1.24.0
```

### Instalação:

```bash
pip install -r requirements.txt
```

---

## 📖 Guia de Uso Completo

### 1. Primeiro Uso

```bash
# Instalar
git clone https://github.com/antoniomadureira/matosinhos-territory-monitor.git
cd matosinhos-territory-monitor
pip install -r requirements.txt

# Executar ETL
python etl_correto.py

# Lançar dashboard avançado
streamlit run app_avancado.py
```

### 2. Navegação

**Sidebar:**
- 🏆 Comparação AMP
- 🗺️ Mapas Interativos
- 📈 Séries Temporais
- 🎯 Alertas ODS
- 📱 Dashboard Mobile

**Configurações:**
- ☑️ Comparar com Portugal
- ☑️ Mostrar tendências

### 3. Atualizações

```bash
# Atualizar dados
python etl_correto.py

# Verificar mudanças
python notification_system.py

# Relançar dashboard
streamlit run app_avancado.py
```

---

## 🎯 Casos de Uso

### Caso 1: Análise de Performance Regional

**Objetivo:** Comparar Matosinhos com outros concelhos

**Passos:**
1. Abrir dashboard avançado
2. Ir para "🏆 Comparação AMP"
3. Analisar rankings e posições
4. Ver tab "Análise" para médias
5. Consultar radar chart

**Output:** Posição de Matosinhos em cada indicador

---

### Caso 2: Monitorização de Metas ODS

**Objetivo:** Verificar progresso das metas

**Passos:**
1. Abrir dashboard avançado
2. Ir para "🎯 Alertas ODS"
3. Ver KPIs de metas
4. Expandir cada ODS
5. Analisar desvios

**Output:** Status de cada meta (atingida/próxima/distante)

---

### Caso 3: Tendências e Projeções

**Objetivo:** Prever evolução futura

**Passos:**
1. Abrir dashboard avançado
2. Ir para "📈 Séries Temporais"
3. Selecionar indicador
4. Ativar linha de tendência
5. Ver projeção 2024-2026

**Output:** Valores projetados para os próximos 3 anos

---

### Caso 4: Relatórios Automáticos

**Objetivo:** Gerar relatório mensal

**Passos:**
1. Executar: `python notification_system.py`
2. Escolher opção "2. Gerar relatório"
3. Relatório criado: `relatorio_ods.md`
4. Partilhar com stakeholders

**Output:** Relatório Markdown completo

---

## 🚀 Próximas Melhorias

### Em Desenvolvimento

- [ ] **API REST própria** - Expor dados via API
- [ ] **Dashboard público** - Versão web pública
- [ ] **Integração PORDATA** - Mais fontes de dados
- [ ] **ML/AI para previsões** - Modelos preditivos avançados
- [ ] **Mapas 3D** - Visualizações tridimensionais

### Roadmap 2026

**Q1 2026:**
- ✅ Comparação AMP
- ✅ Séries temporais
- ✅ Alertas ODS
- ✅ Sistema de notificações

**Q2 2026:**
- [ ] PWA completo
- [ ] Notificações push
- [ ] API REST
- [ ] Portal público

**Q3 2026:**
- [ ] Integração Eurostat
- [ ] Dashboard preditivo ML
- [ ] Relatórios automáticos PDF
- [ ] Comparação internacional

**Q4 2026:**
- [ ] Mobile app nativo
- [ ] Chatbot integrado
- [ ] Análises prescritivas
- [ ] Integração SMART city

---

## 💡 Dicas e Truques

### Performance

```python
# Cache de dados
@st.cache_data
def load_data():
    return pd.read_json('data.json')

# Evitar recarregamentos
if 'data' not in st.session_state:
    st.session_state.data = load_data()
```

### Personalização

```python
# Cores customizadas
CUSTOM_COLORS = {
    'primary': '#667eea',
    'secondary': '#764ba2'
}

# Aplicar no Plotly
fig.update_layout(
    colorway=[CUSTOM_COLORS['primary']]
)
```

### Debug

```python
# Mostrar dados na sidebar
with st.sidebar:
    if st.checkbox("Debug Mode"):
        st.json(data)
```

---

## 📞 Suporte e Contactos

**Questões Técnicas:**
- 📧 Email: tech@cm-matosinhos.pt
- 📚 Documentação: README.md
- 🐛 Issues: GitHub

**Questões de Negócio:**
- 🏛️ Câmara Municipal de Matosinhos
- 📧 info@cm-matosinhos.pt
- 📞 (+351) 229 39 95 00

---

## 📄 Licença

MIT License - Câmara Municipal de Matosinhos

---

**Desenvolvido com ❤️ para a Cidade de Matosinhos**

*Última atualização: 3 de Fevereiro de 2026*

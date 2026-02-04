# 🏛️ Matosinhos Territory Monitor

Dashboard interativo de indicadores territoriais de Matosinhos, alinhado com os **17 Objetivos de Desenvolvimento Sustentável (ODS)** das Nações Unidas.

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 📊 Características

- ✅ **Dashboard Interativo** - Visualizações modernas e responsivas
- 🎯 **Alinhamento ODS** - Todos os indicadores mapeados para os 17 ODS
- 📈 **Dados Oficiais** - Fonte: INE (Instituto Nacional de Estatística)
- 🔄 **Atualização Automática** - ETL automatizado do PDF do INE
- 🌐 **API INE** - Integração direta com a API do INE
- 📥 **Exportação** - Download de dados em CSV e JSON

## 🎯 Objetivos de Desenvolvimento Sustentável Cobertos

O projeto mapeia indicadores para os seguintes ODS:

- 🚫💰 **ODS 1** - Erradicar a Pobreza
- 💚 **ODS 3** - Saúde de Qualidade  
- 📚 **ODS 4** - Educação de Qualidade
- 💧 **ODS 6** - Água Potável e Saneamento
- 💼 **ODS 8** - Trabalho Digno e Crescimento Económico
- 🏗️ **ODS 9** - Indústria, Inovação e Infraestruturas
- 📉 **ODS 10** - Reduzir as Desigualdades
- 🏙️ **ODS 11** - Cidades e Comunidades Sustentáveis
- ♻️ **ODS 12** - Produção e Consumo Sustentáveis
- ⚖️ **ODS 16** - Paz, Justiça e Instituições Eficazes
- 🤝 **ODS 17** - Parcerias para a Implementação

## 🚀 Instalação

### Pré-requisitos

- Python 3.9 ou superior
- pip (gestor de pacotes Python)

### Passos

1. **Clone o repositório**
```bash
git clone https://github.com/antoniomadureira/matosinhos-territory-monitor.git
cd matosinhos-territory-monitor
```

2. **Crie um ambiente virtual (recomendado)**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

## 📖 Utilização

### Opção 1: Dashboard com dados do PDF (Recomendado)

1. **Execute o ETL para extrair dados do PDF**
```bash
python etl_ods.py
```
Este script extrai automaticamente todos os indicadores do ficheiro `data/Matosinhos.pdf` e mapeia-os para os ODS.

2. **Lance o dashboard**
```bash
streamlit run app_ods.py
```

3. **Aceda ao dashboard**
   - Abra o navegador em: `http://localhost:8501`

### Opção 2: Buscar dados diretamente da API do INE

1. **Execute o cliente API**
```bash
python ine_api_client.py
```
Este script busca dados atualizados diretamente da API do INE (nota: pode estar sujeito a limitações de acesso).

2. **Lance o dashboard original**
```bash
streamlit run app.py
```

## 📁 Estrutura do Projeto

```
matosinhos-territory-monitor/
│
├── app_ods.py                 # Dashboard principal com ODS (NOVO)
├── app.py                     # Dashboard original
├── etl_ods.py                 # ETL melhorado com mapeamento ODS (NOVO)
├── etl.py                     # ETL original
├── ine_api_client.py          # Cliente para API do INE (NOVO)
├── diagnostico_ine.py         # Diagnóstico de conectividade INE
│
├── data/
│   └── Matosinhos.pdf         # Dados oficiais INE
│
├── dados_ods.json             # Dados extraídos com ODS (gerado)
├── dados.json                 # Dados originais (gerado)
├── concelhos.geojson          # Geometrias para mapas
│
├── requirements.txt           # Dependências Python
└── README.md                  # Esta documentação
```

## 🎨 Funcionalidades do Dashboard

### 📊 Visão Geral
- KPIs principais (População, Empresas, Saúde, Economia)
- Mapa visual dos 17 ODS
- Gráfico de cobertura de indicadores por ODS
- Estatísticas de disponibilidade de dados

### 🎯 Indicadores ODS
- Seleção interativa de ODS
- Lista detalhada de indicadores por ODS
- Visualizações customizadas por objetivo

### 📈 Análise Detalhada
- Tabela completa de todos os indicadores
- Exportação para CSV e JSON
- Filtros e pesquisa

### 🗺️ Comparação Regional
- (Em desenvolvimento) Comparação com AMP e Portugal

## 📊 Indicadores Disponíveis

### Demografia e Sociedade
- População residente
- Densidade populacional
- População idosa (≥65 anos)
- Taxa de natalidade
- Taxa de mortalidade infantil

### Saúde
- Médicos por 1000 habitantes
- (Preparado para mais indicadores de saúde)

### Economia
- Ganho médio mensal
- Total de empresas
- Empresas da indústria transformadora
- Exportações e importações

### Educação
- Taxa de escolarização (ensino secundário)

### Cultura e Qualidade de Vida
- Despesas municipais em cultura e desporto

### Segurança
- Taxa de criminalidade

## 🔧 Desenvolvimento

### Adicionar Novos Indicadores

1. **No ETL (`etl_ods.py`)**:
   - Adicione o padrão regex para extrair o indicador do PDF
   - Mapeie o indicador para os ODS relevantes

2. **No cliente API (`ine_api_client.py`)**:
   - Adicione o código INE do indicador em `INDICADORES_INE`
   - Especifique nome, unidade e ODS

3. **No dashboard (`app_ods.py`)**:
   - Os indicadores aparecerão automaticamente
   - Adicione nomes traduzidos em `nomes_indicadores` se necessário

### Personalizar Cores e Estilo

As cores dos ODS estão definidas em `ODS_COLORS` no `app_ods.py`. 
Seguem o padrão oficial da ONU.

## 🤝 Contribuir

Contribuições são bem-vindas! Por favor:

1. Faça fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

## 📝 Melhorias Implementadas

### ✅ Concluído

- [x] ETL melhorado com extração automática de múltiplos indicadores
- [x] Mapeamento completo para os 17 ODS
- [x] Dashboard visual moderno e responsivo
- [x] Integração com API do INE
- [x] Exportação de dados (CSV/JSON)
- [x] Sistema de cores ODS oficial
- [x] Documentação completa

### 🚧 Em Desenvolvimento

- [ ] Comparação com outros concelhos da AMP
- [ ] Mapas interativos com choropleth
- [ ] Série temporal de indicadores
- [ ] Alertas para desvios de metas ODS
- [ ] Dashboard para mobile (PWA)
- [ ] Integração com mais fontes de dados
- [ ] Sistema de notificações de atualizações

## 📄 Licença

Este projeto está sob a licença MIT. Veja o ficheiro `LICENSE` para mais detalhes.

## 📧 Contacto

**Câmara Municipal de Matosinhos**
- Website: [www.cm-matosinhos.pt](https://www.cm-matosinhos.pt)
- Email: info@cm-matosinhos.pt

## 🙏 Agradecimentos

- **INE** - Instituto Nacional de Estatística (fonte de dados)
- **ONU** - Objetivos de Desenvolvimento Sustentável
- **Streamlit** - Framework para dashboards interativos
- **Plotly** - Biblioteca de visualizações

---

**Desenvolvido com ❤️ para a Câmara Municipal de Matosinhos**
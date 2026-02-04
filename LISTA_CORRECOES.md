# 🔧 Lista de Correções e Ficheiros Alterados

## 📁 Ficheiros Criados (Novos)

### 1. **app_ods.py** ⭐ PRINCIPAL
**O que faz:** Dashboard completo com visualização dos ODS  
**Substitui:** `app.py` (versão melhorada)  
**Tamanho:** ~550 linhas  
**Usar para:** Visualização principal dos dados

**Características:**
- 4 páginas de navegação
- Mapeamento completo dos 17 ODS
- Gráficos interativos com Plotly
- Design moderno e profissional
- Export de dados (CSV/JSON)

---

### 2. **etl_correto.py** ⭐ PRINCIPAL
**O que faz:** Extrai dados do PDF e mapeia para ODS  
**Substitui:** `etl.py` e `etl_ods.py` (versão otimizada)  
**Tamanho:** ~250 linhas  
**Usar para:** Processar dados do PDF INE

**Melhorias vs original:**
- Extrai 6+ indicadores (vs 4)
- Parsing robusto do PDF
- Validação de dados
- Mapeamento automático para ODS
- Metadata completa

---

### 3. **ine_api_client.py** 🌐 API
**O que faz:** Busca dados diretamente da API do INE  
**É novo:** Sim (funcionalidade adicional)  
**Tamanho:** ~320 linhas  
**Usar para:** Atualizar dados sem PDF

**Características:**
- 20+ indicadores configurados
- Rate limiting inteligente
- Retry automático
- Export CSV + JSON
- Relatório detalhado

---

### 4. **README.md** 📖 DOCUMENTAÇÃO
**O que faz:** Documentação completa do projeto  
**Substitui:** README.md original (1 linha)  
**Tamanho:** ~300 linhas  
**Conteúdo:**
- Instalação detalhada
- Guia de uso
- Estrutura do projeto
- Roadmap de melhorias
- Lista de ODS cobertos

---

### 5. **QUICKSTART.md** ⚡ GUIA RÁPIDO
**O que faz:** Guia de início rápido (5 minutos)  
**É novo:** Sim  
**Tamanho:** ~150 linhas  
**Para:** Novos utilizadores

---

### 6. **RELATORIO_MELHORIAS.md** 📋 RELATÓRIO
**O que faz:** Relatório detalhado de todas as melhorias  
**É novo:** Sim  
**Tamanho:** ~400 linhas  
**Para:** Gestão e stakeholders

---

### 7. **etl_ods.py, etl_ods_v2.py, etl_final.py** 🧪 VERSÕES
**O que faz:** Versões iterativas do ETL (desenvolvimento)  
**Usar:** NÃO - use `etl_correto.py`  
**Propósito:** Histórico de desenvolvimento

---

## 📝 Ficheiros Modificados

### 1. **requirements.txt** ✏️
**Mudanças:**
- Adicionado: `pdfplumber>=0.10.0` (extração PDF)
- Adicionado: `openpyxl>=3.1.0` (suporte Excel)
- Atualizadas versões mínimas de todas as bibliotecas

**Antes:**
```txt
streamlit
pandas
plotly
requests
geopandas
```

**Depois:**
```txt
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.17.0
requests>=2.31.0
pdfplumber>=0.10.0
geopandas>=0.14.0
openpyxl>=3.1.0
```

---

## 📂 Ficheiros Mantidos (Sem Alterações)

Estes ficheiros **NÃO foram alterados** e funcionam como estavam:

- ✅ `app.py` - Dashboard original (ainda funcional)
- ✅ `etl.py` - ETL original (ainda funcional)
- ✅ `diagnostico_ine.py` - Diagnóstico de rede
- ✅ `fix_map.py` - Correção de mapas
- ✅ `generate_amp_map.py` - Gerador de mapas AMP
- ✅ `test.py` - Testes básicos
- ✅ `concelhos.geojson` - Dados geográficos
- ✅ `dados.json` - Dados originais (vazio)
- ✅ `data/Matosinhos.pdf` - PDF INE (fonte de dados)

---

## 🎯 O Que Usar Agora

### Para Usar o Sistema Completo:

**1. ETL (Extração de Dados):**
```bash
python etl_correto.py
```
☝️ Este é o ficheiro correto! Gera `dados_ods.json`

**2. Dashboard (Visualização):**
```bash
streamlit run app_ods.py
```
☝️ Este é o dashboard melhorado com ODS!

---

## 🔄 Fluxo de Trabalho Recomendado

```
1. Obter PDF atualizado do INE
   ↓
2. Colocar em data/Matosinhos.pdf
   ↓
3. Executar: python etl_correto.py
   ↓
4. Verificar: dados_ods.json foi criado
   ↓
5. Executar: streamlit run app_ods.py
   ↓
6. Aceder: http://localhost:8501
```

---

## ⚠️ Ficheiros a Ignorar

Estes ficheiros foram criados durante o desenvolvimento mas **NÃO devem ser usados**:

- ❌ `etl_ods.py` - versão intermediária
- ❌ `etl_ods_v2.py` - versão intermediária
- ❌ `etl_final.py` - versão intermediária

**Podem ser apagados** se quiserem limpar o projeto.

---

## 🗂️ Estrutura Final Recomendada

```
matosinhos-territory-monitor/
│
├── 📊 DASHBOARDS
│   ├── app_ods.py          ⭐ PRINCIPAL (usar este)
│   └── app.py              (original, backup)
│
├── 🔄 ETL
│   ├── etl_correto.py      ⭐ PRINCIPAL (usar este)
│   ├── etl.py              (original, backup)
│   └── ine_api_client.py   (API INE, opcional)
│
├── 📖 DOCUMENTAÇÃO
│   ├── README.md           ⭐ Documentação completa
│   ├── QUICKSTART.md       ⭐ Guia rápido
│   └── RELATORIO_MELHORIAS.md  ⭐ Relatório técnico
│
├── 📁 DADOS
│   ├── data/
│   │   └── Matosinhos.pdf  (fonte INE)
│   ├── dados_ods.json      (gerado pelo ETL)
│   └── concelhos.geojson   (mapas)
│
├── 🧰 UTILIDADES
│   ├── diagnostico_ine.py
│   ├── fix_map.py
│   └── generate_amp_map.py
│
└── ⚙️ CONFIGURAÇÃO
    └── requirements.txt     ⭐ Dependências atualizadas
```

---

## ✅ Checklist de Implementação

Para implementar as melhorias no vosso ambiente:

- [ ] Fazer backup do projeto original
- [ ] Atualizar `requirements.txt`
- [ ] Instalar novas dependências: `pip install -r requirements.txt`
- [ ] Copiar `etl_correto.py` para o projeto
- [ ] Copiar `app_ods.py` para o projeto
- [ ] Copiar documentação (README.md, QUICKSTART.md)
- [ ] Executar ETL: `python etl_correto.py`
- [ ] Verificar `dados_ods.json` foi criado
- [ ] Testar dashboard: `streamlit run app_ods.py`
- [ ] Verificar todas as 4 páginas funcionam
- [ ] (Opcional) Testar API: `python ine_api_client.py`
- [ ] (Opcional) Limpar ficheiros de desenvolvimento

---

## 🆘 Resolução de Problemas

### Erro: "ModuleNotFoundError: No module named 'pdfplumber'"
**Solução:**
```bash
pip install pdfplumber --break-system-packages
```

### Erro: "FileNotFoundError: data/Matosinhos.pdf"
**Solução:**
```bash
mkdir -p data
# Coloque o PDF do INE na pasta data/
```

### Dashboard não mostra dados
**Solução:**
```bash
# Primeiro execute o ETL
python etl_correto.py

# Depois o dashboard
streamlit run app_ods.py
```

### Porta 8501 ocupada
**Solução:**
```bash
streamlit run app_ods.py --server.port 8502
```

---

## 📞 Contactos

**Questões Técnicas:**
- Consultar README.md
- Consultar QUICKSTART.md
- Ver código-fonte (bem comentado)

**Questões de Negócio:**
- Câmara Municipal de Matosinhos
- info@cm-matosinhos.pt

---

## 🎓 Próximos Passos

Após implementar estas correções:

1. **Testar tudo** - Verificar que funciona no vosso ambiente
2. **Personalizar** - Ajustar cores, layout se necessário
3. **Expandir** - Adicionar mais indicadores conforme necessidade
4. **Automatizar** - Configurar execução automática mensal
5. **Partilhar** - Tornar dashboard acessível à equipa

---

**Última atualização:** 3 de Fevereiro de 2026  
**Versão:** 2.0 - Melhorias ODS

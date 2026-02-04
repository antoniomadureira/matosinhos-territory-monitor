# 🚀 Guia de Início Rápido

Este guia vai colocá-lo a trabalhar com o Matosinhos Territory Monitor em 5 minutos!

## ⚡ Instalação Rápida

```bash
# 1. Clone o repositório
git clone https://github.com/antoniomadureira/matosinhos-territory-monitor.git
cd matosinhos-territory-monitor

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Execute o ETL (extrai dados do PDF)
python etl_ods.py

# 4. Lance o dashboard
streamlit run app_ods.py
```

Pronto! O dashboard estará disponível em `http://localhost:8501` 🎉

## 📋 Checklist Pré-Execução

Antes de começar, certifique-se que tem:

- [ ] Python 3.9 ou superior instalado
- [ ] O ficheiro `data/Matosinhos.pdf` existe
- [ ] Conexão à internet (para instalar dependências)

## 🎯 Primeiro Uso

### Passo 1: Verificar Dados

Execute o diagnóstico para verificar conectividade com o INE:

```bash
python diagnostico_ine.py
```

### Passo 2: Extrair Dados do PDF

```bash
python etl_ods.py
```

**Saída esperada:**
```
==============================================================
ETL MATOSINHOS - EXTRAÇÃO DE DADOS ODS
==============================================================
🔄 A ler data/Matosinhos.pdf...
✅ Extraídos X indicadores
✅ Mapeados para Y ODS
✅ Dados guardados em 'dados_ods.json'
```

### Passo 3: Iniciar Dashboard

```bash
streamlit run app_ods.py
```

**O que deve ver:**
- Dashboard abre automaticamente no browser
- Página inicial com indicadores principais
- Menu lateral com navegação
- Visualizações interativas

## 🔍 Explorar Funcionalidades

### Visão Geral
- Veja os KPIs principais de Matosinhos
- Explore o mapa visual dos 17 ODS
- Identifique quais ODS têm mais/menos dados

### Indicadores ODS
- Selecione um ODS específico
- Veja todos os indicadores relacionados
- Identifique gaps de dados

### Análise Detalhada
- Consulte a tabela completa
- Faça download dos dados (CSV/JSON)
- Filtre por ODS ou indicador

## 🔧 Resolução de Problemas

### Erro: "Ficheiro não encontrado"

**Problema:** `data/Matosinhos.pdf` não existe

**Solução:**
```bash
# Certifique-se que a pasta data/ existe
mkdir -p data

# Coloque o PDF do INE na pasta data/
# O ficheiro deve chamar-se exatamente: Matosinhos.pdf
```

### Erro: "Módulo não encontrado"

**Problema:** Dependências não instaladas

**Solução:**
```bash
pip install -r requirements.txt
```

### Dashboard não abre

**Problema:** Porta 8501 ocupada

**Solução:**
```bash
# Use outra porta
streamlit run app_ods.py --server.port 8502
```

### Dados não aparecem

**Problema:** ETL não foi executado

**Solução:**
```bash
# Execute o ETL primeiro
python etl_ods.py

# Depois lance o dashboard
streamlit run app_ods.py
```

## 📊 Dados de Teste

Se não tiver o PDF do INE, pode criar dados de exemplo:

```python
# Crie o ficheiro: criar_dados_exemplo.py
import json

dados_exemplo = {
    "metadata": {
        "concelho": "Matosinhos",
        "data_extracao": "2024-02-03T12:00:00",
        "fonte": "Dados de Exemplo"
    },
    "indicadores": {
        "populacao": {
            "valor": "179 558",
            "ano": "2023",
            "unidade": "habitantes",
            "ods": ["ODS11"]
        },
        "ganho_medio": {
            "valor": "1 424",
            "ano": "2021",
            "unidade": "euros",
            "ods": ["ODS1", "ODS8"]
        }
    },
    "ods": {
        "ODS1": {
            "nome": "Erradicar a Pobreza",
            "cor": "#E5243B",
            "indicadores": [
                {"chave": "ganho_medio", "valor": "1 424", "ano": "2021", "unidade": "euros"}
            ]
        }
    }
}

with open("dados_ods.json", "w", encoding="utf-8") as f:
    json.dump(dados_exemplo, f, ensure_ascii=False, indent=2)

print("✅ Dados de exemplo criados!")
```

Execute:
```bash
python criar_dados_exemplo.py
streamlit run app_ods.py
```

## 🎓 Próximos Passos

Agora que tem o dashboard a funcionar:

1. **Personalize** - Ajuste cores e layout no `app_ods.py`
2. **Adicione Indicadores** - Edite `etl_ods.py` para extrair mais dados
3. **Integre API** - Use `ine_api_client.py` para dados em tempo real
4. **Explore ODS** - Navegue pelos 17 objetivos e identifique gaps

## 💡 Dicas Úteis

- **Atualização automática**: O Streamlit recarrega automaticamente quando altera o código
- **Debug**: Use `st.write()` para imprimir variáveis durante desenvolvimento
- **Performance**: Use `@st.cache_data` para cachear operações pesadas
- **Temas**: Altere tema em Settings → Theme (canto superior direito)

## 📚 Recursos Adicionais

- [Documentação Streamlit](https://docs.streamlit.io)
- [API INE](https://www.ine.pt/xportal/xmain?xpid=INE&xpgid=ine_api)
- [ODS - ONU](https://www.un.org/sustainabledevelopment/)
- [Plotly Python](https://plotly.com/python/)

## ❓ Precisa de Ajuda?

- 📧 Email: info@cm-matosinhos.pt
- 📖 Consulte o README.md completo
- 🐛 Reporte bugs no GitHub Issues

---

**Boa sorte! 🚀**

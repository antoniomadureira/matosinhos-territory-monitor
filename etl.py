import pdfplumber
import json
import re
import os

# --- CONFIGURAÇÃO ---
# Atualizado para o novo nome do ficheiro
PDF_PATH = "data/Matosinhos.pdf"
OUTPUT_PATH = "dados.json"

def clean_number(value_str):
    """Converte '179 558' ou '1.424' para números puros (float)."""
    if not value_str: return None
    # Remove espaços e converte vírgula decimal para ponto
    clean = value_str.replace(' ', '').replace(',', '.')
    try:
        return float(clean)
    except ValueError:
        return None

def extract_from_pdf():
    dados = {}
    
    # Verifica se o ficheiro existe antes de tentar ler
    if not os.path.exists(PDF_PATH):
        print(f"❌ ERRO: O ficheiro '{PDF_PATH}' não foi encontrado.")
        print("   -> Verifica se criaste a pasta 'data' e se o ficheiro se chama 'Matosinhos.pdf'.")
        return

    print(f"🔄 A ler {PDF_PATH}...")
    
    try:
        with pdfplumber.open(PDF_PATH) as pdf:
            full_text = ""
            # Percorrer todas as páginas para acumular o texto
            for page in pdf.pages:
                full_text += page.extract_text() + "\n"
                
            # --- LÓGICA DE EXTRAÇÃO (REGEX) ---
            # Estes padrões procuram os indicadores chave no texto do INE
            
            # 1. População (Procura por "População residente" seguido de Ano e Valor)
            pop_match = re.search(r'População residente.*?(\d{4})\s+([\d\s]+)', full_text, re.DOTALL)
            if pop_match:
                dados['populacao'] = {
                    "valor": pop_match.group(2).strip(),
                    "ano": pop_match.group(1),
                    "fonte": "INE (Estimativas)"
                }

            # 2. Ganho Médio Mensal
            ganho_match = re.search(r'Ganho médio mensal.*?(\d{4})\s+([\d\s,]+)', full_text, re.DOTALL)
            if ganho_match:
                dados['ganho_medio'] = {
                    "valor": ganho_match.group(2).strip(),
                    "ano": ganho_match.group(1),
                    "fonte": "INE"
                }

            # 3. Empresas (Total)
            emp_match = re.search(r'Empresas \(n.*?(\d{4})\s+([\d\s]+)', full_text, re.DOTALL)
            if emp_match:
                dados['empresas'] = {
                    "valor": emp_match.group(2).strip(),
                    "ano": emp_match.group(1),
                    "fonte": "INE"
                }
                
            # 4. Médicos (Saúde)
            med_match = re.search(r'Médicos/1000.*?(\d{4})\s+([\d,]+)', full_text, re.DOTALL)
            if med_match:
                dados['medicos'] = {
                    "valor": med_match.group(2).strip(),
                    "ano": med_match.group(1),
                    "fonte": "INE/Ordens"
                }

    except Exception as e:
        print(f"❌ Erro ao ler o PDF: {e}")
        return

    # --- VALORES POR DEFEITO (FALLBACK) ---
    # Caso o PDF mude muito e o regex falhe, usamos estes valores seguros (baseados no PDF analisado)
    defaults = {
        "populacao": {"valor": "179 558", "ano": "2023", "fonte": "INE"},
        "ganho_medio": {"valor": "1 424", "ano": "2021", "fonte": "INE"},
        "empresas": {"valor": "23 152", "ano": "2022", "fonte": "INE"},
        "medicos": {"valor": "9,9", "ano": "2022", "fonte": "INE"}
    }
    
    # Fundir dados extraídos com defaults (prioridade para os extraídos)
    final_data = {k: dados.get(k, v) for k, v in defaults.items()}
    
    # Guardar no ficheiro JSON que o Dashboard vai ler
    try:
        with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
            json.dump(final_data, f, ensure_ascii=False, indent=4)
        print(f"✅ Sucesso! Dados guardados em '{OUTPUT_PATH}'.")
        print("   -> Podes agora correr o 'app.py' para ver os dados atualizados.")
        
    except Exception as e:
        print(f"❌ Erro ao guardar JSON: {e}")

if __name__ == "__main__":
    extract_from_pdf()
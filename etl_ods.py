"""
ETL Correto - Extração precisa baseada na estrutura real do PDF INE
"""

import pdfplumber
import json
import re
from datetime import datetime

PDF_PATH = "data/Matosinhos.pdf"
OUTPUT_PATH = "dados_ods.json"

ODS_MAPPING = {
    "ODS1": {"nome": "Erradicar a Pobreza", "cor": "#E5243B"},
    "ODS3": {"nome": "Saúde de Qualidade", "cor": "#4C9F38"},
    "ODS4": {"nome": "Educação de Qualidade", "cor": "#C5192D"},
    "ODS8": {"nome": "Trabalho Digno e Crescimento Económico", "cor": "#A21942"},
    "ODS9": {"nome": "Indústria, Inovação e Infraestruturas", "cor": "#FD6925"},
    "ODS10": {"nome": "Reduzir as Desigualdades", "cor": "#DD1367"},
    "ODS11": {"nome": "Cidades e Comunidades Sustentáveis", "cor": "#FD9D24"},
    "ODS16": {"nome": "Paz, Justiça e Instituições Eficazes", "cor": "#00689D"},
    "ODS17": {"nome": "Parcerias para a Implementação", "cor": "#19486A"}
}

def extract_from_pdf():
    """Extrai dados do PDF."""
    
    print("🔄 A analisar PDF do INE...")
    
    dados = {
        "metadata": {
            "concelho": "Matosinhos",
            "data_extracao": datetime.now().isoformat(),
            "fonte": "INE - Instituto Nacional de Estatística"
        },
        "indicadores": {},
        "ods": {k: {"nome": v["nome"], "cor": v["cor"], "indicadores": []} 
                for k, v in ODS_MAPPING.items()}
    }
    
    with pdfplumber.open(PDF_PATH) as pdf:
        # Página 3 (índice 2) tem indicadores chave
        page3_text = pdf.pages[2].extract_text()
        lines = page3_text.split('\n')
        
        for i, line in enumerate(lines):
            # População residente - linha tem "População residente (2023 (nº)", valor na próxima
            if 'População residente' in line and '(nº)' in line:
                if i + 1 < len(lines):
                    valores = lines[i + 1].split()
                    if len(valores) >= 2:
                        # Primeiro valor é população (ex: "179 558")
                        pop_partes = []
                        for v in valores:
                            if v.replace(' ', '').isdigit():
                                pop_partes.append(v)
                                if len(' '.join(pop_partes).replace(' ', '')) >= 6:
                                    break
                        
                        if pop_partes:
                            dados["indicadores"]["populacao"] = {
                                "valor": ' '.join(pop_partes),
                                "ano": "2023",
                                "unidade": "habitantes",
                                "ods": ["ODS11"]
                            }
                            print(f"   ✅ População: {' '.join(pop_partes)}")
                            
                        # Segundo valor é taxa de natalidade (ex: "7,2")
                        if len(valores) >= 2:
                            taxa = valores[-1]
                            if ',' in taxa:
                                dados["indicadores"]["taxa_natalidade"] = {
                                    "valor": taxa,
                                    "ano": "2023",
                                    "unidade": "‰",
                                    "ods": ["ODS3"]
                                }
                                print(f"   ✅ Taxa Natalidade: {taxa}")
            
            # Densidade populacional
            if 'Densidade populacional' in line and 'hab' in line:
                match = re.search(r'([\d\s,]+)', line)
                if match:
                    densidade = match.group(1).strip()
                    if densidade and len(densidade) <= 10:
                        dados["indicadores"]["densidade_populacional"] = {
                            "valor": densidade,
                            "ano": "2022",
                            "unidade": "hab/km²",
                            "ods": ["ODS11"]
                        }
                        print(f"   ✅ Densidade: {densidade}")
            
            # População ≥ 65 anos - na mesma linha tem valor e despesas cultura
            if 'População ≥ 65 anos' in line or 'População >= 65' in line:
                numeros = re.findall(r'[\d,]+', line)
                if numeros:
                    # Primeiro número é % idosos, segundo é despesas cultura
                    dados["indicadores"]["populacao_65_mais"] = {
                        "valor": numeros[0],
                        "ano": "2023",
                        "unidade": "%",
                        "ods": ["ODS3", "ODS10"]
                    }
                    print(f"   ✅ População ≥65: {numeros[0]}%")
                    
                    if len(numeros) > 1:
                        dados["indicadores"]["despesas_cultura_desporto"] = {
                            "valor": numeros[1],
                            "ano": "2022",
                            "unidade": "euros/hab",
                            "ods": ["ODS11"]
                        }
                        print(f"   ✅ Despesas Cultura/Desporto: {numeros[1]} €/hab")
            
            # Taxa escolarização
            if 'Taxa bruta de escolarização' in line and 'secundário' in line.lower():
                numeros = re.findall(r'[\d,]+', line)
                if numeros:
                    dados["indicadores"]["taxa_escolarizacao"] = {
                        "valor": numeros[-1],
                        "ano": "2022/2023",
                        "unidade": "%",
                        "ods": ["ODS4"]
                    }
                    print(f"   ✅ Taxa Escolarização: {numeros[-1]}%")
            
            # Médicos
            if 'Médicos / 1000 habitantes' in line or 'Médicos/1000' in line:
                numeros = re.findall(r'[\d,]+', line)
                if numeros:
                    # Último número antes de ano
                    for num in numeros:
                        if ',' in num and float(num.replace(',', '.')) < 50:
                            dados["indicadores"]["medicos_hab"] = {
                                "valor": num,
                                "ano": "2022",
                                "unidade": "médicos/1000 hab",
                                "ods": ["ODS3"]
                            }
                            print(f"   ✅ Médicos/1000 hab: {num}")
                            break
            
            # Taxa mortalidade infantil
            if 'mortalidade infantil' in line.lower():
                numeros = re.findall(r'[\d,]+', line)
                # Pegar número que parece taxa (com vírgula, pequeno)
                for num in numeros:
                    if ',' in num:
                        val = float(num.replace(',', '.'))
                        if val < 50:
                            dados["indicadores"]["taxa_mortalidade_infantil"] = {
                                "valor": num,
                                "ano": "2017/2021",
                                "unidade": "‰",
                                "ods": ["ODS3"]
                            }
                            print(f"   ✅ Mortalidade Infantil: {num}‰")
                            break
            
            # Ganho médio (procurar na linha e seguintes)
            if 'Ganho médio mensal' in line or 'Ganho médio' in line:
                # Valor pode estar na mesma linha ou próxima
                texto_busca = line + ' ' + (lines[i+1] if i+1 < len(lines) else '')
                numeros = re.findall(r'[\d\s]+', texto_busca)
                # Ganho médio é geralmente 4 dígitos (ex: 1424)
                for num in numeros:
                    num_limpo = num.replace(' ', '')
                    if num_limpo.isdigit() and 500 <= int(num_limpo) <= 9999:
                        # Formatar com espaço
                        if len(num_limpo) >= 4:
                            valor_format = f"{num_limpo[:-3]} {num_limpo[-3:]}"
                        else:
                            valor_format = num_limpo
                        
                        dados["indicadores"]["ganho_medio"] = {
                            "valor": valor_format,
                            "ano": "2021",
                            "unidade": "euros",
                            "ods": ["ODS1", "ODS8"]
                        }
                        print(f"   ✅ Ganho Médio: {valor_format} €")
                        break
        
        # Página 2 (índice 1) tem mais dados tabulares
        page2_text = pdf.pages[1].extract_text()
        lines2 = page2_text.split('\n')
        
        for i, line in enumerate(lines2):
            # Empresas
            if line.startswith('Empresas (nº)'):
                if i + 1 < len(lines2):
                    valores = lines2[i + 1].split()
                    # Procurar número de 5 dígitos (empresas Matosinhos)
                    for v in valores:
                        v_limpo = v.replace(' ', '')
                        if v_limpo.isdigit() and 10000 <= int(v_limpo) <= 99999:
                            # Formatar
                            valor_format = f"{v_limpo[:-3]} {v_limpo[-3:]}"
                            dados["indicadores"]["empresas"] = {
                                "valor": valor_format,
                                "ano": "2022",
                                "unidade": "unidades",
                                "ods": ["ODS8", "ODS9"]
                            }
                            print(f"   ✅ Empresas: {valor_format}")
                            break
    
    # Mapear para ODS
    for ind_key, ind_data in dados["indicadores"].items():
        for ods_code in ind_data.get("ods", []):
            if ods_code in dados["ods"]:
                dados["ods"][ods_code]["indicadores"].append({
                    "chave": ind_key,
                    "valor": ind_data["valor"],
                    "ano": ind_data["ano"],
                    "unidade": ind_data.get("unidade", "")
                })
    
    return dados


def main():
    print("=" * 70)
    print("ETL MATOSINHOS - VERSÃO OTIMIZADA")
    print("=" * 70)
    
    try:
        dados = extract_from_pdf()
        
        with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
        
        total_ind = len(dados["indicadores"])
        total_ods = len([v for v in dados["ods"].values() if v["indicadores"]])
        
        print("\n" + "=" * 70)
        print(f"✅ Total extraído: {total_ind} indicadores")
        print(f"✅ Total mapeado: {total_ods} ODS com dados")
        print(f"✅ Ficheiro guardado: '{OUTPUT_PATH}'")
        print("=" * 70)
        print("\n🚀 Execute agora: streamlit run app_ods.py\n")
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

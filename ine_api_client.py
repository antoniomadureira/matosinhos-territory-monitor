"""
Integração com API do INE (Instituto Nacional de Estatística)
Obtém dados atualizados diretamente da fonte oficial
"""

import requests
import json
import pandas as pd
from datetime import datetime
import time

# Configuração
INE_BASE_URL = "https://www.ine.pt/ine/json_indicador/pindica.jsp"
CODIGO_CONCELHO_MATOSINHOS = "130800"  # Código INE de Matosinhos

# Indicadores prioritários com seus códigos INE
INDICADORES_INE = {
    # DEMOGRAFIA
    "0011609": {"nome": "População residente", "ods": ["ODS11"], "unidade": "habitantes"},
    "0011608": {"nome": "Densidade populacional", "ods": ["ODS11"], "unidade": "hab/km²"},
    "0007868": {"nome": "Índice de envelhecimento", "ods": ["ODS3", "ODS10"], "unidade": "%"},
    "0007871": {"nome": "Taxa bruta de natalidade", "ods": ["ODS3"], "unidade": "‰"},
    "0007872": {"nome": "Taxa bruta de mortalidade", "ods": ["ODS3"], "unidade": "‰"},
    
    # SAÚDE
    "0011625": {"nome": "Médicos por 1000 habitantes", "ods": ["ODS3"], "unidade": "médicos/1000 hab"},
    "0011626": {"nome": "Enfermeiros por 1000 habitantes", "ods": ["ODS3"], "unidade": "enfermeiros/1000 hab"},
    "0007889": {"nome": "Taxa de mortalidade infantil", "ods": ["ODS3"], "unidade": "‰"},
    
    # ECONOMIA
    "0011627": {"nome": "Ganho médio mensal", "ods": ["ODS1", "ODS8"], "unidade": "euros"},
    "0011628": {"nome": "Empresas", "ods": ["ODS8", "ODS9"], "unidade": "unidades"},
    "0011629": {"nome": "Volume de negócios", "ods": ["ODS8"], "unidade": "10³ euros"},
    "0011636": {"nome": "Exportações", "ods": ["ODS8", "ODS17"], "unidade": "10³ euros"},
    "0011637": {"nome": "Importações", "ods": ["ODS8", "ODS17"], "unidade": "10³ euros"},
    
    # EDUCAÇÃO
    "0011640": {"nome": "Taxa de escolarização ensino secundário", "ods": ["ODS4"], "unidade": "%"},
    "0011641": {"nome": "Alunos matriculados ensino superior", "ods": ["ODS4"], "unidade": "alunos"},
    
    # AMBIENTE
    "0011650": {"nome": "Resíduos urbanos recolhidos", "ods": ["ODS12"], "unidade": "kg/hab"},
    "0011651": {"nome": "Água residual tratada", "ods": ["ODS6"], "unidade": "%"},
    
    # INFRAESTRUTURAS
    "0011655": {"nome": "Alojamentos com internet", "ods": ["ODS9"], "unidade": "%"},
    "0011656": {"nome": "Despesas municípios em cultura e desporto", "ods": ["ODS11"], "unidade": "euros/hab"},
    
    # SEGURANÇA
    "0011660": {"nome": "Taxa de criminalidade", "ods": ["ODS16"], "unidade": "‰"},
}

class INEDataFetcher:
    """Classe para buscar dados da API do INE."""
    
    def __init__(self, verbose=True):
        self.verbose = verbose
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def log(self, message):
        """Imprime mensagem se verbose ativado."""
        if self.verbose:
            print(message)
    
    def fetch_indicator(self, codigo_indicador, codigo_concelho=CODIGO_CONCELHO_MATOSINHOS):
        """
        Busca um indicador específico da API do INE.
        
        Args:
            codigo_indicador: Código do indicador no INE
            codigo_concelho: Código do concelho (default: Matosinhos)
        
        Returns:
            dict com dados ou None se falhar
        """
        params = {
            'op': '2',
            'lang': 'PT',
            'id_indicador': codigo_indicador
        }
        
        try:
            self.log(f"   Buscando indicador {codigo_indicador}...")
            response = self.session.get(INE_BASE_URL, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Processar resposta (estrutura varia por indicador)
                if isinstance(data, list) and len(data) > 0:
                    # Encontrar dados para Matosinhos
                    for item in data:
                        if 'geocod' in item and str(item['geocod']) == codigo_concelho:
                            return {
                                'valor': item.get('valor'),
                                'ano': item.get('periodo'),
                                'unidade': item.get('unidade', '')
                            }
                    
                    # Se não encontrou por geocod, pegar primeiro resultado
                    primeiro = data[0]
                    return {
                        'valor': primeiro.get('valor'),
                        'ano': primeiro.get('periodo'),
                        'unidade': primeiro.get('unidade', '')
                    }
                
                self.log(f"      ⚠️  Formato inesperado ou sem dados")
                return None
            
            elif response.status_code == 403:
                self.log(f"      ❌ Acesso bloqueado (403)")
                return None
            
            elif response.status_code == 404:
                self.log(f"      ❌ Indicador não encontrado (404)")
                return None
            
            else:
                self.log(f"      ❌ Erro HTTP {response.status_code}")
                return None
        
        except requests.exceptions.Timeout:
            self.log(f"      ⏰ Timeout ao buscar indicador")
            return None
        
        except Exception as e:
            self.log(f"      💀 Erro: {e}")
            return None
    
    def fetch_all_indicators(self, delay=1.0):
        """
        Busca todos os indicadores configurados.
        
        Args:
            delay: Tempo de espera entre requests (para não sobrecarregar API)
        
        Returns:
            dict com todos os dados coletados
        """
        self.log("=" * 70)
        self.log("INICIANDO COLETA DE DADOS DO INE")
        self.log("=" * 70)
        
        dados_coletados = {
            "metadata": {
                "concelho": "Matosinhos",
                "codigo_concelho": CODIGO_CONCELHO_MATOSINHOS,
                "data_coleta": datetime.now().isoformat(),
                "fonte": "INE - API json_indicador"
            },
            "indicadores": {},
            "erros": []
        }
        
        total = len(INDICADORES_INE)
        sucesso = 0
        
        for i, (codigo, info) in enumerate(INDICADORES_INE.items(), 1):
            self.log(f"\n[{i}/{total}] {info['nome']}")
            
            resultado = self.fetch_indicator(codigo)
            
            if resultado:
                dados_coletados["indicadores"][codigo] = {
                    "nome": info["nome"],
                    "valor": resultado["valor"],
                    "ano": resultado["ano"],
                    "unidade": info["unidade"],
                    "ods": info["ods"]
                }
                sucesso += 1
                self.log(f"      ✅ Sucesso: {resultado['valor']} ({resultado['ano']})")
            else:
                dados_coletados["erros"].append({
                    "codigo": codigo,
                    "nome": info["nome"]
                })
                self.log(f"      ❌ Falhou")
            
            # Delay para não sobrecarregar API
            if i < total:
                time.sleep(delay)
        
        self.log("\n" + "=" * 70)
        self.log(f"COLETA CONCLUÍDA: {sucesso}/{total} indicadores obtidos")
        self.log("=" * 70)
        
        return dados_coletados
    
    def save_to_json(self, dados, filepath="dados_ine_api.json"):
        """Guarda os dados coletados em JSON."""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(dados, f, ensure_ascii=False, indent=2)
            self.log(f"\n✅ Dados guardados em '{filepath}'")
            return True
        except Exception as e:
            self.log(f"\n❌ Erro ao guardar: {e}")
            return False
    
    def create_summary_dataframe(self, dados):
        """Cria um DataFrame pandas para análise."""
        rows = []
        
        for codigo, ind in dados["indicadores"].items():
            rows.append({
                "Código": codigo,
                "Indicador": ind["nome"],
                "Valor": ind["valor"],
                "Ano": ind["ano"],
                "Unidade": ind["unidade"],
                "ODS": ", ".join(ind["ods"])
            })
        
        return pd.DataFrame(rows)


def main():
    """Função principal - executa coleta completa."""
    
    print("\n🌐 MATOSINHOS TERRITORY MONITOR - INE API CLIENT")
    print("=" * 70)
    
    # Criar fetcher
    fetcher = INEDataFetcher(verbose=True)
    
    # Buscar todos os indicadores
    dados = fetcher.fetch_all_indicators(delay=1.5)
    
    # Guardar resultados
    fetcher.save_to_json(dados)
    
    # Criar resumo
    if dados["indicadores"]:
        print("\n📊 RESUMO DOS DADOS COLETADOS:")
        print("-" * 70)
        
        df = fetcher.create_summary_dataframe(dados)
        print(df.to_string(index=False))
        
        # Guardar também em CSV
        csv_path = "dados_ine_api.csv"
        df.to_csv(csv_path, index=False, encoding='utf-8')
        print(f"\n✅ CSV guardado em '{csv_path}'")
    
    # Erros
    if dados["erros"]:
        print(f"\n⚠️  INDICADORES COM ERRO ({len(dados['erros'])}):")
        for erro in dados["erros"]:
            print(f"   • {erro['nome']} (código: {erro['codigo']})")
    
    print("\n" + "=" * 70)
    print("✅ PROCESSO CONCLUÍDO")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()

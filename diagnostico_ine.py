import requests
import socket
import sys

print("--- 🕵️ RELATÓRIO DE DIAGNÓSTICO DE REDE (INE) ---")

# 1. Teste de DNS (Sabemos onde fica a casa do INE?)
print("\n1. A testar resolução de nomes (DNS)...")
try:
    ip = socket.gethostbyname("www.ine.pt")
    print(f"✅ SUCESSO: www.ine.pt resolve para o IP {ip}")
except Exception as e:
    print(f"❌ FALHA CRÍTICA: Não conseguimos encontrar o servidor. Erro: {e}")
    sys.exit()

# 2. Teste de Endpoints (Vamos bater à porta)
# Vamos testar o endereço antigo e o novo (Legacy)
endpoints = [
    {
        "nome": "API Moderna (ine_servicos_informaticos)",
        "url": "https://www.ine.pt/ine_servicos_informaticos/service/srv/p_indicador?id_indicador=0011609&lang=PT"
    },
    {
        "nome": "API Legacy (pindica.jsp)",
        "url": "https://www.ine.pt/ine/json_indicador/pindica.jsp?op=2&lang=PT&id_indicador=0011609"
    }
]

# Headers para fingir que somos um computador normal e não um robot
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

print("\n2. A testar ligação HTTP...")

for api in endpoints:
    print(f"\nTesting: {api['nome']}...")
    try:
        r = requests.get(api['url'], headers=headers, timeout=10)
        
        print(f"   Status Code: {r.status_code}")
        
        if r.status_code == 200:
            print("   ✅ LIGAÇÃO BEM SUCEDIDA!")
            print(f"   Conteúdo recebido (primeiros 100 chars): {r.text[:100]}")
            if "Dados" in r.text or "valor" in r.text:
                print("   ✅ JSON Válido detetado.")
            else:
                print("   ⚠️ Alerta: Recebemos 200 OK, mas o conteúdo parece HTML ou erro.")
                
        elif r.status_code == 403:
            print("   ⛔ BLOQUEADO (403): O INE sabe que estás no GitHub e bloqueou o acesso.")
            
        elif r.status_code == 404:
            print("   ❌ NÃO ENCONTRADO (404): Este endereço já não existe.")
            
        elif r.status_code == 500 or r.status_code == 503:
            print("   🔥 ERRO SERVIDOR (500/503): O servidor do INE está em baixo ou em manutenção.")
            
    except requests.exceptions.SSLError:
        print("   🔒 ERRO SSL: O certificado de segurança do INE foi rejeitado.")
    except requests.exceptions.Timeout:
        print("   ⏰ TIMEOUT: O INE demorou demasiado a responder (firewall silenciosa).")
    except Exception as e:
        print(f"   💀 Erro desconhecido: {e}")

print("\n--- FIM DO RELATÓRIO ---")
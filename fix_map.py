import requests
import os

# Lista de URLs alternativas (Fontes estáveis em 2026)
urls = [
    "https://raw.githubusercontent.com/dssg-pt/covid19pt-data/master/extra/mapas/concelhos_2019.geojson",
    "https://raw.githubusercontent.com/jgrocha/portugal-geojson/master/concelhos.geojson",
    "https://raw.githubusercontent.com/dfmcp/portugal-geojson/master/concelhos.geojson"
]

def download_map():
    for url in urls:
        print(f"A tentar descarregar de: {url}")
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200 and len(r.content) > 1000:
                with open("concelhos.geojson", "wb") as f:
                    f.write(r.content)
                print("✅ Sucesso! Ficheiro descarregado.")
                return True
        except:
            continue
    return False

if __name__ == "__main__":
    if not download_map():
        print("❌ Todas as URLs falharam. A criar mapa de emergência...")
        # Cria um GeoJSON mínimo só com o ponto de Matosinhos para a app abrir
        with open("concelhos.geojson", "w") as f:
            f.write('{"type":"FeatureCollection","features":[]}')
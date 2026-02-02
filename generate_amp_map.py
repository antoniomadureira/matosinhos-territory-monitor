import json

# Coordenadas aproximadas (simplificadas) para Matosinhos e vizinhos da AMP
# Isto garante que o mapa renderiza mesmo sem downloads externos
amp_features = [
    {"type": "Feature", "id": "1308", "properties": {"name": "Matosinhos", "code": "1308"}, "geometry": {"type": "Polygon", "coordinates": [[[-8.71, 41.22], [-8.66, 41.24], [-8.62, 41.21], [-8.65, 41.17], [-8.70, 41.17], [-8.71, 41.22]]]}},
    {"type": "Feature", "id": "1312", "properties": {"name": "Porto", "code": "1312"}, "geometry": {"type": "Polygon", "coordinates": [[[-8.65, 41.17], [-8.58, 41.18], [-8.57, 41.14], [-8.65, 41.14], [-8.65, 41.17]]]}},
    {"type": "Feature", "id": "1306", "properties": {"name": "Maia", "code": "1306"}, "geometry": {"type": "Polygon", "coordinates": [[[-8.66, 41.24], [-8.58, 41.26], [-8.57, 41.21], [-8.62, 41.21], [-8.66, 41.24]]]}},
    {"type": "Feature", "id": "1317", "properties": {"name": "Vila Nova de Gaia", "code": "1317"}, "geometry": {"type": "Polygon", "coordinates": [[[-8.65, 41.14], [-8.56, 41.13], [-8.57, 41.05], [-8.66, 41.05], [-8.65, 41.14]]]}}
]

geo_data = {
    "type": "FeatureCollection",
    "features": amp_features
}

with open("concelhos.geojson", "w") as f:
    json.dump(geo_data, f)

print("✅ Mapa Lite da AMP criado com sucesso!")
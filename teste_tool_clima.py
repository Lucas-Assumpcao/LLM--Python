import requests

def buscar_previsao_tempo(latitude: float, longitude: float, data: str) -> dict:
    """Busca a previsão do tempo para uma coordenada e data específica (formato YYYY-MM-DD)."""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max",
        "timezone": "auto",
        "start_date": data,
        "end_date": data,
    }
    resposta = requests.get(url, params=params)
    dados = resposta.json()
    return {
        "temp_max": dados["daily"]["temperature_2m_max"][0],
        "temp_min": dados["daily"]["temperature_2m_min"][0],
        "chance_chuva": dados["daily"]["precipitation_probability_max"][0],
    }

resultado = buscar_previsao_tempo(latitude=21.16, longitude=-86.85, data="2026-07-15")
print(resultado)
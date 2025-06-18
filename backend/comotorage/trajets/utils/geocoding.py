
import requests

def geocode(adresse):
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": adresse, "format": "json"}
    headers = {"User-Agent": "comotorage-bot/1.0 (https://comotorage.local)"}

    try:
        response = requests.get(url, params=params, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data:
                return float(data[0]["lat"]), float(data[0]["lon"])
    except requests.exceptions.RequestException as e:
        print(f"[Erreur géocodage] {adresse} → {e}")
    return None, None

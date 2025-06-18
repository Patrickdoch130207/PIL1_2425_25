
import requests

def get_osrm_route_info(start_lon, start_lat, end_lon, end_lat):
    url = f"http://router.project-osrm.org/route/v1/driving/{start_lon},{start_lat};{end_lon},{end_lat}?overview=false"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data["routes"]:
            return {
                "distance_km": data["routes"][0]["distance"] / 1000,
                "duration_min": data["routes"][0]["duration"] / 60
            }
    return None

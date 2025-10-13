import requests

def get_daily_consumption(prm: str, start: str, end: str, token: str):
    """
    Récupère les données de consommation journalière pour un compteur (PRM)
    entre les dates start (incluse) et end (exclue).
    
    :param prm: le PRM (14 chiffres)
    :param start: date de début au format 'YYYY-MM-DD'
    :param end: date de fin (non incluse) au format 'YYYY-MM-DD'
    :param token: le token d’authentification Bearer
    :return: réponse JSON si succès, sinon lève une exception
    """
    base_url = "https://conso.boris.sh/api/daily_consumption"
    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": "MonApp/1.0 (contact@example.com)"  # optionnel mais recommandé
    }
    params = {
        "prm": prm,
        "start": start,
        "end": end
    }
    
    response = requests.get(base_url, headers=headers, params=params)
    # Vérifier le code HTTP
    if response.status_code != 200:
        raise Exception(f"Erreur HTTP {response.status_code} : {response.text}")
    
    return response.json()


def get_consumption_load(prm: str, start: str, end: str, token: str):
    """
    Récupère les données de consommation journalière pour un compteur (PRM)
    entre les dates start (incluse) et end (exclue).
    
    :param prm: le PRM (14 chiffres)
    :param start: date de début au format 'YYYY-MM-DD'
    :param end: date de fin (non incluse) au format 'YYYY-MM-DD'
    :param token: le token d’authentification Bearer
    :return: réponse JSON si succès, sinon lève une exception
    """
    base_url = "https://conso.boris.sh/api/consumption_load_curve"
    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": "MonApp/1.0 (contact@example.com)"  # optionnel mais recommandé
    }
    params = {
        "prm": prm,
        "start": start,
        "end": end
    }
    
    response = requests.get(base_url, headers=headers, params=params)
    # Vérifier le code HTTP
    if response.status_code != 200:
        raise Exception(f"Erreur HTTP {response.status_code} : {response.text}")
    
    return response.json()

if __name__ == "__main__":
    # Exemple d’utilisation :
    PRM = "02297250326360"
    start_date = "2025-01-08"
    end_date   = "2025-01-11"
    token = "eyJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3NjAyNjMyNTksImV4cCI6MTg1NDc4NDg1OSwic3ViIjpbIjAyMjk3MjUwMzI2MzYwIl19.N0tP2NOkYwmCzFRo4tbxxfnS7OGMdRpc2p6v8zs2Pmo"  # remplace avec ton token
    
    data = get_consumption_load(PRM, start_date, end_date, token)
    print(data)
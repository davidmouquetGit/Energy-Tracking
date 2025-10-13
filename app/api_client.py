



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

    import requests
    
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
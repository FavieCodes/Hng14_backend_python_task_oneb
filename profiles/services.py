import requests
from datetime import datetime

def get_age_group(age):
    """Determine age group from age"""
    if age is None:
        return None
    if 0 <= age <= 12:
        return "child"
    elif 13 <= age <= 19:
        return "teenager"
    elif 20 <= age <= 59:
        return "adult"
    elif age >= 60:
        return "senior"
    return None

def fetch_genderize_data(name):
    """Fetch gender data from Genderize API"""
    try:
        url = f"https://api.genderize.io/?name={name}"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        # Check for invalid response
        if data.get('gender') is None or data.get('count', 0) == 0:
            return None, "Genderize returned an invalid response"
        
        return {
            'gender': data['gender'],
            'gender_probability': data['probability'],
            'sample_size': data['count']
        }, None
    except requests.RequestException:
        return None, "Genderize returned an invalid response"

def fetch_agify_data(name):
    """Fetch age data from Agify API"""
    try:
        url = f"https://api.agify.io/?name={name}"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        # Check for invalid response
        if data.get('age') is None:
            return None, "Agify returned an invalid response"
        
        age = data['age']
        age_group = get_age_group(age)
        
        if age_group is None:
            return None, "Agify returned an invalid response"
        
        return {
            'age': age,
            'age_group': age_group
        }, None
    except requests.RequestException:
        return None, "Agify returned an invalid response"

def fetch_nationalize_data(name):
    """Fetch nationality data from Nationalize API"""
    try:
        url = f"https://api.nationalize.io/?name={name}"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        # Check for invalid response
        if not data.get('country') or len(data['country']) == 0:
            return None, "Nationalize returned an invalid response"
        
        # Get country with highest probability
        top_country = max(data['country'], key=lambda x: x['probability'])
        
        return {
            'country_id': top_country['country_id'],
            'country_probability': top_country['probability']
        }, None
    except requests.RequestException:
        return None, "Nationalize returned an invalid response"
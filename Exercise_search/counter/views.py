from django.shortcuts import render
import requests
import json

def home(request):
    allowed_body_parts = [
        "back", "cardio", "chest", "lower arms", "lower legs",
        "neck", "shoulders", "upper arms", "upper legs", "waist"
    ]

    if request.method == 'POST':
        query = request.POST.get('query', '').strip().lower()
        
        if query not in allowed_body_parts:
            return render(request, 'home.html', {'error': 'Invalid body part. Please enter a valid query.'})

        api_url = f"https://exercisedb.p.rapidapi.com/exercises/bodyPart/{query}"

        headers = {
            "x-rapidapi-key": "b8619783cbmshfa72ddd405dade0p19fdebjsn3eacfe092b53",
            "x-rapidapi-host": "exercisedb.p.rapidapi.com"
        }

        response = requests.get(api_url, headers=headers)
        
        try:
            api = json.loads(response.content)
        except json.JSONDecodeError:
            api = "Oops! There was an error decoding the response."
        
        return render(request, 'home.html', {'api': api})

    return render(request, 'home.html')

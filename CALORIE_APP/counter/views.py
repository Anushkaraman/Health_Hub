from django.shortcuts import render
import json
import requests

# Create your views here.
def home(request):
    if request.method == 'POST':
        query = request.POST['calories']
        api_url = 'https://api.spoonacular.com/recipes/findByNutrients?maxCalories=' + query
        api_key = '0fb2112c1ea8496a87e8e67c1cbe4122'
        
        api_request = requests.get(api_url, headers={'X-Api-Key': api_key})
        try:
            api = json.loads(api_request.content)
            print(api_request.content)
        except Exception as e:
            api = "Oops! There was an error"
            print(e)
        return render(request, 'home.html', {'api': api})
    else:
        return render(request, 'home.html', {'calories': 'Enter a valid query'})

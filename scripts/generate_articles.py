import json
import random
import datetime
import os
import re
import requests

API_URL = "https://api.mistral.ai/v1/chat/completions"
API_KEY = os.environ.get('MISTRAL_API_KEY')

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

payload = {
    "model": "mistral-medium",
    "messages": [{
        "role": "user",
        "content": "Generate exactly 7 newspaper articles for Journal de la Métropole in Canadian French, early 20th century style. Each article must be a JSON object with: id (one of: lead, 1, 2, featured, 3, 4, 5), title, content (3-4 detailed sentences in Canadian French), byline (in French). Return ONLY a valid JSON array with exactly 7 articles, no extra text, no markdown, no code blocks."
    }],
    "temperature": 0.7,
    "max_tokens": 2500
}

# Fallback articles in case API fails
FALLBACK_ARTICLES = [
    {
        "id": "lead",
        "title": "La Métropole Transformée : Le Conseil Municipal Approuve un Plan de Modernisation Ambitieux",
        "content": "Le Conseil municipal a voté hier à l'unanimité pour approuver un vaste plan de modernisation qui apportera l'éclairage électrique public à tous les quartiers d'ici la fin de la décennie. \"C'est une nouvelle ère pour notre grande ville,\" a déclaré le maire Théodore Whitmore. Le plan comprend également l'extension du service de tramway et la construction d'un nouvel hôtel de ville sur la place centrale.",
        "byline": "Par Harold Winslow, Correspondant Principal"
    },
    {
        "id": "1",
        "title": "Magnat Industriel Annonce une Nouvelle Usine en Banlieue",
        "content": "Le puissant industriel Charlesworth Sterling a révélé hier ses plans pour une nouvelle installation de fabrication en banlieue de Montréal. L'usine, d'une valeur de 2 millions de dollars, devrait créer plus de cinq cents nouveaux emplois et stimuler considérablement l'économie locale. Les travaux devraient commencer au printemps prochain.",
        "byline": "Par Margaret Holloway, Rédactrice Économique"
    },
    {
        "id": "2",
        "title": "Aviateur Québécois Établit un Nouveau Record de Distance en Vol",
        "content": "L'audacieuse aviatrice Amélie Fairchild a de nouveau fait la une en battant le record de distance pour un vol sans escale. Son voyage de 2 100 milles a été accompli en 14 heures à bord de son fidèle biplan, le \"Esprit de l'Aventure\". Mlle Fairchild a déclaré qu'elle prévoyait tenter une traversée transatlantique au printemps prochain.",
        "byline": "Agence de Presse"
    },
    {
        "id": "featured",
        "title": "Le Grand Débat : Progrès versus Tradition à la Métropole",
        "content": "Notre ville se trouve à la croisée des chemins. Alors que nous embrassons les merveilles de l'âge moderne avec l'électricité et les automobiles, nous ne devons pas oublier les valeurs et les traditions qui ont fait de nous ce que nous sommes. La nouvelle génération recherche le changement à un rythme sans précédent, tandis que les aînés prônent la patience et la réflexion.",
        "byline": "Éditorial par Edmund Blackwood"
    },
    {
        "id": "3",
        "title": "Agriculture Locale : Récolte Abondante Prévue pour l'Automne",
        "content": "Les agriculteurs de toute la région de la Métropole signalent une saison de croissance exceptionnellement prometteuse. L'extension agricole du comté prévoit une récolte de blé qui pourrait dépasser tous les records précédents. \"Les pluies ont été opportunes et le soleil généreux,\" a souligné l'agriculteur Jean Thistlewaite.",
        "byline": "Par Thomas Greenleaf, Correspondant Agricole"
    },
    {
        "id": "4",
        "title": "Merveille Médicale : Un Nouveau Traitement Contre la Tuberculose Montre des Résultats Prometteurs",
        "content": "Le Dr Éléonore Whitmore de l'Hôpital Général de la Métropole a annoncé hier le succès des essais cliniques d'un nouveau traitement contre la tuberculose qui tourmente notre population depuis des décennies. Les premiers résultats montrent une amélioration remarquable.",
        "byline": "Par Helen Fairfax, Rédactrice Santé"
    },
    {
        "id": "5",
        "title": "Société : Grand Bal de Charité au Waldorf Attire la Fine Fleur de la Métropole",
        "content": "L'événement social de la saison a eu lieu hier soir à l'hôtel Waldorf, où la fine fleur de la société s'est réunie pour le bal de charité annuel. Plus de cinq cents invités distingués ont assisté à l'événement.",
        "byline": "Correspondant Société"
    }
]

def get_fallback_articles():
    """Return articles with themes and random layout"""
    themes = ['Politique', 'Économie', 'Technologie', 'Santé', 'Culture', 'Sports', 'Société']
    for i, art in enumerate(FALLBACK_ARTICLES):
        art['theme'] = themes[i % len(themes)]
    
    ids = [a['id'] for a in FALLBACK_ARTICLES]
    random.shuffle(ids)
    layout = {
        'lead': ids[0],
        'featured': ids[1],
        'article-1': ids[2],
        'article-2': ids[3],
        'article-3': ids[4],
        'article-4': ids[5],
        'article-5': ids[6]
    }
    
    return {
        'articles': FALLBACK_ARTICLES,
        'layout': layout,
        'generated_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

try:
    response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    
    content = response.json()['choices'][0]['message']['content']
    print(f"Raw response content type: {type(content)}")
    print(f"First 200 chars: {content[:200]}")
    
    # Try to extract JSON from markdown code blocks if present
    # The API might wrap the JSON in markdown like: ```json
    # [...array...]
    # ```
    json_match = re.search(r'(\[.*\])', content, re.DOTALL)
    if json_match:
        content = json_match.group(1)
    
    articles = json.loads(content)
    
    if not isinstance(articles, list) or len(articles) != 7:
        raise ValueError(f"Expected 7 articles, got {len(articles) if isinstance(articles, list) else type(articles)}")
    
    # Add themes
    themes = ['Politique', 'Économie', 'Technologie', 'Santé', 'Culture', 'Sports', 'Société']
    for i, art in enumerate(articles):
        art['theme'] = themes[i % len(themes)]
    
    # Create random layout
    ids = [a['id'] for a in articles]
    random.shuffle(ids)
    layout = {
        'lead': ids[0],
        'featured': ids[1],
        'article-1': ids[2],
        'article-2': ids[3],
        'article-3': ids[4],
        'article-4': ids[5],
        'article-5': ids[6]
    }
    
    result = {
        'articles': articles,
        'layout': layout,
        'generated_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    with open('data/articles.json', 'w') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print("Successfully generated articles from API")
    
except Exception as e:
    import traceback
    traceback.print_exc()
    print(f"Error: {e}")
    print("Using fallback articles...")
    result = get_fallback_articles()
    with open('data/articles.json', 'w') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

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
        "content": "Génère exactement 7 articles de journal pour le Journal de la Métropole en français canadien, style début du 20e siècle. Utilise EXACTEMENT ces 7 catégories/thèmes, une seule par article : Politique, Économie, Technologie, Santé, Culture, Sports, Société. Chaque article doit correspondre parfaitement à sa catégorie. Chaque article doit être un objet JSON avec : id (l'un de : lead, 1, 2, featured, 3, 4, 5), title, content (3-4 phrases détaillées en français québécois formel), byline (en français), theme (la catégorie correspondante). Assure-toi que le thème correspond exactement au contenu de l'article. Retourne UNIQUEMENT un tableau JSON valide avec exactement 7 articles, sans texte supplémentaire, sans markdown, sans blocs de code."
    }],
    "temperature": 0.7,
    "max_tokens": 2500
}

# Fallback articles in case API fails (in Canadian French)
# Each article has a theme that matches its content
FALLBACK_ARTICLES = [
    {
        "id": "lead",
        "title": "La Métropole se modernise : éclairage électrique pour tous les quartiers",
        "content": "Le Conseil municipal a voté hier à l'unanimité pour approuver un vaste plan de modernisation qui apportera l'éclairage électrique public à tous les quartiers d'ici la fin de la décennie. \"C'est une nouvelle ère pour notre grande ville,\" a déclaré le maire Théodore Lavoie. Le plan comprend également l'extension du service de tramway et la construction d'un nouvel hôtel de ville sur la place centrale.",
        "byline": "Par Henri Laurendeau, Correspondant Principal",
        "theme": "Politique"
    },
    {
        "id": "1",
        "title": "Magnat industriel annonce une nouvelle usine en banlieue",
        "content": "Le puissant industriel Charles Tremblay a révélé hier ses plans pour une nouvelle installation de fabrication en banlieue de Montréal. L'usine, d'une valeur de 2 millions de dollars, devrait créer plus de cinq cents nouveaux emplois et stimuler considérablement l'économie locale. Les travaux devraient commencer au printemps prochain.",
        "byline": "Par Marguerite Leblanc, Rédactrice Économique",
        "theme": "Économie"
    },
    {
        "id": "2",
        "title": "Le téléphonique sans fil révolutionne les communications à Montréal",
        "content": "Une invention révolutionnaire venue d'Europe fait sensation dans notre ville : le téléphone sans fil portatif. Cette merveille de la technologie moderne permet désormais de communiquer à distance sans être attaché à un poste fixe. Les premiers appareils ont été installés à l'hôtel de ville et chez quelques industriels.",
        "byline": "Par Georges Laplace, Correspondant Technologique",
        "theme": "Technologie"
    },
    {
        "id": "featured",
        "title": "Merveille médicale : un nouveau traitement contre la tuberculose montre des résultats prometteurs",
        "content": "Le Dr Éléonore Tremblay de l'Hôpital Général de la Métropole a annoncé hier le succès des essais cliniques d'un nouveau traitement contre la tuberculose qui tourmente notre population depuis des décennies. Les premiers résultats montrent une amélioration remarquable chez les patients.",
        "byline": "Par Hélène Lapierre, Rédactrice Santé",
        "theme": "Santé"
    },
    {
        "id": "3",
        "title": "Le grand ballet national en tournée à la Métropole",
        "content": "La célèbre troupe du Grand Ballet National a offert hier soir une représentation exceptionnelle au théâtre Royal. Les danseurs ont interprétée une nouvelle œuvre inspirée des légendes autochtones du Québec, sous la direction du maître chorégraphe Antoine Delacroix.",
        "byline": "Par Sophie Girard, Correspondante Culturelle",
        "theme": "Culture"
    },
    {
        "id": "4",
        "title": "Le Canadien bat le record de victoires consécutives",
        "content": "L'équipe de hockey du Canadien de Montréal a établi un nouveau record en remportant sa 15e victoire consécutive hier soir contre les Maple Leafs de Toronto. Les partisans ont envahi la patinoire après le match historique. Le capitaine Jean Bellemare a soulevé la coupe sous les acclamations de la foule.",
        "byline": "Par Pierre Moreau, Correspondant Sportif",
        "theme": "Sports"
    },
    {
        "id": "5",
        "title": "Grand bal de charité au Waldorf attire la fine fleur de la société",
        "content": "L'événement social de la saison a eu lieu hier soir à l'hôtel Waldorf, où la fine fleur de la société s'est réunie pour le bal de charité annuel. Plus de cinq cents invités distingués ont assisté à l'événement. Les fonds recueillis serviront à construire un nouvel orphelinat.",
        "byline": "Par Marie-Claire Dubois, Correspondante Société",
        "theme": "Société"
    }
]

def get_fallback_articles():
    """Return articles with themes and random layout"""
    # FALLBACK_ARTICLES already have themes assigned
    # Just create random layout
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
    
    # Verify all articles have themes and they are valid
    valid_themes = {'Politique', 'Économie', 'Technologie', 'Santé', 'Culture', 'Sports', 'Société'}
    for art in articles:
        if 'theme' not in art:
            raise ValueError(f"Article missing theme: {art.get('title', 'unknown')}")
        if art['theme'] not in valid_themes:
            raise ValueError(f"Invalid theme '{art['theme']}' for article: {art.get('title', 'unknown')}")
    
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

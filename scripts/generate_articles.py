import json
import random
import datetime
import os
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
        "content": "Generate exactly 7 newspaper articles for Journal de la Métropole in Canadian French, early 20th century style. Each article must be a JSON object with: id (one of: lead, 1, 2, featured, 3, 4, 5), title, content (3-4 detailed sentences in Canadian French), byline (in French). Return ONLY a valid JSON array with exactly 7 articles, no extra text."
    }],
    "temperature": 0.7,
    "max_tokens": 2500
}

try:
    response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    content = response.json()['choices'][0]['message']['content']
    articles = json.loads(content)
    
    if not isinstance(articles, list) or len(articles) != 7:
        raise ValueError(f"Expected 7 articles, got {len(articles)}")
    
    themes = ['Politique', 'Économie', 'Technologie', 'Santé', 'Culture', 'Sports', 'Société']
    for i, art in enumerate(articles):
        art['theme'] = themes[i % len(themes)]
    
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
    
    print("Successfully generated articles")
    
except Exception as e:
    import traceback
    traceback.print_exc()
    with open('data/articles.json', 'w') as f:
        json.dump({
            'error': str(e),
            'articles': [],
            'layout': {},
            'generated_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }, f, ensure_ascii=False, indent=2)

# Journal de la Métropole

Un site web de journal en ligne avec une mise en page en colonnes style début du 20e siècle, entièrement en français canadien.

## Architecture

Ce projet utilise une **approche statique avec génération quotidienne** :

- **GitHub Actions** génère de nouveaux articles chaque matin à 6h (heure de Montréal)
- Les articles sont **statiques** et servis depuis un fichier JSON
- Pas d'appels API côté client = chargement rapide et sécurisé

## Structure des Fichiers

```
headlines/
├── index.html          # Page principale
├── style.css           # Styles du journal
├── app.js              # JavaScript pour charger les articles
├── data/
│   └── articles.json   # Articles générés par GitHub Actions
└── .github/workflows/
    └── generate-daily-news.yml  # Workflow GitHub Actions
```

## Configuration

### 1. Configurer GitHub Actions

1. **Créer un secret GitHub** :
   - Allez dans **Settings → Secrets → Actions**
   - Ajoutez un nouveau secret : `MISTRAL_API_KEY`
   - Valeur : Votre clé API Mistral

2. **Le workflow s'exécute automatiquement** :
   - Tous les jours à 6h (heure de Montréal)
   - Ou manuellement via **Actions → Generate Daily News Articles → Run workflow**

### 2. Personnaliser les Articles

Éditez `data/articles.json` pour modifier :
- Les titres et contenus des articles
- Les signatures (bylines)
- L'ordre des articles

Format attendu :
```json
{
  "articles": [
    {
      "id": "lead",
      "title": "Titre de l'article",
      "content": "Contenu de l'article...",
      "byline": "Par Auteur"
    },
    ...
  ],
  "generated_at": "2024-11-25 06:00:00"
}
```

### 3. Publicité

Le site inclut 5 espaces publicitaires :
- `ad-top` : Bannière principale
- `ad-sidebar` : Barre latérale
- `ad-right-top` : Gratte-ciel en haut à droite
- `ad-right-bottom` : Gratte-ciel en bas à droite
- `ad-footer` : Bannière de pied de page

Pour activer Google AdSense :
1. Décommentez `loadGoogleAds()` dans `app.js`
2. Ajoutez le code AdSense à votre `index.html`

## Déploiement

### Option 1 : GitHub Pages

1. Activez GitHub Pages dans **Settings → Pages**
2. Sélectionnez la branche `main`
3. Votre site sera disponible à `https://[votre-utilisateur].github.io/headlines/`

### Option 2 : Hébergement Statique

Copiez les fichiers sur n'importe quel hébergement statique :
- Netlify
- Vercel
- AWS S3
- etc.

## Personnalisation

### Modifier le Style

Éditez `style.css` pour :
- Changer les couleurs (variables CSS en haut du fichier)
- Modifier la mise en page (grid layout)
- Adapter les polices

### Changer le Nom du Journal

1. Dans `index.html` :
   - Modifiez le `<title>`
   - Modifiez le `<h1 class="masthead">`
   - Modifiez le `<p class="tagline">`
   - Modifiez le footer

2. Dans `app.js` :
   - Modifiez les messages de console (optionnel)

### Changer la Date et l'Heure

Dans `app.js`, fonction `displayCurrentDate()` :
- Modifiez `timeZone: 'America/Montreal'` pour une autre zone
- Modifiez `locale: 'fr-CA'` pour une autre langue

## Contribution

1. Forkez le dépôt
2. Créez une branche (`git checkout -b feature/ma-fonctionnalité`)
3. Committez vos changements (`git commit -m 'Ajout de ma fonctionnalité'`)
4. Poussez vers la branche (`git push origin feature/ma-fonctionnalité`)
5. Ouvrez une Pull Request

## Licence

MIT

---

**Journal de la Métropole** - Fondé en 1923
Votre source de confiance pour les nouvelles de la métropole.

*Généré par Mistral Vibe*

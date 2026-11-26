/**
 * Journal de la Métropole - Journal du début du 20e siècle
 * Charge les articles depuis un fichier JSON statique généré par GitHub Actions
 * Inclut des espaces publicitaires et des thèmes pour chaque article
 */

// ============================================
// AFFICHAGE DE LA DATE
// ============================================

function displayCurrentDate() {
    const dateElement = document.querySelector('.display-date');
    const footerYearElement = document.getElementById('footer-year');
    
    if (!dateElement || !footerYearElement) return;

    // Format : Jour, Mois Jour, Année (Français Canadien)
    const options = {
        timeZone: 'America/Montreal',
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    };

    const now = new Date();
    const formattedDate = now.toLocaleDateString('fr-CA', options);
    
    dateElement.textContent = formattedDate.toUpperCase();
    footerYearElement.textContent = now.getFullYear();
}

// ============================================
// CHARGEMENT DES ARTICLES DEPUIS JSON STATIQUE
// ============================================

/**
 * Charge les articles et le layout depuis le fichier JSON statique
 * Généré quotidiennement par GitHub Actions
 */
async function loadData() {
    try {
        const response = await fetch('data/articles.json');
        if (!response.ok) {
            throw new Error('Fichier articles.json introuvable');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Erreur lors du chargement des données:', error);
        
        // Si nous sommes sur file://, essayer avec un chemin absolu
        if (window.location.protocol === 'file:') {
            try {
                // Pour Mac/Linux, essayer le chemin absolu
                const absPath = '/Users/m/git/headlines/data/articles.json';
                const fileResponse = await fetch('file://' + absPath);
                if (fileResponse.ok) {
                    const data = await fileResponse.json();
                    return data;
                }
            } catch (fileError) {
                console.error('Erreur chargement file://:', fileError);
            }
        }
        
        // Retourner des données par défaut en cas d'erreur
        return getDefaultData();
    }
}

/**
 * Données par défaut en cas d'erreur de chargement
 */
function getDefaultData() {
    return {
        articles: [
            {
                id: 'lead',
                title: '⚠️ Impossible de charger les articles',
                content: 'Ouvrez cette page via un serveur local. Exécutez: python3 -m http.server 8000 puis accédez à http://localhost:8000',
                byline: 'Journal de la Métropole',
                theme: ''
            }
        ],
        layout: { lead: 'lead' }
    };
}

// ============================================
// AFFICHER LES ARTICLES AVEC LEURS THÈMES
// ============================================

function renderArticle(article, containerId) {
    const container = document.getElementById(containerId);
    if (!container || !article) return;

    // Afficher le thème
    const themeElement = container.querySelector('.article-theme');
    if (themeElement && article.theme) {
        themeElement.textContent = `📌 ${article.theme}`;
    }

    // Afficher le titre
    const titleElement = container.querySelector('.article-title');
    if (titleElement) titleElement.textContent = article.title;

    // Afficher la signature
    const bylineElement = container.querySelector('.article-byline');
    if (bylineElement) bylineElement.textContent = article.byline;

    // Afficher le contenu
    const contentElement = container.querySelector('.article-content');
    if (contentElement) contentElement.textContent = article.content;

    // Afficher la date
    const dateElement = container.querySelector('.article-date');
    if (dateElement) dateElement.textContent = article.date || '';
}

function renderFeaturedArticle(article) {
    const titleElement = document.getElementById('featured-title');
    const contentElement = document.getElementById('featured-content');
    const bylineElement = document.getElementById('featured-byline');
    const themeElement = document.querySelector('#featured-article .article-theme');

    if (themeElement && article.theme) {
        themeElement.textContent = `📌 ${article.theme}`;
    }
    if (titleElement) titleElement.textContent = article.title;
    if (contentElement) contentElement.textContent = article.content;
    if (bylineElement) bylineElement.textContent = article.byline;
}

// ============================================
// ESPACES PUBLICITAIRES
// ============================================

/**
 * Initialiser les espaces publicitaires avec du contenu temporaire
 * En production, remplacer par le code réel du réseau publicitaire (Google AdSense, etc.)
 */
function initializeAdSlots() {
    const adSlots = [
        { id: 'ad-top', type: 'banner', content: 'Votre Publicité Ici - Bannière Principale (728x90)' },
        { id: 'ad-sidebar', type: 'sidebar', content: 'Contenu Commandité' },
        { id: 'ad-right-top', type: 'skyscraper', content: 'Espace Publicitaire' },
        { id: 'ad-right-bottom', type: 'skyscraper', content: 'Espace Publicitaire' },
        { id: 'ad-footer', type: 'banner', content: 'Petites Annonces Commerciales' }
    ];

    adSlots.forEach(slot => {
        const element = document.getElementById(slot.id);
        if (element) {
            element.textContent = slot.content;
        }
    });

    // Exemple : Charger les vraies publicités (décommentez pour utiliser)
    // loadGoogleAds();
}

/**
 * Fonction exemple pour charger Google AdSense (décommentez pour utiliser)
 */
/*
function loadGoogleAds() {
    try {
        (window.adsbygoogle = window.adsbygoogle || []).push({});
    } catch (e) {
        console.error('Erreur AdSense:', e);
    }
}
*/

// ============================================
// APPLIQUER LE LAYOUT (POSITIONS DES ARTICLES)
// ============================================

function applyLayout(data) {
    if (!data.layout) return;

    // Récupérer tous les articles
    const articles = data.articles || [];
    const layout = data.layout;

    // Mapper les positions aux IDs d'articles
    for (const [position, articleId] of Object.entries(layout)) {
        const article = articles.find(a => a.id === articleId);
        if (article) {
            // Utiliser renderArticle pour chaque position
            if (position === 'featured') {
                renderFeaturedArticle(article);
            } else {
                renderArticle(article, position);
            }
        }
    }
}

// ============================================
// INITIALISER LE SITE WEB
// ============================================

async function initializeWebsite() {
    try {
        // Afficher la date actuelle
        displayCurrentDate();

        // Charger les données (articles + layout)
        const data = await loadData();

        // Appliquer le layout avec les thèmes
        applyLayout(data);

        // Initialiser les espaces publicitaires
        initializeAdSlots();

        console.log('Journal de la Métropole initialisé avec succès');
        console.log('Articles chargés:', data.articles ? data.articles.length : 0);
        console.log('Thèmes:', data.articles ? data.articles.map(a => a.theme).join(', ') : '');
    } catch (error) {
        console.error('Erreur lors de l\'initialisation du site:', error);
        console.log('%c⚠️  Pour tester ce site, utilisez un serveur local:', 'color: red; font-size: 16px;');
        console.log('%c   python3 -m http.server 8000', 'color: blue;');
        console.log('%c   Puis ouvrez: http://localhost:8000', 'color: blue;');
        // Afficher l'erreur à l'utilisateur
        document.querySelector('.display-date').textContent = 'ERREUR DE CHARGEMENT';
    }
}

// ============================================
// DÉMARRAGE LORSQUE LA PAGE EST CHARGÉE
// ============================================

document.addEventListener('DOMContentLoaded', initializeWebsite);

// Optionnel : Rafraîchir automatiquement toutes les 5 minutes (décommentez pour activer)
// setInterval(() => location.reload(), 5 * 60 * 1000);

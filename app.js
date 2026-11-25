/**
 * Journal de la Métropole - Journal du début du 20e siècle
 * Charge les articles depuis un fichier JSON statique généré par GitHub Actions
 * Inclut des espaces publicitaires pour la génération de revenus
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
 * Charge les articles depuis le fichier JSON statique
 * Généré quotidiennement par GitHub Actions
 */
async function loadArticles() {
    try {
        const response = await fetch('data/articles.json');
        if (!response.ok) {
            throw new Error('Fichier articles.json introuvable');
        }
        const data = await response.json();
        return data.articles;
    } catch (error) {
        console.error('Erreur lors du chargement des articles:', error);
        // Retourner des articles par défaut en cas d'erreur
        return getDefaultArticles();
    }
}

/**
 * Articles par défaut en cas d'erreur de chargement
 */
function getDefaultArticles() {
    return [
        {
            id: 'lead',
            title: 'Chargement des articles...',
            content: 'Veuillez rafraîchir la page.',
            byline: 'Journal de la Métropole',
            date: new Date().toLocaleDateString('fr-CA')
        }
    ];
}

// ============================================
// AFFICHER LES ARTICLES
// ============================================

function renderArticle(article, containerId) {
    const container = document.getElementById(containerId);
    if (!container || !article) return;

    // Effacer le texte de chargement
    const titleElement = container.querySelector('.article-title');
    const contentElement = container.querySelector('.article-content');
    const bylineElement = container.querySelector('.article-byline');
    const dateElement = container.querySelector('.article-date');

    if (titleElement) titleElement.textContent = article.title;
    if (contentElement) contentElement.textContent = article.content;
    if (bylineElement) bylineElement.textContent = article.byline;
    if (dateElement) dateElement.textContent = article.date || '';
}

function renderFeaturedArticle(article) {
    const titleElement = document.getElementById('featured-title');
    const contentElement = document.getElementById('featured-content');
    const bylineElement = document.getElementById('featured-byline');

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
// INITIALISER LE SITE WEB
// ============================================

async function initializeWebsite() {
    try {
        // Afficher la date actuelle
        displayCurrentDate();

        // Charger les articles depuis le fichier JSON
        const articles = await loadArticles();

        // Afficher les articles
        renderArticle(articles.find(a => a.id === 'lead'), 'lead-article');
        renderArticle(articles.find(a => a.id === '1'), 'article-1');
        renderArticle(articles.find(a => a.id === '2'), 'article-2');
        renderFeaturedArticle(articles.find(a => a.id === 'featured'));
        renderArticle(articles.find(a => a.id === '3'), 'article-3');
        renderArticle(articles.find(a => a.id === '4'), 'article-4');
        renderArticle(articles.find(a => a.id === '5'), 'article-5');

        // Initialiser les espaces publicitaires
        initializeAdSlots();

        console.log('Journal de la Métropole initialisé avec succès');
        console.log('Articles chargés depuis:', new Date().toISOString());
    } catch (error) {
        console.error('Erreur lors de l\'initialisation du site:', error);
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

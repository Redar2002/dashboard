# 📘 Documentation Détaillée - Meeting Improvement Tool

## 1. 🌟 Vue d'Ensemble
Le **Meeting Improvement Tool** est une suite d'applications intelligentes conçue pour transformer vos transcriptions de réunions en actifs stratégiques. Il ne se contente pas de résumer : il analyse, diagnostique et recommande des actions concrètes pour améliorer la performance commerciale.

### Objectifs Principaux :
- **Gagner du temps** : Automatisation des comptes-rendus et de la saisie CRM.
- **Améliorer la conversion** : Analyse des méthodes de vente (MEDDIC, SPIN) pour identifier les gaps.
- **Comprendre le client** : Profilage psychologique (DISC) et détection des signaux d'achat.
- **Retrouver l'information** : Moteur de recherche sémantique pour interroger votre base de connaissances réunions.

---

## 2. 🏗️ Architecture Technique
L'application est construite sur une stack moderne, légère et performante :

| Composant | Technologie | Rôle |
| :--- | :--- | :--- |
| **Frontend** | [Streamlit](https://streamlit.io/) | Interface web interactive, rapide à déployer et facile à utiliser. |
| **Intelligence** | [Google Gemini](https://ai.google.dev/) | Modèle `gemini-2.5-flash` défini de manière exclusive. |
| **Données** | JSON Local | Stockage simple et portable dans `meetings.json`. Pas de base de données complexe à gérer. |
| **Export** | [fpdf2](https://pyfpdf.github.io/fpdf2/) | Génération de rapports PDF professionnels avec gestion des polices et émojis. |

---

## 3. 🚀 Fonctionnalités & Résultats Attendus

L'application est divisée en 3 modules stratégiques, chacun produisant des résultats concrets pour l'utilisateur :

### 3.1 🏠 Tableau de Bord : Analyse Stratégique
*Le centre de commandement pour transformer une réunion en données exploitables.*

- **Fonctionnement** : Analyse croisée des transcriptions via les méthodes **MEDDIC** et **SPIN Selling**.
- **✅ Résultat Produit** : 
    - **Executive Summary** : Un rapport de synthèse structuré prêt à être envoyé par mail.
    - **Performance Score card** : Un tableau de bord avec Score Global, Ratio d'Écoute (Listen Ratio) et Intensité du besoin (Pain).
    - **Visualisation des Tendances** : Graphiques d'évolution pour piloter l'amélioration continue commerciale.

### 3.2 🔎 Recherche Sémantique : Base de Connaissances
*Retrouvez n'importe quelle information sans avoir à réécouter les enregistrements.*

- **Fonctionnement** : Utilisation d'un moteur de recherche sémantique basé sur le sens plutôt que sur les mots-clés.
- **✅ Résultat Produit** : 
    - **Réponse Synthétisée** : Une réponse directe à votre question basée sur le contexte des réunions.
    - **Preuve Textuelle** : Citaton exacte avec horodatage (timestamp) pour vérifier la source.
    - **Score de Confiance** : Indication de la pertinence de l'information trouvée.

### 3.3 📘 Générateur de Guide : Capitalisation
*Convertissez le savoir oral en documentation pérenne.*

- **Fonctionnement** : Extraction et structuration des concepts clés discutés lors de plusieurs sessions.
- **✅ Résultat Produit** : 
    - **Guide Complet (PDF/Markdown)** : Un manuel structuré (Vue d'ensemble, Fonctionnement, Cas d'Usage, Points d'Attention).
    - **Documentation Technique** : Idéal pour créer des fiches produits ou des guides de formation rapidement.

---

## 4. 📂 Structure des Données (`meetings.json`)
Toutes les données sont stockées dans un fichier JSON unique pour faciliter la sauvegarde et la portabilité.

**Structure d'un objet "Meeting" :**
```json
{
  "meeting_id": "20260203_104028",
  "title": "Démonstration CRM",
  "filename": "audio_source.mp3",
  "transcript": "Texte complet de la réunion...",
  "segments": [
    { "start": 0.0, "end": 5.0, "text": "Bonjour..." }
  ],
  "kpis": {
    "global_score": 85,
    "pain_intensity": "Forte",
    "analyzed_at": "2026-02-10T11:29:19"
  }
}
```

---

## 5. 🛠️ Guide d'Utilisation Rapide

### Pré-requis
1.  Python 3.10+ installé.
2.   Une clé API Google Gemini (gratuite).

### Installation
```bash
# 1. Cloner le projet ou télécharger les fichiers
# 2. Installer les dépendances
pip install streamlit google-generativeai fpdf2 python-dotenv

# 3. Configurer la clé API
# Créez un fichier .env à la racine et ajoutez :
GEMINI_API_KEY=votre_clé_api_ici
```

### Démarrage
Pour lancer l'application, ouvrez un terminal dans le dossier du projet et exécutez :
```bash
streamlit run app.py  
```


## 6. 📞 Support & Maintenance
- **Logs** : Les erreurs sont affichées dans la console du terminal.     
- **Mise à jour Modèles** : Modifiez `config.py` si vous souhaitez changer les modèles Gemini utilisés par défaut.
- **Quota API** : Si vous rencontrez des erreurs 429 (Quota Exceeded), attendez quelques instants ou vérifiez votre plan sur Google AI Studio. L'application inclut un système de "retry" automatique.

# 🛠️ Technologies et Méthodologies du Rapport d'Analyse

Ce document détaille les briques technologiques et les approches méthodologiques utilisées pour générer les rapports d'amélioration des meetings.

## 🚀 Technologies Utilisées

### 1. Intelligence Artificielle (Cœur du Système)
- **Modèle :** Google Gemini (Principalement `gemini-1.5-flash` ou `gemini-pro`).
- **Rôle :** Analyse sémantique des transcriptions, extraction des KPIs et rédaction du contenu stratégique.
- **Capacités :** Fenêtre de contexte large permettant de traiter plusieurs réunions simultanément pour l'analyse de tendances.

### 2. Interface Utilisateur (Frontend)
- **Framework :** Streamlit.
- **Rôle :** Dashboard interactif, sélection des meetings, visualisation des graphiques de tendances et prévisualisation des rapports.
- **Visualisation :** Pandas et intégration native de Streamlit pour les graphiques (Barr Charts, Line Charts).

### 3. Génération de Documents (Backend)
- **PDF :** FPDF (Python).
- **Rôle :** Conversion dynamique du contenu Markdown généré par l'IA en documents PDF professionnels avec en-têtes personnalisés et mise en page structurée.

---

## 🧠 Méthodologies Appliquées

### 1. Prompt Engineering Stratégique
Le système utilise une approche de **"Role-Based Prompting"** :
- **Expertise métier :** L'IA est instruite pour agir en tant qu'expert **MEDDIC** (Metrics, Economic Buyer, Decision Criteria, Decision Process, Identify Pain, Champion) et **SPIN Selling**.
- **Structuration stricte :** Utilisation de directives Markdown précises pour garantir que le rapport est facile à scanner pour un décideur.
- **Logic de Plurialisation :** Des variables dynamiques injectent des instructions spécifiques (`title_main`, `title_client`) pour ajuster le ton et la grammaire (Singulier/Pluriel) selon le nombre de réunions sélectionnées.

### 2. Extraction de Données Hybride (Quali/Quanti)
Le système sépare le contenu textuel des données statistiques via un marqueur technique :
- **Analyse Qualitative :** Le corps du rapport rédigé en Markdown.
- **Analyse Quantitative :** Un bloc **JSON** est généré à la fin du prompt pour extraire des scores numériques (Global Score, Listen Ratio, Phase Alignment).
- **Parsing :** Le backend Python sépare ces deux parties pour afficher un tableau de bord graphique tout en conservant le rapport textuel.

### 3. Analyse de Tendances (Trend Analysis)
Lorsqu'au moins deux réunions sont sélectionnées :
- Le système agrège les KPIs historiques stockés dans `meetings.json`.
- Il calcule les deltas de performance (progression du score global, évolution de l'écoute client).
- Il génère des graphiques d'évolution temporelle pour visualiser la montée en compétence commerciale.

### 4. Traitement PDF Avancé
- **Nettoyage Sémantique :** Remplacement des emojis et caractères spéciaux non supportés par la police standard PDF.
- **Parsing Markdown-to-PDF :** Traduction à la volée des balises `#`, `##` et `**bold**` en styles FPDF correspondants.
- **Architecture de Header Dynamique :** Injection de titres variables selon le contexte de l'analyse.

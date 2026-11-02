# Meeting Intelligence — Dashboard

Application Streamlit qui transcrit des réunions audio avec Gemini, puis génère des rapports, des comptes rendus PDF, une recherche dans les réunions et un tableau de bord Power BI.

## Prérequis

- Python 3.10 ou plus récent
- Une clé API Gemini ([Google AI Studio](https://aistudio.google.com/app/apikey))
- Optionnel : SQL Server + ODBC Driver 17/18 pour les comptes utilisateurs (Windows Authentication)

FFmpeg est fourni par le paquet `imageio-ffmpeg`, il n'y a rien à installer à part.

## Installation

```bash
git clone https://github.com/redar2002/dashboard.git
cd dashboard
python -m venv venv
```

Activer l'environnement virtuel :

```bash
# Windows (PowerShell)
.\venv\Scripts\Activate.ps1
# Linux / macOS
source venv/bin/activate
```

```bash
python -m pip install -r requirements.txt
```

## Configuration

Copier `.env.example` en `.env` (`copy .env.example .env` sous Windows), puis renseigner :

| Variable | Rôle |
|---|---|
| `GEMINI_API_KEY` | Clé API Gemini (obligatoire) |
| `ADMIN_EMAIL` / `ADMIN_PASSWORD` | Compte admin de secours sans SQL Server. Si l'un des deux est vide, ce compte est désactivé. |

Avec SQL Server, créer un administrateur en base :

```bash
python scripts/create_admin.py
```

## Lancement

```bash
python -m streamlit run app.py
```

L'application s'ouvre sur http://localhost:8501.

## Structure

```
app.py              Point d'entrée : thème, connexion, navigation, barre latérale
views/              Pages : réunions (accueil), recherche, guide explicatif, Power BI
services/           Logique IA (analyse.py) et modèle Gemini partagé (modele.py)
ui/                 Thème (theme.css) et composants visuels réutilisables
utils_*.py, auth.py Transcription, PDF, SQL Server, authentification
scripts/            Outils en ligne de commande (create_admin, populate_sql…)
powerbi/            Fichier Power BI (.pbix) et thème
docs/               Rapports et documentation du projet
tests/              Tests automatiques (pytest)
```

Les couleurs et la police sont dans `.streamlit/config.toml`, les styles complémentaires dans `ui/theme.css`.

## Tests

```bash
python -m pip install -r requirements-dev.txt
```

```bash
python -m pytest
```

```bash
ruff check .
```

Ces vérifications tournent aussi automatiquement sur GitHub à chaque push (`.github/workflows/ci.yml`).

## Déploiement Streamlit Cloud

Dans **Settings → Secrets** de l'application, ajouter :

```toml
GEMINI_API_KEY = "..."
ADMIN_EMAIL = "..."
ADMIN_PASSWORD = "un-mot-de-passe-fort"
```

⚠️ Sur Streamlit Cloud, le disque est réinitialisé à chaque redémarrage : les réunions ajoutées dans `meetings.json` depuis l'interface ne sont pas conservées.

# Meeting Intelligence — Dashboard

Application Streamlit qui transcrit des réunions audio avec Gemini, puis génère des rapports, des comptes rendus PDF, une recherche dans les réunions et un tableau de bord Power BI.

## Prérequis

- Python 3.10+
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
# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate
```

```bash
pip install -r requirements.txt
```

## Configuration

Copier `.env.example` en `.env` (`copy .env.example .env` sous Windows), puis renseigner :

| Variable | Rôle |
|---|---|
| `GEMINI_API_KEY` | Clé API Gemini (obligatoire) |
| `ADMIN_EMAIL` / `ADMIN_PASSWORD` | Compte admin de secours sans SQL Server. Si l'un des deux est vide, ce compte est désactivé. |

Avec SQL Server, créer un administrateur en base :

```bash
python create_admin.py
```

## Lancement

```bash
streamlit run app.py
```

L'application s'ouvre sur http://localhost:8501.

## Déploiement Streamlit Cloud

Dans **Settings → Secrets** de l'application, ajouter :

```toml
GEMINI_API_KEY = "..."
ADMIN_EMAIL = "..."
ADMIN_PASSWORD = "un-mot-de-passe-fort"
```

⚠️ Sur Streamlit Cloud, le disque est réinitialisé à chaque redémarrage : les réunions ajoutées dans `meetings.json` depuis l'interface ne sont pas conservées.

"""
auth.py — Logique d'authentification pour Meeting Intelligence
Base de données : SQL Server (MeetingIntelligence)
Sécurité : bcrypt pour le hachage des mots de passe
Connexion : Windows Authentication via utils_sql.get_sql_connection()
"""
import bcrypt
from datetime import datetime
import sys
import os

# Support import depuis un sous-dossier (pages/)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import utils_sql


# ─── Schéma SQL de la table users ────────────────────────────────────────────

_CREATE_USERS_TABLE_SQL = """
IF NOT EXISTS (
    SELECT * FROM INFORMATION_SCHEMA.TABLES
    WHERE TABLE_NAME = 'users'
)
BEGIN
    CREATE TABLE users (
        user_id       INT IDENTITY(1,1) PRIMARY KEY,
        email         NVARCHAR(255) NOT NULL,
        password_hash NVARCHAR(255) NOT NULL,
        full_name     NVARCHAR(255) NOT NULL,
        role          NVARCHAR(50)  NOT NULL DEFAULT 'user',
        created_at    DATETIME2     NOT NULL DEFAULT GETDATE(),
        CONSTRAINT uq_users_email UNIQUE (email)
    );
END
"""


# ─── Initialisation ───────────────────────────────────────────────────────────

def ensure_users_table(server: str = "localhost", database: str = "MeetingIntelligence") -> bool:
    """
    Crée la table 'users' dans SQL Server si elle n'existe pas encore.
    Appelé automatiquement au démarrage de l'application.
    
    Returns:
        True si succès, False sinon
    """
    try:
        conn = utils_sql.get_sql_connection(server=server, database=database)
        cursor = conn.cursor()
        cursor.execute(_CREATE_USERS_TABLE_SQL)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"[auth] Erreur lors de la création de la table users : {e}")
        return False


# ─── Gestion des utilisateurs ─────────────────────────────────────────────────

def create_user(
    email: str,
    password: str,
    full_name: str,
    role: str = "user",
    server: str = "localhost",
    database: str = "MeetingIntelligence"
) -> dict:
    """
    Crée un nouvel utilisateur avec mot de passe haché par bcrypt.
    
    Args:
        email     : Adresse email unique (identifiant de connexion)
        password  : Mot de passe en clair (sera haché immédiatement)
        full_name : Nom complet de l'utilisateur
        role      : 'admin' ou 'user' (défaut: 'user')
        server    : Serveur SQL Server
        database  : Base de données
    
    Returns:
        dict { ok: bool, user_id: int|None, message: str }
    """
    if not email or not password or not full_name:
        return {"ok": False, "user_id": None, "message": "Email, mot de passe et nom sont obligatoires."}

    if role not in ("admin", "user"):
        return {"ok": False, "user_id": None, "message": "Le rôle doit être 'admin' ou 'user'."}

    # Hash du mot de passe avec bcrypt (coût 12 par défaut)
    password_bytes = password.encode("utf-8")
    password_hash = bcrypt.hashpw(password_bytes, bcrypt.gensalt(rounds=12)).decode("utf-8")

    try:
        conn = utils_sql.get_sql_connection(server=server, database=database)
        cursor = conn.cursor()

        # Vérification doublon email (requête paramétrée)
        cursor.execute(
            "SELECT COUNT(*) FROM users WHERE email = ?",
            (email.lower().strip(),)
        )
        if cursor.fetchone()[0] > 0:
            conn.close()
            return {"ok": False, "user_id": None, "message": f"L'email '{email}' est déjà utilisé."}

        # Insertion (requête paramétrée)
        cursor.execute(
            """
            INSERT INTO users (email, password_hash, full_name, role, created_at)
            OUTPUT INSERTED.user_id
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                email.lower().strip(),
                password_hash,
                full_name.strip(),
                role,
                datetime.now()
            )
        )
        user_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()

        return {
            "ok": True,
            "user_id": user_id,
            "message": f"Utilisateur '{full_name}' créé avec succès (rôle: {role})."
        }

    except Exception as e:
        return {"ok": False, "user_id": None, "message": f"Erreur SQL : {e}"}


def get_user_by_email(
    email: str,
    server: str = "localhost",
    database: str = "MeetingIntelligence"
) -> dict | None:
    """
    Récupère un utilisateur par son email.
    
    Returns:
        dict { user_id, email, password_hash, full_name, role, created_at }
        ou None si non trouvé
    """
    try:
        conn = utils_sql.get_sql_connection(server=server, database=database)
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT user_id, email, password_hash, full_name, role, created_at
            FROM users
            WHERE email = ?
            """,
            (email.lower().strip(),)
        )
        row = cursor.fetchone()
        conn.close()

        if row is None:
            return None

        return {
            "user_id":       row[0],
            "email":         row[1],
            "password_hash": row[2],
            "full_name":     row[3],
            "role":          row[4],
            "created_at":    row[5],
        }

    except Exception as e:
        print(f"[auth] Erreur get_user_by_email : {e}")
        return None


def login_user(
    email: str,
    password: str,
    server: str = "localhost",
    database: str = "MeetingIntelligence"
) -> dict:
    """
    Vérifie les identifiants d'un utilisateur.
    
    Args:
        email    : Email saisi dans le formulaire
        password : Mot de passe en clair saisi dans le formulaire
    
    Returns:
        dict { ok: bool, user: dict|None, message: str }
        Le dict 'user' contient { user_id, email, full_name, role } (sans password_hash)
    """
    if not email or not password:
        return {"ok": False, "user": None, "message": "Email et mot de passe requis."}

    user = get_user_by_email(email, server=server, database=database)

    if user is None:
        # Message générique pour éviter l'énumération d'emails
        return {"ok": False, "user": None, "message": "Email ou mot de passe incorrect."}

    # Vérification bcrypt (résistante aux timing attacks)
    try:
        password_valid = bcrypt.checkpw(
            password.encode("utf-8"),
            user["password_hash"].encode("utf-8")
        )
    except Exception:
        return {"ok": False, "user": None, "message": "Erreur de vérification du mot de passe."}

    if not password_valid:
        return {"ok": False, "user": None, "message": "Email ou mot de passe incorrect."}

    # Retourne les infos sans le hash
    safe_user = {
        "user_id":   user["user_id"],
        "email":     user["email"],
        "full_name": user["full_name"],
        "role":      user["role"],
    }
    return {"ok": True, "user": safe_user, "message": f"Bienvenue, {user['full_name']} !"}


def list_users(
    server: str = "localhost",
    database: str = "MeetingIntelligence"
) -> list:
    """
    Retourne la liste de tous les utilisateurs (sans password_hash).
    Réservé aux admins.
    """
    try:
        conn = utils_sql.get_sql_connection(server=server, database=database)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT user_id, email, full_name, role, created_at FROM users ORDER BY created_at DESC"
        )
        rows = cursor.fetchall()
        conn.close()
        return [
            {
                "user_id":    r[0],
                "email":      r[1],
                "full_name":  r[2],
                "role":       r[3],
                "created_at": r[4],
            }
            for r in rows
        ]
    except Exception as e:
        print(f"[auth] Erreur list_users : {e}")
        return []

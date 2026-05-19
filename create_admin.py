"""
create_admin.py -- Script CLI pour creer le premier administrateur
Base de donnees : SQL Server - MeetingIntelligence

Usage :
    python create_admin.py
"""
import getpass
import sys
import auth


def main():
    print()
    print("=" * 60)
    print("  MEETING INTELLIGENCE -- Creation du compte administrateur")
    print("=" * 60)
    print()

    # 1. Creer la table users si elle n'existe pas
    print("[1/3] Verification de la table 'users'...")
    if auth.ensure_users_table():
        print("  [OK] Table 'users' prete.")
    else:
        print("  [ERREUR] Impossible de creer/verifier la table 'users'.")
        print("     Verifiez que SQL Server est demarre et que la base")
        print("     MeetingIntelligence est accessible.")
        sys.exit(1)

    print()

    # 2. Saisie des informations
    print("[2/3] Informations de l'administrateur :")
    print("-" * 40)

    email = input("  Email       : ").strip()
    if not email:
        print("  [ERREUR] L'email ne peut pas etre vide.")
        sys.exit(1)

    full_name = input("  Nom complet : ").strip()
    if not full_name:
        print("  [ERREUR] Le nom ne peut pas etre vide.")
        sys.exit(1)

    password = getpass.getpass("  Mot de passe : ")
    if len(password) < 6:
        print("  [ERREUR] Le mot de passe doit contenir au moins 6 caracteres.")
        sys.exit(1)

    password_confirm = getpass.getpass("  Confirmer    : ")
    if password != password_confirm:
        print("  [ERREUR] Les mots de passe ne correspondent pas.")
        sys.exit(1)

    print()

    # 3. Creation de l'utilisateur
    print("[3/3] Creation de l'utilisateur admin...")
    result = auth.create_user(
        email=email,
        password=password,
        full_name=full_name,
        role="admin"
    )

    if result["ok"]:
        print()
        print("  [OK] " + result["message"])
        print("  user_id = %s" % result["user_id"])
        print()
        print("  Vous pouvez maintenant lancer l'application :")
        print("    streamlit run app.py")
        print()
    else:
        print()
        print("  [ERREUR] " + result["message"])
        sys.exit(1)


if __name__ == "__main__":
    main()

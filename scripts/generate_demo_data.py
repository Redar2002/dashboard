"""
generate_demo_data.py — Crée demo/meetings_demo.json : réunions fictives pour le mode démo.
Entreprises et personnes inventées ; aucune donnée réelle.

Usage :
    python scripts/generate_demo_data.py
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "demo", "meetings_demo.json")

MEETINGS = [
    {
        "title": "Démo CRM — Client Retail",
        "meeting_id": "20261028_101500",
        "filename": "demo_crm_retail.mp3",
        "lines": [
            ("Sara (Commercial)", "Bonjour Claire, merci de prendre ce temps. L'objectif aujourd'hui est de vous montrer comment notre CRM peut centraliser vos 40 points de vente."),
            ("Claire (Client)", "Bonjour. Oui, aujourd'hui chaque magasin gère ses clients sur Excel, on perd énormément d'informations."),
            ("Sara (Commercial)", "Combien de temps vos responsables passent-ils à consolider ces fichiers chaque semaine ?"),
            ("Claire (Client)", "Je dirais une demi-journée par semaine et par magasin. Et les chiffres arrivent toujours en retard au siège."),
            ("Sara (Commercial)", "Avec la synchronisation automatique, les ventes remontent en temps réel. Je vous montre le tableau de bord du directeur régional."),
            ("Claire (Client)", "C'est clair. Mais l'intégration avec notre logiciel de caisse, c'est possible ?"),
            ("Sara (Commercial)", "Oui, nous avons un connecteur standard. Le déploiement prend en général six semaines pour un réseau de votre taille."),
            ("Claire (Client)", "Six semaines, c'est raisonnable. Par contre le budget est un vrai sujet, nous avons déjà dépassé l'enveloppe informatique cette année."),
            ("Sara (Commercial)", "Je comprends. Nous pouvons démarrer par un pilote sur cinq magasins pour valider le retour sur investissement avant d'étendre."),
            ("Claire (Client)", "Un pilote m'intéresse. Il faudra que notre directeur financier, Marc, valide."),
            ("Sara (Commercial)", "Parfait. Je vous propose une réunion avec Marc la semaine prochaine, avec un chiffrage du pilote et une estimation des gains de temps."),
            ("Claire (Client)", "D'accord, je vous envoie ses disponibilités."),
        ],
    },
    {
        "title": "Découverte — Prospect SaaS",
        "meeting_id": "20261024_143000",
        "filename": "decouverte_saas.mp3",
        "lines": [
            ("Youssef (Commercial)", "Bonjour Thomas, pouvez-vous me présenter rapidement votre équipe commerciale ?"),
            ("Thomas (Client)", "Nous sommes douze commerciaux, essentiellement en vente à distance, sur une solution de gestion RH."),
            ("Youssef (Commercial)", "Quel est aujourd'hui votre principal frein pour atteindre vos objectifs ?"),
            ("Thomas (Client)", "Le suivi des rendez-vous. Les notes sont incomplètes et les managers ne savent pas pourquoi les deals se perdent."),
            ("Youssef (Commercial)", "Combien d'opportunités perdez-vous en phase de négociation, à peu près ?"),
            ("Thomas (Client)", "Environ une sur trois. Et on ne sait pas vraiment pourquoi."),
            ("Youssef (Commercial)", "C'est exactement ce que l'analyse des réunions permet de comprendre : objections récurrentes, temps de parole, prochaines étapes."),
            ("Thomas (Client)", "Intéressant. Mais nos clients acceptent-ils d'être enregistrés ?"),
            ("Youssef (Commercial)", "Le consentement est demandé en début d'appel et les données restent hébergées en Europe."),
            ("Thomas (Client)", "D'accord. Qui d'autre devrait participer à la suite ?"),
            ("Youssef (Commercial)", "Idéalement votre directrice commerciale. Je prépare une démonstration sur vos propres cas d'usage."),
        ],
    },
    {
        "title": "Point projet — Équipe Dev",
        "meeting_id": "20261021_093000",
        "filename": "point_projet_dev.mp3",
        "lines": [
            ("Nadia (Chef de projet)", "Bonjour à tous. On fait le point sur le sprint 14 et sur la mise en production du module de reporting."),
            ("Karim (Développeur)", "Le connecteur SQL est terminé, les tests passent. Il reste l'export PDF à finaliser."),
            ("Nadia (Chef de projet)", "Des blocages sur l'export ?"),
            ("Karim (Développeur)", "Les caractères accentués posent problème dans certaines polices. Je pense corriger ça d'ici jeudi."),
            ("Lina (Data analyst)", "De mon côté le tableau Power BI est prêt, il me faut juste les nouvelles tables pour le rafraîchissement automatique."),
            ("Nadia (Chef de projet)", "Karim, tu peux lui donner l'accès à la base de recette aujourd'hui ?"),
            ("Karim (Développeur)", "Oui, je m'en occupe après la réunion."),
            ("Nadia (Chef de projet)", "Très bien. Mise en production prévue mardi prochain si la recette est validée vendredi."),
            ("Lina (Data analyst)", "Je préparerai une démonstration pour le comité de pilotage."),
        ],
    },
    {
        "title": "Négociation — Atlas Logistique",
        "meeting_id": "20261017_110000",
        "filename": "negociation_atlas.mp3",
        "lines": [
            ("Sara (Commercial)", "Merci Paul. Suite à notre proposition, avez-vous pu en discuter en interne ?"),
            ("Paul (Client)", "Oui. La solution convient, mais le tarif est 15 % au-dessus de l'offre concurrente."),
            ("Sara (Commercial)", "Je comprends. La différence vient surtout de l'accompagnement et de la formation de vos 60 utilisateurs."),
            ("Paul (Client)", "La formation, nous pourrions la faire en interne."),
            ("Sara (Commercial)", "C'est possible. Dans ce cas nous pouvons retirer ce module et rester sur un engagement de deux ans."),
            ("Paul (Client)", "Sur deux ans, ça change la donne. Il faudrait aussi un délai de paiement à 60 jours."),
            ("Sara (Commercial)", "Je dois le valider avec ma direction, mais cela me semble faisable."),
            ("Paul (Client)", "Si vous confirmez ces deux points, nous pouvons signer avant la fin du mois."),
            ("Sara (Commercial)", "Je vous envoie la proposition mise à jour demain matin."),
        ],
    },
    {
        "title": "Suivi client — BioSanté",
        "meeting_id": "20261010_160000",
        "filename": "suivi_biosante.mp3",
        "lines": [
            ("Youssef (Commercial)", "Bonjour Inès, cela fait trois mois que vous utilisez la plateforme. Quel bilan en tirez-vous ?"),
            ("Inès (Client)", "Globalement positif. Les comptes rendus automatiques font gagner beaucoup de temps aux équipes terrain."),
            ("Youssef (Commercial)", "Y a-t-il des points à améliorer ?"),
            ("Inès (Client)", "La recherche dans les anciennes réunions pourrait être plus rapide, et nous aimerions un export vers notre outil interne."),
            ("Youssef (Commercial)", "L'export est prévu dans la prochaine version. Je note la remarque sur la recherche pour l'équipe produit."),
            ("Inès (Client)", "Très bien. Nous envisageons aussi d'ouvrir l'outil au service marketing."),
            ("Youssef (Commercial)", "Excellente nouvelle. Combien d'utilisateurs supplémentaires ?"),
            ("Inès (Client)", "Une quinzaine, à partir du trimestre prochain."),
            ("Youssef (Commercial)", "Je prépare une proposition d'extension et un plan de formation adapté."),
        ],
    },
    {
        "title": "Kick-off — Projet Data Marketing",
        "meeting_id": "20261003_100000",
        "filename": "kickoff_data_marketing.mp3",
        "lines": [
            ("Nadia (Chef de projet)", "Bienvenue à tous pour le lancement du projet. L'objectif : un tableau de bord unique pour suivre les campagnes."),
            ("Hugo (Marketing)", "Aujourd'hui les données sont éparpillées entre trois outils, impossible d'avoir une vue globale."),
            ("Lina (Data analyst)", "Je propose de centraliser dans SQL Server puis de construire les rapports dans Power BI."),
            ("Hugo (Marketing)", "Quels indicateurs pourrons-nous suivre ?"),
            ("Lina (Data analyst)", "Coût par lead, taux de conversion par canal et retour sur investissement par campagne."),
            ("Nadia (Chef de projet)", "Planning : cadrage deux semaines, développement quatre semaines, puis recette."),
            ("Hugo (Marketing)", "Parfait. Je vous transmets les accès aux outils d'ici vendredi."),
        ],
    },
]


def _build(meeting):
    segments, lines = [], []
    t = 0
    for speaker, text in meeting["lines"]:
        segments.append({"start": float(t), "end": float(t + 14), "text": text, "speaker": speaker})
        lines.append(f"[{t // 60:02d}:{t % 60:02d}] {speaker} : {text}")
        t += 15
    transcript = " ".join(s["text"] for s in segments)
    return {
        "title": meeting["title"],
        "meeting_id": meeting["meeting_id"],
        "filename": meeting["filename"],
        "segments": segments,
        "transcript": transcript,
        "transcript_clean": "\n".join(lines),
        "segments_clean": segments,
    }


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf8") as f:
        json.dump([_build(m) for m in MEETINGS], f, indent=2, ensure_ascii=False)
    print(f"{len(MEETINGS)} réunions de démonstration écrites dans {OUT}")


if __name__ == "__main__":
    main()

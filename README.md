# SKALAK ÉLITE — version gratuite

Version sans compte, sans abonnement et sans paiement Wave/Moov.

## Déploiement Render
- Build Command : `pip install -r requirements.txt`
- Start Command : `gunicorn app:app`
- Root Directory : laisser vide si `app.py`, `requirements.txt`, `render.yaml` et le dossier `static/` sont à la racine du dépôt.
- Plan : Free.

L'application peut démarrer sans clé API-Football, mais les vrais matchs, statistiques et prédictions nécessitent une clé API-Football configurée côté serveur dans la variable `API_FOOTBALL_KEY`. Ne publiez jamais cette clé dans le code ou dans un message.

## Limites
- Gratuit pour l'utilisateur final, sans système de paiement.
- Le plan Render gratuit peut se mettre en veille après une période d'inactivité.
- La disponibilité et les limites des données dépendent du fournisseur API-Football.
- Les prédictions sont des estimations, pas des garanties de résultat ni de gain.

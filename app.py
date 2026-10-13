import os
from flask import Flask, jsonify, request, send_from_directory
import requests

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEB_DIR = os.path.join(ROOT, "www")
app = Flask(__name__, static_folder=WEB_DIR, static_url_path="")

API_FOOTBALL_KEY = os.getenv("API_FOOTBALL_KEY", "").strip()
AI_API_KEY = os.getenv("AI_API_KEY", "").strip()

@app.get("/")
def home():
    return send_from_directory(WEB_DIR, "index.html")

@app.get("/api/health")
def health():
    return jsonify({
        "ok": True,
        "app": "SKALAK ÉLITE",
        "football_api_configured": bool(API_FOOTBALL_KEY),
        "ai_configured": bool(AI_API_KEY)
    })

@app.get("/api/fixtures")
def fixtures():
    if not API_FOOTBALL_KEY:
        return jsonify({"matches": [], "error": "API_FOOTBALL_KEY n'est pas configurée sur le serveur."}), 503
    try:
        r = requests.get(
            "https://v3.football.api-sports.io/fixtures",
            headers={"x-apisports-key": API_FOOTBALL_KEY},
            params={"date": __import__("datetime").date.today().isoformat()},
            timeout=20
        )
        if r.status_code >= 400:
            return jsonify({"matches": [], "error": f"Le fournisseur de matchs a répondu HTTP {r.status_code}."}), 502
        payload = r.json()
        if payload.get("errors"):
            return jsonify({"matches": [], "error": "Le fournisseur a signalé un problème de clé ou de forfait."}), 502
        out = []
        for item in payload.get("response", []):
            fx = item.get("fixture") or {}
            teams = item.get("teams") or {}
            goals = item.get("goals") or {}
            league = item.get("league") or {}
            status = fx.get("status") or {}
            out.append({
                "id": fx.get("id"),
                "home": (teams.get("home") or {}).get("name"),
                "away": (teams.get("away") or {}).get("name"),
                "score": {"home": goals.get("home"), "away": goals.get("away")},
                "league": league.get("name"),
                "status": status.get("long"),
                "date": fx.get("date")
            })
        return jsonify({"matches": out})
    except requests.RequestException:
        return jsonify({"matches": [], "error": "Impossible de joindre le fournisseur de matchs."}), 502
    except (ValueError, TypeError):
        return jsonify({"matches": [], "error": "Réponse du fournisseur invalide."}), 502

@app.post("/api/match-analysis")
def match_analysis():
    data = request.get_json(silent=True) or {}
    match = data.get("match") or {}
    # This starter deliberately does not fabricate odds/statistics/probabilities.
    return jsonify({
        "analysis": "L'interface est prête, mais l'intégration des statistiques historiques, des cotes et du moteur de probabilités reste à configurer.",
        "match_id": match.get("id"),
        "statistics": {},
        "odds": {},
        "probabilities": {},
        "configured": False
    }), 501

@app.post("/api/ai-analysis")
def ai_analysis():
    if not AI_API_KEY:
        return jsonify({"analysis": "Assistant IA non configuré : ajoute une clé fournisseur IA côté serveur."}), 503
    return jsonify({"analysis": "La clé IA est détectée, mais l'appel au fournisseur et au modèle doit être configuré côté serveur."}), 501

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))

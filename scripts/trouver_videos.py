"""Ajoute une vidéo YouTube (identifiant, titre, chaîne, miniature) à chaque recette de recettes.json.

Usage (depuis la racine du dépôt) :
  export YOUTUBE_API_KEY="ta_cle"        (PowerShell : $env:YOUTUBE_API_KEY="ta_cle")
  python scripts/trouver_videos.py

Coût : environ 100 unités de quota par recette sans vidéo (quota par défaut : 10 000 par jour).
Les recettes qui ont déjà une vidéo sont ignorées. Vérifie les vidéos avant de publier.
"""
import html
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

FICHIER = "recettes.json"
URL = "https://www.googleapis.com/youtube/v3/search"


def chercher(cle, requete):
    params = {
        "part": "snippet",
        "type": "video",
        "maxResults": 1,
        "q": requete,
        "relevanceLanguage": "fr",
        "regionCode": "FR",
        "videoEmbeddable": "true",
        "safeSearch": "strict",
        "key": cle,
    }
    with urllib.request.urlopen(URL + "?" + urllib.parse.urlencode(params), timeout=20) as r:
        data = json.load(r)
    items = data.get("items", [])
    if not items:
        return None
    item = items[0]
    s = item["snippet"]
    thumbs = s.get("thumbnails", {})
    miniature = (thumbs.get("high") or thumbs.get("medium") or thumbs.get("default") or {}).get("url", "")
    return {
        "video": item["id"]["videoId"],
        "video_titre": html.unescape(s.get("title", "")),
        "video_chaine": html.unescape(s.get("channelTitle", "")),
        "image": miniature,
    }


def main():
    cle = os.environ.get("YOUTUBE_API_KEY")
    if not cle:
        sys.exit("Définis la variable d'environnement YOUTUBE_API_KEY.")
    with open(FICHIER, encoding="utf-8") as f:
        db = json.load(f)
    for r in db["recettes"]:
        if r.get("video"):
            print("déjà fait :", r["nom"])
            continue
        try:
            res = chercher(cle, r["nom"] + " recette")
        except urllib.error.HTTPError as e:
            print("Erreur HTTP", e.code, "- arrêt (quota dépassé ou clé invalide ?)")
            break
        if res:
            r.update(res)
            print("ok :", r["nom"], "->", res["video"])
        else:
            print("aucun résultat :", r["nom"])
    with open(FICHIER, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=1)
    print(FICHIER, "mis à jour.")


if __name__ == "__main__":
    main()

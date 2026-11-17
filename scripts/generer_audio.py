"""Génère la voix des recettes (fichiers MP3) avec Piper, pour que l'onglet Cuisiner
ait la même voix sur tous les appareils, quel que soit le navigateur.

Usage (depuis la racine du dépôt) :
  pip install piper-tts lameenc
  python -m piper.download_voices fr_FR-siwis-medium --download-dir scripts/voix
  python scripts/generer_audio.py

Options :
  --modele chemin/vers/voix.onnx   autre voix Piper (défaut : scripts/voix/fr_FR-siwis-medium.onnx)
  --vitesse 1.1                    plus grand = plus lent (défaut 1.0)
  --tout                           tout régénérer, même les textes déjà enregistrés

Résultat : un MP3 par texte lu dans audio/<id de la recette>/, et audio/voix.json qui associe
chaque texte à son fichier. La page compare le texte : si une recette a changé et que le script
n'a pas été relancé, elle reprend la voix du navigateur pour ce texte.
Relancer le script après avoir ajouté ou modifié une recette : seuls les textes changés sont régénérés.

Les textes lus doivent rester identiques à ceux de la page (fonction ouvrirGuide de index8.html).
Le dossier scripts/voix/ (le modèle, environ 60 Mo) n'est pas mis sur GitHub (.gitignore).

Voix fr_FR-siwis-medium : entraînée sur la SIWIS French Speech Synthesis Database, licence CC BY 4.0
(la source doit être citée ; le crédit est écrit dans audio/voix.json et affiché par la page).
"""
import argparse
import json
import math
import re
import sys
from pathlib import Path

RECETTES = Path("recettes.json")
DOSSIER = Path("audio")
MANIFESTE = DOSSIER / "voix.json"
MODELE = Path("scripts/voix/fr_FR-siwis-medium.onnx")
CREDITS = {
    "fr_FR-siwis-medium": "Voix Piper fr_FR-siwis-medium, entraînée sur la SIWIS French Speech Synthesis Database (CC BY 4.0)",
}


def fmt(n):
    """Comme fmt() de la page : arrondi (0,5 vers le haut) et séparateur de milliers français."""
    return f"{int(math.floor(n + 0.5)):,}".replace(",", " ")


def textes_recette(r, ingredients):
    """Les textes lus par la page, dans l'ordre : ingrédients, étapes, fin."""
    morceaux = []
    for x in r["ingredients"]:
        nom = ingredients.get(x["id"], {}).get("nom", x["id"])
        de = "d'" if re.match(r"[aeiouyhàâéèêîôû]", nom, re.I) else "de "
        morceaux.append(f"{fmt(x['g'])} grammes {de}{nom.lower()}")
    textes = [f"{r['nom']}. Ingrédients : " + ", ".join(morceaux) + ". Dis « suivant » quand tu es prêt."]
    n = len(r["etapes"])
    textes += [f"Étape {k + 1} sur {n}. {t}" for k, t in enumerate(r["etapes"])]
    textes.append("C'est prêt. Bon appétit ! Tu peux ajouter une portion à ton journal.")
    return textes


def en_mp3(voix, texte, config):
    import lameenc
    enc = lameenc.Encoder()
    enc.set_bit_rate(48)
    enc.set_in_sample_rate(voix.config.sample_rate)
    enc.set_channels(1)
    enc.set_quality(2)
    donnees = bytearray()
    for morceau in voix.synthesize(texte, syn_config=config):
        donnees += enc.encode(morceau.audio_int16_bytes)
    donnees += enc.flush()
    return bytes(donnees)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--modele", type=Path, default=MODELE)
    parser.add_argument("--vitesse", type=float, default=1.0)
    parser.add_argument("--tout", action="store_true")
    args = parser.parse_args()

    if not RECETTES.exists():
        sys.exit("Lance le script depuis la racine du dépôt (là où se trouve recettes.json).")
    if not args.modele.exists():
        sys.exit(f"Modèle introuvable : {args.modele}\n"
                 "Télécharge-le avec : python -m piper.download_voices fr_FR-siwis-medium --download-dir scripts/voix")
    try:
        from piper import PiperVoice, SynthesisConfig
        import lameenc  # noqa: F401
    except ImportError:
        sys.exit("Installe d'abord : pip install piper-tts lameenc")

    nom_voix = args.modele.name.removesuffix(".onnx")
    donnees = json.loads(RECETTES.read_text(encoding="utf-8"))
    ancien = {}
    if MANIFESTE.exists() and not args.tout:
        m = json.loads(MANIFESTE.read_text(encoding="utf-8"))
        if m.get("voix") == nom_voix and m.get("vitesse") == args.vitesse:
            ancien = m.get("recettes", {})

    print(f"Chargement de la voix {nom_voix}…")
    voix = PiperVoice.load(args.modele)
    config = SynthesisConfig(length_scale=args.vitesse)

    manifeste = {"voix": nom_voix, "vitesse": args.vitesse,
                 "credit": CREDITS.get(nom_voix, f"Voix Piper {nom_voix}"), "recettes": {}}
    crees = gardes = 0
    for r in donnees["recettes"]:
        dossier = DOSSIER / r["id"]
        dossier.mkdir(parents=True, exist_ok=True)
        deja = {c["texte"]: c["fichier"] for c in ancien.get(r["id"], [])}
        clips = []
        for k, texte in enumerate(textes_recette(r, donnees["ingredients"])):
            fichier = f"audio/{r['id']}/{k}.mp3"
            if deja.get(texte) == fichier and Path(fichier).exists():
                gardes += 1
            else:
                Path(fichier).write_bytes(en_mp3(voix, texte, config))
                crees += 1
                print("  ", fichier)
            clips.append({"texte": texte, "fichier": fichier})
        # Supprime les anciens fichiers de cette recette qui ne servent plus
        utiles = {Path(c["fichier"]).name for c in clips}
        for f in dossier.glob("*.mp3"):
            if f.name not in utiles:
                f.unlink()
        manifeste["recettes"][r["id"]] = clips

    MANIFESTE.write_text(json.dumps(manifeste, ensure_ascii=False, indent=1), encoding="utf-8")
    taille = sum(f.stat().st_size for f in DOSSIER.rglob("*.mp3")) // 1024
    print(f"{crees} fichier(s) créé(s), {gardes} gardé(s). Dossier audio : {taille} Ko. Manifeste : {MANIFESTE}")


if __name__ == "__main__":
    main()

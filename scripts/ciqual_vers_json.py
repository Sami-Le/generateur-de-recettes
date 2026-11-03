"""Convertit la table Ciqual de l'ANSES (fichier Excel ou CSV) en aliments.json pour le site.

Usage (depuis la racine du dépôt) :
  pip install openpyxl                       (pour un fichier .xlsx)
  pip install xlrd                           (pour un ancien fichier .xls, comme Ciqual 2020)
  python scripts/ciqual_vers_json.py chemin/vers/table_ciqual.xlsx

Le script garde, pour chaque aliment : code Ciqual, nom, groupe, et pour 100 g :
énergie (kcal), protéines, glucides, lipides (g).
Conventions de la table : "traces" -> 0 ; "< x" -> x / 2 ; "-" ou vide -> inconnu.
Les aliments sans valeur d'énergie sont ignorés (on ne peut pas les compter dans le journal).
"""
import csv
import json
import os
import sys
import unicodedata

SORTIE = "aliments.json"


def norm(texte):
    """Minuscules, sans accents ni espaces superflus, pour reconnaître les colonnes."""
    t = unicodedata.normalize("NFD", str(texte or "")).encode("ascii", "ignore").decode()
    # Ciqual 2025 coupe ses en-têtes par des retours à la ligne à la place des « / » :
    # on remplace « / » par un espace pour comparer les deux versions de la même façon.
    return " ".join(t.lower().replace("/", " ").split())


# Pour chaque information : mots qui doivent tous apparaître dans le nom de colonne,
# par ordre de préférence (la table a changé de libellés selon les versions).
COLONNES = {
    "code": [["alim_code"]],
    "nom": [["alim_nom_fr"]],
    "groupe": [["alim_ssgrp_nom_fr"], ["alim_grp_nom_fr"]],
    "kcal": [["energie", "1169 2011", "kcal"], ["energie", "jones", "kcal"], ["energie", "kcal"]],
    "p": [["proteines", "jones"], ["proteines", "6.25"], ["proteines", "g 100"]],
    "c": [["glucides", "g 100"]],
    "f": [["lipides", "g 100"]],
}


def trouver_colonnes(entetes):
    """Pour chaque information, la liste des colonnes possibles, par ordre de préférence."""
    noms = [norm(e) for e in entetes]
    trouve = {}
    for cle, options in COLONNES.items():
        for mots in options:
            idx = next((i for i, n in enumerate(noms) if all(m in n for m in mots)), None)
            if idx is not None and idx not in trouve.setdefault(cle, []):
                trouve[cle].append(idx)
        if not trouve.get(cle):
            sys.exit(f"Colonne introuvable pour « {cle} ». En-têtes lus :\n- " + "\n- ".join(map(str, entetes)))
    return trouve


def valeur(v):
    """Convertit une cellule Ciqual en nombre (ou None si inconnue)."""
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str) and v.strip() == "":
        return None
    t = str(v).strip().replace(",", ".").replace(" ", "")
    if t in ("", "-"):
        return None
    if t.lower() == "traces":
        return 0.0
    if t.startswith("<"):
        try:
            return float(t[1:].strip()) / 2
        except ValueError:
            return None
    try:
        return float(t)
    except ValueError:
        return None


def lire_lignes(chemin):
    if chemin.lower().endswith(".xls"):
        try:
            import xlrd
        except ImportError:
            sys.exit("Installe d'abord xlrd : pip install xlrd")
        feuille = xlrd.open_workbook(chemin).sheet_by_index(0)
        return [feuille.row_values(i) for i in range(feuille.nrows)]
    if chemin.lower().endswith((".xlsx", ".xlsm")):
        try:
            import openpyxl
        except ImportError:
            sys.exit("Installe d'abord openpyxl : pip install openpyxl")
        feuille = openpyxl.load_workbook(chemin, read_only=True, data_only=True).active
        return [list(r) for r in feuille.iter_rows(values_only=True)]
    with open(chemin, encoding="utf-8-sig", newline="") as f:
        echantillon = f.read(4096)
        f.seek(0)
        separateur = ";" if echantillon.count(";") > echantillon.count(",") else ","
        return list(csv.reader(f, delimiter=separateur))


def premiere(ligne, indices, convertir=True):
    """Première valeur connue parmi les colonnes possibles (ex. protéines Jones, sinon N x 6,25)."""
    for i in indices:
        v = ligne[i] if i < len(ligne) else None
        # Texte : on remplace les retours à la ligne des cellules par des espaces
        v = valeur(v) if convertir else (" ".join(str(v).split()) if v is not None else "")
        if v not in (None, ""):
            return v
    return None if convertir else ""


def arrondi(x):
    return None if x is None else round(x, 1)


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    lignes = lire_lignes(sys.argv[1])
    # La ligne d'en-tête est la première qui contient alim_code
    debut = next((i for i, l in enumerate(lignes) if any(norm(c) == "alim_code" for c in l)), None)
    if debut is None:
        sys.exit("En-tête « alim_code » introuvable : est-ce bien la table Ciqual ?")
    col = trouver_colonnes(lignes[debut])

    aliments, ignores = [], 0
    for l in lignes[debut + 1:]:
        if not l:
            continue
        nom = premiere(l, col["nom"], False)
        kcal = premiere(l, col["kcal"])
        if not nom or kcal is None:
            ignores += 1
            continue
        code = premiere(l, col["code"], False)
        groupe = premiere(l, col["groupe"], False)
        aliments.append([code, nom, groupe, round(kcal),
                         arrondi(premiere(l, col["p"])), arrondi(premiere(l, col["c"])), arrondi(premiere(l, col["f"]))])

    aliments.sort(key=lambda a: norm(a[1]))
    donnees = {
        "source": "Table de composition nutritionnelle des aliments Ciqual, ANSES",
        "url": "https://ciqual.anses.fr/",
        "fichier": os.path.basename(sys.argv[1]),
        "colonnes": ["code", "nom", "groupe", "kcal", "p", "c", "f"],
        "unite": "pour 100 g ; p, c, f en grammes ; null = valeur inconnue",
        "aliments": aliments,
    }
    with open(SORTIE, "w", encoding="utf-8") as f:
        json.dump(donnees, f, ensure_ascii=False, separators=(",", ":"))
    taille = os.path.getsize(SORTIE) // 1024
    print(f"{len(aliments)} aliments écrits dans {SORTIE} ({taille} Ko), {ignores} lignes ignorées (sans énergie).")


if __name__ == "__main__":
    main()

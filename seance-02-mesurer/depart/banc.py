#!/usr/bin/env python3
"""Banc de mesure — tri des tickets de support par un LLM local (Ollama).

Vous n'avez PAS à modifier ce fichier : vous modifiez le prompt, le schéma
et vos étiquettes, puis vous mesurez. Trois commandes :

    python banc.py mesurer --prompt prompts/v0.txt --ids 1-20
    python banc.py accord etiquettes.csv etiquettes_voisin.csv
    python banc.py verifier

Options de `mesurer` :
    --prompt FICHIER       le prompt système (obligatoire)
    --schema FICHIER       un JSON Schema : Ollama contraint alors sa réponse
    --ids 1-20             les tickets mesurés (ex. 1-20, 21-30, 1,4,7)
    --tickets FICHIER      par défaut tickets.jsonl
    --etiquettes FICHIER   par défaut etiquettes.csv (les réponses attendues)
    --temperature T        par défaut, celle du modèle
    --repetitions N        rejoue N fois la même mesure (défaut 1)
    --modele NOM           par défaut qwen2.5:1.5b, ou la variable MODELE
    --note "texte"         une remarque recopiée dans le journal

Le serveur Ollama est lu dans la variable OLLAMA_HOST (défaut
http://localhost:11434). Pour utiliser le serveur de la salle :
    export OLLAMA_HOST=http://<adresse donnée par l'enseignant>:11434

Aucune dépendance : bibliothèque standard de Python 3.10 et plus.
"""

import argparse
import csv
import hashlib
import json
import os
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

ICI = Path(__file__).resolve().parent
CATEGORIES = ["poste", "logiciel", "reseau", "acces", "impression"]
PRIORITES = ["P1", "P2", "P3"]
MODELE = os.environ.get("MODELE", "qwen2.5:1.5b")
HOTE = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
if not HOTE.startswith("http"):
    HOTE = "http://" + HOTE


# ─── Lecture des fichiers ────────────────────────────────────────────────────

def lire_tickets(chemin):
    tickets = {}
    with open(chemin, encoding="utf-8") as f:
        for n, ligne in enumerate(f, 1):
            if ligne.strip():
                t = json.loads(ligne)
                tickets[int(t["id"])] = t
    return tickets


def lire_etiquettes(chemin):
    """{id: {"categorie": ..., "priorite": ...}} ; les cases vides restent vides."""
    etiq = {}
    with open(chemin, encoding="utf-8", newline="") as f:
        for ligne in csv.DictReader(f):
            if not (ligne.get("id") or "").strip():
                continue
            etiq[int(ligne["id"])] = {
                "categorie": normaliser_categorie(ligne.get("categorie") or ""),
                "priorite": normaliser_priorite(ligne.get("priorite") or ""),
            }
    return etiq


def lire_ids(texte, disponibles):
    if not texte:
        return sorted(disponibles)
    ids = []
    for morceau in texte.split(","):
        morceau = morceau.strip()
        if "-" in morceau:
            a, b = morceau.split("-", 1)
            ids.extend(range(int(a), int(b) + 1))
        elif morceau:
            ids.append(int(morceau))
    inconnus = [i for i in ids if i not in disponibles]
    if inconnus:
        sys.exit(f"❌ Tickets inconnus : {inconnus}")
    return ids


# ─── Normalisation : ce que le banc accepte comme « la même valeur » ─────────
# Volontairement étroite : « Réseau » vaut « reseau », mais « network » ou
# « Matériel » ne valent rien. C'est au prompt et au schéma d'obtenir les
# valeurs attendues, pas au banc de deviner.

def sans_accents(s):
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn")


def normaliser_categorie(v):
    v = sans_accents(str(v)).strip().lower()
    return v if v in CATEGORIES else (v or "")


def normaliser_priorite(v):
    v = str(v).strip().upper().replace(" ", "")
    return v if v in PRIORITES else (v or "")


def extraire_json(texte):
    """Le premier objet JSON lisible dans la réponse, ou None."""
    try:
        v = json.loads(texte)
        return v if isinstance(v, dict) else None
    except (json.JSONDecodeError, TypeError):
        pass
    for m in re.finditer(r"\{.*?\}", texte or "", re.S):
        try:
            v = json.loads(m.group(0))
            if isinstance(v, dict):
                return v
        except json.JSONDecodeError:
            continue
    return None


def lire_reponse(texte):
    """(json_valide, categorie, priorite) à partir du texte du modèle."""
    obj = extraire_json(texte)
    if obj is None:
        return False, "", ""
    cles = {sans_accents(str(k)).lower(): v for k, v in obj.items()}
    return (True,
            normaliser_categorie(cles.get("categorie", "")),
            normaliser_priorite(cles.get("priorite", "")))


# ─── Appel au modèle ─────────────────────────────────────────────────────────

def texte_ticket(t):
    return (f"Ticket n° {t['id']} — reçu le {t['recu']}\n"
            f"Service : {t['service']}\n"
            f"Objet : {t['objet']}\n\n{t['texte']}")


def interroger(prompt, ticket, schema=None, temperature=None, modele=MODELE):
    corps = {
        "model": modele,
        "stream": False,
        "messages": [{"role": "system", "content": prompt},
                     {"role": "user", "content": texte_ticket(ticket)}],
        "options": {},
    }
    if schema is not None:
        corps["format"] = schema
    if temperature is not None:
        corps["options"]["temperature"] = temperature
    req = urllib.request.Request(
        HOTE.rstrip("/") + "/api/chat",
        data=json.dumps(corps).encode("utf-8"),
        headers={"Content-Type": "application/json"})
    debut = time.monotonic()
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            rep = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")
        if "not found" in detail:
            sys.exit(f"❌ Le modèle {modele} n'est pas installé : ollama pull {modele}")
        sys.exit(f"❌ Ollama a refusé la requête ({e.code}) : {detail}")
    except (urllib.error.URLError, ConnectionError, TimeoutError) as e:
        sys.exit(f"❌ Ollama ne répond pas sur {HOTE} ({e}).\n"
                 "   Lancez-le dans un autre terminal : ollama serve\n"
                 "   ou visez le serveur de la salle : export OLLAMA_HOST=http://…:11434")
    return rep.get("message", {}).get("content", ""), time.monotonic() - debut


# ─── Calcul des mesures ──────────────────────────────────────────────────────

def mesurer_lignes(lignes):
    """lignes : [{attendu_cat, attendu_prio, obtenu_cat, obtenu_prio, json_valide, duree}]"""
    n = len(lignes)
    m = {
        "n": n,
        "json_valides": sum(1 for l in lignes if l["json_valide"]),
        "exploitables": sum(1 for l in lignes
                            if l["obtenu_cat"] in CATEGORIES and l["obtenu_prio"] in PRIORITES),
        "cat_ok": sum(1 for l in lignes if l["obtenu_cat"] == l["attendu_cat"]),
        "prio_ok": sum(1 for l in lignes if l["obtenu_prio"] == l["attendu_prio"]),
        "deux_ok": sum(1 for l in lignes if l["obtenu_cat"] == l["attendu_cat"]
                       and l["obtenu_prio"] == l["attendu_prio"]),
        "p1_attendus": sum(1 for l in lignes if l["attendu_prio"] == "P1"),
        "p1_manques": sum(1 for l in lignes
                          if l["attendu_prio"] == "P1" and l["obtenu_prio"] != "P1"),
        "fausses_alertes": sum(1 for l in lignes
                               if l["attendu_prio"] != "P1" and l["obtenu_prio"] == "P1"),
        "duree_moy": (sum(l["duree"] for l in lignes) / n) if n else 0.0,
    }
    cols = PRIORITES + ["?"]
    m["matrice"] = {a: {c: 0 for c in cols} for a in PRIORITES}
    for l in lignes:
        if l["attendu_prio"] in PRIORITES:
            o = l["obtenu_prio"] if l["obtenu_prio"] in PRIORITES else "?"
            m["matrice"][l["attendu_prio"]][o] += 1
    return m


def pct(a, b):
    return f"{round(100 * a / b):>3} %" if b else "  – "


def afficher(m, entete):
    n = m["n"]
    print(entete)
    print(f"  Réponses exploitables (JSON lisible, valeurs connues) : {m['exploitables']}/{n}"
          f"   (JSON lisible : {m['json_valides']}/{n})")
    print(f"  Catégorie exacte  : {m['cat_ok']:>2}/{n}  {pct(m['cat_ok'], n)}")
    print(f"  Priorité exacte   : {m['prio_ok']:>2}/{n}  {pct(m['prio_ok'], n)}")
    print(f"  Les deux exactes  : {m['deux_ok']:>2}/{n}  {pct(m['deux_ok'], n)}")
    print(f"  P1 manqués        : {m['p1_manques']}/{m['p1_attendus']}"
          "   ← un incident grave traité comme une simple gêne")
    print(f"  Fausses alertes P1: {m['fausses_alertes']}")
    print("  Matrice des priorités (ligne = attendu, colonne = obtenu) :")
    print("            P1   P2   P3    ?")
    for a in PRIORITES:
        r = m["matrice"][a]
        print(f"      {a}  " + "".join(f"{r[c]:>5}" for c in PRIORITES + ["?"]))
    print(f"  Temps moyen : {m['duree_moy']:.1f} s par ticket".replace(".", ","))


def empreinte(texte):
    return hashlib.sha256(texte.encode("utf-8")).hexdigest()[:8]


def fuites(prompt, tickets, ids):
    """Tickets mesurés dont le texte figure dans le prompt : leur mesure ne vaut rien."""
    p = " ".join(prompt.split()).lower()
    trouves = []
    for i in ids:
        t = tickets[i]
        for morceau in (t["texte"], t["objet"]):
            m = " ".join(morceau.split()).lower()
            # Une phrase de 40 caractères du ticket suffit à le reconnaître.
            if len(m) >= 40 and any(m[k:k + 40] in p for k in range(0, len(m) - 39, 20)):
                trouves.append(i)
                break
    return trouves


# ─── Commandes ───────────────────────────────────────────────────────────────

def cmd_mesurer(a):
    tickets = lire_tickets(a.tickets)
    etiq = lire_etiquettes(a.etiquettes)
    ids = lire_ids(a.ids, tickets.keys())
    manquants = [i for i in ids if not etiq.get(i, {}).get("categorie")
                 or not etiq.get(i, {}).get("priorite")]
    if manquants:
        sys.exit(f"❌ Pas de réponse attendue pour les tickets {manquants} dans {a.etiquettes}.\n"
                 "   On ne mesure pas sans savoir ce qu'on attend : complétez d'abord vos étiquettes.")
    prompt = Path(a.prompt).read_text(encoding="utf-8")
    schema = json.loads(Path(a.schema).read_text(encoding="utf-8")) if a.schema else None

    fuite = fuites(prompt, tickets, ids)
    if fuite:
        print(f"⚠️  Le prompt contient le texte des tickets {fuite}, que vous mesurez aussi.")
        print("   Sur ces tickets le modèle a la réponse sous les yeux : la mesure est faussée.\n")

    dossier = Path(os.environ.get("BANC_RESULTATS", ICI / "resultats"))
    dossier.mkdir(parents=True, exist_ok=True)
    horo = datetime.now().strftime("%Y%m%d-%H%M%S")
    nom = Path(a.prompt).stem + ("+schema" if schema else "")
    resumes = []

    for rep in range(1, a.repetitions + 1):
        lignes = []
        print(f"\n▶ Passage {rep}/{a.repetitions} — {len(ids)} tickets", flush=True)
        for i in ids:
            brut, duree = interroger(prompt, tickets[i], schema, a.temperature, a.modele)
            ok, cat, prio = lire_reponse(brut)
            l = {"id": i, "attendu_cat": etiq[i]["categorie"], "attendu_prio": etiq[i]["priorite"],
                 "obtenu_cat": cat, "obtenu_prio": prio, "json_valide": ok, "duree": duree,
                 "brut": " ".join(brut.split())[:300]}
            lignes.append(l)
            signe = "✓" if cat == l["attendu_cat"] and prio == l["attendu_prio"] else "✗"
            print(f"  {signe} #{i:<3} attendu {l['attendu_cat']:<10} {l['attendu_prio']}"
                  f"   obtenu {cat or '—':<10} {prio or '—':<3} ({duree:.1f} s)", flush=True)

        fichier = dossier / f"{nom}-{horo}-{rep}.csv"
        with open(fichier, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(lignes[0].keys()))
            w.writeheader()
            w.writerows(lignes)
        m = mesurer_lignes(lignes)
        resumes.append(m)
        afficher(m, f"\n📏 {Path(a.prompt).name} · schéma : {Path(a.schema).name if schema else 'non'}"
                    f" · {a.modele} · tickets {a.ids or 'tous'}"
                    f" · température {a.temperature if a.temperature is not None else 'par défaut'}")
        print(f"  Détail ticket par ticket : {os.path.relpath(fichier)}")
        journaliser(dossier / "journal.csv", horo, rep, a, prompt, m)

    if a.repetitions > 1:
        print("\n🔁 Sur les", a.repetitions, "passages :")
        for cle, lib in (("cat_ok", "Catégorie exacte"), ("prio_ok", "Priorité exacte"),
                         ("p1_manques", "P1 manqués")):
            v = [r[cle] for r in resumes]
            print(f"  {lib:<17}: min {min(v)} · max {max(v)} · sur {resumes[0]['n']}")


def journaliser(chemin, horo, rep, a, prompt, m):
    neuf = not chemin.exists()
    with open(chemin, "a", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        if neuf:
            w.writerow(["horodatage", "passage", "prompt", "empreinte_prompt", "schema", "modele",
                        "temperature", "tickets", "n", "exploitables", "categorie_ok",
                        "priorite_ok", "deux_ok", "p1_manques", "p1_attendus",
                        "fausses_alertes", "duree_moy_s", "note"])
        w.writerow([horo, rep, a.prompt, empreinte(prompt), a.schema or "", a.modele,
                    "" if a.temperature is None else a.temperature, a.ids or "tous", m["n"],
                    m["exploitables"], m["cat_ok"], m["prio_ok"], m["deux_ok"], m["p1_manques"],
                    m["p1_attendus"], m["fausses_alertes"], f"{m['duree_moy']:.1f}", a.note or ""])


def cmd_accord(a):
    e1, e2 = lire_etiquettes(a.fichier1), lire_etiquettes(a.fichier2)
    ids = sorted(i for i in e1 if i in e2 and e1[i]["categorie"] and e2[i]["categorie"])
    if not ids:
        sys.exit("❌ Aucun ticket étiqueté dans les deux fichiers.")
    desaccords = []
    cat = prio = 0
    for i in ids:
        c, p = e1[i]["categorie"] == e2[i]["categorie"], e1[i]["priorite"] == e2[i]["priorite"]
        cat += c
        prio += p
        if not (c and p):
            desaccords.append(i)
    n = len(ids)
    print(f"🤝 Accord entre {a.fichier1} et {a.fichier2} sur {n} tickets")
    print(f"  Catégorie : {cat}/{n}  {pct(cat, n)}")
    print(f"  Priorité  : {prio}/{n}  {pct(prio, n)}")
    if desaccords:
        print("  Désaccords :")
        for i in desaccords:
            print(f"    #{i:<3} {e1[i]['categorie']:<10} {e1[i]['priorite']:<3}  ≠  "
                  f"{e2[i]['categorie']:<10} {e2[i]['priorite']}")
    print("\n  Deux humains qui ne sont pas d'accord à 100 % : c'est le plafond de ce")
    print("  que vous pouvez exiger du modèle — sauf à préciser la grille d'étiquetage.")


def cmd_verifier(a):
    """Ce que la CI contrôle : des livrables complets et cohérents (sans appeler Ollama)."""
    erreurs = []
    ici = Path(a.dossier)
    tickets = lire_tickets(ici / "tickets.jsonl")
    etiq = lire_etiquettes(ici / "etiquettes.csv")
    vides = []
    for i in sorted(tickets):
        e = etiq.get(i)
        if not e or not e["categorie"] or not e["priorite"]:
            vides.append(i)
        else:
            if e["categorie"] not in CATEGORIES:
                erreurs.append(f"etiquettes.csv : ticket {i}, catégorie inconnue « {e['categorie']} »")
            if e["priorite"] not in PRIORITES:
                erreurs.append(f"etiquettes.csv : ticket {i}, priorité inconnue « {e['priorite']} »")

    if vides:
        erreurs.append(f"etiquettes.csv : {len(vides)} ticket(s) non étiqueté(s) : "
                       + ", ".join(map(str, vides)))

    grille = (ici / "GRILLE_ETIQUETAGE.md").read_text(encoding="utf-8")
    if "À COMPLÉTER" in grille:
        erreurs.append("GRILLE_ETIQUETAGE.md : il reste des « À COMPLÉTER »")

    try:
        schema = json.loads((ici / "schema.json").read_text(encoding="utf-8"))
        props = schema.get("properties", {})
        for champ, attendu in (("categorie", CATEGORIES), ("priorite", PRIORITES)):
            enum = props.get(champ, {}).get("enum")
            if sorted(enum or []) != sorted(attendu):
                erreurs.append(f"schema.json : « {champ} » doit avoir enum = {attendu}")
            if champ not in schema.get("required", []):
                erreurs.append(f"schema.json : « {champ} » doit être dans required")
    except json.JSONDecodeError as e:
        erreurs.append(f"schema.json n'est pas du JSON valide : {e}")

    for p in ("prompts/v1.txt", "prompts/v2.txt"):
        if not (ici / p).exists() or len((ici / p).read_text(encoding="utf-8").strip()) < 20:
            erreurs.append(f"{p} manquant ou vide")

    journal = ici / "resultats" / "journal.csv"
    n = sum(1 for _ in open(journal, encoding="utf-8")) - 1 if journal.exists() else 0
    if n < 4:
        erreurs.append(f"resultats/journal.csv : {n} mesure(s), il en faut au moins 4 (v0, v1, v2 réglage, v2 test)")

    tableau = (ici / "TABLEAU_MESURE.md").read_text(encoding="utf-8")
    if "À COMPLÉTER" in tableau:
        erreurs.append("TABLEAU_MESURE.md : il reste des « À COMPLÉTER »")

    if erreurs:
        print("❌ Livrables incomplets :")
        for e in erreurs:
            print("   -", e)
        sys.exit(1)
    print(f"✅ Livrables complets : 30 tickets étiquetés, schéma conforme, {n} mesures au journal.")


def main(argv=None):
    p = argparse.ArgumentParser(description="Banc de mesure du tri des tickets.")
    sp = p.add_subparsers(dest="commande", required=True)

    m = sp.add_parser("mesurer", help="interroger le modèle et mesurer")
    m.add_argument("--prompt", required=True)
    m.add_argument("--schema")
    m.add_argument("--ids")
    m.add_argument("--tickets", default=str(ICI / "tickets.jsonl"))
    m.add_argument("--etiquettes", default=str(ICI / "etiquettes.csv"))
    m.add_argument("--temperature", type=float)
    m.add_argument("--repetitions", type=int, default=1)
    m.add_argument("--modele", default=MODELE)
    m.add_argument("--note")
    m.set_defaults(f=cmd_mesurer)

    c = sp.add_parser("accord", help="comparer deux fichiers d'étiquettes")
    c.add_argument("fichier1")
    c.add_argument("fichier2")
    c.set_defaults(f=cmd_accord)

    v = sp.add_parser("verifier", help="contrôler les livrables (utilisé par la CI)")
    v.add_argument("--dossier", default=str(ICI))
    v.set_defaults(f=cmd_verifier)

    a = p.parse_args(argv)
    a.f(a)


if __name__ == "__main__":
    main()

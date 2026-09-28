"""Tests du banc de mesure — rejoués par la CI, sans Ollama.

Un banc de mesure faux donne des chiffres faux avec le même aplomb qu'un bon.
Ces tests vérifient qu'il compte juste, sur des réponses fabriquées à la main,
et qu'il parle à Ollama comme il faut, grâce à un faux serveur local.

    python -m unittest tests_banc -v
"""

import csv
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import unittest
from contextlib import redirect_stdout
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

ICI = Path(__file__).resolve().parent
sys.path.insert(0, str(ICI))
import banc  # noqa: E402


def ligne(att_c, att_p, obt_c, obt_p, ok=True):
    return {"attendu_cat": att_c, "attendu_prio": att_p, "obtenu_cat": obt_c,
            "obtenu_prio": obt_p, "json_valide": ok, "duree": 1.0}


class LectureDesReponses(unittest.TestCase):

    def test_de_la_prose_n_est_pas_exploitable(self):
        self.assertEqual(banc.lire_reponse("Catégorie : réseau. Priorité : haute."),
                         (False, "", ""))

    def test_un_json_noye_dans_du_texte_est_retrouve(self):
        ok, c, p = banc.lire_reponse('Voici : {"categorie": "reseau", "priorite": "P2"} voilà')
        self.assertEqual((ok, c, p), (True, "reseau", "P2"))

    def test_accents_casse_et_espaces_sont_toleres(self):
        ok, c, p = banc.lire_reponse('{"Catégorie": " Réseau ", "priorité": "p1"}')
        self.assertEqual((ok, c, p), (True, "reseau", "P1"))

    def test_une_valeur_inventee_n_est_pas_corrigee(self):
        ok, c, p = banc.lire_reponse('{"categorie": "network", "priorite": "haute"}')
        self.assertTrue(ok)
        self.assertNotIn(c, banc.CATEGORIES)
        self.assertNotIn(p, banc.PRIORITES)


class CalculDesMesures(unittest.TestCase):

    def setUp(self):
        self.m = banc.mesurer_lignes([
            ligne("poste", "P1", "poste", "P1"),          # juste
            ligne("reseau", "P1", "reseau", "P3"),        # P1 manqué
            ligne("poste", "P1", "poste", "P2"),          # P1 manqué, catégorie juste
            ligne("acces", "P2", "logiciel", "P2"),       # catégorie fausse
            ligne("poste", "P3", "poste", "P1"),          # fausse alerte
            ligne("impression", "P3", "", "", ok=False),  # inexploitable
        ])

    def test_exactitudes(self):
        self.assertEqual((self.m["cat_ok"], self.m["prio_ok"], self.m["deux_ok"]), (4, 2, 1))

    def test_exploitables(self):
        self.assertEqual((self.m["json_valides"], self.m["exploitables"]), (5, 5))

    def test_p1_manques_et_fausses_alertes(self):
        self.assertEqual((self.m["p1_attendus"], self.m["p1_manques"], self.m["fausses_alertes"]),
                         (3, 2, 1))  # volontairement asymétrique

    def test_matrice_des_priorites(self):
        mat = self.m["matrice"]
        self.assertEqual(mat["P1"], {"P1": 1, "P2": 1, "P3": 1, "?": 0})
        self.assertEqual(mat["P3"], {"P1": 1, "P2": 0, "P3": 0, "?": 1})
        self.assertEqual(sum(sum(r.values()) for r in mat.values()), 6)


class DetectionDesFuites(unittest.TestCase):

    def test_un_ticket_recopie_dans_le_prompt_est_signale(self):
        tickets = banc.lire_tickets(ICI / "tickets.jsonl")
        prompt = "Exemple :\n" + tickets[24]["texte"] + "\n→ poste, P1"
        self.assertEqual(banc.fuites(prompt, tickets, range(21, 31)), [24])

    def test_un_prompt_sans_ticket_ne_declenche_rien(self):
        tickets = banc.lire_tickets(ICI / "tickets.jsonl")
        prompt = "Catégories : poste, logiciel, reseau, acces, impression. Réponds en JSON."
        self.assertEqual(banc.fuites(prompt, tickets, range(1, 31)), [])


class FauxOllama(BaseHTTPRequestHandler):
    recues = []

    def do_POST(self):
        corps = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        FauxOllama.recues.append(corps)
        # Réponse fabriquée : P1 pour tout ticket de l'expédition, P3 sinon.
        prio = "P1" if "Expédition" in corps["messages"][1]["content"] else "P3"
        rep = {"message": {"content": json.dumps({"categorie": "poste", "priorite": prio})}}
        data = json.dumps(rep).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *a):
        pass


class DeboutEnBout(unittest.TestCase):

    def setUp(self):
        self.serveur = HTTPServer(("127.0.0.1", 0), FauxOllama)
        threading.Thread(target=self.serveur.serve_forever, daemon=True).start()
        banc.HOTE = f"http://127.0.0.1:{self.serveur.server_port}"
        FauxOllama.recues = []
        self.tmp = Path(tempfile.mkdtemp())
        os.environ["BANC_RESULTATS"] = str(self.tmp / "resultats")
        (self.tmp / "etiq.csv").write_text(
            "id,categorie,priorite\n1,impression,P1\n2,poste,P3\n3,reseau,P2\n", encoding="utf-8")
        (self.tmp / "p.txt").write_text("Classe le ticket.", encoding="utf-8")
        (self.tmp / "s.json").write_text('{"type": "object"}', encoding="utf-8")

    def tearDown(self):
        self.serveur.shutdown()
        self.serveur.server_close()
        os.environ.pop("BANC_RESULTATS", None)
        shutil.rmtree(self.tmp)

    def lancer(self, *args):
        with redirect_stdout(io.StringIO()) as sortie:
            banc.main(["mesurer", "--prompt", str(self.tmp / "p.txt"), "--ids", "1-3",
                       "--etiquettes", str(self.tmp / "etiq.csv"), *args])
        return sortie.getvalue()

    def test_le_prompt_le_ticket_et_le_schema_partent_dans_la_requete(self):
        self.lancer("--schema", str(self.tmp / "s.json"), "--temperature", "0")
        self.assertEqual(len(FauxOllama.recues), 3)
        r = FauxOllama.recues[0]
        self.assertEqual(r["messages"][0], {"role": "system", "content": "Classe le ticket."})
        self.assertIn("Imprimante étiquettes colisage HS", r["messages"][1]["content"])
        self.assertEqual(r["format"], {"type": "object"})
        self.assertEqual(r["options"], {"temperature": 0.0})

    def test_sans_schema_ni_temperature_rien_n_est_impose(self):
        self.lancer()
        r = FauxOllama.recues[0]
        self.assertNotIn("format", r)
        self.assertEqual(r["options"], {})

    def test_le_journal_garde_une_ligne_par_passage(self):
        sortie = self.lancer("--repetitions", "2", "--note", "essai")
        with open(self.tmp / "resultats" / "journal.csv", encoding="utf-8") as f:
            lignes = list(csv.DictReader(f))
        self.assertEqual(len(lignes), 2)
        # ticket 1 : P1 attendu, P1 obtenu ; 2 : P3/P3 ; 3 : P2 attendu, P3 obtenu.
        self.assertEqual((lignes[0]["priorite_ok"], lignes[0]["p1_manques"], lignes[0]["note"]),
                         ("2", "0", "essai"))
        self.assertIn("min 2 · max 2", sortie)

    def test_on_ne_mesure_pas_sans_reponse_attendue(self):
        (self.tmp / "etiq.csv").write_text("id,categorie,priorite\n1,impression,P1\n2,,\n",
                                           encoding="utf-8")
        with self.assertRaises(SystemExit) as e:
            self.lancer()
        self.assertIn("[2, 3]", str(e.exception.code))
        self.assertEqual(FauxOllama.recues, [])


class Verification(unittest.TestCase):
    """`verifier` doit refuser le dossier de départ et accepter un dossier complet."""

    def verifier(self, dossier):
        return subprocess.run([sys.executable, str(ICI / "banc.py"), "verifier",
                               "--dossier", str(dossier)], capture_output=True, text=True)

    def test_le_dossier_de_depart_est_refuse(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            for f in ("tickets.jsonl", "GRILLE_ETIQUETAGE.md", "schema.json", "TABLEAU_MESURE.md"):
                shutil.copy(ICI / f, tmp / f)
            (tmp / "etiquettes.csv").write_text(
                "id,categorie,priorite\n" + "".join(f"{i},,\n" for i in range(1, 31)),
                encoding="utf-8")
            r = self.verifier(tmp)
            self.assertEqual(r.returncode, 1)
            for attendu in ("30 ticket(s) non étiqueté(s)", "GRILLE_ETIQUETAGE.md", "enum",
                            "prompts/v1.txt", "journal.csv", "TABLEAU_MESURE.md"):
                self.assertIn(attendu, r.stdout)
        finally:
            shutil.rmtree(tmp)

    def test_un_dossier_complet_est_accepte(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            shutil.copy(ICI / "tickets.jsonl", tmp)
            (tmp / "etiquettes.csv").write_text(
                "id,categorie,priorite\n" + "".join(f"{i},Réseau,p2\n" for i in range(1, 31)),
                encoding="utf-8")
            (tmp / "GRILLE_ETIQUETAGE.md").write_text("grille remplie", encoding="utf-8")
            (tmp / "TABLEAU_MESURE.md").write_text("tableau rempli", encoding="utf-8")
            (tmp / "schema.json").write_text(json.dumps({
                "type": "object",
                "properties": {"categorie": {"enum": banc.CATEGORIES},
                               "priorite": {"enum": banc.PRIORITES}},
                "required": ["categorie", "priorite"]}), encoding="utf-8")
            (tmp / "prompts").mkdir()
            for v in ("v1", "v2"):
                (tmp / "prompts" / f"{v}.txt").write_text("Un prompt assez long pour compter.",
                                                          encoding="utf-8")
            (tmp / "resultats").mkdir()
            (tmp / "resultats" / "journal.csv").write_text("entete\n" + "l\n" * 4, encoding="utf-8")
            r = self.verifier(tmp)
            self.assertEqual(r.returncode, 0, r.stdout)
        finally:
            shutil.rmtree(tmp)


if __name__ == "__main__":
    unittest.main()

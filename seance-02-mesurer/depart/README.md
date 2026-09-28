# Dossier de travail — séance 2

| Fichier | Rôle | Vous le modifiez ? |
|---|---|---|
| `tickets.jsonl` | les 30 tickets, un objet JSON par ligne | non |
| `etiquettes.csv` | **vos** réponses attendues, une ligne par ticket | oui (mission 1) |
| `GRILLE_ETIQUETAGE.md` | vos définitions des catégories et priorités | oui (mission 1) |
| `prompts/v0.txt` | le prompt de départ, volontairement naïf | non : copiez-le |
| `prompts/v1.txt`, `v2.txt` | vos prompts | oui (missions 2 et 4) |
| `schema.json` | la forme imposée à la réponse | oui (mission 3) |
| `banc.py` | le banc de mesure | **non** |
| `tests_banc.py` | les tests du banc, rejoués par la CI | non |
| `resultats/` | un CSV par mesure + `journal.csv` : la preuve | ne rien effacer |
| `TABLEAU_MESURE.md` | vos mesures, recopiées et commentées | oui |
| `REPONSE_TUTEUR.md` | votre réponse à Karim | oui |

```bash
python banc.py mesurer --prompt prompts/v1.txt --schema schema.json --ids 1-20 --note "ce que j'ai changé"
python banc.py accord etiquettes.csv etiquettes_voisin.csv
python banc.py verifier        # ce que la CI contrôle
```

# 📏 Séance 2 — Prompts et évaluation d'un LLM : trier les tickets de support

> **Verbe dominant : Mesurer.** Aussi : Concevoir · Piloter · Sécuriser
> **Durée :** 3 h · **Contexte :** stage chez Méca Forez, service informatique
> **Livrables** (tous dans `depart/`) : `GRILLE_ETIQUETAGE.md`, `etiquettes.csv`,
> `prompts/v1.txt`, `schema.json`, `prompts/v2.txt`, `resultats/`,
> `TABLEAU_MESURE.md`, `REPONSE_TUTEUR.md`

## 🎯 Ce que vous saurez faire à la fin

- construire un **jeu d'évaluation** : des exemples et la réponse attendue pour chacun ;
- **contraindre** la sortie d'un modèle avec un **JSON Schema** ;
- **mesurer** un prompt par des chiffres, et comparer deux versions sur les mêmes tickets ;
- séparer le **jeu de réglage** du **jeu de test**, et comprendre pourquoi ;
- rendre une recommandation **chiffrée** : on branche, ou pas, et à quelles conditions.

**La règle de la séance : aucune affirmation sans mesure.** « Ça a l'air mieux »
ne compte pas. Chaque changement de prompt se juge par une ligne du journal.

---

## 🗺️ Le déroulé

| Temps | Étape | Ce que vous produisez |
|---|---|---|
| 0:00 – 0:10 | 1. Recevoir la demande | la demande reformulée en 3 lignes |
| 0:10 – 0:35 | 2. Comprendre la technologie | [CONCEPT.md](CONCEPT.md) lu, premier appel au modèle |
| 0:35 – 1:10 | 3. Construire la vérité | mission 🟢 1 |
| 1:10 – 2:35 | 4. Mesurer, contraindre, améliorer | missions 🟢 2, 🟡 3, 🟡 4 |
| 2:35 – 2:50 | 5. Le test à l'aveugle | mission 🔴 5 |
| 2:50 – 3:00 | 6. Rendre compte | `REPONSE_TUTEUR.md` |

---

## 1. Recevoir la demande (10 min)

1. Lisez [DEMANDE_TUTEUR.md](DEMANDE_TUTEUR.md).
2. En haut de `depart/REPONSE_TUTEUR.md`, rubrique **« La demande »**,
   reformulez-la en **trois lignes** : qui a le problème, ce qu'il veut savoir,
   à quel chiffre il verra que c'est réglé.

## 2. Comprendre la technologie (25 min)

1. Lisez [CONCEPT.md](CONCEPT.md) et faites l'auto-évaluation, sans regarder
   les réponses.
2. Vérifiez que le modèle répond. Dans un terminal :

   ```bash
   ollama list                      # qwen2.5:1.5b doit apparaître
   ollama run qwen2.5:1.5b "Réponds seulement : OK"
   ```

   ✅ **Attendu :** une réponse en quelques secondes. La première peut prendre
   30 s : le modèle se charge en mémoire.

   > 🆘 `ollama: command not found` ou `could not connect` → voir l'encadré
   > **Bloqué ?** en bas de page.

3. Lancez le banc sur les trois premiers tickets avec le prompt fourni, pour
   voir à quoi ressemble une mesure. Il faut une réponse attendue pour chaque
   ticket mesuré : remplissez à la main les **trois premières lignes** de
   `etiquettes.csv` (vous les reprendrez à la mission 1).

   ```bash
   cd seance-02-mesurer/depart
   python banc.py mesurer --prompt prompts/v0.txt --ids 1-3
   ```

4. Ouvrez le fichier `resultats/v0-….csv` : la colonne `brut` contient ce que
   le modèle a **vraiment** répondu. Pourquoi le banc ne peut-il rien en faire ?

---

## 3. Construire la vérité (35 min)

### 🟢 Mission 1 — La grille d'étiquetage et les 30 réponses attendues

On ne peut pas dire qu'un modèle se trompe sans avoir écrit, **avant**, ce
qu'est la bonne réponse.

1. Complétez `depart/GRILLE_ETIQUETAGE.md` : une définition **vérifiable** par
   catégorie et par priorité, et vos **questions au tuteur**.
2. Allez poser vos questions au tuteur (l'enseignant). Notez chaque réponse
   dans la grille.
3. Remplissez `depart/etiquettes.csv` pour les **30 tickets**, en suivant
   **votre grille**, pas votre intuition. Valeurs autorisées, en minuscules et
   sans accent : `poste`, `logiciel`, `reseau`, `acces`, `impression` ;
   `P1`, `P2`, `P3`.
4. Échangez votre fichier avec un voisin et mesurez votre accord :

   ```bash
   python banc.py accord etiquettes.csv etiquettes_voisin.csv
   ```

5. Pour chaque désaccord : qui a mal appliqué la grille, ou est-ce la grille
   qui ne tranchait pas ? Dans le second cas, **précisez la grille**, et
   corrigez vos étiquettes.

> 💡 **Indice :** un ticket écrit « URGENT !!! » n'est pas forcément urgent.
> Votre grille doit dire ce qui compte : le ton du message, ou ses conséquences ?

✅ **Validé quand :** la grille ne contient plus de « À COMPLÉTER », les
30 tickets sont étiquetés, et le taux d'accord avec votre voisin est noté
dans `TABLEAU_MESURE.md`.

---

## 4. Mesurer, contraindre, améliorer (1 h 25)

Deux jeux, deux usages. **Ne les mélangez jamais.**

| Jeu | Tickets | Usage |
|---|---|---|
| **Réglage** | 1 à 20 | vous le regardez autant que vous voulez pour améliorer le prompt |
| **Test** | 21 à 30 | vous ne le lisez **pas** ; vous le mesurez **une seule fois**, à la fin de la mission 4 |

### 🟢 Mission 2 — Un prompt qui donne des réponses exploitables

1. Copiez `prompts/v0.txt` en `prompts/v1.txt`. Complétez-le pour qu'il donne
   la **liste exacte** des catégories et des priorités, et demande une réponse
   **en JSON** avec les clés `categorie` et `priorite`.
2. Mesurez sur le jeu de réglage :

   ```bash
   python banc.py mesurer --prompt prompts/v1.txt --ids 1-20 --note "v1 sans schéma"
   ```

3. Recopiez la ligne dans `TABLEAU_MESURE.md`. Regardez la colonne `brut` du
   détail : le modèle respecte-t-il **toujours** vos valeurs ?

✅ **Validé quand :** la mesure v1 est au journal et dans le tableau, avec
votre commentaire sur les valeurs inventées.

### 🟡 Mission 3 — Contraindre la sortie, et mesurer la variabilité

1. Complétez `depart/schema.json` : les deux champs, leur **liste de valeurs
   autorisées** (`enum`), et `required`.
2. Mesurez **le même prompt** avec le schéma :

   ```bash
   python banc.py mesurer --prompt prompts/v1.txt --schema schema.json --ids 1-20 --note "v1 + schéma"
   ```

3. Un modèle ne répond pas toujours la même chose. Rejouez **trois fois** la
   même mesure sur 10 tickets, puis la même chose à température 0 :

   ```bash
   python banc.py mesurer --prompt prompts/v1.txt --schema schema.json --ids 1-10 --repetitions 3
   python banc.py mesurer --prompt prompts/v1.txt --schema schema.json --ids 1-10 --repetitions 3 --temperature 0
   ```

4. Dans le tableau : l'écart min–max de chaque série. Un gain de 1 ticket sur
   20 entre deux prompts est-il **plus grand** que cet écart ?

> 💡 **Indice :** le schéma règle un problème et pas un autre. Qu'est-ce qui
> a changé entre v1 et v1 + schéma : les réponses exploitables, ou les
> réponses justes ?

✅ **Validé quand :** 20/20 réponses exploitables avec le schéma, et les deux
séries de répétitions sont commentées dans le tableau.

### 🟡 Mission 4 — Améliorer le prompt, en mesurant chaque version

1. Écrivez `prompts/v2.txt` à partir de v1 : ajoutez **les définitions de
   votre grille** et **deux ou trois exemples** (ticket → réponse JSON).
   Les exemples sont **inventés**, ou pris dans le jeu de réglage (1 à 20),
   **jamais** dans le jeu de test.
2. Mesurez sur le jeu de réglage, **à température 0**. Regardez les erreurs
   restantes, modifiez le prompt, mesurez à nouveau. Chaque version est une
   ligne du journal : notez ce que vous avez changé avec `--note`.
3. Quand vous êtes satisfait, et **une seule fois**, mesurez le jeu de test :

   ```bash
   python banc.py mesurer --prompt prompts/v2.txt --schema schema.json --ids 21-30 --temperature 0 --note "v2 TEST"
   ```

4. Remplissez la matrice des priorités du test dans le tableau. Comptez les
   **P1 manqués**.

> 💡 **Indice :** si le banc affiche « ⚠️ Le prompt contient le texte des
> tickets… », votre exemple est un ticket mesuré. Le modèle a la réponse sous
> les yeux, et votre score ne veut plus rien dire.

✅ **Validé quand :** au moins deux versions de v2 au journal sur le réglage,
une seule mesure du test, et la question du tableau « Réglage ou test : où
le score est-il le plus haut, et pourquoi ? » a sa réponse.

---

## 5. Le test à l'aveugle (15 min)

### 🔴 Mission 5 — Dix tickets que personne n'a vus

À 2:35, l'enseignant donne le lien d'un fichier `tickets_inedits.jsonl` :
dix tickets arrivés cette nuit, écrits autrement.

1. Téléchargez-le dans `depart/`. Étiquetez les dix tickets dans un nouveau
   fichier `etiquettes_inedits.csv`, **avec votre grille**, avant toute mesure.
2. Mesurez votre meilleur prompt, sans le modifier :

   ```bash
   python banc.py mesurer --prompt prompts/v2.txt --schema schema.json \
     --tickets tickets_inedits.jsonl --etiquettes etiquettes_inedits.csv --temperature 0 --note "INÉDITS"
   ```

3. Lisez les réponses une par une. Un ticket essaie-t-il de **manipuler** le
   modèle ? Un ticket sort-il de vos cinq catégories ? Notez-le.

✅ **Validé quand :** le score sur les inédits est dans le tableau, comparé
au réglage et au test, et vous avez écrit **une condition** sans laquelle
vous ne brancheriez pas le modèle.

---

## 6. Rendre compte (10 min)

Complétez `depart/REPONSE_TUTEUR.md` : le mail à Karim, **dix lignes
maximum**, qui répond à sa question.

- la décision : on branche **oui ou non**, et **dans quel rôle** (trier seul,
  ou proposer à Thomas qui valide) ;
- les chiffres qui la justifient : sur quel jeu, combien de tickets ;
- les P1 manqués, et ce que vous proposez pour eux ;
- comment Karim refera la mesure dans six mois (la commande).

Puis committez tout (`resultats/` compris) et poussez. La CI vérifie que vos
livrables sont complets.

```bash
git add -A && git commit -m "mesure: tri des tickets" && git push
```

---

## ✅ Récapitulatif des missions

| # | Mission | Niveau | Verbe | Preuve |
|---|---|---|---|---|
| 1 | Grille d'étiquetage et 30 réponses attendues | 🟢 | Concevoir | `GRILLE_ETIQUETAGE.md`, `etiquettes.csv`, accord |
| 2 | Un prompt aux réponses exploitables | 🟢 | Piloter · Mesurer | `prompts/v1.txt`, journal |
| 3 | Schéma JSON et variabilité mesurée | 🟡 | Mesurer · Sécuriser | `schema.json`, répétitions |
| 4 | Prompt v2 réglé, puis testé une fois | 🟡 | Mesurer | `prompts/v2.txt`, matrice du test |
| 5 | Test à l'aveugle et condition de mise en service | 🔴 | Mesurer · Sécuriser | inédits dans le tableau |

> ✅ **Dans le portail**, cochez chaque mission dans la carte « Vos missions — séance 12 »
> dès que son critère « Validé quand » est atteint, pas avant.

> 🆘 **Bloqué ?**
> - `ollama: command not found` → le Codespace n'a pas été créé avec la
>   configuration « Séance 2 ». Relancez l'installation : `bash .devcontainer/seance-02/installer-ollama.sh`.
> - `Ollama ne répond pas` → lancez-le dans un autre terminal : `ollama serve`.
> - Une mesure de 20 tickets prend plus de 5 minutes → utilisez le serveur de la
>   salle : `export OLLAMA_HOST=http://<adresse au tableau>:11434`, puis relancez.
>   Notez-le dans le tableau : le temps par ticket n'est plus comparable.
> - `Pas de réponse attendue pour les tickets…` → complétez `etiquettes.csv`.

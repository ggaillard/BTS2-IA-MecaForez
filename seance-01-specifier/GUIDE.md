# 🧭 Séance 1 — Développer à partir d'une spécification, avec un agent

> **Verbe dominant : Concevoir.** Aussi : Piloter · Mesurer · Sécuriser
> **Durée :** 3 h · **Contexte :** stage chez Méca Forez, PME industrielle de
> 85 salariés · **Livrables :** `SPEC.md`, `Prets.feature`, `AGENTS.md`,
> `GRILLE_ECART.md`, `REPONSE_TUTEUR.md` (tous dans `depart/`)

## 🎯 Ce que vous saurez faire à la fin

- transformer une demande floue en **règles de gestion** vérifiables ;
- écrire des **scénarios Gherkin** qui servent à la fois de spécification et de tests ;
- cadrer un **agent de code** avec un fichier `AGENTS.md` ;
- **relire** ce que l'agent a livré et dire, pour chaque écart, d'où il vient.

**La règle de la séance : vous ne tapez pas le code de l'application.** Vous
écrivez la spécification, l'agent code, vous vérifiez. Quand quelque chose ne
va pas, **c'est la spécification que vous corrigez**, puis vous relancez
l'agent.

---

## 🗺️ Le déroulé

| Temps | Étape | Ce que vous produisez |
|---|---|---|
| 0:00 – 0:10 | 1. Recevoir la demande | la demande reformulée en 3 lignes |
| 0:10 – 0:40 | 2. Comprendre la technologie | la fiche [CONCEPT.md](CONCEPT.md) lue, l'auto-évaluation faite |
| 0:40 – 1:40 | 3. Concevoir | missions 🟢 1, 🟢 2, 🟡 3 |
| 1:40 – 2:30 | 4. Piloter et mesurer | mission 🟡 4 |
| 2:30 – 2:50 | 5. Corriger par la spec | mission 🔴 5 |
| 2:50 – 3:00 | 6. Rendre compte | `REPONSE_TUTEUR.md` |

---

## 1. Recevoir la demande (10 min)

1. Lisez [DEMANDE_TUTEUR.md](DEMANDE_TUTEUR.md).
2. En haut de `depart/SPEC.md`, rubrique **« La demande »**, reformulez-la en
   **trois lignes maximum** : qui a le problème, ce qu'il veut, à quoi il verra
   que c'est réglé.

## 2. Comprendre la technologie (30 min)

1. Lisez [CONCEPT.md](CONCEPT.md) et faites l'auto-évaluation, sans regarder
   les réponses.
2. Ouvrez le projet de départ et lancez les tests :

   ```bash
   cd seance-01-specifier/depart
   dotnet test
   ```

   ✅ **Attendu :** `Passed! - Failed: 0, Passed: 1`.

3. Ouvrez côte à côte `tests/PretsMateriel.Specs/Features/Parc.feature` et
   `tests/PretsMateriel.Specs/Steps/ParcSteps.cs`. Pour **chaque ligne** du
   scénario, trouvez la méthode qui l'exécute. C'est exactement ce que l'agent
   devra écrire pour **vos** scénarios.

---

## 3. Concevoir (1 h)

### 🟢 Mission 1 — Les règles de gestion et les questions au tuteur

Dans `depart/SPEC.md`, rubrique **« Règles de gestion »** :

1. Écrivez une règle par ligne, numérotée `RG1`, `RG2`… Une règle est une
   phrase **vérifiable** : on doit pouvoir dire, sur un exemple, si elle est
   respectée ou non.
   - ❌ « Les prêts ne doivent pas durer trop longtemps. »
   - ✅ « RG4 — La date de retour prévue est au plus tard 14 jours calendaires
     après la date du prêt. »
2. Rubrique **« Questions au tuteur »** : listez chaque imprécision du mail
   sous forme de question fermée (réponse courte).
3. Allez poser vos questions au tuteur (l'enseignant). Notez chaque réponse
   **et** la règle qu'elle modifie.

> 💡 **Indice :** cherchez dans le mail les mots qui peuvent se lire de deux
> façons : une durée, un état, une personne, un moment.

✅ **Validé quand :** au moins 7 règles numérotées, chacune testable sur un
exemple ; au moins 4 questions posées, avec leur réponse.

### 🟢 Mission 2 — Six scénarios Gherkin

Dans `tests/PretsMateriel.Specs/Features/Prets.feature` :

1. Écrivez un **Contexte** qui fixe la date du jour et le parc de six PC (copiez
   le tableau de `Parc.feature`).
2. Écrivez **au moins six scénarios**, dont **au moins deux refus**. Chaque
   scénario vérifie **une seule** règle, avec des données concrètes (un nom, un
   code PC, une date).
3. Pour les refus, écrivez le message exact attendu :
   `Alors le prêt est refusé avec le message "PC-02 est déjà prêté"`.
4. Pour une limite (la durée maximale), utilisez un **Plan du scénario** avec
   deux exemples : juste à la limite, et juste au-delà.

> 💡 **Indice :** si votre règle parle de « date du jour », votre scénario
> doit dire **quelle** date. Sans cela, le test donnera un résultat différent
> selon le jour où on le lance.

✅ **Validé quand :** `Prets.feature` contient au moins 6 scénarios, chaque
règle RG est couverte par au moins un scénario, et **aucune ligne ne décrit un
clic ou un écran**.

### 🟡 Mission 3 — La spécification et le fichier de l'agent

1. Complétez `depart/SPEC.md` : rubriques **« Hors périmètre »** (ce que
   l'outil ne fait pas) et **« Contraintes techniques »**.
2. Complétez `depart/AGENTS.md` en suivant ses rubriques : pile technique,
   commandes, conventions, **interdits**, définition de « terminé ».
3. Committez **avant** de lancer l'agent. C'est la preuve que la spécification
   existait avant le code :

   ```bash
   git add SPEC.md AGENTS.md tests/PretsMateriel.Specs/Features/Prets.feature
   git commit -m "spec: règles, scénarios et consignes de l'agent"
   ```

> 💡 **Indice :** la ligne la plus importante d'`AGENTS.md` est celle qui
> interdit de modifier les fichiers `.feature`. Sans elle, un agent qui échoue
> peut « réparer » le test au lieu du code.

✅ **Validé quand :** le commit existe, `AGENTS.md` contient au moins trois
interdits et une définition de « terminé » vérifiable par une commande.

---

## 4. Piloter et mesurer (50 min)

### 🟡 Mission 4 — Lancer l'agent, puis relire ce qu'il a livré

1. Créez une branche pour le travail de l'agent :

   ```bash
   git switch -c agent/prets
   ```

2. Ouvrez Copilot Chat (`Ctrl+Alt+I`), choisissez le mode **Agent**, et
   envoyez ce message, **sans rien ajouter qui ne soit pas dans votre spec** :

   ```text
   Lis #file:SPEC.md et #file:AGENTS.md. Implémente la fonctionnalité décrite
   pour que tous les scénarios de tests/PretsMateriel.Specs/Features passent
   avec `dotnet test`. Ne modifie aucun fichier .feature.
   ```

3. Laissez l'agent travailler. **Ne l'aidez pas** en cours de route : si vous
   lui donnez une information qui n'est pas dans la spec, la spec est
   incomplète, et c'est ce que la séance doit montrer.
4. Quand il a fini, mesurez :

   ```bash
   dotnet test                                     # combien de scénarios verts ?
   git diff main --stat                            # quels fichiers ont bougé ?
   git diff main -- "*.feature"                    # doit être VIDE
   ```

5. Remplissez [GRILLE_ECART.md](depart/GRILLE_ECART.md) : une ligne par scénario,
   puis la liste de vérifications de la revue de code.

> 💡 **Indice :** un scénario vert ne prouve pas que le code est bon. Lisez le
> code produit : où l'agent prend-il la date du jour ? Si c'est
> `DateTime.Now`, votre scénario de retard ne peut pas être fiable.

✅ **Validé quand :** la grille est remplie pour chaque scénario, avec une
**cause** choisie parmi les quatre de la fiche concept.

---

## 5. Corriger par la spécification (20 min)

### 🔴 Mission 5 — Tous les scénarios verts, sans toucher au code

1. Pour chaque écart de la grille, corrigez **la spécification** (`SPEC.md`,
   `AGENTS.md`, ou un scénario **faux**), jamais le code.
2. Committez la correction de spec, puis relancez l'agent sur la même branche.
3. Recommencez jusqu'à ce que `dotnet test` soit entièrement vert **et** que
   `git diff main -- "*.feature"` ne montre que **vos** corrections.
4. Si ce n'est pas déjà fait, ajoutez le scénario de la règle « une personne,
   un seul PC », en suivant la réponse du tuteur.

✅ **Validé quand :** tous les scénarios passent, la grille indique pour chaque
écart la ligne de spec corrigée, et l'historique Git montre au moins un commit
`spec:` **après** le premier passage de l'agent.

---

## 6. Rendre compte (10 min)

Écrivez `depart/REPONSE_TUTEUR.md` : le mail que vous enverriez à Karim, en
**dix lignes maximum**.

- ce qui marche : **combien** de scénarios passent, sur combien ;
- ce qui ne marche pas, ou pas encore ;
- **ce que vous avez dû préciser** dans la spec pour que l'agent réussisse ;
- une chose que vous feriez autrement la prochaine fois.

Puis poussez votre branche et ouvrez une pull request vers `main`. La CI rejoue
les scénarios.

---

## ✅ Récapitulatif des missions

| # | Mission | Niveau | Verbe | Preuve |
|---|---|---|---|---|
| 1 | Règles de gestion et questions au tuteur | 🟢 | Concevoir | `SPEC.md` |
| 2 | Six scénarios Gherkin | 🟢 | Concevoir | `Prets.feature` |
| 3 | Spécification et `AGENTS.md`, committés avant l'agent | 🟡 | Concevoir · Sécuriser | commit `spec:` |
| 4 | Agent lancé, livraison relue | 🟡 | Piloter · Mesurer | `GRILLE_ECART.md` |
| 5 | Tout vert en corrigeant la spec | 🔴 | Concevoir · Mesurer | CI verte, commits `spec:` |

> ✅ **Dans le portail**, cochez chaque mission dans la carte « Vos missions — séance 11 »
> dès que son critère « Validé quand » est atteint, pas avant. C'est ce que je lis pour
> savoir où vous en êtes ; une case cochée par erreur se décoche.

> 🆘 **Bloqué ?** Copilot n'apparaît pas → vérifiez que votre compte GitHub
> Education est actif et que l'extension GitHub Copilot Chat est connectée.
> `dotnet test` ne trouve pas une étape → Reqnroll affiche dans la console le
> code de la méthode manquante : c'est à l'agent de l'écrire, pas à vous.

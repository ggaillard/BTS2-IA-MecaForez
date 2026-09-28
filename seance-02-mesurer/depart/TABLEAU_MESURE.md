# 📊 Tableau de mesure — tri des tickets par qwen2.5:1.5b

> Chaque ligne recopie une ligne de `resultats/journal.csv`. Une affirmation
> sans ligne dans ce tableau ne compte pas.

## 1. La vérité

- Accord avec mon voisin (`banc.py accord`) : catégorie À COMPLÉTER %, priorité À COMPLÉTER %
- Plafond réaliste que j'en tire : À COMPLÉTER

## 2. Les mesures

| # | Prompt | Schéma | Temp. | Tickets | Exploitables | Catégorie | Priorité | P1 manqués | Fausses alertes P1 | s / ticket | Ce que j'ai changé |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | v0 | non | défaut | 1-3 | | | | | | | prompt fourni |
| 2 | v1 | non | défaut | 1-20 | | | | | | | À COMPLÉTER |
| 3 | v1 | oui | défaut | 1-20 | | | | | | | |
| 4 | v2 | oui | 0 | 1-20 | | | | | | | |
| 5 | v2 | oui | 0 | 1-20 | | | | | | | |
| 6 | v2 | oui | 0 | **21-30 (test)** | | | | | | | une seule fois |
| 7 | v2 | oui | 0 | **inédits** | | | | | | | |

## 3. La variabilité (mission 3, tickets 1-10, 3 passages)

| Température | Catégorie min – max | Priorité min – max | P1 manqués min – max |
|---|---|---|---|
| par défaut | | | |
| 0 | | | |

Un gain entre deux prompts est réel s'il dépasse : À COMPLÉTER

## 4. Le test (ligne 6) : matrice des priorités

|  | obtenu P1 | obtenu P2 | obtenu P3 |
|---|---|---|---|
| **attendu P1** | | | |
| **attendu P2** | | | |
| **attendu P3** | | | |

## 5. Ce que les chiffres disent

- v1 sans schéma → v1 avec schéma, ce qui a changé : À COMPLÉTER
- Réglage ou test : où le score est-il le plus haut, et pourquoi ? À COMPLÉTER
- Inédits : ce qui a trompé le modèle (manipulation, catégorie absente…) : À COMPLÉTER
- La condition sans laquelle je ne brancherais pas le modèle : À COMPLÉTER

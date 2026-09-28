# Grille d'écart — ce qui était demandé, ce qui a été livré

> Passage de l'agent n° : `1` · Branche : `agent/prets` · Date : `<jj/mm/aaaa>`

## 1. Mesure

| Mesure | Résultat |
|---|---|
| `dotnet test` : scénarios verts / total | ` / ` |
| `git diff main --stat` : fichiers modifiés ou créés | |
| `git diff main -- "*.feature"` : vide ? | oui / non |
| Paquets NuGet ajoutés par l'agent | |

## 2. Scénario par scénario

**Causes possibles** (fiche concept § 6) : `spec ambiguë` · `oubli de spec` · `scénario faux` · `erreur de l'agent`.

| Scénario | Règle | Résultat | Écart observé | Cause | Correction de spec (fichier, ligne) |
|---|---|---|---|---|---|
| | RG | ✅ / ❌ | | | |
| | RG | ✅ / ❌ | | | |
| | RG | ✅ / ❌ | | | |
| | RG | ✅ / ❌ | | | |
| | RG | ✅ / ❌ | | | |
| | RG | ✅ / ❌ | | | |

## 3. Revue du code livré

Cochez, et justifiez chaque case non cochée.

- [ ] Aucun fichier `.feature` n'a été modifié par l'agent.
- [ ] La date du jour ne vient pas de `DateTime.Now` : elle peut être fixée par les tests.
- [ ] Les messages de refus sont mot pour mot ceux de `SPEC.md`.
- [ ] Chaque règle RG est appliquée à un seul endroit du code, que je sais montrer.
- [ ] L'agent n'a créé aucun fichier que je ne sais pas expliquer.
- [ ] Aucun secret, mot de passe ou chemin personnel dans le code.

## 4. Ce que je retiens de ce passage

<!-- Deux phrases : ce que la spec disait mal, ce que je préciserai dès le départ la prochaine fois. -->

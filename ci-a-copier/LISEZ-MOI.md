# Workflows à déposer à la main

GitHub refuse qu'une application écrive dans `.github/workflows/`. Dans VS Code,
déplacez ces deux fichiers, puis supprimez le dossier `ci-a-copier/` :

| Fichier ici | Destination |
|---|---|
| `seance-01.yml` | `.github/workflows/seance-01.yml` |
| `seance-02.yml` | `.github/workflows/seance-02.yml` |

`seance-01.yml` vérifie à chaque push : au moins six scénarios dans `Prets.feature`, aucun
`.feature` modifié hors d'un commit `spec:` sur une branche `agent/…`, et tous les scénarios verts.

`seance-02.yml` rejoue les tests du banc de mesure (sans Ollama) et vérifie que les livrables
sont complets : 30 tickets étiquetés, schéma conforme, prompts v1 et v2, au moins 4 mesures au
journal, grille et tableau sans « À COMPLÉTER ».

Les configurations Codespaces sont déjà en place dans `.devcontainer/` : la configuration par
défaut (.NET 10, Copilot Chat, Gherkin) et `seance-02/` (Python 3.12, Ollama, `qwen2.5:1.5b`,
Codespace 2 cœurs / 8 Go minimum, à choisir dans *New with options*).

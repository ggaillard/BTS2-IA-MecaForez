# AGENTS.md — consignes pour l'agent de code

> Ce fichier est lu par l'agent avant chaque travail. Écrivez-le comme pour un
> développeur qui arrive le premier jour : court, précis, sans ambiguïté.

## Le projet

<!-- Une phrase : ce que fait l'application, pour qui. Renvoyer vers SPEC.md. -->

## Pile technique

<!-- Langage, version de .NET, framework de test, outil Gherkin. -->

## Commandes

<!-- Les commandes exactes pour compiler et tester, à lancer depuis ce dossier. -->

```bash
dotnet build
dotnet test
```

## Organisation du code

<!-- Où va le code métier, où vont les étapes de test, conventions de nommage. -->

## Interdits

<!-- Au moins trois. Le premier est déjà écrit : ne le retirez pas. -->

- Ne jamais modifier un fichier `.feature` : ils sont le contrat. Si un scénario semble faux, s'arrêter et le signaler.
-

## Définition de « terminé »

<!-- Une condition vérifiable par une commande, pas une impression. -->

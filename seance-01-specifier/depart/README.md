# Projet de départ — suivi des PC de prêt

Solution .NET 10 prête à l'emploi : une bibliothèque `PretsMateriel` et un projet de tests
`PretsMateriel.Specs` (xUnit + Reqnroll, scénarios Gherkin en français).

```bash
dotnet test      # attendu au départ : Passed! - Failed: 0, Passed: 1
```

| Fichier | Rôle | Qui l'écrit |
|---|---|---|
| `SPEC.md` | règles de gestion, messages, questions au tuteur | vous |
| `tests/PretsMateriel.Specs/Features/Prets.feature` | scénarios d'acceptation : le contrat | vous |
| `AGENTS.md` | consignes permanentes de l'agent | vous |
| `src/PretsMateriel/*.cs` | le code métier | l'agent |
| `tests/PretsMateriel.Specs/Steps/*.cs` | le lien entre chaque ligne Gherkin et le code | l'agent |
| `GRILLE_ECART.md`, `REPONSE_TUTEUR.md` | la revue et le compte rendu | vous |

`Parc.feature` et `ParcSteps.cs` sont un exemple complet et fonctionnel : lisez-les avant d'écrire vos scénarios.
Une ligne Gherkin sans méthode associée fait échouer le test (`reqnroll.json`) : c'est voulu.

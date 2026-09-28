using PretsMateriel;

namespace PretsMateriel.Specs.Steps;

/// <summary>
/// État partagé par les étapes d'un même scénario : Reqnroll crée un ContexteParc neuf pour chaque scénario
/// et le passe à toutes les classes [Binding] qui le demandent dans leur constructeur.
/// </summary>
public class ContexteParc
{
    public Parc Parc { get; } = new();
}

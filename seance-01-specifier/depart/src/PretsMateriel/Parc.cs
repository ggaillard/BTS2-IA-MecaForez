namespace PretsMateriel;

/// <summary>
/// Le parc de PC de prêt de Méca Forez.
/// Point de départ : on sait ajouter des PC et lister ceux qui sont disponibles.
/// Tout le reste (prêts, retours, retards) est à faire produire par l'agent, à partir de VOTRE spécification.
/// </summary>
public class Parc
{
    private readonly Dictionary<string, Materiel> _materiels = new();

    public void Ajouter(string code, string libelle) => _materiels.Add(code, new Materiel(code, libelle));

    public IReadOnlyList<Materiel> Disponibles() =>
        _materiels.Values.Where(m => !m.EnReparation).ToList();
}

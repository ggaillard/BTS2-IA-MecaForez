namespace PretsMateriel;

/// <summary>Un PC portable du parc de prêt, identifié par son code (PC-01…).</summary>
public class Materiel(string code, string libelle)
{
    public string Code { get; } = code;
    public string Libelle { get; } = libelle;

    /// <summary>Vrai tant que le technicien l'a déclaré en réparation.</summary>
    public bool EnReparation { get; set; }
}

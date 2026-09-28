using Reqnroll;

namespace PretsMateriel.Specs.Steps;

[Binding]
public class ParcSteps(ContexteParc ctx)
{
    [Given("le parc contient les PC suivants :")]
    public void LeParcContient(DataTable pcs)
    {
        foreach (var ligne in pcs.Rows)
            ctx.Parc.Ajouter(ligne["code"], ligne["libellé"]);
    }

    private int _nbDisponibles;

    [When("je consulte les PC disponibles")]
    public void JeConsulteLesDisponibles() => _nbDisponibles = ctx.Parc.Disponibles().Count;

    [Then("{int} PC sont disponibles")]
    public void NbDisponibles(int attendu) => Assert.Equal(attendu, _nbDisponibles);
}

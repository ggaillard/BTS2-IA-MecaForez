#language: fr
Fonctionnalité: Consulter le parc de prêt
  Afin de savoir quels PC je peux prêter
  En tant que technicien du service informatique
  Je veux voir les PC disponibles

  Scénario: Tous les PC sont disponibles au départ
    Étant donné que le parc contient les PC suivants :
      | code  | libellé            |
      | PC-01 | Dell Latitude 5440 |
      | PC-02 | Dell Latitude 5440 |
      | PC-03 | Dell Latitude 5440 |
      | PC-04 | Lenovo ThinkPad E14 |
      | PC-05 | Lenovo ThinkPad E14 |
      | PC-06 | Lenovo ThinkPad E14 |
    Quand je consulte les PC disponibles
    Alors 6 PC sont disponibles

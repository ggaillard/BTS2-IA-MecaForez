# 📧 La demande du tuteur

> **De :** Karim Belkacem, responsable du service informatique — Méca Forez
> **À :** vous, stagiaire SLAM
> **Objet :** Tri des tickets — avant qu'on branche quoi que ce soit

Salut,

Bravo pour les PC de prêt, Thomas l'utilise tous les jours.

Autre sujet. On reçoit une quarantaine de tickets par jour sur la boîte
support. Chaque matin, Thomas passe une demi-heure à les trier : de quoi ça
parle, et est-ce que c'est **urgent**. Le problème, c'est qu'entre 8h et 8h30
un ticket grave peut attendre derrière dix demandes de souris.

La direction a vu une démo et voudrait « brancher ChatGPT dessus ». Non : les
tickets contiennent des noms, parfois des mots de passe, et des infos sur la
production. **Rien ne sort de chez nous.** J'ai installé Ollama sur une machine
de test, sans carte graphique. Si un petit modèle fait le travail en local,
on regarde.

Mais avant de brancher quoi que ce soit, je veux savoir **à quel point il se
trompe**. Et surtout : est-ce qu'il **rate les urgences** ? Un ticket
« souris » classé urgent, Thomas s'en remettra. Une ligne de production à
l'arrêt classée « pas pressé », non.

Je t'ai extrait **30 tickets** de la semaine dernière, anonymisés
(`depart/tickets.jsonl`). On range les tickets dans cinq catégories : poste,
logiciel, réseau, accès, impression. Et trois priorités, P1, P2, P3.

Ne me dis pas « ça marche plutôt bien ». Je veux des **chiffres**, et je veux
pouvoir refaire la mesure moi-même dans six mois quand on changera de modèle.

À la fin : est-ce qu'on le branche, oui ou non, et à quelles conditions ?

Merci,
Karim

---

> 💡 **Avant de lancer quoi que ce soit :** pour mesurer si le modèle a
> raison, il faut savoir ce qu'est « la bonne réponse ». Or ce mail ne dit ni
> ce qu'est une urgence, ni à partir de quand le modèle est « assez bon ».
> Repérez au moins **quatre imprécisions** et allez poser vos questions au
> tuteur (votre enseignant joue ce rôle pendant la séance).

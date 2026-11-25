# Boucles opérationnelles — catalogue fondateur

Projet : `WT-PROJECT-OSINT-001`
Continuité : `WT-OSINT-CONTINUITY-20261125-01`
Chantier : OSINT-F01 / issue #1. Statut : spécifications, non exécution runtime.
Les socles A01–A18 sont définis dans [AUTOMATION.md](AUTOMATION.md). Les boucles L01–L18 les composent ; elles ne sont pas dix-huit services ni dix-huit autorités de tâches.

| ID | Boucle | Déclencheur / entrée | Socles | Sortie et contrôle |
| --- | --- | --- | --- | --- |
| L01 | Intake | Demande ou événement authentifié | A01 A02 A06 | Mandat qualifié, périmètre ; refus ou clarification si ambigu |
| L02 | Memory | Mandat qualifié ou reprise | A01 A10 A17 | Checkpoint et preuves datées ; divergence signalée |
| L03 | Discovery | Objectif qualifié | A02 A06 A11 A18 | Candidats sources/capacités ; aucun accès sans qualification |
| L04 | Planning | Contexte vérifié | A02 A06 A18 | Plan versionné, DAG sans cycle, critères d'acceptation |
| L05 | Task management | Plan admissible | A03 A04 A05 A06 | Tâche prête ou bloquée ; attribution durable avant effet |
| L06 | Development | Tâche ingénierie détenue | A04 A07 A08 A18 | Diff isolé, tests et références ; aucune écriture hors dépôt |
| L07 | Testing | Candidat versionné | A08 A10 | Résultats positifs/négatifs associés au SHA |
| L08 | Review | Candidat et résultats | A06 A08 A10 | Constats, décisions de revue, aucune auto-approbation simulée |
| L09 | Correction | Échec ou constat | A04 A05 A08 A16 | Correction bornée, nouveau candidat ou blocage motivé |
| L10 | Integration | Candidat revu | A06 A08 A09 | Fusion autorisée, SHA intégré vérifié ; gate sinon |
| L11 | Deployment | Artefact intégré | A06 A09 A10 | Effet attesté, rollback disponible ; pas de déploiement implicite |
| L12 | Certification | Preuves et état réel | A08 A09 A10 A17 | Attestation bornée ou NON_VERIFIABLE |
| L13 | Documentation | Changement ou drift | A01 A10 A17 | Registres et checkpoint alignés ; pas de certification fictive |
| L14 | Intelligence collection | Mission et source approuvées | A03 A05 A06 A11 A12 | Observations sourcées, limites, rétention ; pas de contournement |
| L15 | Intelligence verification | Observations disponibles | A10 A13 A14 | Faits qualifiés, contradictions et lacunes explicites |
| L16 | Intelligence analysis | Faits qualifiés | A06 A13 A14 A15 | Produit sourcé ; abstention si preuve insuffisante |
| L17 | Monitoring | Cadence autorisée ou incident | A03 A10 A15 A16 | Signal dédupliqué, incident ou tâche admissible |
| L18 | Self-improvement | Incident ou mesure vérifiée | A02 A08 A16 A17 | Proposition bornée, tests, passage par L04–L13 ; pas d'auto-élévation |

## Enchaînement de référence
Ingénierie : L01 → L02 → L04 → L05 → L06 → L07 → L08 → L10 → L11 (si autorisé) → L12 → L13. L09 revient à L07 avec un nouveau candidat ; L17/L18 alimentent L01/L04. L03 intervient selon besoin, sans dépendance imposée.
Renseignement : L01 → L02 → L03 → L04 → L05 → L14 → L15 → L16 → publication autorisée via A15 → L13/L17. Un contenu collecté ne donne jamais une autorisation de commande ou de développement.
Un blocage local ne bloque pas les tâches indépendantes admissibles ; une dépendance bloquée n'est pas réputée satisfaite.

## Invariants de passage
- Identité, continuité, run/task, politique versionnée et autorisation vérifiés à chaque passage.
- Aucun effet externe sur lease expiré, fence obsolète, entrée non autorisée ou budget dépassé.
- Aucune nouvelle tentative d'un effet ambigu avant réconciliation ; rejouer seulement les effets dont la sémantique est sûre.
- Checkpoint après transition durable ; erreurs, preuve, prochaine action et dépendances consignées.
- Aucun cron, worker ou exécuteur de collecte activé par ce catalogue.

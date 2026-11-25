# Socles d'automatisation — exigences fondatrices F01

Projet : `WT-PROJECT-OSINT-001`
Continuité : `WT-OSINT-CONTINUITY-20261125-01`
Statut : exigences de conception proposées, non certification runtime.

## Deux plans séparés
- Ingénierie : intake, qualification, plan, tâches, code, tests, revue, intégration, déploiement, certification, maintenance.
- Renseignement : mission, découverte, qualification de source, autorisation, collecte, normalisation, vérification, corrélation, analyse, diffusion, surveillance.
Les identités, permissions, secrets et effets des deux plans sont séparés. Aucune donnée externe ne peut déclencher une commande ou modifier les politiques.

## Catalogue de socles et critères de validation futurs

| ID | Socle | Critère d'acceptation |
| --- | --- | --- |
| A01 | Identité, mémoire, registres et reprise | Reprise d'un checkpoint vérifié sans doublon ; référence stable |
| A02 | Entrées, intentions et planification | Mandat ambigu ou hors périmètre bloqué ; plan et dépendances explicites |
| A03 | File durable, scheduler et déclencheurs | Redémarrage sans perte ; événements dupliqués dédupliqués |
| A04 | Claims, leases, fencing, coordination | Deux workers ne commettent pas le même effet ; jeton périmé rejeté |
| A05 | Idempotence, outbox, retries, DLQ | Rejeu sûr, backoff borné, erreurs terminales visibles |
| A06 | Identités, politiques, secrets, budgets et quotas | Refus par défaut ; aucune fuite de secret ; limites contrôlées |
| A07 | Exécution isolée, outils et sandbox | Aucun accès hors périmètre ; effets externes soumis à autorisation |
| A08 | CI, tests, non-régression et revue | Tests positifs/négatifs reproductibles sur SHA exact |
| A09 | Intégration, artefacts, déploiement et rollback | Artefact lié au SHA, gates, attestation, rollback testé |
| A10 | Observabilité, preuves et audit | Corrélation run/task/effect ; alertes et historique vérifiables |
| A11 | Registre de sources et accès légitime | Source, licence, conditions, cadence, décision d'accès et rétention |
| A12 | Connecteurs, collecte et reprise | Collecte autorisée, incrémentale, limitée, relecture de fixtures |
| A13 | Qualité, provenance et résolution d'entités | Valeurs sourcées, conflits explicites, aucune invention |
| A14 | Orchestration IA, vérification et garde-fous | Injection indirecte contenue ; sorties sourcées ; abstention |
| A15 | Publication, alertes et surveillance | Destinataires autorisés ; déduplication ; corrections versionnées |
| A16 | Auto-diagnostic, remédiation et amélioration | Correction bornée et testée ; arrêt sûr si invariants violés |
| A17 | Reconciliation documentaire et configuration | Drift détecté ; correction attestée ; sources non lues non certifiées |
| A18 | Interopérabilité, contrats et migrations | Versions compatibles ; tests de contrat ; pas d'autorité concurrente |

## Composition opérationnelle
Voir [LOOPS.md](LOOPS.md) pour les 18 boucles et leurs dépendances aux socles. Le catalogue A01–A18 reste la référence des capacités ; les boucles ne constituent pas une seconde autorité.

## Contrat minimal d'une exécution
Une mission doit porter project_id, continuity_id, task_id, run_id, plan (engineering/intelligence), objectif, périmètre autorisé, identité d'exécution, dépendances, version des politiques, état, budget, échéance, clé d'idempotence, références des entrées, effets et preuves, checkpoint et prochaine action. Les claims/leases/fencing ne seront pas simulés : une autorité durable doit être choisie et testée avant d'autoriser les writers concurrents.

États proposés : PENDING -> READY -> CLAIMED -> RUNNING -> VERIFYING -> SUCCEEDED ; branches BLOCKED, RETRY_WAIT, FAILED, CANCELLED. Un état de tâche ne prouve pas l'effet externe : réconcilier avant de rejouer. Un blocage de déploiement n'interdit pas le développement indépendant admissible.

## Insertion dans le fil conducteur existant
- 01.A : constitution et ancrage GitHub ; 01.B : gouvernance, continuité et contrôle documentaire ; 01.C : décision métier.
- 05.A : inventaire des contrats d'automatisation et des effets ; 06.A : recherche de capacités réutilisables (UAES, CUG/GRT, MCP ou autres, sans dépendance imposée).
- 10.A : politique d'accès aux sources, threat model, protection des données ; 11.A : configuration GitHub, Project V2, règles et CI.
- 12.A : dépendances et critères de passage ; 13.A : usine de développement minimale ; 13.B : coordination durable et reprise ; 13.C : certification et intégration gouvernée.
- 14.A : socle runtime de renseignement ; 14.B : pilote sur sources autorisées et fixtures ; 18.A : test des pannes, rollback, exploitation.
Les 19 étapes initiales restent stables. Les sous-étapes sont des extensions et peuvent être raffinées.

## Gates de progression
G0 identité et continuité ; G1 périmètre et exigences ; G2 architecture et sécurité ; G3 contrôle CI et preuve ; G4 coordination durable ; G5 collecte pilote autorisée ; G6 intégration et déploiement attestés ; G7 exploitation et amélioration. Les gates non applicables sont motivés ; aucun gate non vérifié n'est réputé PASS.

## Premier incrément
Un contrôle documentaire local, sans dépendance applicative, vérifie les identifiants et les liens documentaires attendus ; il ne certifie ni la gouvernance complète, ni l'usine autonome. CI sur PR et main si le dépôt et les permissions le permettent. Aucun cron, collecte réseau ni worker permanent activé.

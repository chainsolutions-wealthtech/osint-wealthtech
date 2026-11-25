# Suivi et point de reprise courant

Projet : `WT-PROJECT-OSINT-001`
Continuité : `WT-OSINT-CONTINUITY-20261125-01`
Chantier : [OSINT-F01 — issue #1](https://github.com/chainsolutions-wealthtech/osint-wealthtech/issues/1)
Date : 2026-11-25

## État
- README initial sur main : commit d422bdf140f1ce2aa8e34c519bbe6ad4019592e9, relu.
- Phase 01, fondations : branche foundation/osint-f01-automation ; PR #2 ouverte, non intégrée à main.
- Premier contrôle CI confirmé : [run #1](https://github.com/chainsolutions-wealthtech/osint-wealthtech/actions/runs/45633215886), SUCCESS sur le candidat précédent 356b1d2753739166fe146c527d6ab59e2826ad19 ; ne vaut pas preuve pour les modifications ultérieures.
- Catalogue L01–L18 et registre DECISIONS.md ajoutés ; contrat documentaire à renforcer et retester.
- Décision 01 (périmètre) : ouverte. Aucune stack applicative ou licence choisie.
- GitHub Project V2 : non attesté. Paramétrage admin et rulesets à vérifier.
- Aucun worker, collecte ou déploiement activé.

## Point de reprise
Vérifier le nouveau SHA de la PR, la couverture A01–A18 et L01–L18 et les checks réels ; traiter les limites de configuration, contrôler la cohérence des documents puis intégrer seulement selon autorisation et gates applicables. Ensuite, reprendre la décision 01 sans changer l'identifiant de continuité. Les autres projets restent hors périmètre.

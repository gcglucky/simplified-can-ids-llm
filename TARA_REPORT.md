# Rapport d'Analyse TARA (ISO/SAE 21434) - IDS Automobile

## 1. Données de Télémétrie CAN Capturées
- **Fichier analyse** : candump-2026-10-30_093449.log
- **Nombre total de trames** : 1000
- **Intervalle moyen (Δt)** : 2.21 ms *(Standard attendu : ~100 ms)*
- **Intervalle minimal (Δt min)** : 0.01 ms

## 2. Synthèse d'Incident & Analyse TARA

### A. Identification de l'Item
- **ID CAN ciblé** : `0x0B0`
- **Domaine** : Powertrain / Chassis Control Unit.

### B. Scénario de Menace (Threat Scenario)
- **Type d'attaque** : **Denial of Service (DoS) par Submersion (Flooding)**.
- **Preuve comportementale** : L'injection de 1000 trames avec un Delta_t moyen de 2.21 ms surcharge la bande passante du bus et empêche la réception des messages prioritaires à cycle régulier.

### C. Évaluation de l'Impact (ISO/SAE 21434)
- **Safety Impact** : Élevé (Risque de perte d'affichage de vitesse ou de retard d'exécution de commandes critiques).
- **Financial Impact** : Modéré.
- **Operational Impact** : Élevé (Dégradation du mode de conduite).

### D. Recommandations de Sécurisation (Mitigation)
1. **SecOC (Secure On-Board Communication)** : Implémenter des MAC (Message Authentication Code) pour valider l'authenticité et la fraîcheur des messages.
2. **Filtrage au niveau Gateway** : Bloquer les trames dont la périodicité s'écarte de plus de 50% de leur valeur nominale.
3. **Hardware Isolation** : Séparer les calculateurs télématiques (Infotainment) du bus CAN critique via une Gateway sécurisée.

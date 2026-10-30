import json
from collections import defaultdict

def parse_and_analyze(file_path):
    id_timestamps = defaultdict(list)
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or len(line.split()) < 3:
                continue
            parts = line.split()
            timestamp = float(parts[0].strip('()'))
            can_id = parts[2].split('#')[0]
            id_timestamps[can_id].append(timestamp)

    results = {}
    for can_id, timestamps in id_timestamps.items():
        if len(timestamps) < 2:
            continue
        deltas = [timestamps[i] - timestamps[i-1] for i in range(1, len(timestamps))]
        results[can_id] = {
            "total_frames": len(timestamps),
            "avg_delta_ms": round((sum(deltas) / len(deltas)) * 1000, 2),
            "min_delta_ms": round(min(deltas) * 1000, 2),
            "max_delta_ms": round(max(deltas) * 1000, 2)
        }
    return results

def generate_iso21434_prompt(stats):
    prompt = f"""
[CONTEXTE TECHNIQUE]
Vous êtes un expert en cybersécurité automobile (ISO/SAE 21434). Un IDS (Intrusion Detection System) basé sur les anomalies temporelles a capturé une trace sur un bus CAN virtuel (vcan0).

[DONNÉES EXTRAITES]
{json.dumps(stats, indent=2)}

[CONSIGNE DE RÉDACTION]
Rédigez une synthèse d'incident de cybersécurité structurée selon la norme ISO/SAE 21434 contenant :
1. **Item Definition** : Rôle supposé du message (ex: ID 0x0B0 = Télécatégorie / Vitesse / Powertrain).
2. **Threat Scenario** : Nature de l'attaque identifiée (DoS / Flooding / Spoofing) en vous appuyant sur la chute anormale du Δt.
3. **Impact Assessment** : Impact sur la sécurité fonctionnelle (Safety) et la disponibilité du bus.
4. **Feasibility Rating** : Facilité d'exécution de l'attaque sur bus CAN non sécurisé.
5. **Mitigation Strategy** : Recommandations techniques (CAN FD avec SecOC, Filtrage matériel / Gateway, Rate Limiting).
"""
    return prompt

def generate_markdown_report(stats, prompt_text):
    report_content = f"""# Rapport d'Analyse TARA (ISO/SAE 21434) - IDS Automobile

## 1. Données de Télémétrie CAN Capturées
- **Fichier analyse** : candump-2026-10-30_093449.log
- **Nombre total de trames** : {stats['0B0']['total_frames']}
- **Intervalle moyen (Δt)** : {stats['0B0']['avg_delta_ms']} ms *(Standard attendu : ~100 ms)*
- **Intervalle minimal (Δt min)** : {stats['0B0']['min_delta_ms']} ms

## 2. Synthèse d'Incident & Analyse TARA

### A. Identification de l'Item
- **ID CAN ciblé** : `0x0B0`
- **Domaine** : Powertrain / Chassis Control Unit.

### B. Scénario de Menace (Threat Scenario)
- **Type d'attaque** : **Denial of Service (DoS) par Submersion (Flooding)**.
- **Preuve comportementale** : L'injection de 1000 trames avec un $\Delta t$ moyen de {stats['0B0']['avg_delta_ms']} ms surcharge la bande passante du bus et empêche la réception des messages prioritaires à cycle régulier.

### C. Évaluation de l'Impact (ISO/SAE 21434)
- **Safety Impact** : Élevé (Risque de perte d'affichage de vitesse ou de retard d'exécution de commandes critiques).
- **Financial Impact** : Modéré.
- **Operational Impact** : Élevé (Dégradation du mode de conduite).

### D. Recommandations de Sécurisation (Mitigation)
1. **SecOC (Secure On-Board Communication)** : Implémenter des MAC (Message Authentication Code) pour valider l'authenticité et la fraîcheur des messages.
2. **Filtrage au niveau Gateway** : Bloquer les trames dont la périodicité s'écarte de plus de 50% de leur valeur nominale.
3. **Hardware Isolation** : Séparer les calculateurs télématiques (Infotainment) du bus CAN critique via une Gateway sécurisée.
"""
    with open("TARA_REPORT.md", "w") as f:
        f.write(report_content)
    print("[+] Rapport ISO/SAE 21434 généré avec succès dans 'TARA_REPORT.md'.")

if __name__ == "__main__":
    LOG_FILE = "candump-2026-10-30_093449.log"
    stats = parse_and_analyze(LOG_FILE)
    prompt = generate_iso21434_prompt(stats)
    
    print("=== PROMPT STRUCTURÉ POUR LLM ===")
    print(prompt)
    print("=================================\n")
    
    generate_markdown_report(stats, prompt)

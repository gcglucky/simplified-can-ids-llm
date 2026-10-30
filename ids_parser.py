import sys
from collections import defaultdict

def parse_candump(file_path):
    """Parse le fichier candump et extrait les timestamps par ID CAN."""
    id_timestamps = defaultdict(list)
    
    try:
        with open(file_path, 'r') as f:
            for line in f:
                # Format standard candump : (1730286889.123456) vcan0 0B0#0011223344556677
                line = line.strip()
                if not line:
                    continue
                
                parts = line.split()
                if len(parts) >= 3:
                    # Extraction du timestamp en enlevant les parenthèses
                    timestamp = float(parts[0].strip('()'))
                    
                    # Extraction de l'ID CAN (avant le '#')
                    can_frame = parts[2]
                    can_id = can_frame.split('#')[0]
                    
                    id_timestamps[can_id].append(timestamp)
    except FileNotFoundError:
        print(f"Erreur : Le fichier {file_path} est introuvable.")
        sys.exit(1)
        
    return id_timestamps

def analyze_frequencies(id_timestamps):
    """Calcule les delta t (Δt) entre les trames successives pour détecter les anomalies."""
    results = {}
    
    for can_id, timestamps in id_timestamps.items():
        if len(timestamps) < 2:
            continue
            
        # Calcul des différences de temps entre trames successives
        deltas = [timestamps[i] - timestamps[i-1] for i in range(1, len(timestamps))]
        
        avg_delta = sum(deltas) / len(deltas)
        min_delta = min(deltas)
        max_delta = max(deltas)
        
        # Stockage en millisecondes pour une meilleure lisibilité
        results[can_id] = {
            'count': len(timestamps),
            'avg_delta_ms': avg_delta * 1000,
            'min_delta_ms': min_delta * 1000,
            'max_delta_ms': max_delta * 1000
        }
    return results

if __name__ == "__main__":
    # Remplace par le nom exact de ton fichier généré
    LOG_FILE = "candump-2026-10-30_093449.log" 
    
    print(f"[*] Analyse du fichier : {LOG_FILE}")
    timestamps = parse_candump(LOG_FILE)
    stats = analyze_frequencies(timestamps)
    
    print("\n" + "="*65)
    print(f"{'CAN ID':<10} | {'Nb Trames':<10} | {'Δt Moyen (ms)':<12} | {'Δt Min (ms)':<12}")
    print("="*65)
    
    for can_id, stat in stats.items():
        print(f"{can_id:<10} | {stat['count']:<10} | {stat['avg_delta_ms']:<12.2f} | {stat['min_delta_ms']:<12.2f}")
    print("="*65)
    
    # Préparation du prompt pour la phase 3
    print("\n[+] Prétraitement terminé. Ce tableau sera envoyé au LLM pour classification.")

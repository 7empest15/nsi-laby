import time
from datetime import datetime

class Logger:
    def __init__(self, filename):
        self.filename = filename
        # Créer ou vider le fichier de log
        with open(self.filename, 'w', encoding='utf-8') as f:
            f.write(f"=== Début des logs {datetime.now()} ===\n")
    
    def log(self, message):
        # Ajouter un timestamp et écrire dans le fichier
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        with open(self.filename, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] {message}\n")

# Créer les instances pour les différents types de logs
combat_logger = Logger("combat.log")
pathfind_logger = Logger("pathfind.log") 
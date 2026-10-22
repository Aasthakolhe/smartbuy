import time
import subprocess

def run_pipeline():
    print("\n--- [REAL-TIME SYNC] Running Scraping Pipeline ---")
    subprocess.run(["python", "run_bulk.py"])
    
    print("\n--- [REAL-TIME SYNC] Updating ML Predictions ---")
    subprocess.run(["python", "analysis.py"])
    print("--- [REAL-TIME SYNC] Dashboard Data Ready! ---\n")

if __name__ == "__main__":
    while True:
        run_pipeline()
        # Wait 3600 seconds (1 hour) before the next live sync
        time.sleep(3600)
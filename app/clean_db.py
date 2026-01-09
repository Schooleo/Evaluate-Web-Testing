import os
import subprocess
import time
import sys
import requests

def run_command(command):
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"Command failed with code {result.returncode}")
        # We don't exit here because 'docker compose down' might fail if not running, which is fine-ish
    return result.returncode

def main():
    # Ensure we are in the correct directory (where docker-compose.yml is)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    db_path = os.path.join("content", "data", "ghost.db")
    
    print("Stopping Ghost container...")
    run_command("docker compose down")
    
    if os.path.exists(db_path):
        print(f"Removing database: {db_path}")
        try:
            os.remove(db_path)
            print("Database removed.")
        except OSError as e:
            print(f"Error removing file: {e}")
            print("Please ensure the file is not in use (Docker container stopped).")
            return
    else:
        print(f"Database file not found at {db_path}")

    print("Starting Ghost container...")
    run_command("docker compose up -d")
    
    print("Waiting for Ghost to eventually start...")
    while True:
        try:
            response = requests.get("http://localhost:2368")
            if response.status_code == 200:
                break
        except requests.exceptions.RequestException:
            pass
        time.sleep(1)
    print("Ghost CMS has been restarted.")

if __name__ == "__main__":
    main()

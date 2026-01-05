import json
import time
import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Add current directory to path
sys.path.append(os.getcwd())

from evaluate.evaluator import Evaluator

def main():
    # 1. Load configuration and tasks
    try:
        with open('env_config.json', 'r') as f:
            env_config = json.load(f)
        with open('dataset/tasks.json', 'r') as f:
            tasks = json.load(f)
    except FileNotFoundError as e:
        print(f"Error loading files: {e}")
        return

    # 2. Initialize Evaluator
    evaluator = Evaluator(tasks)

    # 3. Ask user which task to run
    print(f"Loaded {len(tasks)} tasks.")
    task_id = input("Enter Task ID to run (e.g., 1): ").strip()
    
    task = next((t for t in tasks if t['task_id'] == task_id), None)
    
    if not task:
        print(f"Task {task_id} not found.")
        return

    print(f"\n--- Task {task_id} ---")
    print(f"Description: {task['task_description']}")
    
    # Resolve start URL
    start_url_key = task['start_url']
    start_url = start_url_key
    
    # Check if key exists in env_config
    if start_url_key in env_config:
         start_url = env_config[start_url_key]['url']

    print(f"Start URL: {start_url}")

    # 4. Initialize WebDriver (Chrome)
    print("\nLaunching Browser...")
    chrome_options = Options()
    # chrome_options.add_argument("--headless") 
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # 5. Navigate to start
        if start_url.startswith("http"):
            driver.get(start_url)
        else:
            print(f"Warning: Could not resolve valid start URL from {start_url_key}")

        # Handle explicit login requirement mention
        if task.get("require_login"):
            print("\n*** NOTE: This task requires you to be LOGGED IN. ***")
            print("If you are not logged in, please log in manually first (admin@example.com / password).")

        # 6. ACTION PHASE
        print("\n" + "="*50)
        print(f"ACTION REQUIRED: Please perform the task in the opened browser window.")
        print(f"Task: {task['task_description']}")
        print("="*50)
        
        input("\nPress Enter here once you have completed the task in the browser...")

        # 7. EVALUATION PHASE
        print("\nRunning Evaluation...")
        success = evaluator.evaluate_with_selenium(task_id, browser=driver)
        
        if success:
            print("\n✅ PASSED!")
        else:
            print("\n❌ FAILED")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Keep browser open for a moment or close depending on preference
        # driver.quit()
        pass

if __name__ == "__main__":
    main()

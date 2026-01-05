import json
import time
import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Add current directory to path
sys.path.append(os.getcwd())

from evaluate.evaluator import Evaluator

def print_summary(results):
    print("\n" + "="*80)
    print(f"{'ID':<5} | {'Result':<10} | {'Description'}")
    print("-" * 80)
    for res in results:
        status_icon = "✅ PASS" if res['success'] else "❌ FAIL"
        # Truncate description if too long
        desc = (res['description'][:60] + '..') if len(res['description']) > 60 else res['description']
        print(f"{res['id']:<5} | {status_icon:<10} | {desc}")
    print("="*80)
    
    total = len(results)
    passed = sum(1 for r in results if r['success'])
    print(f"Total: {total} | Passed: {passed} | Section Completion Rate: {(passed/total)*100:.1f}%")

def run_task(task, evaluator, driver, env_config):
    print(f"\n--- Task {task['task_id']} ---")
    print(f"Description: {task['task_description']}")
    
    # Resolve start URL
    start_url_key = task['start_url']
    start_url = start_url_key
    if start_url_key in env_config:
         start_url = env_config[start_url_key]['url']

    print(f"Start URL: {start_url}")

    try:
        # Navigate
        if start_url.startswith("http"):
             driver.get(start_url)
        else:
             print(f"Warning: Could not resolve valid start URL from {start_url_key}")
        
        if task.get("require_login"):
            print("(!) Note: This task requires login.")

        # ACTION
        print(f"\n[ACTION REQUIRED] Perform: {task['task_description']}")
        input("Press Enter when done...")

        # EVAL
        print("Evaluating...")
        success = evaluator.evaluate_with_selenium(task['task_id'], browser=driver)
        if success:
            print("✅ PASSED")
        else:
            print("❌ FAILED")
            
        return success
    except Exception as e:
        print(f"Error running task: {e}")
        return False

def main():
    try:
        with open('env_config.json', 'r') as f:
            env_config = json.load(f)
        with open('dataset/tasks.json', 'r') as f:
            tasks = json.load(f)
    except FileNotFoundError as e:
        print(f"Error loading files: {e}")
        return

    evaluator = Evaluator(tasks)
    
    print(f"Loaded {len(tasks)} tasks.")
    choice = input("Enter Task ID to run, or 'all' to run sequence: ").strip()

    tasks_to_run = []
    if choice.lower() == 'all':
        tasks_to_run = tasks
    else:
        task = next((t for t in tasks if t['task_id'] == choice), None)
        if task:
            tasks_to_run = [task]
        else:
            print(f"Task {choice} not found.")
            return

    # Init Browser Once
    print("\nLaunching Browser...")
    chrome_options = Options()
    # chrome_options.add_argument("--headless") 
    driver = webdriver.Chrome(options=chrome_options)

    results = []

    try:
        for task in tasks_to_run:
            success = run_task(task, evaluator, driver, env_config)
            results.append({
                "id": task['task_id'],
                "description": task['task_description'],
                "success": success
            })
            
            if len(tasks_to_run) > 1 and task != tasks_to_run[-1]:
                cont = input("\nProceed to next task? (Y/n): ")
                if cont.lower() == 'n':
                    break
    
    finally:
        # driver.quit() # Optional: close browser
        pass
    
    # Print Summary Table
    print_summary(results)

if __name__ == "__main__":
    main()

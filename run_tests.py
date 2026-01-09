import argparse
import sys
import os
import json

sys.path.append(os.getcwd())

from evaluate.automation_tester import AutomationTester
from evaluate.evaluator import Evaluator
from playwright.sync_api import sync_playwright

def run_manual_mode(task_ids, tasks_file_path='dataset/tasks.json', env_config_path='env_config.json'):
    with open(tasks_file_path, 'r') as f:
        tasks = json.load(f)
    with open(env_config_path, 'r') as f:
        env_config = json.load(f)
    
    tasks_map = {t['task_id']: t for t in tasks}
    
    if "all" in task_ids:
        task_ids = list(tasks_map.keys())
    
    evaluator = Evaluator(tasks=tasks, env_config=env_config)
    results = []
    
    for task_id in task_ids:
        if task_id not in tasks_map:
            print(f"Task ID {task_id} not found. Skipping.")
            continue
        
        task = tasks_map[task_id]
        print("\n" + "="*60)
        print(f"MANUAL MODE - Task ID: {task_id}")
        print(f"Description: {task['task_description']}")
        print("="*60)
        
        start_url = task.get('start_url', '')
        for key, conf in env_config.items():
            if key in start_url:
                start_url = start_url.replace(key, conf.get('url', ''))
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(viewport={'width': 1280, 'height': 800})
            page = context.new_page()
            
            if start_url:
                print(f"Navigating to: {start_url}")
                page.goto(start_url)
                page.wait_for_load_state("networkidle")
            
            print("\n>>> MANUAL INTERACTION MODE <<<")
            print("Perform your actions in the browser window.")
            input("Press ENTER when done to run evaluation...")
            
            print("\n--- EVALUATING ---")
            success = evaluator.evaluate(task_id, page)
            
            result_str = "✅ PASS" if success else "❌ FAIL"
            print(f"Result: {result_str}")
            
            results.append({
                "id": task_id,
                "file": "MANUAL",
                "success": success
            })
            
            context.close()
            browser.close()
    
    return results

def main():
    parser = argparse.ArgumentParser(description='Run modular test scripts.')
    parser.add_argument('--task_id', type=str, default="all", help='Task IDs to run, separated by commas (e.g. "1,20") or "all"')
    parser.add_argument('--headless', action='store_true', default=True, help='Run in headless mode (default: True)')
    parser.add_argument('--no-headless', dest='headless', action='store_false', help='Run in visible mode')
    parser.add_argument('--manual', action='store_true', help='Manual mode: perform actions yourself then evaluate')
    
    args = parser.parse_args()
    
    task_ids = []
    if args.task_id.lower() == "all":
        task_ids = ["all"]
    else:
        clean = args.task_id.replace(',', ' ')
        task_ids = [x.strip() for x in clean.split()]

    if args.manual:
        results = run_manual_mode(task_ids)
    else:
        tester = AutomationTester(
            tasks_file_path='dataset/tasks.json',
            env_config_path='env_config.json',
            headless=args.headless
        )
        results = tester.run_tests(task_ids=task_ids)
    
    print("\n" + "="*60)
    print(f"{'ID':<5} | {'Result':<10} | {'File'}")
    print("-" * 60)
    for res in results:
        status_icon = "✅ PASS" if res['success'] else "❌ FAIL"
        print(f"{res['id']:<5} | {status_icon:<10} | {res['file']}")
    print("="*60)

if __name__ == "__main__":
    main()

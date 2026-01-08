import argparse
import sys
import os

# Add current directory to path so imports work
sys.path.append(os.getcwd())

from evaluate.automation_tester import AutomationTester

def main():
    parser = argparse.ArgumentParser(description='Run modular test scripts.')
    parser.add_argument('--task_id', type=str, default="all", help='Task IDs to run, separated by commas (e.g. "1,20") or "all"')
    parser.add_argument('--headless', action='store_true', default=True, help='Run in headless mode (default: True)')
    parser.add_argument('--no-headless', dest='headless', action='store_false', help='Run in visible mode')
    
    args = parser.parse_args()
    
    # Parse IDs
    task_ids = []
    if args.task_id.lower() == "all":
        task_ids = ["all"]
    else:
        # Handle "1, 20" or "1 20"
        clean = args.task_id.replace(',', ' ')
        task_ids = [x.strip() for x in clean.split()]

    tester = AutomationTester(
        tasks_file_path='dataset/tasks.json',
        env_config_path='env_config.json',
        headless=args.headless
    )

    try:
        tester.start_driver()
        results = tester.run_tests(task_ids=task_ids)
        
        # Summary
        print("\n" + "="*60)
        print(f"{'ID':<5} | {'Result':<10} | {'File'}")
        print("-" * 60)
        for res in results:
            status_icon = "✅ PASS" if res['success'] else "❌ FAIL"
            print(f"{res['id']:<5} | {status_icon:<10} | {res['file']}")
        print("="*60)
        
    finally:
        tester.stop_driver()

if __name__ == "__main__":
    main()

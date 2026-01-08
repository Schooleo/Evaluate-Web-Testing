import os
import importlib.util
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from evaluate.evaluator import Evaluator

class AutomationTester:
    def __init__(self, tasks_file_path, env_config_path, headless=True):
        self.tasks_map = self._load_tasks(tasks_file_path)
        self.env_config = self._load_config(env_config_path)
        self.headless = headless
        self.driver = None

    def _load_tasks(self, path):
        with open(path, 'r') as f:
            tasks = json.load(f)
        # return dict for easy lookup by ID
        return {t['task_id']: t for t in tasks}

    def _load_config(self, path):
        with open(path, 'r') as f:
            return json.load(f)

    def start_driver(self):
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        # Ensure window size is standard
        chrome_options.add_argument("--window-size=1920,1080")
        
        print(f"Launching Browser (Headless: {self.headless})...")
        self.driver = webdriver.Chrome(options=chrome_options)

    def stop_driver(self):
        if self.driver:
            self.driver.quit()
            print("Browser closed.")

    def run_tests(self, task_ids=None):
        """
        Scans test_scripts/ folder and runs matching tasks.
        If task_ids is None URL 'all', runs all found scripts.
        """
        results = []
        script_dir = "test_scripts"
        
        # Get all python files in the directory
        files = [f for f in os.listdir(script_dir) if f.startswith("test_") and f.endswith(".py")]
        files.sort() # Run in order

        for filename in files:
            # Extract ID from filename assuming format: test_ID.py
            # e.g. test_20.py -> 20
            try:
                # split by underscore, take second element, remove extension
                # test_20.py -> ["test", "20.py"] -> "20"
                parts = filename.split('_')
                if len(parts) >= 2:
                    t_id = parts[1].replace('.py', '')
                else:
                    continue
                
                # Filter if specific IDs requested
                if task_ids and "all" not in task_ids and t_id not in task_ids:
                    continue

                print(f"\n{'='*60}")
                print(f"Running Test Script: {filename} (ID: {t_id})")
                
                # Dynamic Import
                file_path = os.path.join(script_dir, filename)
                spec = importlib.util.spec_from_file_location("module.name", file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Instantiate and Run
                # Convention: Script must have a class named 'TaskScript'
                if hasattr(module, 'TaskScript'):
                    test_instance = module.TaskScript(self.driver, self.env_config)
                    
                    # 1. ACTION
                    print("--- ACTION ---")
                    test_instance.action()
                    
                    # 2. VERIFY
                    print("--- VERIFY ---")
                    success = test_instance.verify()
                    
                    result_str = "✅ PASS" if success else "❌ FAIL"
                    print(f"Result: {result_str}")
                    
                    results.append({
                        "id": t_id,
                        "file": filename,
                        "success": success
                    })
                    
                else:
                    print(f"Error: {filename} missing 'TaskScript' class.")

            except Exception as e:
                print(f"Error running {filename}: {e}")
                results.append({
                    "id": t_id if 't_id' in locals() else "unknown",
                    "file": filename,
                    "success": False,
                    "error": str(e)
                })

        return results

import os
import importlib.util
import json
import time
from playwright.sync_api import sync_playwright

class AutomationTester:
    def __init__(self, tasks_file_path, env_config_path, headless=True):
        self.tasks_map = self._load_tasks(tasks_file_path)
        self.env_config = self._load_config(env_config_path)
        self.headless = headless

    def _load_tasks(self, path):
        with open(path, 'r') as f:
            tasks = json.load(f)
        return {t['task_id']: t for t in tasks}

    def _load_config(self, path):
        with open(path, 'r') as f:
            return json.load(f)

    def run_tests(self, task_ids=None):
        results = []
        script_dir = "test_scripts"
        files = [f for f in os.listdir(script_dir) if f.startswith("test_") and f.endswith(".py")]
        files.sort()

        with sync_playwright() as p:
             # Launch browser once (or per test if isolation needed, usually per test for clean state)
            
            for filename in files:
                t_id = "unknown"
                try:
                    parts = filename.split('_')
                    if len(parts) >= 2:
                        t_id = parts[1].replace('.py', '')
                    else:
                        continue
                    
                    if task_ids and "all" not in task_ids and t_id not in task_ids:
                        continue

                    print(f"\n{'='*60}")
                    print(f"Running Test Script: {filename} (ID: {t_id})")
                    
                    # Create context per test
                    print(f"Launching Browser (Headless: {self.headless})...")
                    browser = p.chromium.launch(headless=self.headless)
                    context = browser.new_context(viewport={'width': 1280, 'height': 800})
                    page = context.new_page()

                    file_path = os.path.join(script_dir, filename)
                    spec = importlib.util.spec_from_file_location("module.name", file_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    if hasattr(module, 'TaskScript'):
                        # Pass page, context, or just page? Standard is usually page.
                        # We pass 'page' as the 'driver' equivalent.
                        test_instance = module.TaskScript(page, self.env_config)
                        
                        print("--- ACTION ---")
                        test_instance.action()
                        
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
                    
                    context.close()
                    browser.close()
                    print("Browser closed.")

                except Exception as e:
                    print(f"Error running {filename}: {e}")
                    results.append({
                        "id": t_id,
                        "file": filename,
                        "success": False,
                        "error": str(e)
                    })

        return results

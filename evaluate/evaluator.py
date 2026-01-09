import json
from playwright.sync_api import Page
from evaluate.handlers import *

class Evaluator:
    def __init__(self, tasks=None, env_config=None):
        if tasks is None:
            # Load default
            try:
                with open("dataset/tasks.json", "r") as f:
                    self.tasks = json.load(f)
            except FileNotFoundError:
                print("Error: dataset/tasks.json not found.")
                self.tasks = []
        else:
            self.tasks = tasks

        if env_config is None:
            try:
                with open("env_config.json", "r") as f:
                    self.env_config = json.load(f)
            except FileNotFoundError:
                print("Error: env_config.json not found.")
                self.env_config = {}
        else:
            self.env_config = env_config

    def _resolve_url(self, url_str):
        if not url_str or not isinstance(url_str, str):
            return url_str
        
        for key, conf in self.env_config.items():
            if key in url_str:
                base_url = conf.get('url', '')
                # Handle potential double slashes if placeholder has no validation
                url_str = url_str.replace(key, base_url)
        return url_str
    
    def evaluate(self, task_id, page: Page):
        """
        Evaluate a task using a Playwright Page instance (Synchronous).
        Delegate to handlers based on eval_type.
        """
        task = next((task for task in self.tasks if task['task_id'] == task_id), None)
        if not task:
            print(f"Task ID {task_id} not found.")
            return False
            
        print(f"---------Evaluating task: {task['task_id']}------")
        eval_block = task['eval']
        result = False
        
        for eval_type in eval_block['eval_type']:
            target_conf = eval_block[eval_type].copy()
            
            # Resolve URL if present
            if 'url' in target_conf:
                target_conf['url'] = self._resolve_url(target_conf['url'])

            # Resolve match_value if it contains a placeholder
            if 'match_value' in target_conf and isinstance(target_conf['match_value'], str):
                 target_conf['match_value'] = self._resolve_url(target_conf['match_value'])

            if eval_type == 'dom_match':
                print(f"Evaluating {eval_type} with Playwright...")
                if not dom_match_playwright(target_conf=target_conf, browser=page):
                    return False
                result = True
                
            elif eval_type == 'url_match':
                print(f"Evaluating {eval_type} with Playwright...")
                if not url_match_playwright(target_conf=target_conf, browser=page):
                    return False
                result = True
                
            elif eval_type == 'string_match':
                print(f"Evaluating {eval_type}...")      
                if not string_match(target_conf=target_conf, agent_result=None, task=task['task_description']):
                    return False
                result = True   

            elif eval_type == 'regex_match':
                print(f"Evaluating {eval_type}...")
                if not regex_match(target_conf=target_conf, agent_result=None):
                    return False
                result = True

            elif eval_type == 'multiset_match':
                print(f"Evaluating {eval_type}...")
                if not multiset_match(target_conf=target_conf, agent_result=None):
                    return False
                result = True

            elif eval_type == 'list_match':
                print(f"Evaluating {eval_type}...")
                if not list_match(target_conf=target_conf, agent_result=None):
                    return False
                result = True
                
            else:
                print(f"Unknown eval type: {eval_type}")
                return False
                
        return result

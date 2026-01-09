import json
from playwright.sync_api import Page
from evaluate.handlers import *

class Evaluator:
    def __init__(self, tasks=None):
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
            if eval_type == 'dom_match':
                print(f"Evaluating {eval_type} with Playwright...")
                if not dom_match_playwright(target_conf=eval_block[eval_type], browser=page):
                    return False
                result = True
                
            elif eval_type == 'url_match':
                print(f"Evaluating {eval_type} with Playwright...")
                if not url_match_playwright(target_conf=eval_block[eval_type], browser=page):
                    return False
                result = True
                
            elif eval_type == 'string_match':
                print(f"Evaluating {eval_type}...")      
                if not string_match(target_conf=eval_block[eval_type], agent_result=None, task=task['task_description']):
                    return False
                result = True   

            elif eval_type == 'regex_match':
                print(f"Evaluating {eval_type}...")
                if not regex_match(target_conf=eval_block[eval_type], agent_result=None):
                    return False
                result = True

            elif eval_type == 'multiset_match':
                print(f"Evaluating {eval_type}...")
                if not multiset_match(target_conf=eval_block[eval_type], agent_result=None):
                    return False
                result = True

            elif eval_type == 'list_match':
                print(f"Evaluating {eval_type}...")
                if not list_match(target_conf=eval_block[eval_type], agent_result=None):
                    return False
                result = True
                
            else:
                print(f"Unknown eval type: {eval_type}")
                return False
                
        return result

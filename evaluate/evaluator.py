import time
from .matchers import StringMatcher, URLMatcher, DOMMatcher, SemanticMatcher

class Evaluator:
    def __init__(self, tasks):
        self.tasks = tasks
        self.matchers = {
            "string_match": StringMatcher(),
            "url_match": URLMatcher(),
            "dom_match": DOMMatcher(),
            "semantic_match": SemanticMatcher()
        }

    def evaluate_with_selenium(self, task_id, browser):
        """
        Evaluate a task using a Selenium WebDriver instance.
        """
        task = next((t for t in self.tasks if t['task_id'] == task_id), None)
        if not task:
            print(f"Task {task_id} not found")
            return False

        eval_config = task.get("eval")
        if not eval_config:
            # No evaluation criteria? Assume manual check or pass.
            return True

        if isinstance(eval_config, list):
             # Handle list of criteria if needed (AND logic)
             results = []
             for criteria in eval_config:
                 results.append(self._check_criteria(criteria, browser))
             return all(results)
        else:
             return self._check_criteria(eval_config, browser)

    def _check_criteria(self, criteria, browser):
        eval_type = criteria.get("eval_type", []) # e.g. ["dom_match"]
        
        # eval_type can be a list or string (normalize to list)
        if isinstance(eval_type, str):
            eval_type = [eval_type]

        results = []
        for et in eval_type:
            matcher = self.matchers.get(et)
            if not matcher:
                print(f"[Warn] Matcher {et} not found. Skipping.")
                continue
            
            # The config for this matcher is usually under the key same as eval_type
            matcher_config = criteria.get(et)
            if matcher_config:
                print(f"Running {et}: {matcher_config.get('description', '')}")
                score = matcher.match(browser, matcher_config)
                success = score >= 1.0
                if success:
                     print(f"  -> Pass ({score})")
                else:
                     print(f"  -> Fail ({score})")
                results.append(success)
            else:
                 print(f"[Warn] Configuration for {et} missing.")
                 results.append(False)
        
        return all(results) if results else False

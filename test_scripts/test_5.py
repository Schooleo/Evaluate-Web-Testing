from evaluate.evaluator import Evaluator

class TaskScript:
    def __init__(self, page, env_config):
        self.page = page
        self.env_config = env_config

    def action(self):
        front_url = self.env_config["__GHOST_FRONT__"]["url"]
        
        # Navigate to About page directly
        # If we need to find it in navigation, we could look for 'About', 
        # but direct navigation is more robust for "Navigate to..." tasks if URL is standard.
        # Task 5 config implies checking URL match /about.
        
        target_url = f"{front_url}/about"
        self.page.goto(target_url)
        self.page.wait_for_load_state("networkidle")

    def verify(self):
        evaluator = Evaluator()
        return evaluator.evaluate(task_id="5", page=self.page)

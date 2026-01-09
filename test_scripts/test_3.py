from evaluate.evaluator import Evaluator

class TaskScript:
    def __init__(self, page, env_config):
        self.page = page
        self.env_config = env_config

    def action(self):
        front_url = self.env_config["__GHOST_FRONT__"]["url"]
        
        self.page.goto(front_url)
        self.page.wait_for_load_state("networkidle")
        
        # We need to wait for the content to surely load, although networkidle handles most.
        # Check if "My First Post" is visible? Action method shouldn't verify, but waiting is okay.
        try:
           self.page.wait_for_selector("text=My First Post", timeout=5000)
        except:
           pass

    def verify(self):
        evaluator = Evaluator()
        return evaluator.evaluate(task_id="3", page=self.page)

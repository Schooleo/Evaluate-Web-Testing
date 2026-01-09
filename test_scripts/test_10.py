from evaluate.evaluator import Evaluator

class TaskScript:
    def __init__(self, page, env_config):
        self.page = page
        self.env_config = env_config

    def action(self):
        admin_config = self.env_config["__GHOST_ADMIN__"]
        base_url = admin_config["url"]
        
        # Navigate to Admin
        self.page.goto(base_url)
        self.page.wait_for_load_state("networkidle")
        
        # Login if needed
        if "signin" in self.page.url:
            self.page.fill('input[name="identification"]', admin_config["username"])
            self.page.fill('input[name="password"]', admin_config["password"])
            self.page.click('button[type="submit"]')
            self.page.wait_for_load_state("networkidle")
            
        # Click Search Trigger (Magnifying glass)
        # Selectors: button.gh-nav-btn-search
        self.page.click('button.gh-nav-btn-search')
        self.page.wait_for_selector('input.gh-input-with-select-input')
        
        # Type "About Us"
        self.page.fill('input.gh-input-with-select-input', "About Us")
        
        # Wait for results
        # Selector: li.ember-power-select-option
        self.page.wait_for_selector('li.ember-power-select-option')
        
        # Click first result
        self.page.click('li.ember-power-select-option')
        
        # Wait for navigation to editor and element appearance
        self.page.wait_for_selector('textarea.gh-editor-title', timeout=10000)
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(1000)

    def verify(self):
        evaluator = Evaluator()
        return evaluator.evaluate(task_id="10", page=self.page)

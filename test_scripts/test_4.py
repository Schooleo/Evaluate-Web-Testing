from evaluate.evaluator import Evaluator

class TaskScript:
    def __init__(self, page, env_config):
        self.page = page
        self.env_config = env_config

    def action(self):
        admin_url = self.env_config["__GHOST_ADMIN__"]["url"]
        username = self.env_config["__GHOST_ADMIN__"]["username"]
        password = self.env_config["__GHOST_ADMIN__"]["password"]

        self.page.goto(admin_url)
        self.page.wait_for_load_state("networkidle")

        if self.page.locator("#identification").is_visible():
            self.page.fill("#identification", username)
            self.page.fill("#password", password)
            self.page.click("button.login")
            self.page.wait_for_load_state("networkidle")
        
        # Go to Pages
        self.page.click("a[href='#/pages/']")
        self.page.wait_for_load_state("networkidle")

        # New Page
        self.page.click("a[href='#/editor/page/']")
        self.page.wait_for_load_state("networkidle")
        
        # Title
        self.page.wait_for_selector("textarea.gh-editor-title")
        self.page.fill("textarea.gh-editor-title", "About Us")
        
        # Click body to save
        self.page.click("div.kg-prose")
        self.page.wait_for_timeout(2000)

    def verify(self):
        evaluator = Evaluator()
        return evaluator.evaluate(task_id="4", page=self.page)

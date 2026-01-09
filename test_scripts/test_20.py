from evaluate.evaluator import Evaluator

class TaskScript:
    def __init__(self, page, env_config):
        """
        Initialize with the Playwright page and environment config.
        """
        self.page = page
        self.env_config = env_config

    def action(self):
        """
        Perform the task steps (e.g., Navigate, Click, Type).
        """
        # 1. Navigate to Ghost Admin
        admin_url = self.env_config["__GHOST_ADMIN__"]["url"]
        self.page.goto(admin_url)
        self.page.wait_for_load_state("networkidle")

        # 2. Login if needed
        if "/signin" in self.page.url:
            username = self.env_config["__GHOST_ADMIN__"]["username"]
            password = self.env_config["__GHOST_ADMIN__"]["password"]
            self.page.fill('input[name="identification"]', username)
            self.page.fill('input[name="password"]', password)
            self.page.click('button[type="submit"]')
            self.page.wait_for_load_state("networkidle")

        # 3. Open User Menu
        # Click user avatar / dropdown trigger
        self.page.click('.ember-basic-dropdown-trigger')
        self.page.wait_for_selector('.user-menu-signout')
        
        # 4. Click Sign Out
        self.page.click('.user-menu-signout')
        self.page.wait_for_load_state("networkidle")
        
        # Wait for redirection to signin
        self.page.wait_for_url(lambda url: "/signin" in url)

    def verify(self):
        """
        Verify the outcome.
        Returns:
            bool: True if pass, False if fail.
        """
        evaluator = Evaluator()
        return evaluator.evaluate(task_id="20", page=self.page)

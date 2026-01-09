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

        # 3. Navigate to Settings -> Navigation
        self.page.click('a[href="#/settings/"]')
        self.page.wait_for_load_state("networkidle")

        # Click Navigation link in sidebar to scroll to it/activate it
        self.page.click('#navigation')
        self.page.wait_for_load_state("networkidle")
        
        # Click 'Customize' button for Navigation
        # Use data-testid which is robust
        self.page.locator('[data-testid="navigation"]').get_by_role("button", name="Customize").click()
        self.page.wait_for_selector('input[placeholder="New item label"]')

        # 4. Add new item
        self.page.locator('input[placeholder="New item label"]').fill("Portfolio")
        self.page.keyboard.press("Tab")
        self.page.keyboard.type("/portfolio")

        # 5. Save
        self.page.click('button:has-text("Save")')
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(1000)

    def verify(self):
        """
        Verify the outcome.
        Returns:
            bool: True if pass, False if fail.
        """
        evaluator = Evaluator()
        return evaluator.evaluate(task_id="18", page=self.page)

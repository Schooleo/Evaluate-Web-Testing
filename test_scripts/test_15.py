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

        # 3. Navigate to User Profile
        # Click User Menu (bottom left)
        # It's usually a div with class 'gh-user-avatar' relative parent
        self.page.locator('.gh-user-avatar').click()
        
        # Click "Your profile" from the menu
        self.page.click('text=Your profile')
        self.page.wait_for_load_state("networkidle")

        # 4. Update Name
        # Find input associated with "Full name" label
        # Use get_by_label as it is correctly associated via 'for' attribute
        self.page.get_by_label("Full name").fill("Admin User")
        
        # 5. Save
        self.page.click('button:has-text("Save")')
        self.page.wait_for_load_state("networkidle")
        
        # Wait for "Saved" state or timeout
        self.page.wait_for_selector('button:has-text("Saved")')

    def verify(self):
        """
        Verify the outcome.
        Returns:
            bool: True if pass, False if fail.
        """
        evaluator = Evaluator()
        return evaluator.evaluate(task_id="15", page=self.page)

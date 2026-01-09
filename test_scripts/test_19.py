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

        # 3. Navigate to Settings (General)
        self.page.click('a[href="#/settings/"]')
        self.page.wait_for_load_state("networkidle")
        
        # 4. Open Timezone Picker
        # Click the combobox
        self.page.click('input[role="combobox"]')
        
        # 5. Select Timezone
        # Type to filter
        self.page.fill('input[role="combobox"]', "Bangkok")
        # Click the option
        self.page.click('div[role="option"]:has-text("Bangkok")')
        
        # 6. Save
        # Save button appears after selection
        self.page.click('button:has-text("Save")')
        self.page.wait_for_load_state("networkidle")
        
        # Wait for "Saved" state
        self.page.wait_for_selector('button:has-text("Saved")')

    def verify(self):
        """
        Verify the outcome.
        Returns:
            bool: True if pass, False if fail.
        """
        evaluator = Evaluator()
        return evaluator.evaluate(task_id="19", page=self.page)

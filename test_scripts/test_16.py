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

        # 3. Navigate to Settings -> General (Title & Description)
        # Click settings icon
        self.page.click('a[href="#/settings/"]')
        self.page.wait_for_load_state("networkidle")
        
        # Click 'Edit' in Title & description section
        # The section usually doesn't need a click to reveal if it's the main settings page in some versions,
        # but in recent versions (Admin X), we might need to click "Edit" or navigate to the sub-view.
        # Based on research, we clicked "Edit".
        # Let's find the "Edit" button near "Title & description" or simply try to interact with inputs if visible.
        # Research found: Click 'Edit' button in Title & description.
        # Robust selector for that edit button:
        # We can look for a container with "Title & description" and click "Edit" inside it.
        # Or simpler: The inputs might be hidden. 
        # Research selector: button:has-text("Edit") but that might be ambiguous.
        # The previous attempt failed because multiple "Edit" buttons were found.
        # The error log suggested get_by_test_id("title-and-description") is available.
        self.page.locator('[data-testid="title-and-description"]').get_by_text("Edit").click()
        
        # 4. Fill Site Title
        self.page.fill('input[placeholder="Site title"]', "Agentic Web")
        
        # 5. Save
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
        return evaluator.evaluate(task_id="16", page=self.page)

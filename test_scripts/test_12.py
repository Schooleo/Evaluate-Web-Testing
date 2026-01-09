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

        # 3. Navigate to Members section
        self.page.click('[data-test-nav="members"]')
        self.page.wait_for_load_state("networkidle")

        # 4. Find John Doe and click to edit
        # Use a filter to find specifically John Doe in the list
        self.page.locator("h3").filter(has_text="John Doe").click()
        self.page.wait_for_load_state("networkidle")

        # 5. Fill Note
        self.page.fill('#member-note', "VIP")
        
        # 6. Save
        # In edit mode, save button is roughly same position
        self.page.click('button.gh-btn-primary')
        self.page.wait_for_load_state("networkidle")
        
        # Wait for save confirmation
        self.page.wait_for_timeout(1000)

    def verify(self):
        """
        Verify the outcome.
        Returns:
            bool: True if pass, False if fail.
        """
        evaluator = Evaluator()
        # Note: The eval constraint says "url: last", meaning valid only if page is on the member page.
        return evaluator.evaluate(task_id="12", page=self.page)

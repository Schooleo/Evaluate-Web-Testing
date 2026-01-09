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
        # Use data-test-nav to target desktop sidebar specifically
        self.page.click('[data-test-nav="members"]')
        self.page.wait_for_load_state("networkidle")

        # 4. Click New Member
        # Use a more robust selector if possible, or keep the href one but ensure visibility
        self.page.click('a[href="#/members/new/"]')
        self.page.wait_for_load_state("networkidle")

        # 5. Fill Member Details
        self.page.fill('#member-name', "John Doe")
        self.page.fill('#member-email', "john@example.com")
        
        # 6. Save
        self.page.click('button.gh-btn-primary')
        self.page.wait_for_load_state("networkidle")
        
        # Wait for potential success state (button change or url change)
        self.page.wait_for_timeout(1000)

    def verify(self):
        """
        Verify the outcome.
        Returns:
            bool: True if pass, False if fail.
        """
        evaluator = Evaluator()
        return evaluator.evaluate(task_id="11", page=self.page)

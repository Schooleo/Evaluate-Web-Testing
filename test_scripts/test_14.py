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

        # 3. Navigate to Staff Settings
        # Settings -> Staff
        self.page.click('a[href="#/settings/"]')
        self.page.wait_for_load_state("networkidle")
        
        self.page.click('#staff')
        self.page.wait_for_load_state("networkidle")

        # 4. Click Invite people
        self.page.click('button:has-text("Invite people")')
        self.page.wait_for_selector('input[placeholder="jamie@example.com"]')

        # 5. Fill Email
        self.page.fill('input[placeholder="jamie@example.com"]', "editor@example.com")
        
        # 6. Select Role 'Editor'
        self.page.click('button#editor')
        
        # 7. Send Invitation
        self.page.click('button:has-text("Send invitation")')
        
        # Wait for modal to close and email to appear in the list
        # Ghost usually adds it to the "Invited users" section dynamically
        self.page.wait_for_selector(f"text=editor@example.com")
        self.page.wait_for_load_state("networkidle")

    def verify(self):
        """
        Verify the outcome.
        Returns:
            bool: True if pass, False if fail.
        """
        evaluator = Evaluator()
        return evaluator.evaluate(task_id="14", page=self.page)

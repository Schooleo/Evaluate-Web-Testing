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
        self.page.locator("h3").filter(has_text="John Doe").click()
        self.page.wait_for_load_state("networkidle")

        # 5. Open Actions Menu
        # Click the gear/settings icon at top right
        self.page.click('button.gh-btn-action-icon')
        self.page.wait_for_selector('button.mr2', state="visible")

        # 6. Click Delete Member
        # Use text filter for robustness
        self.page.locator("button").filter(has_text="Delete member").click()
        
        # 7. Confirm Delete
        # Wait for modal and click red delete button
        self.page.wait_for_selector('button.gh-btn-red')
        self.page.click('button.gh-btn-red')
        self.page.wait_for_load_state("networkidle")

        # Wait for redirection to members list
        self.page.wait_for_url(lambda url: "/members" in url)

    def verify(self):
        """
        Verify the outcome.
        Returns:
            bool: True if pass, False if fail.
        """
        evaluator = Evaluator()
        return evaluator.evaluate(task_id="13", page=self.page)

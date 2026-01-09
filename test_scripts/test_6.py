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
        admin_config = self.env_config["__GHOST_ADMIN__"]
        base_url = admin_config["url"]
        
        # Navigate to Ghost Admin
        self.page.goto(base_url)
        self.page.wait_for_load_state("networkidle")
        
        # Handle Login if needed
        if "signin" in self.page.url:
            self.page.fill('input[name="identification"]', admin_config["username"])
            self.page.fill('input[name="password"]', admin_config["password"])
            self.page.click('button[type="submit"]')
            self.page.wait_for_load_state("networkidle")
            
        # Navigate to Tags
        # Selector: a[href="#/tags/"] matches the sidebar link
        self.page.click('a[href="#/tags/"]')
        # Wait for the tags list or the 'New Tag' button to be ready
        self.page.wait_for_selector('a[href="#/tags/new/"]')
        
        # Click New Tag
        self.page.click('a[href="#/tags/new/"]')
        # Wait for the tag form
        self.page.wait_for_selector('input#tag-name')
        
        # Fill Name "Tech"
        self.page.fill('input#tag-name', "Tech")
        
        # Click Save
        self.page.click('button.gh-btn-primary')
        
        # Wait for save to complete (e.g. URL change or "Saved" button state)
        # Using networkidle and a small wait to ensure backend processed it
        self.page.wait_for_load_state("networkidle")
        # Additionally wait for URL to contain "tech" which indicates save was successful and slug triggered
        # or just wait a moment. The verify step checks current URL or last URL.
        # If we navigated, the URL changes.
        self.page.wait_for_timeout(1000) 

    def verify(self):
        """
        Verify the outcome.
        Returns:
            bool: True if pass, False if fail.
        """
        evaluator = Evaluator()
        return evaluator.evaluate(task_id="6", page=self.page)

from evaluate.evaluator import Evaluator

class TaskScript:
    def __init__(self, page, env_config):
        self.page = page
        self.env_config = env_config

    def action(self):
        admin_config = self.env_config["__GHOST_ADMIN__"]
        base_url = admin_config["url"]
        
        # Navigate to Admin
        self.page.goto(base_url)
        self.page.wait_for_load_state("networkidle")
        
        # Login if needed
        if "signin" in self.page.url:
            self.page.fill('input[name="identification"]', admin_config["username"])
            self.page.fill('input[name="password"]', admin_config["password"])
            self.page.click('button[type="submit"]')
            self.page.wait_for_load_state("networkidle")
            
        # Navigate to Posts
        self.page.click('a[href="#/posts/"]')
        self.page.wait_for_load_state("networkidle")
        
        # Click "My First Post"
        # Using :text matches is cleaner in Playwright
        self.page.click('h3:text("My First Post")')
        self.page.wait_for_load_state("networkidle")
        
        # Open Settings
        # Selector for settings toggle (top right)
        self.page.click('button.settings-menu-toggle')
        
        # Wait for settings pane
        self.page.wait_for_selector('#tag-input input')
        
        # Add "Tech" tag
        self.page.click('#tag-input input')
        self.page.fill('#tag-input input', "Tech")
        # Wait for the dropdown option to appear (Ghost used ember-power-select)
        self.page.wait_for_selector('.ember-power-select-option')
        self.page.click('.ember-power-select-option')
        
        # Close Settings
        self.page.click('button.settings-menu-toggle')
        
        # Determine if we need to Publish or Update
        # If "Publish" is visible, we publish.
        if self.page.is_visible('.gh-publish-trigger'):
            self.page.click('.gh-publish-trigger')
            self.page.wait_for_selector('button.gh-publish-cta, button.gh-btn-black')
            # Click Continue
            self.page.click('button.gh-btn-black') # Usually "Continue, final review"
            self.page.wait_for_selector('button.gh-btn-large') # "Publish post, right now"
            self.page.click('button.gh-btn-large')
            
            # Wait for success modal and close it
            self.page.wait_for_selector('.gh-publish-title') # "Boom! It's out there."
            # Close modal to return to editor
            self.page.click('button.gh-publish-back-button') # Or click "Back to editor"
            self.page.wait_for_load_state("networkidle")
            
        # If "Update" is visible or we just need to save draft
        elif self.page.is_visible('.gh-editor-save-trigger'):
            self.page.click('.gh-editor-save-trigger')
            self.page.wait_for_load_state("networkidle")
            self.page.wait_for_timeout(2000)
        else:
            # Fallback to Ctrl+S if neither button is clear (e.g. pure draft save)
            self.page.keyboard.press("Control+s")
            self.page.wait_for_timeout(2000)

    def verify(self):
        evaluator = Evaluator()
        return evaluator.evaluate(task_id="7", page=self.page)

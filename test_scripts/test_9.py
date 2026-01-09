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
        
        # Check if "My First Post" exists
        post_selector = 'h3:text("My First Post")'
        if not self.page.is_visible(post_selector):
            # Create it
            self.page.click('a[href="#/editor/post/"]') # New Post button often in header or sidebar "New Post" (or +)
            # Actually easier to use the "New Post" link in sidebar if available, or just go to editor
            self.page.goto(base_url + "/#/editor/post/")
            self.page.wait_for_load_state("networkidle")
            
            # Fill Title
            self.page.fill('textarea.gh-editor-title', "My First Post")
            self.page.keyboard.press("Enter") # Focus content
            self.page.fill('.koenig-editor__editor', "Some content") # Optional
            self.page.wait_for_timeout(1000)
            
            # Save (Draft) - Ctrl+S
            self.page.keyboard.press("Control+s")
            self.page.wait_for_timeout(1000)
            
            # Navigate back to Posts
            self.page.click('a[href="#/posts/"]')
            self.page.wait_for_load_state("networkidle")
            self.page.reload()
            self.page.wait_for_load_state("networkidle")

        # Now click it
        self.page.click(post_selector)
        self.page.wait_for_load_state("networkidle")
        
        # Open Settings
        self.page.click('button.settings-menu-toggle')
        self.page.wait_for_selector('button.settings-menu-delete-button')
        
        # Click Delete (it might require scrolling, but click usually works if in DOM. If not, scroll)
        # Playwright auto-scrolls.
        self.page.click('button.settings-menu-delete-button')
        
        # Confirm Delete in Modal
        self.page.wait_for_selector('.modal-content button.gh-btn-red')
        self.page.click('.modal-content button.gh-btn-red')
        
        # Wait for navigation to posts
        try:
            self.page.wait_for_url(lambda u: "/posts" in u, timeout=15000)
        except:
             # Force navigation if stuck (fallback)
             self.page.goto(base_url + "/#/posts/")
        
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(2000)

    def verify(self):
        evaluator = Evaluator()
        return evaluator.evaluate(task_id="9", page=self.page)

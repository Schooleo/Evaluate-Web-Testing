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
        
        # Check status of "My First Post"
        # We need to find the specific list item for "My First Post"
        # Since we just want to ensure it is drafted, we can check the status badge if visible.
        # But to be safe, opening it and unpublishing is better if we are unsure.
        # However, checking from list is faster if it's already draft.
        
        post_selector = 'h3:text("My First Post")'
        # Check if we can find it
        if not self.page.is_visible(post_selector):
            # If not in default list, maybe check "Published" filter?
            # But "Posts" shows all usually.
            pass

        # Open the post
        self.page.click(post_selector)
        self.page.wait_for_load_state("networkidle")
        
        # Check if Published (Look for Unpublish trigger or Update button)
        # ".gh-unpublish-trigger" is specific to published posts (in older Ghost it was different, but browser agent found it)
        # Browser agent found "Unpublish" button: `button.gh-unpublish-trigger`
        
        if self.page.is_visible('button.gh-unpublish-trigger'):
            # It is published. Unpublish it.
            self.page.click('button.gh-unpublish-trigger')
            # Wait for confirm
            self.page.wait_for_selector('button.gh-revert-to-draft, button:has-text("Unpublish")')
            # Click confirm
            # Browser agent saw `gh-revert-to-draft`
            if self.page.is_visible('button.gh-revert-to-draft'):
                 self.page.click('button.gh-revert-to-draft')
            else:
                 self.page.click('button:has-text("Unpublish and revert")')
            
            self.page.wait_for_load_state("networkidle")
        
        # If it was already draft, we just need to ensure we are back on the list.
        # Navigate back to posts list (CRITICAL for Eval 8)
        self.page.goto(admin_config["url"] + "/#/posts/")
        self.page.wait_for_load_state("networkidle")
        self.page.reload()
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(2000)

    def verify(self):
        evaluator = Evaluator()
        return evaluator.evaluate(task_id="8", page=self.page)

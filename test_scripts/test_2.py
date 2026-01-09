from evaluate.evaluator import Evaluator


class TaskScript:
    def __init__(self, page, env_config):
        self.page = page
        self.env_config = env_config

    def action(self):
        admin_config = self.env_config["__GHOST_ADMIN__"]
        admin_url = admin_config["url"]
        username = admin_config["username"]
        password = admin_config["password"]

        self.page.goto(admin_url)
        self.page.wait_for_load_state("networkidle")

        if "/signin" in self.page.url:
            self.page.fill('input[name="identification"]', username)
            self.page.fill('input[name="password"]', password)
            self.page.click('button[type="submit"]')
            self.page.wait_for_load_state("networkidle")

        self.page.goto(admin_url + "/#/posts")
        self.page.wait_for_load_state("networkidle")

        self.page.wait_for_selector('.gh-content-entry-title')
        post_item = self.page.locator('.gh-posts-list-item:has-text("My First Post")').first
        post_item.click()
        self.page.wait_for_load_state("networkidle")

        self.page.wait_for_selector('[data-test-button="publish-flow"]', timeout=10000)
        self.page.click('[data-test-button="publish-flow"]')
        self.page.wait_for_selector('[data-test-button="continue"]', timeout=10000)

        self.page.click('[data-test-button="continue"]')
        self.page.wait_for_selector('[data-test-button="confirm-publish"]', timeout=10000)

        self.page.click('[data-test-button="confirm-publish"]')
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(2000)

    def verify(self):
        evaluator = Evaluator()
        return evaluator.evaluate(task_id="2", page=self.page)

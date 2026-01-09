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

        self.page.wait_for_selector('a[href="#/editor/post/"]')
        self.page.click('a[href="#/editor/post/"]')
        self.page.wait_for_load_state("networkidle")

        self.page.wait_for_selector('textarea.gh-editor-title')
        self.page.fill('textarea.gh-editor-title', 'My First Post')

        self.page.wait_for_selector('div[data-kg="editor"]')
        self.page.click('div[data-kg="editor"]')
        self.page.keyboard.type('Hello Ghost')

        self.page.wait_for_load_state("networkidle")

    def verify(self):
        evaluator = Evaluator()
        return evaluator.evaluate(task_id="1", page=self.page)

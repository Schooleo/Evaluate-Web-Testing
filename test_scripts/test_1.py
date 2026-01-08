
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import os
from evaluate.matchers import URLMatcher

class TaskScript:
    def __init__(self, driver, env_config):
        self.driver = driver
        self.env_config = env_config

    def action(self):
        # Navigate to Ghost Admin
        admin_url = self.env_config["__GHOST_ADMIN__"]["url"]
        self.driver.get(admin_url)

        # Check if we are already logged in (redirected to dashboard)
        if "/dashboard" in self.driver.current_url:
            return

        # Wait for the login form
        wait = WebDriverWait(self.driver, 10)
        email_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#identification")))
        
        # Get credentials
        username = self.env_config["__GHOST_ADMIN__"]["username"]
        password = self.env_config["__GHOST_ADMIN__"]["password"]

        # Perform Login
        email_input.clear()
        email_input.send_keys(username)
        
        password_input = self.driver.find_element(By.CSS_SELECTOR, "#password")
        password_input.clear()
        password_input.send_keys(password)
        
        login_btn = self.driver.find_element(By.CSS_SELECTOR, "button.login")
        login_btn.click()
        
        # Wait for navigation to complete (dashboard)
        # We wait for the URL to change implies success, but the verify step handles the check.
        # However, we should give it some time to process.
        try:
             wait.until(EC.url_contains("/dashboard"))
        except:
             pass # If it fails here, verify() will catch it.

    def verify(self):
        # Load task definition to get eval config
        # Assuming run_tests.py runs from root, so dataset/tasks.json is accessible
        tasks_path = os.path.join(os.getcwd(), 'dataset', 'tasks.json')
        with open(tasks_path, 'r') as f:
            tasks = json.load(f)
        
        # Find task 1
        task_config = next((t for t in tasks if t['task_id'] == '1'), None)
        if not task_config:
            raise ValueError("Task 1 not found in dataset/tasks.json")
            
        eval_config = task_config['eval']['url_match']
        
        matcher = URLMatcher()
        result = matcher.match(self.driver, eval_config)
        
        return result == 1.0

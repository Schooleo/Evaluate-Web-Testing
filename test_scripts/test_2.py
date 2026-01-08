from evaluate.test_abstract import TestScript
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

class TaskScript(TestScript):
    def __init__(self, driver, env_config):
        self.driver = driver
        self.env_config = env_config
        self.wait = WebDriverWait(self.driver, 10)

    def _ensure_login(self):
        # Go to admin explicitly to check where we land
        self.driver.get(f"{self.env_config['__GHOST_ADMIN__']['url']}/")
        time.sleep(1)
        if "signin" in self.driver.current_url:
            print("Logging in...")
            try:
                self.driver.find_element(By.NAME, "identification").send_keys("admin@example.com")
                self.driver.find_element(By.NAME, "password").send_keys("VeryAwesomeAdminGuy123@")
                self.driver.find_element(By.CSS_SELECTOR, "button.login").click()
                self.wait.until(EC.url_contains("/dashboard"))
            except Exception as e:
                print(f"Login failed: {e}")
                raise e

    def action(self):
        """
        Task: Create a new post 'My First Post' with content 'Hello Ghost'.
        """
        self._ensure_login()
        
        # Navigate to Posts
        print("Navigating to Posts...")
        self.driver.get(f"{self.env_config['__GHOST_ADMIN__']['url']}/#/posts")
        time.sleep(2)
        
        # Click New Post
        print("Looking for 'New post' button...")
        try:
            # Try finding by specific href first
            new_post_btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='#/editor/post/']")))
            new_post_btn.click()
        except:
            print("Primary selector failed. Trying by text 'New post'...")
            new_post_btn = self.driver.find_element(By.XPATH, "//span[contains(text(), 'New post')]")
            new_post_btn.click()

        print("Entered Editor.")
        
        # Wait for Editor
        title_area = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "textarea.gh-editor-title")))
        
        # Enter Title
        print("Entering title...")
        title_area.clear()
        title_area.send_keys("My First Post")
        
        # Enter Content (click prose, type)
        print("Entering content...")
        try:
            content_area = self.driver.find_element(By.CSS_SELECTOR, "div.kg-prose")
            content_area.click()
            content_area.send_keys("Hello Ghost")
        except:
             # Fallback for older ghost versions or different state
             body = self.driver.find_element(By.TAG_NAME, "body")
             body.send_keys(Keys.TAB) 
             body.send_keys("Hello Ghost")
        
        time.sleep(1) # Allow auto-save trigger

    def verify(self):
        """
        Verify: Post title in editor is 'My First Post'
        """
        try:
            title_val = self.driver.find_element(By.CSS_SELECTOR, "textarea.gh-editor-title").get_attribute("value")
            print(f"Detected Title: {title_val}")
            return "My First Post" in title_val
        except Exception as e:
            print(f"Verification Error: {e}")
            return False

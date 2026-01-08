from evaluate.test_abstract import TestScript
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class TaskScript(TestScript):
    def __init__(self, driver, env_config):
        self.driver = driver
        self.env_config = env_config
        self.wait = WebDriverWait(self.driver, 10)

    def _ensure_login(self):
        self.driver.get(f"{self.env_config['__GHOST_ADMIN__']['url']}/")
        time.sleep(1)
        if "signin" in self.driver.current_url:
            print("Logging in...")
            try:
                self.driver.find_element(By.NAME, "identification").send_keys("admin@example.com")
                self.driver.find_element(By.NAME, "password").send_keys("VeryAwesomeAdminGuy123@")
                self.driver.find_element(By.CSS_SELECTOR, "button.login").click()
                self.wait.until(EC.url_contains("/dashboard"))
            except:
                pass

    def action(self):
        """
        Task: Publish the post titled 'My First Post'.
        """
        self._ensure_login()
        
        # Ensure we are in the editor for 'My First Post'
        self.driver.get(f"{self.env_config['__GHOST_ADMIN__']['url']}/#/posts")
        time.sleep(2)
        
        # Find post by text and click
        try:
            # Check if we have the post in the list
            titles = self.driver.find_elements(By.CSS_SELECTOR, "h3.gh-content-entry-title")
            found = False
            for t in titles:
                if "My First Post" in t.text:
                    t.click()
                    found = True
                    break
            
            if not found:
                print("Could not find 'My First Post' in list via iteration. Trying XPath...")
                post_link = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//h3[contains(text(), 'My First Post')]")))
                post_link.click()
        except Exception as e:
            print(f"Error navigating to post: {e}")
            # Logic to handle if we're already in editor?
            if "/editor/post" in self.driver.current_url:
                print("Already in editor, proceeding...")
            else:
                raise e
        
        time.sleep(1)

        # Trigger Publish Menu
        print("Looking for publish trigger...")
        publish_trigger = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.gh-publish-trigger")))
        publish_trigger.click()
        print("Clicked publish trigger.")
        
        # Step 1: Continue, final review
        print("Looking for continue button...")
        try:
            continue_btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.gh-btn-black")))
            continue_btn.click()
            print("Clicked continue button.")
        except Exception as e:
            print(f"Failed to find/click continue button. We might be in 'Update' mode? {e}")
            # Take screenshot
            self.driver.save_screenshot("debug_test_3_fail.png")
            raise e
        
        # Step 2: Publish right now
        time.sleep(1)
        print("Looking for confirm button...")
        confirm_btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.gh-btn-pulse")))
        confirm_btn.click()
        print("Clicked confirm button.")
        
        time.sleep(2) # Wait for success modal

    def verify(self):
        """
        Verify: Success modal text 'Boom! It's out there.'
        """
        try:
            body_text = self.driver.find_element(By.TAG_NAME, "body").text
            if "Boom! It's out there" in body_text:
                return True
            return False
        except:
            return False

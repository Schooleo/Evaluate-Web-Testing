from abc import ABC, abstractmethod
from urllib.parse import urlparse
import time

class Matcher(ABC):
    @abstractmethod
    def match(self, browser, config):
        pass

class StringMatcher(Matcher):
    def match(self, browser, config):
        # Implementation depends on where we look for string
        # Maybe page source?
        target = config.get("match_value")
        # heuristic: check body text
        body_text = browser.find_element("tag name", "body").text
        if config.get("match_type") == "contains":
            return 1.0 if target in body_text else 0.0
        elif config.get("match_type") == "exact":
            return 1.0 if target == body_text else 0.0
        return 0.0

class URLMatcher(Matcher):
    def match(self, browser, config):
        current_url = browser.current_url
        expected = config.get("match_value")
        match_type = config.get("match_type", "exact")
        
        # Normalize potentially?
        if match_type == "exact":
            return 1.0 if current_url == expected else 0.0
        elif match_type == "contains":
            return 1.0 if expected in current_url else 0.0
        elif match_type == "path":
             # Match path only
             return 1.0 if urlparse(current_url).path == expected else 0.0
        return 0.0

class DOMMatcher(Matcher):
    def match(self, browser, config):
        url_condition = config.get("url")
        if url_condition == "last" or not url_condition:
             # Check on current page
             pass
        # If url_condition is specific, we might need to check if we are there, 
        # but usually the agent should be there.
        
        extractor_js = config.get("dom_extractor")
        match_type = config.get("match_type")
        match_value = config.get("match_value")
        
        try:
            extracted_value = browser.execute_script(f"return {extractor_js}")
            if extracted_value is None:
                return 0.0
            
            # extracted_value might be text or list
            if match_type == "contains":
                return 1.0 if match_value in str(extracted_value) else 0.0
            elif match_type == "exact_match" or match_type == "exact":
                return 1.0 if str(extracted_value) == match_value else 0.0
            elif match_type == "not_null":
                return 1.0 if extracted_value else 0.0
                
            return 0.0
        except Exception as e:
            print(f"DOM Match Error: {e}")
            return 0.0

class SemanticMatcher(Matcher):
    def match(self, browser, config):
        # Placeholder for LLM based matching
        # In a real impl, this would call an LLM API
        print("Semantic Matcher used - returning 1.0 (Mock)")
        return 1.0

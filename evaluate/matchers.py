from abc import ABC, abstractmethod
from urllib.parse import urlparse
import time

class Matcher(ABC):
    @abstractmethod
    def match(self, page, config):
        pass

class StringMatcher(Matcher):
    def match(self, page, config):
        target = config.get("match_value")
        # heuristic: check body text
        body_text = page.inner_text("body")
        if config.get("match_type") == "contains":
            return 1.0 if target in body_text else 0.0
        elif config.get("match_type") == "exact":
            return 1.0 if target == body_text else 0.0
        return 0.0

class URLMatcher(Matcher):
    def match(self, page, config):
        current_url = page.url
        expected = config.get("match_value")
        match_type = config.get("match_type", "exact")
        
        if match_type == "exact":
            return 1.0 if current_url == expected else 0.0
        elif match_type == "contains":
            return 1.0 if expected in current_url else 0.0
        elif match_type == "path":
             return 1.0 if urlparse(current_url).path == expected else 0.0
        return 0.0

class DOMMatcher(Matcher):
    def match(self, page, config):
        url_condition = config.get("url")
        # if url_condition == "last" or not url_condition: pass
        
        extractor_js = config.get("dom_extractor")
        match_type = config.get("match_type")
        match_value = config.get("match_value")
        
        try:
            # Playwright evaluate handles JS execution
            extracted_value = page.evaluate(f"() => {extractor_js}")
            if extracted_value is None:
                return 0.0
            
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
    def match(self, page, config):
        print("Semantic Matcher used - returning 1.0 (Mock)")
        return 1.0

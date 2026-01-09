import re
import time
from evaluate.matchers import *
from collections import Counter
from playwright.sync_api import Page

def string_match(target_conf, agent_result, task=None):
    match_type = target_conf['match_type']
    match_value = target_conf['match_value']

    if match_type == 'exact':
        return exact(agent_result, match_value)
    
    elif match_type == 'contains':
        return check_contains(agent_result, match_value)
        
    elif match_type == 'semantic':
        return semantic(task, agent_result, match_value)
    
    else:
        print(f"Unknown match_type: {match_type}")
        return False

def url_match(target_conf, agent_result):
    url = target_conf['url'].strip().lower()
    match_type = target_conf['match_type']
    match_value = target_conf['match_value']
    if match_type == 'exact':
        return exact(agent_result, match_value)
    
    elif match_type == 'contains':
        return check_contains(agent_result, match_value)
    else:
        print(f"Unknown match_type: {match_type}")
        return False

def url_match_playwright(target_conf, browser: Page=None):    
    current_url = browser.url.strip().lower()
    match_type = target_conf['match_type']
    match_value = target_conf['match_value']
    if match_type == 'exact':
        return exact(current_url, match_value)
    
    elif match_type == 'contains':
        return check_contains(current_url, match_value)
    else:
        print(f"Unknown match_type: {match_type}")
        return False

def dom_match_logic(agent_result, target_conf):
    if agent_result is None:
        print("[dom_match] No value returned from JS script.")
        return False
    match_type = target_conf['match_type']
    match_value = target_conf['match_value']
    if match_type == 'exact':
        return exact(agent_result, match_value)

    elif match_type == 'contains':
        temp = check_contains(agent_result, match_value)
        print(f"[dom_match] Contains check: {temp}")
        return temp
    else:
        print(f"Unknown match_type: {match_type}")
        return False

def dom_match_playwright(target_conf, browser: Page):
    url = target_conf.get('url', '').strip().lower()
    js_script = target_conf['dom_extractor']
    if url in ('', 'current', 'last', None):
        print("[dom_match] Using current page context.")
    else:
        print(f"[dom_match] Expected agent to visit URL: {url}")
        browser.goto(url)
        
    browser.wait_for_timeout(5000)
    agent_result = None
    max_retry = 20
    retry_count = 0

    while agent_result is None and retry_count < max_retry:
        agent_result = browser.evaluate(js_script)
        if agent_result is None:
            time.sleep(1)  # sync sleep
            retry_count += 1

    return dom_match_logic(agent_result, target_conf)

def regex_match(target_conf, agent_result):
    print(f"[regex_match]:\nAgent Value: {agent_result}.\nMatch Conf: {target_conf}")
    if not isinstance(agent_result, dict):
        print("Invalid agent result for regex_match: must be dict")
        return False

    for key, conf in target_conf.items():
        pattern = conf['pattern']
        required = conf['required'] if 'required' in conf else False

        val = agent_result.get(key)
        if required and val is None:
            print(f"Missing required field: {key}")
            return False
        if val and not re.match(pattern, val):
            print(f"Regex failed for {key}: value {val} does not match {pattern}")
            return False
    return True

def multiset_match(target_conf, agent_result):
    expected = target_conf['match_value']
    print(f"[multiset_match] Expected: {expected}, Agent Value: {agent_result}")
    if not isinstance(agent_result, list):
        print("[multiset_match] agent_result must be list-like.")
        return False
    return Counter(expected) == Counter(agent_result)

def list_match(target_conf, agent_result):
    expected = target_conf['match_value']
    print(f"[list_match] Expected: {expected}, Agent Value: {agent_result}")
    if not isinstance(agent_result, list):
        print("[list_match] agent_result must be list.")
        return False
    return expected == agent_result

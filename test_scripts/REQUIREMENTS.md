# Test Script Requirements

All test scripts in this directory must adhere to the following conventions to be recognized by the `AutomationTester`.

## 1. Naming Convention
*   **Format**: `test_<id>.py`
*   **Examples**:
    *   `test_01.py`
    *   `test_20.py`
    *   `test_15.py`
*   **Note**: The `<id>` must match the `task_id` defined in `dataset/tasks.json`.

## 2. Code Structure
Each script **must** define a class named `TaskScript` with the following structure:

```python
class TaskScript:
    def __init__(self, driver, env_config):
        """
        Initialize with the Selenium driver and environment config.
        """
        self.driver = driver
        self.env_config = env_config

    def action(self):
        """
        Perform the task steps (e.g., Navigate, Click, Type).
        """
        pass

    def verify(self):
        """
        Verify the outcome.
        Returns:
            bool: True if pass, False if fail.
        """
        return True
```

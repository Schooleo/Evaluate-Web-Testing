from abc import ABC, abstractmethod

class TestScript(ABC):
    def __init__(self, page, env_config):
        self.page = page
        self.env_config = env_config

    @abstractmethod
    def action(self):
        """
        Perform the task steps (e.g., Navigate, Click, Type).
        """
        pass

    @abstractmethod
    def verify(self):
        """
        Verify the outcome.
        Returns:
            bool: True if pass, False if fail.
        """
        pass

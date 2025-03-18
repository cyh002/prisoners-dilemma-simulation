from src.strategies.base import Strategy
from abc import abstractmethod

class Agent(Strategy):
    """
    Base class for more complex agents that may have additional
    learning or decision-making capabilities beyond simple strategies.
    """
    def __init__(self, name):
        super().__init__(name)
        
    @abstractmethod
    def update(self, reward, state=None):
        """
        Update agent's internal knowledge based on reward feedback.
        
        Args:
            reward: Numerical reward received from the environment
            state: State representation (if applicable)
        """
        pass
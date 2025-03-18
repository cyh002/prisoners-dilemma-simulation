from src.strategies.base import Strategy
import random

class AlwaysCooperate(Strategy):
    def __init__(self):
        super().__init__("AlwaysCooperate")
    
    def move(self) -> str:
        return "C"

class AlwaysDefect(Strategy):
    def __init__(self):
        super().__init__("AlwaysDefect")
    
    def move(self) -> str:
        return "D"

class RandomStrategy(Strategy):
    def __init__(self, p_cooperate=0.5):
        super().__init__("RandomStrategy")
        self.p_cooperate = p_cooperate
    
    def move(self) -> str:
        return "C" if random.random() < self.p_cooperate else "D"
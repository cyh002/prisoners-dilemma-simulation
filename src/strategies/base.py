from abc import ABC, abstractmethod

class Strategy(ABC):
    def __init__(self, name):
        self.name = name
        self.my_history = []
        self.opponent_history = []
        self.reputation = 0.5  # Default neutral reputation

    def __str__(self):
        return self.name

    @abstractmethod
    def move(self) -> str:
        """Return 'C' for cooperate or 'D' for defect."""
        pass

    def record(self, my_move: str, opp_move: str):
        """Record the moves made by both players."""
        self.my_history.append(my_move)
        self.opponent_history.append(opp_move)

    def reset(self):
        """Reset the strategy state."""
        self.my_history = []
        self.opponent_history = []
        
    def update_reputation(self):
        """Update reputation based on cooperation rate."""
        total_moves = len(self.my_history)
        if total_moves == 0:
            return
        coop_rate = self.my_history.count("C") / total_moves
        # Gradually update reputation (avoid sudden swings)
        self.reputation = (self.reputation * 2 + coop_rate) / 3
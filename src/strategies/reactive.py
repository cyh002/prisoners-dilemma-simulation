from src.strategies.base import Strategy
import random

class TitForTatExtended(Strategy):
    def __init__(self, forgiveness_chance=0.1):
        """
        TitForTat with forgiveness - usually copies opponent's last move,
        but occasionally forgives a defection.
        """
        super().__init__("TitForTatExtended")
        self.forgiveness_chance = forgiveness_chance
        
    def move(self) -> str:
        if not self.opponent_history:
            return "C"  # Start with cooperation
        
        if self.opponent_history[-1] == "D" and random.random() < self.forgiveness_chance:
            return "C"  # Forgive with some probability
        
        return self.opponent_history[-1]  # Otherwise copy opponent's last move

class Grudger(Strategy):
    def __init__(self):
        """
        Cooperates until the opponent defects, then always defects.
        """
        super().__init__("Grudger")
        self.has_defected = False
        
    def move(self) -> str:
        if not self.opponent_history:
            return "C"
        
        if "D" in self.opponent_history:
            self.has_defected = True
            
        return "D" if self.has_defected else "C"
    
    def reset(self):
        super().reset()
        self.has_defected = False

class Joss(Strategy):
    def __init__(self, defect_prob=0.1):
        """
        Like TitForTat but occasionally defects when it would normally cooperate.
        """
        super().__init__("Joss")
        self.defect_prob = defect_prob
        
    def move(self) -> str:
        if not self.opponent_history:
            return "C"
            
        # Usually copy opponent's last move
        move = self.opponent_history[-1]
        
        # Occasionally defect when we would normally cooperate
        if move == "C" and random.random() < self.defect_prob:
            move = "D"
            
        return move

class TitForTwoTats(Strategy):
    def __init__(self):
        """
        Defects only if the opponent has defected twice in a row.
        """
        super().__init__("TitForTwoTats")
        
    def move(self) -> str:
        if len(self.opponent_history) < 2:
            return "C"
            
        if self.opponent_history[-1] == "D" and self.opponent_history[-2] == "D":
            return "D"
        else:
            return "C"

class HumanStrategy(Strategy):
    """
    A strategy that allows a human to make decisions.
    Useful for interactive gameplay and testing.
    """
    def __init__(self):
        super().__init__("HumanPlayer")
        
    def move(self) -> str:
        print("\n--- Your Turn ---")
        print(f"Your history: {','.join(self.my_history) if self.my_history else 'None'}")
        print(f"Opponent history: {','.join(self.opponent_history) if self.opponent_history else 'None'}")
        
        while True:
            choice = input("Enter C to cooperate or D to defect: ").strip().upper()
            if choice in ["C", "D"]:
                return choice
            print("Invalid choice. Please enter C or D.")
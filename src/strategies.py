import random
from abc import ABC, abstractmethod

class Strategy(ABC):
    def __init__(self, name: str):
        self.name = name
        self.my_history = []
        self.opponent_history = []
        self.reputation = 1.0  # start neutral

    def reset(self):
        self.my_history = []
        self.opponent_history = []

    @abstractmethod
    def move(self) -> str:
        """Return 'C' or 'D'."""
        pass

    def record(self, my_move: str, opp_move: str):
        self.my_history.append(my_move)
        self.opponent_history.append(opp_move)

    def update_reputation(self):
        # Simple reputation update: fraction of cooperative moves.
        if not self.my_history:
            self.reputation = 1.0
        else:
            self.reputation = self.my_history.count("C") / len(self.my_history)

    def __str__(self):
        return self.name

# Basic strategies
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
    def __init__(self):
        super().__init__("RandomStrategy")
    def move(self) -> str:
        return random.choice(["C", "D"])

# Extended Tit-for-Tat that looks at the last 3 moves.
class TitForTatExtended(Strategy):
    def __init__(self, memory=3):
        super().__init__("TitForTatExtended")
        self.memory = memory
    def move(self) -> str:
        if not self.opponent_history:
            return "C"
        recent = self.opponent_history[-self.memory:]
        # If more than half of the recent moves are defection, defect.
        if recent.count("D") > len(recent)/2:
            return "D"
        return "C"

class Grudger(Strategy):
    def __init__(self):
        super().__init__("Grudger")
        self.grudge = False
    def move(self) -> str:
        if "D" in self.opponent_history:
            self.grudge = True
        return "D" if self.grudge else "C"
    def reset(self):
        super().reset()
        self.grudge = False

class Joss(Strategy):
    def __init__(self, defect_prob=0.1):
        super().__init__("Joss")
        self.defect_prob = defect_prob
    def move(self) -> str:
        if random.random() < self.defect_prob:
            return "D"
        return self.opponent_history[-1] if self.opponent_history else "C"

class TitForTwoTats(Strategy):
    def __init__(self):
        super().__init__("TitForTwoTats")
    def move(self) -> str:
        if len(self.opponent_history) < 2:
            return "C"
        if self.opponent_history[-1] == "D" and self.opponent_history[-2] == "D":
            return "D"
        return "C"

# Human interactive strategy.
class HumanStrategy(Strategy):
    def __init__(self):
        super().__init__("HumanStrategy")
    def move(self) -> str:
        while True:
            inp = input("Your move (C/D): ").strip().upper()
            if inp in ["C", "D"]:
                return inp
            print("Invalid input. Please enter 'C' or 'D'.")

# MetaAgent that can switch between a set of base strategies.
class MetaAgent(Strategy):
    def __init__(self, base_strategy_names, switch_frequency=50):
        super().__init__("MetaAgent")
        # For simplicity, create new instances of base strategies.
        from src.strategies import AlwaysCooperate, AlwaysDefect, RandomStrategy, TitForTatExtended, Grudger, Joss, TitForTwoTats, HumanStrategy
        mapping = {
            "AlwaysCooperate": AlwaysCooperate,
            "AlwaysDefect": AlwaysDefect,
            "RandomStrategy": RandomStrategy,
            "TitForTatExtended": TitForTatExtended,
            "Grudger": Grudger,
            "Joss": Joss,
            "TitForTwoTats": TitForTwoTats,
            "HumanStrategy": HumanStrategy
        }
        self.base_strategies = [mapping[name]() for name in base_strategy_names if name in mapping]
        self.current_strategy = self.base_strategies[0]
        self.switch_frequency = switch_frequency
        self.round_counter = 0

    def move(self) -> str:
        # Use the current strategy.
        self.round_counter += 1
        # Every switch_frequency rounds, evaluate and switch strategy if needed.
        if self.round_counter % self.switch_frequency == 0:
            self.switch_strategy()
        return self.current_strategy.move()

    def switch_strategy(self):
        # For demonstration, randomly pick a different base strategy.
        self.current_strategy = random.choice(self.base_strategies)

    def record(self, my_move: str, opp_move: str):
        # Record in both meta and current strategy.
        super().record(my_move, opp_move)
        self.current_strategy.record(my_move, opp_move)
        self.current_strategy.update_reputation()


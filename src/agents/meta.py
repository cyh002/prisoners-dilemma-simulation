import random
from src.agents.base import Agent
from src.strategies.base import Strategy

class MetaAgent(Agent):
    """
    MetaAgent that can switch between a set of base strategies.
    Implements a meta-strategy that evaluates and changes underlying strategies
    at certain intervals based on performance.
    """
    def __init__(self, base_strategies=None, switch_frequency=50):
        super().__init__("MetaAgent")
        
        # Default strategies if none provided
        if base_strategies is None:
            base_strategies = ["TitForTatExtended", "AlwaysDefect", "RandomStrategy"]
        
        # Import strategies here to avoid circular imports
        from src.strategies.basic import AlwaysCooperate, AlwaysDefect, RandomStrategy
        from src.strategies.reactive import TitForTatExtended, Grudger, Joss, TitForTwoTats, HumanStrategy
        
        # Map strategy names to classes
        self.strategy_mapping = {
            "AlwaysCooperate": AlwaysCooperate,
            "AlwaysDefect": AlwaysDefect,
            "RandomStrategy": RandomStrategy,
            "TitForTatExtended": TitForTatExtended,
            "Grudger": Grudger,
            "Joss": Joss,
            "TitForTwoTats": TitForTwoTats,
            "HumanStrategy": HumanStrategy
        }
        
        # Initialize base strategies
        self.base_strategies = []
        for name in base_strategies:  # Changed from base_strategy_names
            if name in self.strategy_mapping:
                self.base_strategies.append(self.strategy_mapping[name]())
        
        # Ensure we have at least one strategy
        if not self.base_strategies:
            self.base_strategies.append(TitForTatExtended())
            
        # Setup initial strategy and counters
        self.current_strategy = self.base_strategies[0]
        self.switch_frequency = switch_frequency
        self.round_counter = 0
        
        # Track performance of each strategy
        self.strategy_scores = {str(strategy): 0 for strategy in self.base_strategies}
        self.last_score = 0
        
    def move(self) -> str:
        """Return the move determined by the current active strategy."""
        # Every switch_frequency rounds, evaluate and switch strategy if needed
        self.round_counter += 1
        if self.round_counter % self.switch_frequency == 0:
            self.switch_strategy()
            
        # Use the selected strategy's move
        return self.current_strategy.move()

    def switch_strategy(self):
        """Evaluate and possibly change the active strategy."""
        # For now, randomly pick a different base strategy
        # In a more sophisticated implementation, this could use 
        # performance metrics to choose the best strategy
        new_strategy = random.choice(self.base_strategies)
        
        # Ensure we don't pick the same strategy if possible
        if len(self.base_strategies) > 1:
            while new_strategy == self.current_strategy:
                new_strategy = random.choice(self.base_strategies)
        
        self.current_strategy = new_strategy

    def record(self, my_move: str, opp_move: str):
        """Record moves in both the meta-agent and the current strategy."""
        super().record(my_move, opp_move)
        
        # Also record moves in the current strategy
        self.current_strategy.record(my_move, opp_move)
        self.current_strategy.update_reputation()
    
    def update(self, reward, state=None):
        """
        Update performance metrics for the current strategy.
        
        Args:
            reward: Reward received after the last move
            state: Current state (not used in this implementation)
        """
        # Track the score for the current strategy
        self.strategy_scores[str(self.current_strategy)] += reward
        self.last_score = reward
    
    def reset(self):
        """Reset the agent's state."""
        super().reset()
        self.round_counter = 0
        
        # Reset all base strategies
        for strategy in self.base_strategies:
            strategy.reset()
            
        # Reset performance tracking
        self.strategy_scores = {str(strategy): 0 for strategy in self.base_strategies}
        self.last_score = 0
        
        # Start with the first strategy again
        self.current_strategy = self.base_strategies[0]
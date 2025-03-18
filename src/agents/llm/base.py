from abc import abstractmethod
import os
from src.strategies.base import Strategy
from dotenv import load_dotenv
from src.agents.llm.prompt_templates import BASIC_PROMPT, ADVANCED_PROMPT

# Load environment variables
load_dotenv()

class LLMAgentBase(Strategy):
    def __init__(self, name="LLMAgent", temperature=0.1, extended_prompt=True, reward_visibility="none"):
        super().__init__(name)
        self.temperature = temperature
        self.extended_prompt = extended_prompt
        self.reward_visibility = reward_visibility  # Options: "none", "self", "both"
        self.payoff_matrix = None  # Will be set by the tournament
    
    def move(self) -> str:
        prompt = self.build_prompt()
        decision = self.get_llm_decision(prompt)
        return decision

    def build_prompt(self) -> str:
        rounds = len(self.my_history)
        
        if rounds == 0:
            return f"No history. Please choose C or D. Your reputation is {self.reputation:.2f}."
            
        history = f"Your moves: {','.join(self.my_history)}; Opponent moves: {','.join(self.opponent_history)}."
        
        # Build a reward info string based on configuration
        rewards_info = self.build_rewards_info()
        
        if self.extended_prompt and self.payoff_matrix:
            prompt = ADVANCED_PROMPT.format(
                history=history,
                reputation=self.reputation,
                rewards_info=rewards_info,
                payoff_cc=self.payoff_matrix.get('CC', 3),
                payoff_cd=self.payoff_matrix.get('CD', 0),
                payoff_dc=self.payoff_matrix.get('DC', 5),
                payoff_dd=self.payoff_matrix.get('DD', 1)
            )
        else:
            prompt = BASIC_PROMPT.format(history=history, reputation=self.reputation)
            
        return prompt
    
    def build_rewards_info(self) -> str:
        if self.reward_visibility == "none" or not hasattr(self, 'round_rewards'):
            return ""
            
        my_total = sum(self.round_rewards) if hasattr(self, 'round_rewards') else 0
        
        if self.reward_visibility == "self":
            return f"Your total reward: {my_total}"
        elif self.reward_visibility == "both" and hasattr(self, 'opponent_rewards'):
            opp_total = sum(self.opponent_rewards)
            return f"Your total reward: {my_total}\nOpponent's total reward: {opp_total}"
        
        return ""
    
    @abstractmethod
    def get_llm_decision(self, prompt: str) -> str:
        """Get decision from an LLM. Must be implemented by subclasses."""
        pass
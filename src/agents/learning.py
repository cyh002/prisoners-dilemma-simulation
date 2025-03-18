import random
from src.strategies.base import Strategy

class QLearningAgent(Strategy):
    def __init__(self, learning_rate=0.1, discount_factor=0.9, exploration_rate=0.2):
        super().__init__("QLearningAgent")
        self.lr = learning_rate
        self.df = discount_factor
        self.epsilon = exploration_rate
        self.q_values = {}
        self.last_state = None
        self.last_action = None

    def get_state(self):
        if not self.my_history or not self.opponent_history:
            return None
        # Using extended history (last 2 moves) as state.
        return (tuple(self.my_history[-2:]), tuple(self.opponent_history[-2:]))

    def move(self) -> str:
        state = self.get_state()
        if state not in self.q_values:
            self.q_values[state] = {"C": 0.0, "D": 0.0}
        if random.random() < self.epsilon:
            action = random.choice(["C", "D"])
        else:
            action = max(self.q_values[state], key=lambda a: self.q_values[state][a])
        self.last_state = state
        self.last_action = action
        return action

    def update(self, reward, new_state):
        if self.last_state is None:
            return
        if new_state not in self.q_values:
            self.q_values[new_state] = {"C": 0.0, "D": 0.0}
        old = self.q_values[self.last_state][self.last_action]
        future = max(self.q_values[new_state].values())
        self.q_values[self.last_state][self.last_action] = old + self.lr * (reward + self.df * future - old)

    def record(self, my_move: str, opp_move: str, reward=0):
        super().record(my_move, opp_move)
        new_state = self.get_state()
        self.update(reward, new_state)

    def reset(self):
        super().reset()
        self.last_state = None
        self.last_action = None
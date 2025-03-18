import random
import copy
import networkx as nx
from src.config import TournamentConfig
from src.logger import setup_logger
from src.strategies.basic import AlwaysCooperate, AlwaysDefect, RandomStrategy
from src.strategies.reactive import TitForTatExtended, Grudger, Joss, TitForTwoTats, HumanStrategy
from src.agents.learning import QLearningAgent
from src.agents.meta import MetaAgent
from src.agents.llm.remote import RemoteLLMAgent
from src.agents.llm.local import LocalLLMAgent

# Mapping strategy names to classes or factory functions
STRATEGY_MAP = {
    "AlwaysCooperate": AlwaysCooperate,
    "AlwaysDefect": AlwaysDefect,
    "RandomStrategy": RandomStrategy,
    "TitForTatExtended": TitForTatExtended,
    "Grudger": Grudger,
    "Joss": Joss,
    "TitForTwoTats": TitForTwoTats,
    "HumanStrategy": HumanStrategy,
    "QLearningAgent": QLearningAgent,
    "RemoteLLMAgent": RemoteLLMAgent,
    "LocalLLMAgent": LocalLLMAgent,
    "MetaAgent": MetaAgent
}

class Match:
    def __init__(self, player1, player2, config: TournamentConfig, logger):
        self.p1 = player1
        self.p2 = player2
        self.config = config
        self.logger = logger
        self.rounds = config.rounds
        if config.rounds_random:
            self.rounds = random.randint(config.min_rounds, config.max_rounds)
        self.payoffs = config.payoff_matrix.dict()
        self.dynamic_payoffs = config.dynamic_payoffs
        self.noise = config.noise
        self.shock_frequency = config.shock_frequency
        self.shock_duration = config.shock_duration

    def apply_noise(self, move: str, current_noise: float) -> str:
        if random.random() < current_noise:
            return "D" if move == "C" else "C"
        return move

    def get_round_reward(self, move1: str, move2: str) -> int:
        key = move1 + move2
        return self.payoffs.get(key, 0)

    def update_dynamic_payoffs(self, global_coop_rate: float):
        if self.dynamic_payoffs:
            # For example, if global cooperation is low, increase temptation payoff.
            if global_coop_rate < 0.4:
                self.payoffs["DC"] = 7
            else:
                self.payoffs["DC"] = 5

    def play(self, global_coop_rate: float):
        # Optionally update payoffs based on global cooperation.
        self.update_dynamic_payoffs(global_coop_rate)
        self.p1.reset()
        self.p2.reset()
        
        # Pass payoff matrix to LLM agents if they support it
        if hasattr(self.p1, 'payoff_matrix'):
            self.p1.payoff_matrix = self.payoffs
        if hasattr(self.p2, 'payoff_matrix'):
            self.p2.payoff_matrix = self.payoffs
        
        p1_total = 0
        p2_total = 0

        shock_remaining = 0
        for r in range(self.rounds):
            # Possibly trigger a shock event.
            if shock_remaining == 0 and random.random() < self.shock_frequency:
                shock_remaining = self.shock_duration
                self.logger.info("Shock event triggered! Noise is doubled for next rounds.")
            current_noise = self.noise * 2 if shock_remaining > 0 else self.noise
            if shock_remaining > 0:
                shock_remaining -= 1

            m1 = self.apply_noise(self.p1.move(), current_noise)
            m2 = self.apply_noise(self.p2.move(), current_noise)
            reward1 = self.get_round_reward(m1, m2)
            reward2 = self.get_round_reward(m2, m1)
            p1_total += reward1
            p2_total += reward2

            if hasattr(self.p1, "record"):
                if isinstance(self.p1, QLearningAgent):
                    self.p1.record(m1, m2, reward1)
                else:
                    self.p1.record(m1, m2)
            if hasattr(self.p2, "record"):
                if isinstance(self.p2, QLearningAgent):
                    self.p2.record(m2, m1, reward2)
                else:
                    self.p2.record(m2, m1)

            # Store rewards for LLM agents
            if hasattr(self.p1, 'round_rewards'):
                if not hasattr(self.p1, 'round_rewards'):
                    self.p1.round_rewards = []
                self.p1.round_rewards.append(reward1)
                
            if hasattr(self.p2, 'round_rewards'):
                if not hasattr(self.p2, 'round_rewards'):
                    self.p2.round_rewards = []
                self.p2.round_rewards.append(reward2)
                
            # For reward_visibility="both" scenario
            if hasattr(self.p1, 'opponent_rewards'):
                if not hasattr(self.p1, 'opponent_rewards'):
                    self.p1.opponent_rewards = []
                self.p1.opponent_rewards.append(reward2)
                
            if hasattr(self.p2, 'opponent_rewards'):
                if not hasattr(self.p2, 'opponent_rewards'):
                    self.p2.opponent_rewards = []
                self.p2.opponent_rewards.append(reward1)

            self.logger.debug(f"Round {r+1}: {self.p1} played {m1}, {self.p2} played {m2}. Rewards: {reward1, reward2}")

        # Update reputation after the match.
        if hasattr(self.p1, "update_reputation"):
            self.p1.update_reputation()
        if hasattr(self.p2, "update_reputation"):
            self.p2.update_reputation()

        return p1_total, p2_total

class Tournament:
    def __init__(self, config: TournamentConfig):
        self.config = config
        self.logger = setup_logger(config.logging.log_file, config.logging.verbose)
        self.players = self.create_players()
        if config.network.enabled:
            self.graph = self.build_network(len(self.players), config.network)
        else:
            self.graph = None
        self.scores = {str(player): 0 for player in self.players}
        self.match_results = []

    def create_players(self):
        players = []
        for strat_name in self.config.strategies:
            if strat_name not in STRATEGY_MAP:
                self.logger.warning(f"Unknown strategy {strat_name} in config; skipping.")
                continue
                
            if strat_name == "QLearningAgent":
                params = self.config.rl_params.dict()
                player = STRATEGY_MAP[strat_name](**params)
            elif strat_name == "RemoteLLMAgent":
                params = self.config.remote_llm_params.dict()
                player = STRATEGY_MAP[strat_name](**params)
            elif strat_name == "LocalLLMAgent":
                params = self.config.local_llm_params.dict() 
                player = STRATEGY_MAP[strat_name](**params)
            elif strat_name == "Joss":
                player = STRATEGY_MAP[strat_name](defect_prob=0.1)
            elif strat_name == "MetaAgent":
                params = self.config.meta_agent.dict()
                player = STRATEGY_MAP[strat_name](**params)
            else:
                player = STRATEGY_MAP[strat_name]()
            
            players.append(player)
        return players

    def build_network(self, n: int, net_params) -> 'nx.Graph':
        if net_params.type == "random":
            G = nx.erdos_renyi_graph(n, net_params.connectivity)
        elif net_params.type == "scale_free":
            G = nx.scale_free_graph(n)
            G = nx.Graph(G)  # convert to simple graph
        else:
            G = nx.complete_graph(n)
        # Ensure all nodes exist.
        for i in range(n):
            if i not in G.nodes():
                G.add_node(i)
        self.logger.info(f"Network built with {len(G.edges())} edges.")
        return G

    def global_cooperation_rate(self) -> float:
        # Calculate cooperation rate across all players (from last match).
        total = 0
        moves = 0
        for player in self.players:
            total += player.my_history.count("C")
            moves += len(player.my_history)
        return total / moves if moves > 0 else 1.0

    def run(self):
        n = len(self.players)
        self.logger.info(f"Starting tournament with {n} players.")
        if self.graph:
            # For network structure, let each player play with its neighbors.
            for i in self.graph.nodes():
                for j in self.graph.neighbors(i):
                    if i < j:
                        self.logger.info(f"Network match: {self.players[i]} vs {self.players[j]}")
                        p1 = copy.deepcopy(self.players[i])
                        p2 = copy.deepcopy(self.players[j])
                        match = Match(p1, p2, self.config, self.logger)
                        gcoop = self.global_cooperation_rate()
                        score1, score2 = match.play(gcoop)
                        self.logger.info(f"Result: {p1} scored {score1}, {p2} scored {score2}")
                        self.scores[str(self.players[i])] += score1
                        self.scores[str(self.players[j])] += score2
                        self.match_results.append({
                            "player1": str(self.players[i]),
                            "player2": str(self.players[j]),
                            "score1": score1,
                            "score2": score2
                        })
        else:
            # Full round-robin tournament.
            for i in range(n):
                for j in range(i+1, n):
                    self.logger.info(f"Match: {self.players[i]} vs {self.players[j]}")
                    p1 = copy.deepcopy(self.players[i])
                    p2 = copy.deepcopy(self.players[j])
                    match = Match(p1, p2, self.config, self.logger)
                    gcoop = self.global_cooperation_rate()
                    score1, score2 = match.play(gcoop)
                    self.logger.info(f"Result: {p1} scored {score1}, {p2} scored {score2}")
                    self.scores[str(self.players[i])] += score1
                    self.scores[str(self.players[j])] += score2
                    self.match_results.append({
                        "player1": str(self.players[i]),
                        "player2": str(self.players[j]),
                        "score1": score1,
                        "score2": score2
                    })

        self.logger.info("Tournament finished. Leaderboard:")
        sorted_scores = sorted(self.scores.items(), key=lambda x: x[1], reverse=True)
        for rank, (player, score) in enumerate(sorted_scores, start=1):
            self.logger.info(f"{rank}. {player}: {score}")

    def save_results(self, filename="results.csv"):
        import csv
        fieldnames = ["player1", "player2", "score1", "score2"]
        with open(filename, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in self.match_results:
                writer.writerow(row)
        self.logger.info(f"Results saved to {filename}")

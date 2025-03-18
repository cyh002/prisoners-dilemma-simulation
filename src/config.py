from pydantic import BaseModel, Field
from typing import List

class PayoffMatrix(BaseModel):
    CC: int = Field(..., description="Payoff for mutual cooperation")
    CD: int = Field(..., description="Payoff when player cooperates and opponent defects")
    DC: int = Field(..., description="Payoff when player defects and opponent cooperates")
    DD: int = Field(..., description="Payoff for mutual defection")

class RLParams(BaseModel):
    learning_rate: float = 0.1
    discount_factor: float = 0.9
    exploration_rate: float = 0.2

class LLMParams(BaseModel):
    use_api: bool = False
    api_key: str = ""
    model: str = "local_model"
    temperature: float = 0.5
    extended_prompt: bool = True

class MetaAgentParams(BaseModel):
    enabled: bool = True
    base_strategies: List[str] = ["TitForTatExtended", "AlwaysDefect", "RandomStrategy"]
    switch_frequency: int = 50

class NetworkParams(BaseModel):
    enabled: bool = True
    type: str = "random"
    connectivity: float = 0.5

class LoggingConfig(BaseModel):
    log_file: str = "tournament.log"
    verbose: bool = True

class GUIConfig(BaseModel):
    enabled: bool = True

class TournamentConfig(BaseModel):
    strategies: List[str] = ["AlwaysCooperate", "AlwaysDefect", "RandomStrategy", "TitForTatExtended", "Grudger", "Joss", "TitForTwoTats", "QLearningAgent", "LLMAgent", "HumanStrategy", "MetaAgent"]
    rounds: int = 200
    rounds_random: bool = False
    min_rounds: int = 150
    max_rounds: int = 250
    shadow_probability: float = 0.95
    payoff_matrix: PayoffMatrix
    dynamic_payoffs: bool = False
    noise: float = 0.05
    shock_frequency: float = 0.02
    shock_duration: int = 20
    reputation_weight: float = 0.5
    rl_params: RLParams
    llm_params: LLMParams
    meta_agent: MetaAgentParams
    network: NetworkParams
    logging: LoggingConfig
    gui: GUIConfig

def load_config(cfg: dict) -> TournamentConfig:
    return TournamentConfig(**cfg)

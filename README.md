# Advanced Iterated Prisoner’s Dilemma Tournament

This project is an advanced simulation of the classic Iterated Prisoner’s Dilemma (IPD) tournament inspired by Robert Axelrod’s work. It incorporates classical strategies, reinforcement learning agents, a large language model (LLM) based agent, and human interactive play. In addition, the simulation features:

- **Extended Memory & Reputation:** Strategies can consider several past rounds and update a reputation score.
- **Dynamic Payoffs:** The payoff matrix adapts based on global cooperation levels.
- **Network Structure:** Agents interact on a configurable network (random or scale-free) to simulate local interactions.
- **Stochastic Shock Events:** Random events that temporarily change game parameters (e.g. doubling the noise level).
- **Meta-Strategies:** A meta-agent that switches between different base strategies.
- **Interactive GUI:** A Tkinter-based interface shows the leaderboard and live cooperation rate.
- **Hydra & Pydantic Configuration:** Easy-to-modify configuration using Hydra and validated with Pydantic.
- **Extensibility:** Users can add their own strategies by subclassing the abstract base class.

## Project Structure

```
project/
├── conf
│   └── config.yaml         # Hydra configuration file with extended parameters
├── main.py                 # Entry point for the tournament
└── src
    ├── config.py           # Pydantic models and config loader
    ├── gui.py              # Tkinter GUI for leaderboard and visualization
    ├── logger.py           # Logger setup
    ├── strategies.py       # Abstract strategy class and built-in strategies (including HumanStrategy and MetaAgent)
    ├── agents.py           # Reinforcement learning and LLM-based agents
    └── tournament.py       # Tournament engine: network, dynamic payoffs, shocks, and reputation updating
```

## Features

- **Multiple Strategies:** Includes classic IPD strategies (Always Cooperate, Always Defect, Tit-for-Tat variants, etc.) plus advanced agents such as Q-Learning, LLM-based, and MetaAgent.
- **Dynamic & Complex Environment:** Adjusts payoffs, noise, and interactions based on ongoing game dynamics and network structure.
- **Interactive Play:** Allows users to play interactively via the command line by including `HumanStrategy` in the configuration.
- **Graphical Interface:** Visualizes the leaderboard and trends in cooperation through an integrated GUI.
- **Flexible Configuration:** Modify tournament settings, agent parameters, and network settings easily using Hydra configuration (YAML) and Pydantic for type safety.
- **Extensible Framework:** Easily add new strategies or integrate custom models (e.g., finetuned LLMs) with minimal changes.

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/advanced-ipd-tournament.git
   cd advanced-ipd-tournament
   ```

2. **Create a Virtual Environment and Install Dependencies:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

   *Dependencies include:*  
   - `hydra-core`
   - `omegaconf`
   - `pydantic`
   - `networkx`
   - `matplotlib`
   - Additional libraries as needed (e.g., `tkinter` is typically bundled with Python)

## Configuration

All settings are managed in the `conf/config.yaml` file. You can adjust:
- The list of strategies (include or exclude agents like `HumanStrategy` or `MetaAgent`).
- Round parameters (fixed or random rounds, shadow probability).
- Payoff matrix and dynamic payoff settings.
- Noise level and shock event parameters.
- Reinforcement learning and LLM agent parameters.
- Network structure settings (random vs. scale-free).
- GUI options.

Hydra loads the configuration at runtime and the values are validated via Pydantic models (see `src/config.py`).

## Running the Tournament

To start the tournament, simply run:

```bash
python main.py
```

Hydra will output the effective configuration, then the tournament engine will run:
- A network of matches will be scheduled (either full round-robin or via the configured network).
- Each match will execute multiple rounds with dynamic payoffs, shock events, and noise.
- After all matches, scores are aggregated and a leaderboard is produced.

The results are saved to `tournament_results.csv` and detailed logs are recorded in `tournament.log`.

## GUI & Visualization

If GUI is enabled in the configuration, a Tkinter window will appear at the end showing:
- A ranked leaderboard.
- A live-updating matplotlib plot that visualizes the global cooperation rate over matches.

## Extending the Project

- **Adding New Strategies:**  
  Create a new subclass of the abstract `Strategy` in `src/strategies.py` and add it to the `STRATEGY_MAP` in `src/tournament.py`. Then, include its name in the configuration file.

- **Custom LLM Integration:**  
  The `LLMAgent` in `src/agents.py` is set up to support both API-based calls and local HuggingFace models. Update its `get_llm_decision()` method as needed to integrate your own model.

- **Network & Meta-Strategies:**  
  Experiment with different network types or adjust the meta-agent behavior by modifying the relevant sections in `conf/config.yaml`.

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with detailed explanations and tests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by Robert Axelrod’s classic IPD tournaments.
- Built with Hydra, Pydantic, and NetworkX.
- Thanks to the community for continuous inspiration in multi-agent learning and game theory research.

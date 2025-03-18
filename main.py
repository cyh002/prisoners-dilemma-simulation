import hydra
from omegaconf import DictConfig, OmegaConf
from src.config import load_config
from src.tournament import Tournament
from src.gui import show_leaderboard

@hydra.main(config_path="conf", config_name="config")
def main(cfg: DictConfig):
    print(OmegaConf.to_yaml(cfg))
    config = load_config(OmegaConf.to_container(cfg, resolve=True))
    tournament = Tournament(config)
    tournament.run()
    tournament.save_results("tournament_results.csv")
    # Prepare leaderboard data.
    sorted_scores = sorted(tournament.scores.items(), key=lambda x: x[1], reverse=True)
    # For demonstration, we simulate cooperation rate history as random values.
    # In practice, you would record the global cooperation rate after each match.
    coop_rate_history = [round(0.5 + 0.1 * (i % 3) - 0.05*i, 2) for i in range(len(tournament.match_results))]
    if config.gui.enabled:
        show_leaderboard(sorted_scores, coop_rate_history)

if __name__ == "__main__":
    main()

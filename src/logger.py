import logging

def setup_logger(log_file="tournament.log", verbose=True):
    logger = logging.getLogger("TournamentLogger")
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG if verbose else logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    if not logger.handlers:
        logger.addHandler(fh)
        logger.addHandler(ch)
    return logger

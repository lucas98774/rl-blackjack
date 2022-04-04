from blackjack.environment import GameWAgents
from blackjack.methods.MonteCarlo import MonteCarloExploringStarts as MCES


def test_agent():
    game = GameWAgents(MCES, nrounds=5)
    try:
        game.play()
    except Exception as e:
        raise e
    
    return
    
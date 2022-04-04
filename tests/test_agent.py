from blackjack.environment import GameWAgents
from blackjack.methods.MonteCarlo import MonteCarloExploringStarts as MCES

def test_agent(n_rounds=5):
    game = GameWAgents(MCES, nrounds=n_rounds)
    try:
        game.play()
    except Exception as e:
        raise e
    
    return
    
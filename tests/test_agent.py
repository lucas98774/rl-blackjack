import blackjack.methods

from blackjack import GameWAgents
from blackjack.methods import MCExploringStarts as MCES

def test_agent(n_rounds=5):
    game = GameWAgents(MCES, nrounds=n_rounds)
    try:
        game.play()
    except Exception as e:
        raise e
    
    return
    
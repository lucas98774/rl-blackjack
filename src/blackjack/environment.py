from .players import Dealer, Player, IPlayer, Agent
from .round import start_round, play_round, cleanup_round

class Game(object):
    """
    Class to play a game of blackjack with an arbitary number of players

    TODO: Think about what high level metrics should be kept across rounds --- scores? Wins?
    """
    def __init__(self, nplayers:int = 1, nrounds:int = 1, **kwargs):
        """
        Initialization function for a game

        Parameters
        ----------
        nplayers : int
            the number of players (not including the dealer) playing the game
        kwargs : Dict
            keyword arguments for the Deck:

            shuffle : bool (default = True)
                whether to shuffle the deck
            repeats : int
                the number of decks to use for the game
        """
        super(Game, self).__init__()
        self.dealer = Dealer(**kwargs)
        self.players = [Player() for i in range(nplayers)]
        self.nrounds = nrounds

    def __repr__(self) -> str:
        return f"Game"

    def show_score(self) -> None:
        # show scores of the players

        # preallocate list
        winners = [False] * (len(self.players)+1)
        for i, player in enumerate(self.players):
            print(f'Players {i} final score: {player.total}')
            if player.total > self.dealer.total and not player.bust:
                # if you beat the dealer and did not bust
                winners[i] = True
            elif self.dealer.bust and not player.bust:
                # if the dealer busted and you did not bust
                winners[i] = True

        print(f"Dealer's score: {self.dealer.total}")

        winners = [str(i) for winner in winners if winner]
        
        if winners:
            print(f"Winning players were: {', '.join(winners)}")
        else:
            print('Bummer no one beat the house ... :(')

    def play(self) -> None:
        # NOTE: Think about what metrics should be tracked ...
        for i in range(self.nrounds):
            print(f'Starting round {i} ...')
            self.dealer.reset_deck()
            start_round(self.dealer, self.players)
            play_round(self.dealer, self.players)
            self.show_score()
            this_score, this_busted = cleanup_round(self.dealer, self.players)

class InteractiveGame(Game):
    """ Class for an interactive Game --- assuming the player is the interactive portion """
    def __init__(self, nplayers: int = 1, nrounds: int = 1, **kwargs):
        print("NOTE: There is only one player supported for interactive games right now ...")
        # new constructor
        self.dealer = Dealer(**kwargs)
        self.players = [IPlayer()]
        self.nrounds = nrounds

# TODO: does this need to be a separate class?
class GameWAgents(Game):
    """
    Class to play blackjack with reinforcement learning agents that are learning to play 
   
    """
    def __init__(self, rl_method, rl_kwargs={}, nagents: int=1, nplayers: int = 0, nrounds: int = 1, **kwargs):
        super().__init__(nplayers, nrounds, **kwargs)
        """
        Initialization function for a game

        Parameters
        ----------
        rl_method : RLMethod
            reinforcement learning method
        rl_kwargs : Dict[str, ?]
            kwargs for reinforcement learning method
        nagents : int, default=1
            number of agents 
        nplayers : int, default=0
            number of players (not including the dealer) playing the game
        nrounds : int, default=1
            number of rounds to play
        kwargs : Dict
            keyword arguments for the Deck:

            shuffle : bool (default = True)
                whether to shuffle the deck
            repeats : int
                the number of decks to use for the game
        """
        # add the agents into the game at the end so they can count cards ...
        self.players += [Agent(rl_method, **rl_kwargs) for i in range(nagents)]
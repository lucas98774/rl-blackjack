from tools import Dealer, Player
from round import start_round, play_round

class Game(object):
    """
    Class to play a game of blackjack with an arbitary number of players

    TODO: Think about what high level metrics should be kept across rounds
    
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
            ace_val : int      
        """
        super(Game, self).__init__()
        self.dealer = Dealer(**kwargs)
        self.players = [Player() for i in range(nplayers)]
        self.nrounds = nrounds

    def __repr__(self) -> str:
        return f"Game"

    def show_score(self) -> None:
        # show scores of the players
        winners = []
        for i, player in enumerate(self.players):
            print(f'Players {i} final score: {player.total}')
            if player.total > self.dealer.total and not player.bust:
                # if you beat the dealer and did not bust
                winners.append(str(i))
            elif self.dealer.bust and not player.bust:
                # if the dealer busted and you did not bust
                winners.append(str(i))

        print(f"Dealer's score: {self.dealer.total}")
        
        if winners:
            print(f"Winning players were: {', '.join(winners)}")
        else:
            print('Bummer no one beat the house ... :(')

    def play(self) -> None:
        # NOTE: Think about what metrics should be tracked ...
        for _ in range(self.nrounds):
            self.dealer.reset_deck()
            start_round(self.dealer, self.players)
            this_score, this_busted = play_round(self.dealer, self.players)
            self.show_score()

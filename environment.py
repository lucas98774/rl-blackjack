from tools import Dealer, Player
from round import play_round

# TODO: consider making this class to be a container for a single round: Then make another class for an entire game
# The Game would set the players and keep track of how each players is doing
# The round would conduct running a single game of blackjack ...

# NOTE: Think of how to migrate this to a round instead of a game ...
# Idea 1:
# 1. Make  the functions to play a round in a Round class which is essentially a namespace
# 2. Make a game that holds the players and the dealers which the round is played with

# Idea 2:
# Simply rename the class to round and then create a game class --- the Round will still hold the players and the dealer
# also the same players and dealer would not get reused across the rounds but this may not be a big deal ...

# Leaning toward option 1 ... 


class Game(object):
    """
    Class to play a game of blackjack with an arbitary number of players
    
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

    def __repr__(self) -> str:
        return f"Game"

    def show_score(self) -> None:
        # show scores of the players
        winners = []
        for i, player in enumerate(self.players):
            print(f'Players {i} score was {player.total}')
            if player.total > self.dealer.total and not player.bust:
                # if you beat the dealer and did not bust
                winners.append(str(i))
            elif self.dealer.bust and not player.bust:
                # if the dealer busted and you did not bust
                winners.append(str(i))

        print(f"Dealers score: {self.dealer.total}")
        
        if winners:
            print(f"Winning players were: {', '.join(winners)}")
        else:
            print('Bummer no one beat the house ... :(')

    def play(self) -> None:
        play_round(self.dealer, self.players)
        self.show_score()

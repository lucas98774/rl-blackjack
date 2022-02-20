from tools import Hand, Dealer, Player

# TODO: consider making this class to be a container for a single round: Then make another class for an entire game
# The Game would set the players and keep track of how each players is doing
# The round would conduct running a single game of blackjack ...
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

    def __repr__(self):
        return f"Game"

    def double_func(func):
        """ Decorator to run a function twice """
        def wrapper(*args, **kwargs):
            """ Function to call a function twice """
            func(*args, **kwargs)
            func(*args, **kwargs)
            return 
        return wrapper

    @double_func
    def start_round(self):
        """ Function to deal one set of cards to everyone (dealer included) """
        for player in self.players:
            self.dealer.deal_card(player)

        # TODO: see if this works
        self.dealer.deal_card(self.dealer)
        return 

    def single_hand_one_player(self, player, dealers_card):
        """ Function to play out a single player's hand against the dealer """
        # the policy maps the state to the action
        action = player.policy(dealers_card)
        print(f"Dealers Value: {dealers_card}")

        if action == 'stay':
            return 
        else:
            # the player has hit
            print(f'Players Total: {player.total}\n Dealing another card to them')
            self.dealer.deal_card(player)
            self.single_hand_one_player(player, dealers_card)

    def play_round(self):
        """ Function to play a round of blackjack  """
        # dealers second card is face up
        dealers_card = self.dealer.hand[1].value

        for i, player in enumerate(self.players):
            print(f"Dealing player {i}")
            # TODO: implement a recursive function to play a single hand between a player and a dealer
            self.single_hand_one_player(player, dealers_card)

        # dealer finishes his hand
        print("Dealer finishing the round")
        self.single_hand_one_player(self.dealer, dealers_card)

        # NOTE: should I collect the scores of the game here? or in another function?
        return

    def show_score(self):
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

    def play(self):
        self.start_round()
        self.play_round()
        self.show_score()
        return


class TwoPlayerGame(object):
    """
    Class to represent a two player game of blackjack --- one dealer and one player

    Attributes
    ----------
    """

    def __init__(self):
        super(TwoPlayerGame, self)
        self.dealer=Hand()
        self.player=Hand()
from tools import Hand, Deck

class Player(object):
    """
    Class for a player in the game
    The idea is the player has a hand and __takes actions___ (this is key for rl)
    
    """ 
    # NOTE: this is the actions space
    actions = {
        'stay': 0,
        'hit': 1
    }

    def __init__(self):
        super(Player, self)
        self.hand=Hand()

    def __repr__(self) -> str:
        return f"Player"

    def add_card(self, card) -> None:
        self.hand.cards.append(card)
        return

    @property
    def total(self) -> int:
        return self.hand.total
    
    @property
    def bust(self) -> bool:
        return self.hand.bust

    def policy(self, dealers_value, *other_palyers) -> str:
        # the policy will be a function of this players hand, the dealers hand and possibly the other players card as well
        # TODO: add an encoding for the other_players hands to map to a state ... need to think about how to do this  
        
        # hardcode a policy for now to simulate a game ...
        assumed_total = dealers_value + 8
        if self.total <= assumed_total and self.total < 18:
            return 'hit'
        return 'stay'

class IPlayer(Player):
    """
    Class for an interactive player where the a prompt is given for an action

    # NOTE: this class has not been tested yet ...
    """
    def get_action(self) -> str:
        print('---Current Hand---')
        for c in self.hand.cards:
            print(f'  {c} -> {int(c)}')

        options = list(self.actions.keys())
        valid_options = ', '.join(options)
        action = str(input(f"Please enter an action (one of {valid_options}): "))

        assert action in options, f"Selected option {action} is not one of {valid_options}"
        return action

    def policy(self, dealers_value) -> str:
        print(f"----Your value is {self.total} and the dealer has a face up card with a value of {dealers_value}")

        while True and self.total <= 21:
            try:
                action = self.get_action()
                return action
            except AssertionError:
                print("Please select a valid option")

        return "stay"

class Dealer(Player):
    """
    Class for a dealer ... This is the house
    The difference between a dealer and a player is a dealer has a predefined policy where a player can change, learn
    and update their policy (method to choose an action)

    """
    def __init__(self, **kwargs):
        super().__init__()
        # NOTE: Should the dealer have the deck and the cards?
        self.deck_kwargs = kwargs  # save the deck kwargs
        self.deck = Deck(shuffle=True, **kwargs)

    def __repr__(self) -> str:
        return f"Dealer"
    
    def policy(self, dealers_value=None) -> str:
        # need to intake the second parameter for ease of implementation
        # Basic policy for the dealer
        total = self.hand.total
        if total < 17:
            return 'hit'
        else:
            return 'stay'
    
    def deal_card(self, player) -> None:
        """
        Method to deal a card to another player from the deck
        """
        # deal the card and pass it to the player --- handle the odd case where you run out of cards
        try:
            card = self.deck.deal_card()
        except IndexError:
            print("Dealer ran out of cards, grabbing a new deck")
            self.reset_deck()
            card = self.deck.deal_card()
        player.add_card(card)

        return 
    
    def reset_deck(self) -> None:
        self.deck = Deck(shuffle=True, **self.deck_kwargs)
        return

class Agent(Player):
    """
    Class to add functionality of learning a policy via rl ... hence an agent instead of a human player
    
    NOTE: This will need to implement all the rl ---
    1. Initialization of all the states and rewards --- and how that will be stored
    2. Keeping track of the state and the selected actions and the corresponding rewards
    3. ...    
    """
    # NOTE: additional setup here --- need to define the state space and the initialize the value function
    # 1. state space will be all possible states that can be visited a (potentially use a default dict)
    # 2. value function will estimate how good it is to be in the curren state (this will get updated in rl)
    # 3. policy will choose an action based on the value function given the current state
    # 4. after a reward is received the value function will be updated according to the rl algorithm 

    def policy(self, dealers_value, *other_players) -> str:
        # NOTE: this will need to be overriden
        return super().policy(dealers_value,  *other_players)
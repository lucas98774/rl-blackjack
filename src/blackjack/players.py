from random import choice
from typing import Dict, List, Tuple
from .tools import Hand, Deck, VALUES, LABELS, SUITS


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

# TODO: define an interative mean function:
def iterative_mean(current_val, current_mean, count) -> Tuple[float, int]:
    """
    Function to compute the iterative mean

    Parameters
    ----------
    current_val : float
        the current value to add to the mean (this will be the reward)
    current_mean : float
        the current mean (this will be the current return)
    count : int
        the number of observations so far

    Returns
    -------
    new_mean : float
        the updated mean
    count : int
        the updated number of observations
    """
    # see here: https://datagenetics.com/blog/november22017/index.html#:~:text=To%20find%20the%20mean%2C%20you,Done!
    # NOTE: could also use the sum of the numbers which may be better in the long term
    return current_mean + (current_val - current_mean) / (count+1), count+1



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

    # define action space
    actions = {
        'hit': 1,
        'stay': 0
    }

    rewards = {
        'win': 1,
        'lose': -1,
        'push': 0
    }

    player_values = list(range(12, 22))  # 12-22 (22+ = bust) (this represents the state)
    dealer_values = list(range(2, 12))
    # NOTE: Think about implementing the rl in a different module then run through here??? ...

    def __init__(self, init_val:int = 5):
        # TODO: accept any params that will affect the rl --- ie: exploring starts ...
        super().__init__()
        self.init_val = init_val

        # initialize the policy and the 
        self.policy_func = self._init_policy()
        self.q_func = self._init_q_func(self.init_val)
        
        # define metrics to store for the returns --- one for each state-action pair
        self.return_func = self.make_return_func(self.q_func)


    def _init_policy(self) -> Dict[Tuple(int, int), str]:
        """ Function to initialize the policy function --- policy intakes the state and then chooses an action """
        policy_func = {}
        for player_value, dealer_value in self.player_values, self.dealer_values:
            # TODO: check this random initialization
            policy_func[(player_value, dealer_value)] = choice(list(self.actions.keys()))

        return policy_func

    def _init_q_func(self, init_val=5) -> Dict[Tuple(int, int, str), float]:
        """ Function to init the state-action function --- will estimate the return from the current state and action """
        # TODO: find a better place to put this ...
        # key will be the state and the action --- your hand, dealer value and action

        q_func = {}

        for player_value, dealer_value, action in self.player_values, self.dealer_values, self.action.keys():
            q_func[player_value, dealer_value, action] = init_val

        return q_func

    def make_return_func(self, this_dict) -> Dict[Tuple(int, int, str), Tuple(int, int)]:
        """ Function to make a return function which will return the return for being in a state-action pair """
        return_func = {}
        for key in this_dict.keys():
            # initalize the count and the return for each state-action pair to zero-zero
            return_func[key] = (0, 0)
        return return_func

    def policy(self, dealers_value, *other_players) -> str:
        # NOTE: other players hands are not taken into account rn ...
        if self.bust:
            return 'stay'
        return self.policy_func[self.total, dealers_value]

    # NOTE: need to add method for updating the policy as well as updating the state-action function (qfunc)

    def update_policy_func(self):
        """ Function to update the policy """
        pass

    def update_q_func(self, state, current_val) -> None:
        """ Function to update the q function """
        count, current_return = self.q_func[state]

        new_return, new_count = iterative_mean(current_val, current_return, count)
        self.q_func[state] = (new_count, new_return)
        return 

from functools import wraps
import json
import os
import os.path as osp
from typing import Dict, Tuple

from .tools import Hand, Deck


# setup helpers for types
_state = tuple(int, int)
_state_and_action = tuple(int, int, str)

# utility function  NOTE: deprecated ...
# def set_kwargs(**default_kwargs):
#     """ decorator with args """
#     def outer(func):
#         """ decorator to set default kwargs """
#         @wraps(func)
#         def inner(*args, **kwargs):

#             # update kwargs if default not provided
#             kwargs.update({k:v for k,v in default_kwargs.items() if k not in kwargs})

#             res = func(*args, **kwargs)
#             return res
#         return inner
#     return outer

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

    def clear_hand(self) -> None:
        """ Function to reset the hand at the end of the round """
        self.hand = Hand()

    def end_round(self, *args, **kwargs) -> None:
        """ Function to do any end of round clean up for a player ..."""
        self.clear_hand()

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
    
    An agent is a player that is trying to learn via reinforcement learning, although the specific algorithm is an input
    an agent will:
    1. define the action space and rewards recieved
    2. define the states of the game
    3. initialize and track a value or q function (with help from rl method)
    4. initialize and track a policy (with help from rl method)
    5. use a policy for making decisions
    6. keep track of the states
    7. keep track of the rewards
    """

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

    def __init__(self, rl_method, **rl_kwargs):
        super().__init__()

        self.method = rl_method(**rl_kwargs)
        self.states = []  # keep track of the states ...

        # initialize the policy and the 
        self.policy_func = self._init_policy()
        self.q_func = self._init_q_func()
        
        # define metrics to store for the returns --- one for each state-action pair
        self.return_func = self.make_return_func(self.q_func)

    def _init_policy(self):
        return self.method._init_policy(player_values=self.player_values, dealer_values=self.dealer_values, actions=self.actions)
    
    def _init_q_func(self):
        return self.method._init_q_func(player_values=self.player_values, dealer_values=self.dealer_values, actions=self.actions)

    def make_return_func(self, this_dict) -> Dict[_state_and_action, Tuple[int, float]]:
        """ 
        Function to make a return function which will return the return for being in a state-action pair 

        Parameters
        ----------
        this_dict : Dict[_state_and_action, float]
            q function
        
        Returns
        -------
        return_func : Dict[_state_and_action, Tuple(int, float)]
            return function mapping the state to the count and how good it is to be in that state
        """
        return_func = {}
        for key in this_dict.keys():
            # initalize the count and the return for each state-action pair to zero-zero
            return_func[key] = (0, 0)
        return return_func

    def policy(self, dealers_value, *other_players) -> str:
        """
        Override policy to save the states as well as return the action:
        agent will need to go backwards in time to update the state-action function
        based on the reward

        Parameters
        ----------
        dealers_value : int
            value of the face up card for the dealer
        other_players : List[?]
            hands of the other players

        Returns
        -------
        _ : str
            action
        """
        # TODO: figure out we want to encode the other players hands ...
        if self.bust:
            return 'stay'
        # NOTE: figure out if I want to keep track of the busted hands as well or not ...
        self.states.append(dealers_value)
        return self.policy_func[self.total, dealers_value]

    # TODO: define a way to traverse through the states and update the policy and the q function after a round
    def update(self, j, final_state_reward):
        """
        Function to replay the states in reverse and update the q function and/or the policy

        Parameters
        ----------
        j : int
            round index
        final_state_reward : int
            reward from the final state

        Returns
        -------
        """
        # TODO: This function must assign the return and update the corresponding states .--- not sold that 
        # a separate variable is needed for the returns but idk what else to do ...
        self.states.reverse
        round_return = 0

        # trade off between policy improvement and evaluation ...
        if j % 2 == 0:
            update_func = self.method.policy_improvement
        else:
            update_func = self.method.policy_evaluation

        # this will be looping backward since the states have been reversed 
        for i, rstate in enumerate(self.states[1:],start=2):
            round_reward += self.return_func[rstate]
            if rstate not in self.states[i:]:
                # update q_function by evaluating the policy
                self.q_func = self.method.policy_evaluation(rstate, round_reward, self.q_func, self.return_func)
                # update the policy by making it greedy wrt to the q_func
                self.policy_func = self.method.policy_improvement(rstate, self.actions, self.policy_func)

                


        return

    def save(self, out_path=os.getcwd(), indent=4) -> None:
        """
        Function to save the results of an agent

        Parameters
        ----------
        out_path : str, default=os.getcwd()
            output path for the files
        indent : int
            indent for json file

        Returns
        -------
        """
        with open(osp.join(out_path, 'policy.json'), 'w') as fp:
            json.dump(self.policy_func, fp, indent=indent)

        with open(osp.join(out_path, 'q_func.json'), 'w') as fp:
            json.dump(self.q_func, fp, indent=indent)

        return

    def load(self, in_path=os.getcwd()) -> None:
        """
        Function to load an agent q function and policy

        Parameters
        ----------
        in_path : str, default=os.getcwd()
            input path for the policy.json and q_func.json files

        Returns
        -------
        """

        with open(osp.join(in_path, 'policy.json'), 'r') as fp:
            self.policy_func = json.load(fp)

        with open(osp.join(in_path, 'q_func.json'), 'w') as fp:
            self.q_func = json.load(fp)
        
        return 

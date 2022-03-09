from typing import Tuple, List
"""
Class to hold play a round of a blackjack ... this object will essentially be a namespace as it provides
functionality to play a round however a round of blackjack only exists with a game
"""

def double_func(func):
    """ Decorator to run a function twice """
    def wrapper(*args, **kwargs):
        """ Function to call a function twice """
        func(*args, **kwargs)
        func(*args, **kwargs)
        return 
    return wrapper

@double_func
def start_round(dealer, players) -> None:
    """ 
    Function to deal one set of cards to everyone (dealer included) 
    
    Parameters
    ----------
    dealer : Dealer
        The dealer for this round
    players : List[Player]
        The players for this round    
    """
    for player in players:
        dealer.deal_card(player)

    dealer.deal_card(dealer)
    return 

def single_hand_one_player(dealer, player) -> None:
    """ 
    Function to play out a single player's hand against the dealer 
    
    Parameters
    ----------
    dealer : Dealer
        The dealer for this round
    players : List[Player]
        The players for this round
    """
    dealers_card = dealer.hand[1].value
    # the policy maps the state to the action
    action = player.policy(dealers_card)
    print(f"--Dealers Value: {dealers_card}\n--Players Total: {player.total}")

    if action == 'stay':
        return 
    else:
        # the player has hit
        print('\tDealing another card to them')
        dealer.deal_card(player)
        single_hand_one_player(dealer, player)

def play_round(dealer, players) -> Tuple[List[int], List[bool]]:
    """ 
    Function to play a round of blackjack  
    
    Parameters
    ----------
    dealer : Dealer
        The dealer for this round
    players : List[Player]
        The players for this round

    Returns
    -------
     : Tuple[List[int], List[bool]]
        Tuple containing the scores (first element) and which players busted (second element) --- 
        in both lists, the dealer comes first
    """
    # dealers second card is face up
    for i, player in enumerate(players):
        print(f"Dealing player {i} ...")
        # TODO: implement a recursive function to play a single hand between a player and a dealer
        single_hand_one_player(dealer, player)

    # dealer finishes his hand
    print("Dealer finishing the round")
    single_hand_one_player(dealer, dealer)

    # NOTE: Think about returning the scores and who busted here ...
    scores = []
    busted = []
    for player in [dealer, *players]:
        scores.append(player.hand.total)
        busted.append(player.hand.bust)
        
    return scores, busted

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

def single_hand_one_player(dealer, player, other_players=[]) -> None:
    """ 
    Function to play out a single player's hand against the dealer 
    
    Parameters
    ----------
    dealer : Dealer
        The dealer for this round
    player : Player
        The current player who is selecting an action
    other_players : List[Player]  # NOTE: Think about this!!! What should be passed here
        The other players in the current round  
    """
    dealers_card = dealer.hand[1].value
    # NOTE: the policy maps the state to the action, based on the current players hand, the dealers card 
    # and possibly the other face up cards as well 
    action = player.policy(dealers_card, *other_players)
    print(f"--Dealers Value: {dealers_card}\n--Players Total: {player.total}")

    if action == 'stay':
        return 
    else:
        # the player has hit
        print('\tDealing another card to them')
        dealer.deal_card(player)
        single_hand_one_player(dealer, player, other_players)

def calc_winner(dealer_score, player_score) -> int:
    """
    Function to calc the winner between the dealer and a player
    
    Parameters
    ----------
    dealer_score : int
        dealer's score
    player_score : int
        player's score
    
    Returns
    -------
    result : int
        whether the _player_ won --- 1, 0 is push and -1 is loss
    """
    if player_score > dealer_score:
        return 1
    elif player_score == dealer_score:
        return 0
    return -1

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
        # grab the other players so the policy can be based on all cards in play ...
        other_players = [player for j, player in enumerate(players) if  j != i]
        print(f"Dealing player {i} ...")
        # TODO: implement a recursive function to play a single hand between a player and a dealer
        single_hand_one_player(dealer, player, other_players)

    # dealer finishes his hand
    print("Dealer finishing the round")
    single_hand_one_player(dealer, dealer)

    # NOTE: Think about returning the scores and who busted here ...
    scores = [dealer.hand.total] + [None] * len(players)
    busted = [dealer.hand.bust] + [None] * len(players)
    for i, player in enumerate(players, start=1):
        scores[i] = player.hand.total
        busted[i] = player.hand.bust
        result = calc_winner(dealer.hand.total, player.hand.total)
        player.end_round(result)

        
    return scores, busted

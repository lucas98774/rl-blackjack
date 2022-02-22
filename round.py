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
    print(f"Dealers Value: {dealers_card}")

    if action == 'stay':
        return 
    else:
        # the player has hit
        print(f'Players Total: {player.total}\n Dealing another card to them')
        dealer.deal_card(player)
        single_hand_one_player(dealer, player)

def play_round(dealer, players) -> None:
    """ 
    Function to play a round of blackjack  
    
    Parameters
    ----------
    dealer : Dealer
        The dealer for this round
    players : List[Player]
        The players for this round
    """
    # dealers second card is face up
    dealers_card = dealer.hand[1].value

    for i, player in enumerate(players):
        print(f"Dealing player {i}")
        # TODO: implement a recursive function to play a single hand between a player and a dealer
        single_hand_one_player(player, dealers_card)

    # dealer finishes his hand
    print("Dealer finishing the round")
    single_hand_one_player(dealer, dealer)

    return

def play(dealer, players) -> None:
    """ 
    High Level Function call to play 
    
    Parameters
    ----------
    dealer : Dealer
        The dealer for this round
    players : List[Player]
        The players for this round
    """
    start_round(dealer, players)
    play_round(dealer, players)
    return

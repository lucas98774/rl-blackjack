import random
from abc import ABC, abstractmethod

class Card(object):
    # This is a fundamental object
    """
    Card Class
    
    Attributes
    ----------
    label : str
        The label of the card (2-10 Jack, Queen, King, Ace)

    suit : str
        The suit (Hearts, Clubs, Diamonds, Spades)

    value : int
        The number value of the card (2-10, 11 or 1)
    """
    def __init__(self, label:str, suit:str, value:int):
        super(Card, self).__init__()
        self.label = label
        self.suit = suit
        self.value = value

    def __repr__(self):
        return f"{self.label} of {self.suit}"
    
    def __int__(self) -> int:
        """ Function to allow coersion to an int """
        return self.value

    def __add__(self, other_card) -> int:
        if not isinstance(other_card, (int, float, Card)):
            raise AssertionError(f"Addition for Cards is only supported for other cards, ints or float\nRecieved type: {type(other_card)}")

        if isinstance(other_card, (int, float)):
            return self.value + other_card

        return self.value + other_card.value

    def __radd__(self, other_card) -> int:
        return self.__add__(other_card)

# NOTE: Should a hand and a deck be releated??
# Idea: Implement a stack of cards --- allows:
# 1. Holding multiple cards
# 2. Traversing that stack of cards on at a time (it is an iterator)

class CardStack(ABC):
    """
    Class to hold multiple cards and to allow iterating across the cards
    """
    @abstractmethod
    def __init__(self, *args):
        self.cards = list(args)
        self.msg = f"{len(self.cards)} cards"

    def __len__(self) -> int:
        return len(self.cards)

    def __getitem__(self, index):
        """ Function to show a card given an index """
        if index > len(self):
            raise AssertionError(f"That index is outside the size of this deck\nDeck size: {len(self)}, Index recieved {index}")
        return self.cards[index] 

class Hand(CardStack):
    # This represents the state
    """
    Class for a hand of Blackjack

    Attributes
    ----------
    cards : List[Card]
        list of the cards
    """
    def __init__(self, *args):
        super(Hand, self).__init__(*args)
        self.msg += f" totaling {self.total}"

    def __repr__(self):
        # this is not copy be reference since it is a primative ... NOTE: check this
        msg = self.msg
        if self.bust:
            msg += "\nOver 21 ... Busted"
        return msg

    @property
    def total(self):
        return sum(self.cards)

    @property
    def bust(self):
        if self.total < 21:
            return False
        return True

class Deck(CardStack):
    # This represents the environment
    """
    Class for a single Deck of Cards ---

    Extends CardStack in two ways:
    1. Sets up a deck (or decks) which means setting up the predefined combination of suits and values to 
    create a standard deck (allows setting up deck with some options)
    2. Allowing to traverse over the cards using an iterator of convience

    Attributes
    ----------
    values : List[str]
        values that can be taken by a card (2-10, Jack, Queen, King, Ace)

    suits : List[str]
        suits that a card can take (Clubs, Diamonds, Spades, Hearts)
    """
    suits = ('Hearts', 'Diamonds', 'Clubs', 'Spades')

    labels = [str(i) for i in range(2,11)]
    labels.extend(('Jack', 'Queen', 'King', 'Ace'))

    values = list(range(2, 11))
    values.extend((10,10,10,11))

    def __init__(self, shuffle:bool = True, repeats:int = 1, ace_val:int = 11):
        """
        Init function for a deck

        Parameters
        ----------
        shuffle : bool
            whether to shuffle the deck
        repeats : int
            the number of decks to use for the game
        ace_val : int
            the value of the ace (either 11 or 1)        
        """
        # TODO: Should we allow for an infinite deck?
        # NOTE: do not pass any cards to the constructor of card stack
        super(Deck, self).__init__()
        self.shuffle = shuffle
        self.repeats = repeats
        self.values[-1] = ace_val

        self.label_to_value = dict(zip(self.labels, self.values))
        # reassign self.cards to the deck
        self.cards = self._create_deck()
        self.counter=0
        
    def _create_deck(self):
        """
        Function to create a Deck

        Returns
        -------

        deck : List[Card]
            List of cards
        """
        # create the number of decks
        decks = [[Card(label, suit, self.label_to_value[label]) for label in self.labels for suit in self.suits] for i in range(self.repeats)]
        # flatten the decks into a single full deck
        full_deck = [card for deck in decks for card in deck]
        if self.shuffle:
            random.shuffle(full_deck)
        return full_deck
    
    def __repr__(self) -> str:
        return f"{self.repeats} Deck(s) with " + self.msg

    def deal_card(self):
        """ Function to deal a single card from the deck """
        # NOTE: is this useful?
        card = self.cards.pop(0)
        return card

    def __iter__(self):
        return self

    def __next__(self):
        if self.counter >= len(self):
            raise StopIteration
        current_card = self.__getitem__(self.counter)
        self.counter += 1
        return current_card

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

    def add_card(self, card):
        self.hand.cards.append(card)

    @property
    def total(self):
        return self.hand.total
    
    @property
    def bust(self):
        return self.hand.bust

    def policy(self, dealers_value):
        # the policy will be a function of this players hand and the dealers hand ...
        # hardcode a policy for now to simulate a game ...

        assumed_total = dealers_value + 8
        if self.total <= assumed_total and self.total < 18:
            return 'hit'
        return 'stay'

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
    
    def policy(self, dealers_value=None):
        # need to intake the second parameter for ease of implementation
        # Basic policy for the dealer
        total = self.hand.total
        if total < 17:
            return 'hit'
        else:
            return 'stay'
    
    def deal_card(self, player):
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
    
    def reset_deck(self):
        self.deck = Deck(suffle=True, **self.deck_kwargs)





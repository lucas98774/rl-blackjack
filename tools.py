import random
from typing import List
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

    def __repr__(self) -> str:
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

    def __getitem__(self, index) -> Card:
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

    def __repr__(self) -> str:
        # this is not copy be reference since it is a primative ... NOTE: check this
        msg = self.msg
        if self.bust:
            msg += "\nOver 21 ... Busted"
        return msg

    @property
    def total(self) -> int:
        num_aces = 0
        total_value = 0
        for card in self.cards:
            if card.label == 'Ace':
                num_aces += 1
            total_value += card.value
        for i in range(num_aces):
            if total_value > 21:
                total_value -= 10
        return total_value

    @property
    def bust(self) -> bool:
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
        
    def _create_deck(self) -> List[Card]:
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

    def deal_card(self) -> Card:
        """ Function to deal a single card from the deck """
        # NOTE: is this useful?
        card = self.cards.pop(0)
        return card

    def __iter__(self):
        return iter(self.cards)
    
    # NOTE: This is the full code to make an iterator from a class
    # def __iter__(self):
    #     return self

    # def __next__(self) -> Card:
    #     if self.counter >= len(self):
    #         raise StopIteration
    #     current_card = self.__getitem__(self.counter)
    #     self.counter += 1
    #     return current_card

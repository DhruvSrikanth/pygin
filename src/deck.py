import random
from copy import deepcopy
from typing import List
from errors import EmptyDeckError
from card import Card
from constants import FULL_DECK


class Deck(object):
    def __init__(self):
        self.reset_deck()

    def __len__(self):
        return len(self.cards)

    def __str__(self):
        return f"Deck with {len(self)} cards."

    def __repr__(self):
        return f"Deck(cards={self.cards})"

    def reset_deck(self):
        """Resets the deck to a full set of 52 cards and shuffles it."""
        self.cards: List[Card] = deepcopy(FULL_DECK)
        self.shuffle_deck()

    def shuffle_deck(self):
        """Shuffles the deck."""
        random.shuffle(self.cards)

    def draw_card(self) -> Card:
        """Draws a card from the deck."""
        if len(self.cards) == 0: raise EmptyDeckError
        return self.cards.pop()

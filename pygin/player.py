from .card import Card
from .hand import Hand
from .errors import CardDoesNotExistError


class Player(object):
    def __init__(self, name: str):
        self.name = name
        self.hand: Hand = Hand()

    def __str__(self):
        return f"Player {self.name} with hand: {self.hand}" if len(self.hand) > 0 else f"Player {self.name}, Empty Hand"

    def __repr__(self):
        return f"Player(name={self.name}, hand={self.hand})"

    def get_hand(self) -> Hand:
        return self.hand

    def take_card(self, card: Card):
        self.hand.add_card(card)

    def discard_card(self, card: Card):
        try:
            self.hand.remove_card(card)
        except CardDoesNotExistError:
            print(f"{self.name} cannot discard the card. It does not exist in the hand.")

    def clear_hand(self):
        """Resets the player's hand to an empty set of cards."""
        self.hand.clear()

from card import Card
from hand import Hand
from deck import Deck
from errors import EmptyDeckError, CardDoesNotExistError


class Player(object):
    def __init__(self, name: str):
        self.name = name
        self.hand = Hand()

    def __str__(self):
        return f"Player {self.name} with hand: {self.hand}" if len(self.hand) > 0 else f"Player {self.name}, Empty Hand"

    def __repr__(self):
        return f"Player(name={self.name}, hand={self.hand})"

    def draw_card(self, deck: Deck):
        try:
            card = deck.draw_card()
            self.hand.add_card(card)
        except EmptyDeckError:
            print(f"{self.name} cannot draw a card. The deck is empty.")

    def discard_card(self, card: Card):
        try:
            self.hand.remove_card(card)
        except CardDoesNotExistError:
            print(f"{self.name} cannot discard the card. It does not exist in the hand.")


if __name__ == '__main__':
    deck = Deck()
    player = Player(name="Alice")
    print(player)
    player.draw_card(deck)
    player.draw_card(deck)
    player.draw_card(deck)
    print(player)
    player.discard_card(player.hand[0])
    print(player)

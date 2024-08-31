from card import Card
from errors import CardDoesNotExistError


class Hand(object):
    def __init__(self):
        self.cards = []

    def __len__(self):
        return len(self.cards)

    def __str__(self):
        return ", ".join(map(str, self.cards))

    def __repr__(self):
        return f"Hand(cards={self.cards})"

    def __iter__(self):
        return iter(self.cards)

    def __getitem__(self, index: int) -> Card:
        return self.cards[index]

    def add_card(self, card: Card):
        """Adds a card to the hand."""
        self.cards.append(card)

    def has_card(self, card: Card) -> bool:
        """Returns True if the hand has the card, False otherwise."""
        return card in self.cards

    def remove_card(self, card: Card):
        """Removes a card from the hand if it exists."""
        if not self.has_card(card=card): raise CardDoesNotExistError
        self.cards.remove(card)

    def clear(self):
        """Resets the hand to an empty set of cards."""
        self.cards = []

from dataclasses import dataclass


@dataclass
class Card:
    rank: str
    suit: str

    def __str__(self):
        return f"{self.rank} of {self.suit}"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit

    def __hash__(self):
        return hash((self.rank, self.suit))


if __name__ == '__main__':
    card = Card('Q', 'Hearts')
    print(card)
    print(card == Card('Q', 'Hearts'))
    print(card == Card('Q', 'Spades'))

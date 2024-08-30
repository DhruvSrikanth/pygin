from card import Card

SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
FULL_DECK = [
    Card(rank=rank, suit=suit)
    for suit in SUITS
    for rank in RANKS
]
MAX_SCORE = 100
HAND_SIZE = 10
KNOCK_LIMIT = 10
GIN_BONUS = 25
UNDERCUT_BONUS = 10

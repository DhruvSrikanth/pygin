"""
Gin Rummy Game Engine

Rules:
1. Gin Rummy is a two-player card game.
2. The objective is to form sets (three or four cards of the same rank) and runs (three or more cards in sequence of the same suit).
3. Each player is dealt 10 cards.
4. Players take turns drawing a card from either the deck or the discard pile and then discarding one card.
5. When the deck is empty, the discard pile is shuffled and becomes the new deck.
6. At any given time, a player's hand consists of 10 cards.
7. Players cannot see the cards in the opponent's hand.
8. Players also cannot see the cards in the deck.
9. Players can see the top card of the discard pile.
10. The round ends when a player "knocks" (ends the round) by discarding a card and revealing their hand or when any player has "Gin" (ends the round by revealing their hand with no unmatched cards) or "Big Gin" (ends the round by revealing their hand with no unmatched cards after drawing the top card of the discard pile).
11. A player can "knock" only if the total value of unmatched cards in their hand is less than or equal to 10 points and when it is their turn.
12. The points for a hand are calculated by adding the values of the unmatched cards in the hand. (Face cards are worth 10 points, Aces are worth 1 point, and numbered cards are worth their face value.)
13. When a player "knocks", both players reveal their hands and form sets and runs with their respective hands.
14. The player who did not knock can add unmatched cards from their hand to the sets and runs formed by the other player to reduce the points in their hand.
15. The player with the lowest deadwood (unmatched cards) points wins the round.
16. The winner of the round scores the difference in points (deadwood points) between the two players.
17. If the player who did not knock has less deadwood points than the knocking player, the knocking player is "undercut" and the non-knocking player scores the difference in points plus a 10-point bonus.
18. If a player has Gin, they score the deadwood points of the opponent plus a 25-point bonus.
19. The game ends when a player reaches 100 points.
"""

import random
from .player import Player
from .deck import Deck
from .hand import Hand
from .card import Card
from .utils import mark_deadwood
from .constants import HAND_SIZE, KNOCK_LIMIT, GIN_BONUS, BIG_GIN_BONUS, UNDERCUT_BONUS, ROUND_WIN_BONUS


class GinRummyEngine(object):
    def __init__(self, player1: str, player2: str):
        self.players = [Player(name=player1), Player(name=player2)]
        self.deck = Deck()
        self.discard_stack = []
        self.start_player_idx = random.randint(0, 1)
        self.current_player_index = self.start_player_idx
        self.scores = [0, 0]
        self.rounds_won = [0, 0]

    def get_player(self, player_name: str) -> Player:
        """Return the player object with the given name."""
        return next((p for p in self.players if p.name == player_name), None)

    def deal_initial_hands(self):
        """Deal 10 cards to each player from the deck."""
        for _ in range(HAND_SIZE):
            for idx in [self.start_player_idx, self.get_next_player_idx(player_idx=self.start_player_idx)]:
                self.players[idx].take_card(card=self.deck.draw_card())

    def get_next_player_idx(self, player_idx: int) -> int:
        """Return the index of the next player."""
        return (player_idx + 1) % 2

    def get_current_player_idx(self) -> int:
        """Return the index of the current player."""
        return self.current_player_index

    def get_opponent_player_idx(self) -> int:
        """Return the index of the opponent player."""
        return (self.current_player_index + 1) % 2

    def get_current_player(self) -> Player:
        """Return the current player."""
        return self.players[self.get_current_player_idx()]

    def get_opponent_player(self) -> Player:
        """Return the opponent player."""
        return self.players[self.get_opponent_player_idx()]

    def switch_turn(self):
        """Switch the turn to the next player."""
        self.current_player_index = self.get_opponent_player_idx()

    def draw_card(self, from_discard_stack: bool) -> Card:
        """Draw a card from the deck or the discard pile."""
        if from_discard_stack and self.discard_stack: card = self.discard_stack.pop()  # The top card of the discard pile is the last card in the list.
        else: card = self.deck.draw_card()
        self.get_current_player().take_card(card=card)
        return card

    def discard_card(self, card: Card):
        """Discard a card from the current player's hand."""
        self.get_current_player().discard_card(card=card)
        self.discard_stack.append(card)

    def can_knock(self) -> bool:
        """Check if the current player is allowed to knock."""
        player_hand = self.get_current_player().get_hand()
        deadwood_count = self.get_deadwood_count(hand=player_hand)
        return deadwood_count <= KNOCK_LIMIT

    def mark_deadwood(self, hand: Hand) -> Hand:
        """Mark the deadwood cards in a given hand."""
        return mark_deadwood(hand=hand)

    def get_card_value(self, card: Card) -> int:
        """Get the value of a card for scoring purposes."""
        if card.rank in ['J', 'Q', 'K']: return 10
        elif card.rank == 'A': return 1
        else: return int(card.rank)

    def get_deadwood_count(self, hand: Hand) -> int:
        """Calculate the deadwood count (unmatched cards value) for a given hand."""
        marked_hand = self.mark_deadwood(hand=hand)
        deadwood_cards = [card for card in marked_hand if card.is_deadwood]
        return sum(self.get_card_value(card=card) for card in deadwood_cards)

    def knock(self):
        """Handle the knock action by the current player."""
        current_player_deadwood = self.get_deadwood_count(hand=self.get_current_player().get_hand())
        opponent_player_deadwood = self.get_deadwood_count(hand=self.get_opponent_player().get_hand())
        deadwood_difference = opponent_player_deadwood - current_player_deadwood
        if deadwood_difference > 0:
            self.scores[self.get_current_player_idx()] += deadwood_difference
            self.rounds_won[self.get_current_player_idx()] += 1
        else:
            self.scores[self.get_opponent_player_idx()] += -deadwood_difference + UNDERCUT_BONUS
            self.rounds_won[self.get_opponent_player_idx()] += 1

    def is_gin(self):
        """Check if the current player has Gin."""
        assert len(self.get_current_player().get_hand()) == HAND_SIZE
        is_gin = self.get_deadwood_count(hand=self.get_current_player().get_hand()) == 0
        win_amount = self.get_deadwood_count(hand=self.get_opponent_player().get_hand()) + GIN_BONUS if is_gin else 0
        return is_gin, win_amount

    def is_big_gin(self):
        """Check if the current player has Big Gin."""
        assert len(self.get_current_player().get_hand()) == HAND_SIZE + 1
        is_big_gin = self.get_deadwood_count(hand=self.get_current_player().get_hand()) == 0
        win_amount = self.get_deadwood_count(hand=self.get_opponent_player().get_hand()) + BIG_GIN_BONUS if is_big_gin else 0
        return is_big_gin, win_amount

    def reset_round(self):
        """Reset the game state for a new round."""
        self.deck.reset_deck()
        self.discard_stack = []
        for player in self.players: player.clear_hand()
        self.start_player_idx = self.get_next_player_idx(player_idx=self.start_player_idx)
        self.deal_initial_hands()

    def compute_final_scores(self):
        self.scores[self.get_current_player_idx()] += self.rounds_won[self.get_current_player_idx()] * ROUND_WIN_BONUS
        self.scores[self.get_opponent_player_idx()] += self.rounds_won[self.get_opponent_player_idx()] * ROUND_WIN_BONUS

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

from constants import HAND_SIZE, KNOCK_LIMIT, GIN_BONUS, UNDERCUT_BONUS, MAX_SCORE
from player import Player
from deck import Deck
from hand import Hand
from card import Card


class GinRummyEngine(object):
    def __init__(self, player1: str, player2: str):
        self.players = [Player(name=player1), Player(name=player2)]
        self.deck = Deck()
        self.discard_pile = []
        self.current_player_index = 0
        self.scores = [0, 0]

    def deal_initial_hands(self):
        """Deal 10 cards to each player from the deck."""
        for _ in range(HAND_SIZE):
            for player in self.players:
                player.draw_card(self.deck)

    def get_current_player(self) -> Player:
        """Return the current player."""
        return self.players[self.current_player_index]

    def get_opponent_player(self) -> Player:
        """Return the opponent player."""
        return self.players[(self.current_player_index + 1) % 2]

    def switch_turn(self):
        """Switch the turn to the next player."""
        self.current_player_index = (self.current_player_index + 1) % 2

    def draw_card(self, from_discard_pile: bool) -> Card:
        """Draw a card from the deck or the discard pile."""
        if from_discard_pile and self.discard_pile:
            card = self.discard_pile.pop()
        else:
            card = self.deck.draw_card()
        self.get_current_player().draw_card(card)
        return card

    def discard_card(self, card: Card):
        """Discard a card from the current player's hand."""
        self.get_current_player().discard_card(card)
        self.discard_pile.append(card)

    def is_knock_allowed(self) -> bool:
        """Check if the current player is allowed to knock."""
        player_hand = self.get_current_player().hand
        unmatched_cards = [card for card in player_hand if not self.is_card_matched(card, player_hand)]
        deadwood_count = sum(self.get_card_value(card) for card in unmatched_cards)
        return deadwood_count <= KNOCK_LIMIT

    def is_card_matched(self, card: Card, hand: Hand) -> bool:
        """Check if a card is part of a set or run in the given hand."""
        rank_counts = {rank: sum(1 for c in hand if c.rank == rank) for rank in set(c.rank for c in hand)}
        suit_counts = {suit: sum(1 for c in hand if c.suit == suit) for suit in set(c.suit for c in hand)}

        # Check for sets
        if rank_counts.get(card.rank, 0) >= 3:
            return True

        # Check for runs
        sorted_cards = sorted(hand, key=lambda c: (c.suit, RANKS.index(c.rank)))
        run_length = 1
        prev_card = sorted_cards[0]
        for curr_card in sorted_cards[1:]:
            if curr_card.suit == prev_card.suit and RANKS.index(curr_card.rank) == RANKS.index(prev_card.rank) + 1:
                run_length += 1
            else:
                run_length = 1
            if run_length >= 3 and curr_card == card:
                return True
            prev_card = curr_card

        return False

    def get_card_value(self, card: Card) -> int:
        """Get the value of a card for scoring purposes."""
        if card.rank in ['J', 'Q', 'K']:
            return 10
        elif card.rank == 'A':
            return 1
        else:
            return int(card.rank)

    def get_deadwood_count(self, hand: Hand) -> int:
        """Calculate the deadwood count (unmatched cards value) for a given hand."""
        unmatched_cards = [card for card in hand if not self.is_card_matched(card, hand)]
        return sum(self.get_card_value(card) for card in unmatched_cards)

    def knock(self):
        """Handle the knock action by the current player."""
        if not self.is_knock_allowed():
            print(f"{self.get_current_player().name} is not allowed to knock.")
            return

        current_player_hand = self.get_current_player().hand
        opponent_player_hand = self.get_opponent_player().hand

        current_player_deadwood = self.get_deadwood_count(current_player_hand)
        opponent_player_deadwood = self.get_deadwood_count(opponent_player_hand)

        print(f"{self.get_current_player().name}'s hand: {current_player_hand}")
        print(f"{self.get_opponent_player().name}'s hand: {opponent_player_hand}")

        if current_player_deadwood == 0:
            self.scores[self.current_player_index] += opponent_player_deadwood + GIN_BONUS
            print(f"{self.get_current_player().name} has Gin! Score: {self.scores[self.current_player_index]}")
        elif opponent_player_deadwood < current_player_deadwood:
            self.scores[(self.current_player_index + 1) % 2] += current_player_deadwood + UNDERCUT_BONUS
            print(f"{self.get_opponent_player().name} undercut {self.get_current_player().name}! Score: {self.scores[(self.current_player_index + 1) % 2]}")
        else:
            self.scores[self.current_player_index] += opponent_player_deadwood
            print(f"{self.get_current_player().name} wins the round! Score: {self.scores[self.current_player_index]}")

        self.reset_round()

    def reset_round(self):
        """Reset the game state for a new round."""
        self.deck.reset_deck()
        self.discard_pile.clear()
        for player in self.players:
            player.hand.cards.clear()
        self.deal_initial_hands()

    def play_game(self):
        """Play the Gin Rummy game."""
        self.reset_round()

        while max(self.scores) < MAX_SCORE:
            current_player = self.get_current_player()
            print(f"\n{current_player.name}'s turn.")
            print(f"Discard pile top card: {self.discard_pile[-1] if self.discard_pile else 'None'}")

            action = input("Draw from deck (d) or discard pile (p)? ").lower()
            if action == 'd':
                drawn_card = self.draw_card(from_discard_pile=False)
            elif action == 'p' and self.discard_pile:
                drawn_card = self.draw_card(from_discard_pile=True)
            else:
                print("Invalid action. Skipping turn.")
                self.switch_turn()
                continue

            print(f"{current_player.name} drew {drawn_card}")
            print(f"{current_player.name}'s hand: {current_player.hand}")

            discard_action = input("Discard a card (enter the card value, e.g., 'Ah' for Ace of Hearts): ").strip()
            try:
                discard_card = Card(rank=discard_action[0], suit=discard_action[1].capitalize())
                if discard_card not in current_player.hand:
                    print("Invalid card. You do not have that card in your hand.")
                    continue
                self.discard_card(discard_card)
            except (IndexError, ValueError):
                print("Invalid card format. Skipping turn.")
                self.switch_turn()
                continue

            print(f"{current_player.name} discarded {discard_card}")

            knock_action = input("Knock (k) or pass (p)? ").lower()
            if knock_action == 'k':
                self.knock()
            else:
                self.switch_turn()

        winner = self.players[self.scores.index(max(self.scores))]
        print(f"\n{winner.name} wins the game with a score of {max(self.scores)}!")


if __name__ == "__main__":
    engine = GinRummyEngine()
    engine.play_game()

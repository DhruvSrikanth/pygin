from typing import List, Tuple
from itertools import combinations, groupby
from copy import deepcopy
from card import Card
from hand import Hand
from constants import RANKS


def mark_deadwood(hand: Hand) -> Hand:
    """Mark the deadwood cards in a given hand."""
    hand_copy = deepcopy(hand)
    arrangements = generate_arrangements(hand_copy)
    min_deadwood_arrangement = min(arrangements, key=lambda x: len(x[2]))
    for card in hand_copy: card.is_deadwood = card in min_deadwood_arrangement[2]
    return hand_copy


def generate_arrangements(hand: Hand) -> List[Tuple[List[Card], List[Card], List[Card]]]:
    """Generate all possible arrangements of sets and runs for the given hand."""
    arrangements = []
    generate_arrangements_helper(hand, [], [], [], arrangements)
    return arrangements


def generate_arrangements_helper(hand: Hand, sets: List[Card], runs: List[Card], deadwood: List[Card], arrangements: List[Tuple[List[Card], List[Card], List[Card]]]):
    """Recursive helper function to generate all possible arrangements."""
    if not hand:
        arrangements.append((sets[:], runs[:], deadwood[:]))
        return

    # Try adding the current card to existing sets
    for i, set_cards in enumerate(sets):
        if len(set_cards) < 4 and hand[0].rank == set_cards[0].rank:
            sets[i].append(hand[0])
            generate_arrangements_helper(hand[1:], sets, runs, deadwood, arrangements)
            sets[i].pop()

    # Try adding the current card to existing runs
    for i, run_cards in enumerate(runs):
        if can_extend_run(run_cards, hand[0]):
            runs[i].append(hand[0])
            generate_arrangements_helper(hand[1:], sets, runs, deadwood, arrangements)
            runs[i].pop()

    # Try creating a new set with the current card
    for size in range(3, 5):
        for new_set in combinations(hand, size):
            if all(card.rank == new_set[0].rank for card in new_set):
                sets.append(list(new_set))
                generate_arrangements_helper(
                    [card for card in hand if card not in new_set],
                    sets, runs, deadwood, arrangements
                )
                sets.pop()

    # Try creating a new run with the current card
    sorted_hand = sorted(hand, key=lambda card: (card.suit, card.rank))
    for _, group in groupby(sorted_hand, key=lambda card: card.suit):
        group_list = list(group)
        for start in range(len(group_list)):
            for end in range(start + 2, len(group_list) + 1):
                run = group_list[start:end]
                if is_valid_run(run):
                    runs.append(run)
                    generate_arrangements_helper(
                        [card for card in hand if card not in run],
                        sets, runs, deadwood, arrangements
                    )
                    runs.pop()

    # If the current card cannot be added to any set or run, add it to deadwood
    deadwood.append(hand[0])
    generate_arrangements_helper(hand[1:], sets, runs, deadwood, arrangements)
    deadwood.pop()


def can_extend_run(run: List[Card], card: Card) -> bool:
    """Check if a card can be added to an existing run."""
    if not run:
        return True
    prev_card = run[-1]
    prev_rank_index = RANKS.index(prev_card.rank)
    card_rank_index = RANKS.index(card.rank)
    return (
        card.suit == prev_card.suit
        and (
            card_rank_index == prev_rank_index + 1
            or card_rank_index == 0 and prev_rank_index == len(RANKS) - 1
            or card_rank_index == prev_rank_index - len(run)
        )
    )


def is_valid_run(run: List[Card]) -> bool:
    """Check if a list of cards forms a valid run."""
    ranks = [card.rank for card in run]
    suits = [card.suit for card in run]
    return len(set(suits)) == 1 and len(set(ranks)) == len(run) and ranks == list(RANKS[RANKS.index(ranks[0]):RANKS.index(ranks[0]) + len(run)])

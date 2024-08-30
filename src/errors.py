class EmptyDeckError(Exception):
    """Exception raised when attempting to draw a card from an empty deck."""
    def __init__(self, message="The deck is empty. Cannot draw a card."):
        self.message = message
        super().__init__(self.message)


class CardDoesNotExistError(Exception):
    """Exception raised when attempting to remove a card from a hand that doesn't exist."""
    def __init__(self, message="The card does not exist in the hand."):
        self.message = message
        super().__init__(self.message)

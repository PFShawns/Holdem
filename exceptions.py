class PokerError(Exception):    """Generic poker error"""class CardError(PokerError):    """Card-related error"""class HandError(PokerError):    """Hand-related error"""class DeckError(PokerError):    """Deck-related error"""class CardCreationError(CardError):    """Attempt to create a Card object using invalid arguments"""class CardArithmeticError(CardError):    """Invalid arithmetic operation on a Card object"""class CardComparisonError(CardError):    """Invalid comparison of a Card object"""class HandCreationError(HandError):    """Attempt to create a Hand object using invalid arguments"""class HandComparisonError(HandError):    """Invalid comparison of a Hand object"""class DeckNotIntegerError(DeckError):    """Given draw count is not an integer"""class DeckTooManyError(DeckError):    """Given draw count is greater than the count of remaining cards"""
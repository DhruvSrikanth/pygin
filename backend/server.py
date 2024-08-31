from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from pygin import GinRummyEngine
import uvicorn

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Global game instance
game: Optional[GinRummyEngine] = None


class CardModel(BaseModel):
    rank: str
    suit: str


class PlayerModel(BaseModel):
    name: str
    hand: List[CardModel]


class GameStateModel(BaseModel):
    players: List[PlayerModel]
    scores: List[int]
    rounds_won: List[int]
    current_player_index: int
    deck_size: int
    discard_stack: List[CardModel]
    game_over: bool
    can_knock: bool


@app.post("/api/initialize_game", response_model=GameStateModel)
async def initialize_game():
    global game
    game = GinRummyEngine("Player 1", "Player 2")
    game.deal_initial_hands()
    return get_game_state()


@app.post("/api/draw_card", response_model=GameStateModel)
async def draw_card(from_discard: bool):
    if game is None:
        raise HTTPException(status_code=400, detail="Game not initialized")
    game.draw_card(from_discard)
    return get_game_state()


@app.post("/api/discard_card", response_model=GameStateModel)
async def discard_card(card: CardModel):
    if game is None:
        raise HTTPException(status_code=400, detail="Game not initialized")
    discard_card = Card(rank=card.rank, suit=card.suit)
    game.discard_card(discard_card)
    return get_game_state()


@app.post("/api/knock", response_model=GameStateModel)
async def knock():
    if game is None:
        raise HTTPException(status_code=400, detail="Game not initialized")
    game.knock()
    return get_game_state()


def get_game_state() -> GameStateModel:
    if game is None:
        raise HTTPException(status_code=400, detail="Game not initialized")
    return GameStateModel(
        players=[
            PlayerModel(name=player.name, hand=[CardModel(rank=card.rank, suit=card.suit) for card in player.get_hand()])
            for player in game.players
        ],
        scores=game.scores,
        rounds_won=game.rounds_won,
        current_player_index=game.get_current_player_idx(),
        deck_size=len(game.deck.cards),
        discard_stack=[CardModel(rank=card.rank, suit=card.suit) for card in game.discard_stack],
        game_over=max(game.scores) >= 100,
        can_knock=game.can_knock()
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
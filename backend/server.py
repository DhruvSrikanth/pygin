from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from pygin import GinRummyEngine, Card
import uvicorn
from .utils import load_config

# Load configuration
config = load_config('config.yaml')

# Initialize FastAPI app
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


class HandModel(BaseModel):
    cards: List[CardModel]


class PlayerModel(BaseModel):
    name: str
    hand: HandModel


@app.post("/start_game")
def start_game(player1_name: str, player2_name: str):
    if player1_name == player2_name:
        raise HTTPException(status_code=400, detail="Player names must be different")

    global game
    game = GinRummyEngine(player1=player1_name, player2=player2_name)
    game.deal_initial_hands()
    return {"message": "Game started successfully"}


@app.get("/get_player_hand")
def get_player_hand(player_name: str):
    if not game:
        raise HTTPException(status_code=400, detail="Game not started")

    player = game.get_player(player_name)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    hand = player.get_hand()
    cards = list(map(lambda c: c.to_dict(), hand))
    return {"hand": cards}


@app.post("/draw_card")
def draw_card(from_discard_stack: bool):
    if not game:
        raise HTTPException(status_code=400, detail="Game not started")

    card = game.draw_card(from_discard_stack=from_discard_stack)
    return {"card": card.to_dict()}


@app.post("/discard_card")
def discard_card(card: CardModel):
    if not game:
        raise HTTPException(status_code=400, detail="Game not started")

    game.discard_card(Card(card.rank, card.suit))
    return {"message": "Card discarded successfully"}


@app.post("/knock")
def knock():
    if not game:
        raise HTTPException(status_code=400, detail="Game not started")

    if not game.can_knock():
        raise HTTPException(status_code=400, detail="Cannot knock")

    game.knock()
    return {"message": "Player knocked successfully"}


@app.post("/reset_game")
def reset_game():
    global game
    game = None
    return {"message": "Game reset successfully"}


@app.get("/reset_round")
def reset_round():
    game.reset_round()
    return {"message": "Round reset successfully"}


@app.get("/get_game_state")
def get_game_state(player_name: str):
    if not game:
        raise HTTPException(status_code=400, detail="Game not started")

    player = game.get_player(player_name)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    player_hand = player.get_hand()
    opponent_hand_size = len(game.get_opponent_player().get_hand())
    discard_pile_top = game.discard_stack[-1].to_dict() if game.discard_stack else None
    deck_size = len(game.deck)
    can_knock = game.can_knock()
    is_gin, gin_score = game.is_gin()
    is_big_gin, big_gin_score = game.is_big_gin()

    return {
        "player_hand": list(map(lambda c: c.to_dict(), player_hand)),
        "opponent_hand_size": opponent_hand_size,
        "discard_pile_top": discard_pile_top,
        "deck_size": deck_size,
        "is_current_player": player_name == game.get_current_player().name,
        "can_knock": can_knock,
        "is_gin": is_gin,
        "gin_score": gin_score,
        "is_big_gin": is_big_gin,
        "big_gin_score": big_gin_score,
    }


if __name__ == "__main__":
    uvicorn.run(
        app,
        host=config.get('host', '0.0.0.0'),
        port=config.get('port', 8000),
    )

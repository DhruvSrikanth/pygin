import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Card, Deck } from 'react-playing-cards';

function PlayerView({ playerName }) {
  const [gameState, setGameState] = useState(null);

  useEffect(() => {
    const fetchGameState = async () => {
      try {
        const response = await axios.get(`/get_game_state?player_name=${playerName}`);
        setGameState(response.data);
      } catch (error) {
        console.error('Error fetching game state:', error);
      }
    };

    fetchGameState();
  }, [playerName]);

  if (!gameState) {
    return <div>Loading...</div>;
  }

  const {
    player_hand,
    opponent_hand_size,
    discard_pile_top,
    deck_size,
    is_current_player,
    can_knock,
    is_gin,
    gin_score,
    is_big_gin,
    big_gin_score,
  } = gameState;

  const handleDrawCard = async (fromDiscardPile) => {
    try {
      const response = await axios.post('/draw_card', { from_discard_stack: fromDiscardPile });
      // Update the game state with the response data
      setGameState(response.data);
    } catch (error) {
      console.error('Error drawing card:', error);
    }
  };

  const handleDiscardCard = async (card) => {
    try {
      await axios.post('/discard_card', card);
      // Update game state after discarding the card
    } catch (error) {
      console.error('Error discarding card:', error);
    }
  };

  const handleKnock = async () => {
    try {
      await axios.post('/knock');
      // Update game state after knocking
    } catch (error) {
      console.error('Error knocking:', error);
    }
  };

  return (
    <div>
      <h2>Your Hand</h2>
      <div>
        {player_hand.map((card) => (
          <Card
            key={`${card.rank}${card.suit}`}
            rank={card.rank}
            suit={card.suit.toLowerCase()}
            draggable
            onDragStart={() => handleDiscardCard(card)}
          />
        ))}
      </div>
      <h2>Opponent's Hand</h2>
      <div>
        <Deck count={opponent_hand_size} />
      </div>
      <h2>Discard Pile</h2>
      <div
        draggable
        onDragStart={() => handleDrawCard(true)}
      >
        {discard_pile_top ? (
          <Card
            rank={discard_pile_top.rank}
            suit={discard_pile_top.suit.toLowerCase()}
          />
        ) : (
          'Empty'
        )}
      </div>
      <h2>Deck</h2>
      <div
        draggable
        onDragStart={() => handleDrawCard(false)}
      >
        <Deck count={deck_size} />
      </div>
      {is_current_player && (
        <>
          {can_knock && <button onClick={handleKnock}>Knock</button>}
          {is_gin && <button>Gin ({gin_score} points)</button>}
          {is_big_gin && <button>Big Gin ({big_gin_score} points)</button>}
        </>
      )}
    </div>
  );
}

export default PlayerView;
import React, { useState } from 'react';
import PlayerView from './PlayerView';

function GameBoard({ playerNames }) {
  const [currentPlayer, setCurrentPlayer] = useState(playerNames[0]);

  const handlePlayerChange = () => {
    setCurrentPlayer(currentPlayer === playerNames[0] ? playerNames[1] : playerNames[0]);
  };

  return (
    <div>
      <h2>Game Board</h2>
      <PlayerView playerName={currentPlayer} />
      <button onClick={handlePlayerChange}>Switch Player View</button>
    </div>
  );
}

export default GameBoard;
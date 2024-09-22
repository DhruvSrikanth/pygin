import React, { useState } from 'react';

function GameSetup({ onStartGame }) {
  const [player1, setPlayer1] = useState('');
  const [player2, setPlayer2] = useState('');

  const handleStartGame = () => {
    if (player1 && player2 && player1 !== player2) {
      onStartGame(player1, player2);
    } else {
      alert('Please enter different names for both players.');
    }
  };

  return (
    <div>
      <h2>Game Setup</h2>
      <input
        type="text"
        placeholder="Player 1 Name"
        value={player1}
        onChange={(e) => setPlayer1(e.target.value)}
      />
      <input
        type="text"
        placeholder="Player 2 Name"
        value={player2}
        onChange={(e) => setPlayer2(e.target.value)}
      />
      <button onClick={handleStartGame}>Start Game</button>
    </div>
  );
}

export default GameSetup;
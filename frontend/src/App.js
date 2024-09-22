import React, { useState } from 'react';
import GameSetup from './components/GameSetup';
import GameBoard from './components/GameBoard';

function App() {
  const [gameStarted, setGameStarted] = useState(false);
  const [playerNames, setPlayerNames] = useState(['', '']);

  const startGame = (player1, player2) => {
    setPlayerNames([player1, player2]);
    setGameStarted(true);
  };

  return (
    <div>
      {!gameStarted ? (
        <GameSetup onStartGame={startGame} />
      ) : (
        <GameBoard playerNames={playerNames} />
      )}
    </div>
  );
}

export default App;
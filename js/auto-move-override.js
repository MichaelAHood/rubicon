// Modify and override these functions to aid you in defeating Caesar.

// Called by Rubicon when a player moves.
// PlayerMoved can be overridden.
function PlayerMoved(playerId, nodeId, movesRemaining) {
    window.RequestGameState();
    move = `Player ${playerId} has moved: ${nodeId}. Remaining: ${movesRemaining}`;
    console.log(move);
  }
  
// Called by Rubicon when Game State is requested
// ReceiveGameState can be overridden.
function ReceiveGameState(gameState) {
    window.localStorage.setItem("game-state", String(gameState));
}

// Called by Rubicon when Board State is requested
// ReceiveBoardState can be overridden.
function ReceiveBoardState(boardState) {
    boardJSON = JSON.parse(boardState);
    window.localStorage.setItem("board-state", JSON.stringify(boardJSON));
}

// Call this to execute a move
// window.DoMoveExternal(12)
function DoMoveExternal(tileId) {
    gameInstance.SendMessage("Public", "DoMoveExternal", tileId);
}

// Call this to request the Board State
// window.RequestBoardState()
function RequestBoardState() {
    gameInstance.SendMessage("Public", "RequestBoardState");
}

// Call this to request the Game State
// window.RequestBoardState()
function RequestGameState() {
    gameInstance.SendMessage("Public", "RequestGameState");
}

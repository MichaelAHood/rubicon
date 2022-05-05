import json


def get_js_helpers():
    return {
    "player_moved_function": """
        function PlayerMoved(playerId, nodeId, movesRemaining) {
            window.RequestGameState();
            move = `Player ${playerId} has moved: ${nodeId}. Remaining: ${movesRemaining}`;
            console.log(move);
        };
    """,
    "receive_game_state_function": """
        function ReceiveGameState(gameState) {
            console.log("game state");
            window.localStorage.setItem("game-state", String(gameState));
            console.log(gameState);
        };
    """,
    "play_game_template": """   
        moves = $moves;
        window.RequestGameState();
        gameStateString = window.localStorage.getItem("game-state");
        gameState = JSON.parse(gameStateString.replace("True", "true"));
        if (gameState.turn === 2) {
            moveIx = window.localStorage.getItem("move-count");
            if (!moveIx) {
                moveIx = 0;
            }
            // Execute the desired move
            window.DoMoveExternal(moves[moveIx]);
            moveIx++;
            // Update the move count for the next turn
            window.localStorage.setItem("move-count", moveIx);
        };
    """,
}


def sanitize_json(s):
    return s.replace("True", "true").replace("False", "false")


def get_game_state(storage):
    game_state_string = storage.get("game-state")
    if game_state_string:
        return json.loads(sanitize_json(game_state_string))
    else:
        return False

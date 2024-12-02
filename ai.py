# Every piece assigned a value
PIECE_VALUES = {
    "pawn": 1,
    "knight": 3,
    "bishop": 3,
    "rook": 5,
    "queen": 9,
    "king": 0  
}

# Evaluate board and return a score
def evaluate_board(board, ai_color):
    # Store score
    score = 0
    # Traverse chess game board
    for _, piece in board.items():
        piece_color, piece_type = piece.split("_")
        value = PIECE_VALUES[piece_type]
        # Update score
        if piece_color == ai_color:
            score += value
        else:
            score -= value
    # Return the score
    return score

# Simple minimax algorithm for AI 
def minimax(board, depth, is_maximizing, ai_color, movement, alpha=-float('inf'), beta=float('inf')):
    # Run till base case reached and return the score
    if depth == 0:
        return evaluate_board(board, ai_color)

    # Enemy color and initial score
    enemy = "white" if ai_color == "black" else "black"
    best_score = -float('inf') if is_maximizing else float('inf')

    # Traverse chess game board
    for position, piece in list(board.items()): 
        piece_color, piece_type = piece.split("_")
        if piece_color != (ai_color if is_maximizing else enemy):
            continue
        # Get x, y pos and move
        x, y = ord(position[0]) - ord('a'), 8 - int(position[1])
        moves = getattr(movement, f"{piece_type}Movement")(x, y, board)
        # Traverse moves
        for move in moves:
            # get pos and update board
            new_pos = f"{chr(move[0] + ord('a'))}{8 - move[1]}"
            captured_piece = board.pop(new_pos, None)
            board[new_pos] = piece
            del board[position]

            # DO recursive call till base case reached
            score = minimax(board, depth - 1, not is_maximizing, ai_color, movement, alpha, beta)

            # Undo the move as to not affect actual board
            board[position] = piece
            if captured_piece:
                board[new_pos] = captured_piece
            else:
                del board[new_pos]
            # Update scores and alpha and beta values
            if is_maximizing:
                best_score = max(best_score, score)
                alpha = max(alpha, best_score)
            else:
                best_score = min(best_score, score)
                beta = min(beta, best_score)
            # If condition reached then prune branch
            if beta <= alpha:
                break 
    # Return the best score
    return best_score

# For AI to make a move based on best score
def ai_move(board, movement, depth=2):
    # Set up AI
    ai_color = "black"
    best_score = -float('inf')
    best_move = None

    # Traverse the chess game board
    for position, piece in list(board.items()):
        piece_color, piece_type = piece.split("_")
        if piece_color != ai_color:
            continue
        # Get x, y pos and move
        x, y = ord(position[0]) - ord('a'), 8 - int(position[1])
        moves = getattr(movement, f"{piece_type}Movement")(x, y, board)
        # Traverse moves
        for move in moves:
            # get pos and update board
            new_pos = f"{chr(move[0] + ord('a'))}{8 - move[1]}"
            captured_piece = board.pop(new_pos, None)
            board[new_pos] = piece
            del board[position]

            # Call to get score
            score = minimax(board, depth=depth, is_maximizing=False, ai_color=ai_color, movement=movement)

            # Undo the move made
            board[position] = piece
            if captured_piece:
                board[new_pos] = captured_piece
            else:
                del board[new_pos]

            # Update best score and move for that score
            if score > best_score:
                best_score = score
                best_move = (position, new_pos)
    # Check if move has value
    if best_move:
        # Get the pos and update the board based on the AI move
        start, end = best_move
        board[end] = board[start]
        del board[start]
        print(f"AI moved {board[end]} from {start} to {end}")

# Object for calculating the piece movements within the game board.
# Works for both Humna player = white and AI player = black
# Will be used in chessMain.py for geting new valid positions.
class Movement:
    # Constructor for Movement
    # Takes color type white or black to determine who is currently looking for a move.
    def __init__(self, color):
        # Set the object to work for either white or black player
        self.color = color
        # If black pawn moves down else if white pawn moves up. Determines direction to go
        self.direction = -1 if color == "white" else 1 

    # Calculate the valid moves the king can make based on current position on the board.
    # Take x pos, y pos and game stae board
    # Return the valid moves of king piece
    def kingMovement(self, x, y, board):
        # Store valid moves king could do
        moves = []
        # direction of x, direction of y, Traverse through the possible ways KING can move (valid movement of a KING)
        for dirx, diry in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            # Increment x pos and y pos
            nextX, nextY = x + dirx, y + diry
            # Check if new positions is within the boards of the game chess board
            if 0 <= nextX < 8 and 0 <= nextY < 8: 
                # Get new position
                new_pos = f"{chr(nextX + ord('a'))}{8 - nextY}"
                # Add move if position to move to is empty or if there is an enemy piece in that position
                if new_pos not in board or board[new_pos].startswith("white" if self.color == "black" else "black"):
                    moves.append((nextX, nextY))
        # Return the valid moves the KING could take from his current position
        return moves
    # Calculate the ROOK movement in the game chess board
    # Take current x,y and game state board
    # Return the valid moves rook can take 
    def rookMovement(self, x, y, board):
        # Store valid moves rook can take
        moves = []
        # Direction x,y travering thorugh valid rook possible direction movements
        for dirX, dirY in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            # Store
            nextX, nextY = x, y
            # Run til get all moves if any else break
            while True:
                # Update x and y
                nextX += dirX
                nextY += dirY
                # Check if next pos is within boards of the game chess board
                if 0 <= nextX < 8 and 0 <= nextY < 8:  
                    # Get the position
                    new_pos = f"{chr(nextX + ord('a'))}{8 - nextY}"
                    # Check if already on board
                    if new_pos in board:
                        # Check piece type and add
                        if board[new_pos].startswith("white" if self.color == "black" else "black"):
                            moves.append((nextX, nextY)) 
                        # Made a move break
                        break 
                    # The space is empty, no piece so add
                    else:
                        moves.append((nextX, nextY)) 
                # Pos out of bounds break
                else:
                    break 
        # Return the valid moves the rook can do from his current position
        return moves
    # Calculate the bishop movement in the chess game board
    # Take x,y pos and game board
    # Return the valid moves the bishop can take
    def bishopMovement(self, x, y, board):
        # Valid moves bishop could take
        moves = []
        # Direction x,y traversing possible directions bishop could take
        for dirX, dirY in [(1, 1), (-1, -1), (1, -1), (-1, 1)]:
            # Update next pos
            nextX, nextY = x, y
            # Run till break which is out of bounds and no moves
            while True:
                # Update the next pos
                nextX += dirX
                nextY += dirY
                # Check if wihtin bounds of the chess game board
                if 0 <= nextX < 8 and 0 <= nextY < 8: 
                    # Get pos
                    new_pos = f"{chr(nextX + ord('a'))}{8 - nextY}"
                    # Check if square filled (frien or enemy)
                    if new_pos in board: 
                        # ADD move to valid moves
                        if board[new_pos].startswith("white" if self.color == "black" else "black"):
                            moves.append((nextX, nextY))
                        # Stop friend piece
                        break 
                    # Board empty add piece pos
                    else:
                        moves.append((nextX, nextY))
                # Piece pos out of bounds
                else:
                    break  
        # Return valid moves the bishop could make from his current positon in the chess game board
        return moves
    # Calculate the queen movement
    # Basically rook movement and bishop movement
    # Take x,y, game board
    # Return valid moves of queen
    def queenMovement(self, x, y, board):
        # Return valid moves of rook and bishop
        return self.rookMovement(x, y, board) + self.bishopMovement(x, y, board)

    # Calculate knight movement 
    # Take x,y game state board
    # Return the valid moves knight could take from position within the board
    def knightMovement(self, x, y, board):
        # Valid moves knight could take
        moves = []
        # Direction x,y traversing possible directions knight could take
        for dirX, dirY in [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]:
            # Update next pos
            nextX, nextY = x + dirX, y + dirY
            # Check if pos within the bounds of chess game board
            if 0 <= nextX < 8 and 0 <= nextY < 8: 
                # Get pos
                new_pos = f"{chr(nextX + ord('a'))}{8 - nextY}"
                # Add valid move
                if new_pos not in board or board[new_pos].startswith("white" if self.color == "black" else "black"):
                    moves.append((nextX, nextY))
        # Return valid moves knight could take from current position within the chess game board
        return moves
    
    # Calculate the pawn movement 
    # Take x,y and game state board
    # Return the valid moves pawn could take
    def pawnMovement(self, x, y, board):
        # Store valid moves of pawn
        moves = []
        start_row = 6 if self.color == "white" else 1  # Starting row for double move

        # Pawn movement, moving forawrd
        forward_one = (x, y + self.direction)
        # Check if within bounds of the game chess board
        if 0 <= forward_one[1] < 8: 
            # Get pos
            forward_one_pos = f"{chr(forward_one[0] + ord('a'))}{8 - forward_one[1]}"
            # Check if pos empty no piece, then add move
            if forward_one_pos not in board: 
                moves.append(forward_one)

                # Check if pawn is at starting row if so then pawn can move 2 spces forward
                if y == start_row:
                    # Update pos
                    forward_two = (x, y + 2 * self.direction)
                    forward_two_pos = f"{chr(forward_two[0] + ord('a'))}{8 - forward_two[1]}"
                    # Check if pos is empty, then add
                    if forward_two_pos not in board: 
                        moves.append(forward_two)

        # Pawn can only move diagnol if captuing a piece, so we have to check
        # Direction x, travering possible direction left, right
        for dx in [-1, 1]: 
            # Get capture
            capture = (x + dx, y + self.direction)
            # Check if within chess game board
            if 0 <= capture[0] < 8 and 0 <= capture[1] < 8: 
                # Get pos
                capture_pos = f"{chr(capture[0] + ord('a'))}{8 - capture[1]}"
                # Check if board filled to capture and if enemy add valid move
                if capture_pos in board and board[capture_pos].startswith("white" if self.color == "black" else "black"):
                    moves.append(capture)
        # Return valid moves pawn could take from current positon within chess game board
        return moves
    
    # For AI use only when calculating for potential places to move
    # Mapp piece type of their respective movement
    # Take x,y game state board
    # Return valid move function else emtpy list
    def piece_moves(self, piece, x,y, board):
        # Dictionary mapping of piece to their movement
        pieceMoveType = {
            "king": self.kingMovement,
            "rook": self.rookMovement,
            "bishop": self.bishopMovement,
            "queen": self.queenMovement,
            "knight": self.knightMovement,
            "pawn": self.pawnMovement,
        }
        # Get piece type
        piece_type = piece.split("_")[1]
        # Get move function based on piece type
        move_function = pieceMoveType.get(piece_type)
        # Check if we have a valid move fucntion, if so return it
        if move_function:
            return move_function(x, y, board)
        # Else return empty list
        else:
            return [] 
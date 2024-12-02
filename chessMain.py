import pygame
from movement import Movement
from ai import ai_move

pygame.init()            # Initialize Pygame

WIDTH, HEIGHT = 800,800  # Set up the screen dimensions
SQUARE_SIZE= WIDTH//8    # Set up the Square sizes

LIGHT_COLOR = (240,217,181) # Light brown for chess board
DARK_COLOR = (181,136,99)   # Dark brown for chess board
SELECTED_COLOR  = (0,255,0) # Green highlighted for chess board

# Initialize screen
screen = pygame.display.set_mode((WIDTH,HEIGHT)) 
pygame.display.set_caption("Chess Board")

'''
Load and resize the chess pieces from folder Chess_Pieces to play game
and setup their starting positions on the chess board
and return the chess piece images and the chess piece starting positions
'''
def configure_chess_pieces():

    # Will store the images of the chess pieces
    chess_pieces = {}
    # Go through piece colors that a chess board piece has
    for color in ['white','black']:
        # Go though every pieces that is in a chess board
        for piece in ['pawn','rook','knight','bishop','queen','king']:
            # Store the specified chess piece
            img = f"{piece}-{color}"
            # Load in the specified chess piece
            chess_pieces[f"{color}_{piece}"] = pygame.image.load(f"Chess_Pieces/{img}.png")
    # Go Through the loaded chess pieces and resize them for chess board to fit in pygame
    for key in chess_pieces:
        chess_pieces[key] = pygame.transform.scale(chess_pieces[key],(SQUARE_SIZE, SQUARE_SIZE) )
    
    # Initial the piece positions on the chess board, this is the starting positons of pieces always the same every start of a new game
    initial_piece_pos = {
        "a2": "white_pawn", "b2": "white_pawn", "c2": "white_pawn", "d2": "white_pawn",
        "e2": "white_pawn", "f2": "white_pawn", "g2": "white_pawn", "h2": "white_pawn",
        "a7": "black_pawn", "b7": "black_pawn", "c7": "black_pawn", "d7": "black_pawn",
        "e7": "black_pawn", "f7": "black_pawn", "g7": "black_pawn", "h7": "black_pawn",
        "a1": "white_rook", "h1": "white_rook", "a8": "black_rook", "h8": "black_rook",
        "b1": "white_knight", "g1": "white_knight", "b8": "black_knight", "g8": "black_knight",
        "c1": "white_bishop", "f1": "white_bishop", "c8": "black_bishop", "f8": "black_bishop",
        "d1": "white_queen", "e1": "white_king", "d8": "black_queen", "e8": "black_king"
    }

    # Return the chess pieces and the chess piece initial stating positions
    return chess_pieces, initial_piece_pos

'''
Draw the chess pieces positions on the chess board
Take chess pieces and postion to draw on chess game board
'''
def draw_pieces(chess_pieces, pos):
    # Run through the pieces and their positions witin the chess game board
    for pos, piece in pos.items():
        # Calculate the column index (0 to 7) by converting the file letter to a number.
        # 'ord(pos[0])' gets the ASCII value of the file letter (e.g., 'a' to 'h').
        # Subtract 'ord('a')' to normalize 'a' to 0.
        col = ord(pos[0]) - ord('a')
        # Calculate the row index (0 to 7) by converting the rank number.
        # 'int(pos[1])' converts the rank character to an integer.
        # Subtract from 8 to invert the row index since the top row is 0 in the display.
        row = 8 - int(pos[1])
        # Get image piece
        img = chess_pieces[piece]
        # Draw the image piece on the board in correct position within the chess game board
        screen.blit(img, (col*SQUARE_SIZE, row*SQUARE_SIZE))

'''
Draw the chess board 8 rows, 8 columns is a chess board.
Using the light and dark brown color the chess board 
# Take optional selected squre for highlight what you selected
'''
def draw_board(selected_square=None):
    # Hard coded traverse 8 rows, 8 columns of board
    for row in range(8):
        for col in range(8):
            # Determine color of square (light or dark brown)
            color = LIGHT_COLOR if (row+col) % 2 == 0 else DARK_COLOR
            # Draw the square on the game chess board
            rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(screen, color, rect)
            # Check if opotinal parameter passed, if so piece selected so if at the position highlight the square GREEN
            if selected_square == (col, row):
                pygame.draw.rect(screen, SELECTED_COLOR, rect, 5)
                
'''
Get the specified square box 
'''
def getSQUARE():
    x,y = pygame.mouse.get_pos()
    col = x //SQUARE_SIZE
    row = y // SQUARE_SIZE
    return col, row


'''
Main program, Calls everything
'''
def main():
    # Stoed chess pieces to access globally
    global chess_pieces
    # Configure teh chess game board
    chess_pieces, initial_piece_pos = configure_chess_pieces()
    # Initialize the white and black players
    player = Movement("white")
    aiPlayer = Movement("black")
    # For running game till end
    running = True
    # For highlighing square and moving to new positon on chess game board
    current_selected_square = None
    current_selected_piece = None
    valid_moves = []
    # player one == Human player, player 2 === AI player
    is_turn = True  

    # Runn till terminal
    while running:
        # If exit clicked exit game, set running to false
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # If clicked within chess game board
            elif event.type == pygame.MOUSEBUTTONDOWN and is_turn:
                # Get postion of the square that was clicked and store the column and row positions
                col, row = getSQUARE()
                clickedSquare = (col, row)

                # Check if piece was selected and if so move it if valid moves
                if current_selected_piece:
                    if clickedSquare in valid_moves:
                        # Get the previuous square and new square pos
                        prev_square = f"{chr(current_selected_square[0] + ord('a'))}{8 - current_selected_square[1]}"
                        new_square = f"{chr(clickedSquare[0] + ord('a'))}{8 - clickedSquare[1]}"
                     
                        # Update the board and delete old pos
                        initial_piece_pos[new_square] = current_selected_piece
                        del initial_piece_pos[prev_square]
                        # Print in terminal what is going on for debugging purposes
                        print(f"Moved {current_selected_piece} from {prev_square} to {new_square}")

                        # Now human has finished a move so reset to allow for AI to make a move
                        # is turn is set to false for AI 
                        current_selected_piece = None
                        current_selected_square = None
                        valid_moves = []
                        is_turn = False  
                    # No valid move reset to try again, do not want to freeze if selected a piece
                    else:
                        print("Invalid move. Try again.")
                        current_selected_piece = None
                        current_selected_square = None
                        valid_moves = []
                # If no piece selected select one
                else:
                    # Traverse pos, piece to select a piece within the chess game board
                    for pos, piece in initial_piece_pos.items():
                        # Get column and row pos
                        col_piece = ord(pos[0]) - ord('a')
                        row_piece = 8 - int(pos[1])
                        # Check if square was clicked on for that pos and we can only move white pieces since we are human
                        if clickedSquare == (col_piece, row_piece) and piece.startswith("white"):
                            # Get pice and sqaure
                            current_selected_piece = piece
                            current_selected_square = clickedSquare
                            # Get move and exit
                            valid_moves = getattr(player, f"{piece.split('_')[1]}Movement")(col_piece, row_piece, initial_piece_pos)
                            print(f"Selected {piece} at {pos}. Valid moves: {valid_moves}")
                            break
        # AI turn to make a move
        if not is_turn:
            print("AI turn to make a move")
            ai_move(initial_piece_pos, aiPlayer)
            is_turn = True  
         # Check if either king is missing
        if "white_king" not in initial_piece_pos.values():
            print("Black wins! White's king has been captured.")
            running = False
        elif "black_king" not in initial_piece_pos.values():
            print("White wins! Black's king has been captured.")
            running = False

        # Draw the game board, pieces within the chess game board and the balck captured pieces
        draw_board(current_selected_square)
        draw_pieces(chess_pieces, initial_piece_pos)
        # draw_black_captured_pieces(black_captured_pieces, 10, HEIGHT + 10)

        # Highlight valid moves that human player selected within the chess game board
        for move in valid_moves:
            pygame.draw.rect(screen, SELECTED_COLOR, (move[0] * SQUARE_SIZE, move[1] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)

        pygame.display.flip()

    pygame.quit()


# Run the chess game board
if __name__ == "__main__":
    main()
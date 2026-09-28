# AI Chess (first version)

My first chess AI: a pygame chessboard where you play White against a computer opponent that uses minimax search with alpha-beta pruning. Built in fall 2024.

> **There's a newer, complete version:** [**AI-chess**](https://github.com/Afaguayo/AI-chess) plays by the full rules (check, checkmate, castling, en passant, promotion) with a much stronger search. This repo is kept as the starting point.

## Run it

```bash
pip install pygame
python3 chessMain.py
```

Click one of your pieces to select it (its legal moves print in the terminal), then click a square to move. The AI replies right away.

## How it works

| File | What it does |
|---|---|
| `chessMain.py` | The pygame window: draws the board and the pieces from [`Chess_Pieces/`](Chess_Pieces), handles clicks, and alternates turns with the AI. |
| `movement.py` | Move generation for each piece type: sliding rooks, bishops and queens; knight jumps; king steps; pawn pushes, double steps and diagonal captures. |
| `ai.py` | The opponent. `evaluate_board` counts material (pawn 1, knight/bishop 3, rook 5, queen 9). `minimax` searches 2 moves ahead with alpha-beta pruning, and `ai_move` plays the move with the best score. |

## Limitations

This version keeps the rules simple. There's no check or checkmate detection: the game ends when a king is **captured**. There's also no castling, en passant or promotion. Material-only scoring and a depth-2 search make the AI greedy: it grabs pieces but doesn't plan. All of this is fixed in [AI-chess](https://github.com/Afaguayo/AI-chess).

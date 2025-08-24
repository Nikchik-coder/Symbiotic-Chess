# Symbiotic Chess

A chess variant where you can merge your pieces to create powerful new units with combined abilities.

## The Core Concept

Symbiotic Chess builds upon the classic rules of chess, introducing "merge" and "disintegrate" actions that allow you to combine and split your pieces. This creates a dynamic battlefield where your army can adapt and evolve.

## New Rules and Mechanics

### 1. The "Merge" Action

On your turn, you can merge two of your own adjacent pieces. The first piece selected moves to the square of the second, which is removed from the board. The remaining piece becomes a "Combined Piece."

**Conditions for Merging:**
- The two pieces must be of different types.
- **The King and Queen cannot be merged.**
- Pawns can merge with any other valid piece.
- There is a limit of **three** merges per player per game.

### 2. The "Disintegrate" Action

You can use your turn to "disintegrate" a combined piece. The primary piece moves to an empty adjacent square, and the secondary piece re-emerges on the original square. This allows you to split your forces for tactical advantage.

### 3. Combined Pieces

A Combined Piece gains the movement capabilities of all its constituent parts.

**Standard Combined Pieces:**
- **Chancellor (Rook + Knight):** Moves as a Rook or a Knight.
- **Archbishop (Bishop + Knight):** Moves as a Bishop or a Knight.
- **Queen (Rook + Bishop):** A piece with the combined movement of a Rook and a Bishop is equivalent to a Queen.

**Advanced Combined Pieces:**
- **Grand Chancellor (Rook + Knight + Bishop):** A formidable piece that combines the powers of a Rook, Knight, and Bishop.
- **Archmagister (Bishop + Knight + Rook):** Another name for the Grand Chancellor, reflecting its mastery of the board.

*Note: The game will use 'G' to represent the Grand Chancellor/Archmagister.*

## How to Play

Run the `symbiotic_chess.py` file to start the game.

- **To move a piece:** Use algebraic notation (e.g., `e2e4`).
- **To merge pieces:** Type `merge [pos1] [pos2]` (e.g., `merge e1 d1`).
- **To disintegrate a piece:** Type `disintegrate [pos] [target_pos]` (e.g., `disintegrate c4 b5`).
- **To quit:** Type `quit`.
import copy
from colorama import Fore, Style, init
import os

# Function to clear the console screen - No longer needed for the API
# def clear_screen():
#     os.system('cls' if os.name == 'nt' else 'clear')

# Represents a single chess piece

SPECIAL_PIECE_INFO = {
    'G': {'name': 'Grand Chancellor', 'moves': 'as a Rook, Knight, and Bishop'},
    'M': {'name': 'Amazon', 'moves': 'as a Queen and a Knight'},
    'A': {'name': 'Archbishop', 'moves': 'as a Bishop and a Knight'},
    'C': {'name': 'Chancellor', 'moves': 'as a Rook and a Knight'},
    'Q': {'name': 'Queen', 'moves': 'as a Rook and a Bishop'}
}

class Piece:
    def __init__(self, piece_type, color):
        self.piece_type = piece_type
        self.color = color
        self.combined_pieces = []  # Stores types of merged pieces, e.g., ['R', 'N']

    def get_display_info(self):
        """Determines the piece's symbol for display, especially for merged pieces."""
        if self.is_combined():
            combined_set = set(self.combined_pieces)
            # Order of checks is important for pieces with multiple combinations
            if {'R', 'N', 'B'}.issubset(combined_set):
                return 'G', True  # Grand Chancellor / Archmagister
            if {'Q', 'N'}.issubset(combined_set):
                return 'M', True  # Amazon
            elif {'B', 'N'}.issubset(combined_set):
                return 'A', True  # Archbishop
            elif {'R', 'N'}.issubset(combined_set):
                return 'C', True  # Chancellor
            elif {'B', 'R'}.issubset(combined_set):
                return 'Q', True   # Queen
        return self.piece_type, False

    def __str__(self):
        # Unicode and custom characters for chess pieces
        symbols = {
            'P': '♙', 'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔',
            'p': '♟', 'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚',
            'A': 'A', 'C': 'C', 'M': 'M', 'G': 'G', # Archbishop, Chancellor, Amazon, Grand Chancellor
            'a': 'a', 'c': 'c', 'm': 'm', 'g': 'g'
        }

        display_type, is_special_combo = self.get_display_info()

        symbol_key = display_type.upper()
        if self.color == 'black':
            symbol_key = display_type.lower()
        
        symbol = symbols.get(symbol_key, '?')
        color_code = Fore.WHITE if self.color == 'white' else Fore.LIGHTBLACK_EX
        
        # For non-special combinations (e.g., Pawn+), show base piece with '+'
        if self.is_combined() and not is_special_combo:
            base_symbol_key = self.piece_type.upper()
            if self.color == 'black':
                base_symbol_key = self.piece_type.lower()
            base_symbol = symbols.get(base_symbol_key, '?')
            return f"{color_code}{base_symbol}+{Style.RESET_ALL}"
        
        # For regular pieces and special combinations
        return f"{color_code}{symbol} {Style.RESET_ALL}"

    def is_combined(self):
        return len(self.combined_pieces) > 0

# Manages the board and game logic
class SymbioticChessGame:
    def __init__(self):
        self.board = self.setup_board()
        self.current_turn = 'white'
        self.merge_count = {'white': 0, 'black': 0}
        self.max_merges = 3 # Setting a limit for merges per player
        self.last_move = None
        self.captured_pieces = {'white': [], 'black': []}
        self.status_message = ""
        self.last_merge_info = None
        init(autoreset=True)

    def setup_board(self):
        # Creates the initial board setup
        board = [[None for _ in range(8)] for _ in range(8)]
        
        # Place pieces
        for color in ['white', 'black']:
            row = 7 if color == 'white' else 0
            pawn_row = 6 if color == 'white' else 1
            
            board[row][0] = Piece('R', color)
            board[row][1] = Piece('N', color)
            board[row][2] = Piece('B', color)
            board[row][3] = Piece('Q', color)
            board[row][4] = Piece('K', color)
            board[row][5] = Piece('B', color)
            board[row][6] = Piece('N', color)
            board[row][7] = Piece('R', color)
            
            for i in range(8):
                board[pawn_row][i] = Piece('P', color)
        return board

    def print_board(self):
        print("  a  b  c  d  e  f  g  h")
        print(" +------------------------+")
        for i, row in enumerate(self.board):
            print(f"{8 - i}|", end="")
            for j, piece in enumerate(row):
                bg_color = Fore.LIGHTBLUE_EX if (i + j) % 2 == 0 else Fore.BLUE
                if piece:
                    print(f"{bg_color}{piece}", end=" ")
                else:
                    print(f"{bg_color}. ", end=" ")
            print(f"{Style.RESET_ALL}|{8 - i}")
        print(" +------------------------+")
        print("  a  b  c  d  e  f  g  h")

    def parse_move(self, move_str):
        # Converts algebraic notation (e.g., "e2e4") to board coordinates
        try:
            col_map = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
            from_col = col_map[move_str[0]]
            from_row = 8 - int(move_str[1])
            to_col = col_map[move_str[2]]
            to_row = 8 - int(move_str[3])
            return (from_row, from_col), (to_row, to_col)
        except (ValueError, KeyError, IndexError):
            return None, None

    def is_valid_move(self, start_pos, end_pos):
        # Basic validation (to be expanded for full chess rules)
        if not (0 <= start_pos[0] < 8 and 0 <= start_pos[1] < 8 and
                0 <= end_pos[0] < 8 and 0 <= end_pos[1] < 8):
            return False
        
        piece = self.board[start_pos[0]][start_pos[1]]
        if not piece or piece.color != self.current_turn:
            return False
            
        target = self.board[end_pos[0]][end_pos[1]]
        if target and target.color == self.current_turn:
            return False # Cannot capture your own piece
            
        # Check movement rules for all combined piece types
        all_possible_types = list(set([piece.piece_type] + piece.combined_pieces))
        
        for piece_type in all_possible_types:
            temp_piece = Piece(piece_type, piece.color) 
            if self.is_valid_piece_move(temp_piece, start_pos, end_pos):
                return True
                
        return False
        
    def is_valid_piece_move(self, piece, start_pos, end_pos):
        # Check moves for a single piece type
        piece_type = piece.piece_type
        
        if piece_type == 'P':
            return self.is_valid_pawn_move(start_pos, end_pos, piece.color)
        elif piece_type == 'R':
            return self.is_valid_rook_move(start_pos, end_pos)
        elif piece_type == 'N':
            return self.is_valid_knight_move(start_pos, end_pos)
        elif piece_type == 'B':
            return self.is_valid_bishop_move(start_pos, end_pos)
        elif piece_type == 'Q':
            return self.is_valid_queen_move(start_pos, end_pos)
        elif piece_type == 'K':
            return self.is_valid_king_move(start_pos, end_pos)
        
        return False

    def is_path_clear(self, start_pos, end_pos):
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        row_step = 0
        if end_row > start_row: row_step = 1
        elif end_row < start_row: row_step = -1
        col_step = 0
        if end_col > start_col: col_step = 1
        elif end_col < start_col: col_step = -1

        current_row, current_col = start_row + row_step, start_col + col_step
        while (current_row, current_col) != (end_row, end_col):
            if self.board[current_row][current_col] is not None:
                return False
            current_row += row_step
            current_col += col_step
        return True

    def is_valid_pawn_move(self, start_pos, end_pos, color):
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        target_piece = self.board[end_row][end_col]
        
        direction = -1 if color == 'white' else 1
        start_rank = 6 if color == 'white' else 1
        
        # Standard one-step move
        if start_col == end_col and end_row == start_row + direction and not target_piece:
            return True
        
        # Two-step move from starting position
        if start_col == end_col and start_row == start_rank and end_row == start_row + 2 * direction and not target_piece:
            # Check if path is clear
            return self.is_path_clear(start_pos, end_pos)

        # Capture move
        if abs(start_col - end_col) == 1 and end_row == start_row + direction and target_piece:
            return True
            
        return False

    def is_valid_rook_move(self, start_pos, end_pos):
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        
        if start_row == end_row or start_col == end_col:
            return self.is_path_clear(start_pos, end_pos)
        return False

    def is_valid_knight_move(self, start_pos, end_pos):
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        
        row_diff = abs(start_row - end_row)
        col_diff = abs(start_col - end_col)
        
        return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)

    def is_valid_bishop_move(self, start_pos, end_pos):
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        
        if abs(start_row - end_row) == abs(start_col - end_col):
            return self.is_path_clear(start_pos, end_pos)
        return False

    def is_valid_queen_move(self, start_pos, end_pos):
        return self.is_valid_rook_move(start_pos, end_pos) or self.is_valid_bishop_move(start_pos, end_pos)

    def is_valid_king_move(self, start_pos, end_pos):
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        
        row_diff = abs(start_row - end_row)
        col_diff = abs(start_col - end_col)
        
        return row_diff <= 1 and col_diff <= 1
        
    def play_game(self):
        while True:
            self.print_board()
            
            # Display captured pieces
            white_captured = ' '.join(str(p) for p in self.captured_pieces['white'])
            black_captured = ' '.join(str(p) for p in self.captured_pieces['black'])
            print(f"Captured by White: {white_captured}")
            print(f"Captured by Black: {black_captured}")
            
            turn_color = Fore.WHITE if self.current_turn == 'white' else Fore.LIGHTBLACK_EX
            print(f"\n{turn_color}{self.current_turn.capitalize()}'s turn.")
            
            if self.last_move:
                print(f"Last move: {self.last_move}")

            if self.status_message:
                print(f"{Fore.YELLOW}{self.status_message}{Style.RESET_ALL}")
                self.status_message = ""  # Clear the message after displaying it

            print("Enter move, 'merge [pos1] [pos2]', 'disintegrate [pos] [target]', or 'quit'.")
            
            action = input(f"{Fore.CYAN}> {Style.RESET_ALL}").strip()
            
            if action.lower() == 'quit':
                print("Game ended.")
                break
                
            if action.lower().startswith('merge'):
                try:
                    _, pos1_str, pos2_str = action.split()
                    pos1, _ = self.parse_move(f"{pos1_str}a1") # Dummy conversion
                    pos2, _ = self.parse_move(f"{pos2_str}a1") # Dummy conversion
                    
                    self.attempt_merge(pos1, pos2)

                except ValueError:
                    self.status_message = "Invalid merge command. Use 'merge [pos1] [pos2]'."
                continue
            
            if action.lower().startswith('disintegrate'):
                try:
                    _, pos_str, target_pos_str = action.split()
                    pos, _ = self.parse_move(f"{pos_str}a1")
                    target_pos, _ = self.parse_move(f"{target_pos_str}a1")
                    
                    self.attempt_disintegrate(pos, target_pos)
                except ValueError:
                    self.status_message = "Invalid disintegrate command. Use 'disintegrate [pos] [target]'."
                continue

            start_pos, end_pos = self.parse_move(action)
            if start_pos is None:
                self.status_message = "Invalid move format. Use algebraic notation (e.g., 'e2e4')."
                continue

            if self.is_valid_move(start_pos, end_pos):
                self.move_piece(start_pos, end_pos)
                self.switch_turn()
            else:
                self.status_message = "Invalid move."

    def move_piece(self, start_pos, end_pos):
        self.last_merge_info = None
        piece_to_move = self.board[start_pos[0]][start_pos[1]]
        
        # Basic check for game over
        target_piece = self.board[end_pos[0]][end_pos[1]]
        if target_piece:
            self.captured_pieces[self.current_turn].append(target_piece)
            
        if target_piece and (target_piece.piece_type == 'K' or 'K' in target_piece.combined_pieces):
             print(f"\nGame Over! {self.current_turn.capitalize()} wins by capturing the King!")
             exit()

        self.board[end_pos[0]][end_pos[1]] = piece_to_move
        self.board[start_pos[0]][start_pos[1]] = None
        
        # Format the last move string
        from_str = f"{chr(97+start_pos[1])}{8-start_pos[0]}"
        to_str = f"{chr(97+end_pos[1])}{8-end_pos[0]}"
        self.last_move = f"{from_str}{to_str}"
        
        # Check for pawn promotion
        self.check_pawn_promotion(end_pos)
        
    def check_pawn_promotion(self, pos):
        row, col = pos
        piece = self.board[row][col]
        
        if piece and piece.piece_type == 'P':
            if (piece.color == 'white' and row == 0) or \
               (piece.color == 'black' and row == 7):
                
                while True:
                    promotion_choice = input("Promote pawn to (Q, R, B, N): ").upper()
                    if promotion_choice in ['Q', 'R', 'B', 'N']:
                        piece.piece_type = promotion_choice
                        # If the pawn was part of a combined piece, remove the 'P'
                        if 'P' in piece.combined_pieces:
                            piece.combined_pieces.remove('P')
                        # Add the new piece type to the combined list for consistency
                        if promotion_choice not in piece.combined_pieces:
                             piece.combined_pieces.append(promotion_choice)
                        print(f"Pawn promoted to {promotion_choice}.")
                        break
                    else:
                        print("Invalid choice. Please enter Q, R, B, or N.")

    def attempt_merge(self, pos1, pos2):
        if self.merge_count[self.current_turn] >= self.max_merges:
            self.status_message = f"Merge limit reached for {self.current_turn}."
            return

        p1_row, p1_col = pos1
        p2_row, p2_col = pos2
        
        piece1 = self.board[p1_row][p1_col]
        piece2 = self.board[p2_row][p2_col]
        
        # Validation checks for merge
        if not piece1 or not piece2:
            self.status_message = "One of the squares is empty."
            return
        if piece1.color != self.current_turn or piece2.color != self.current_turn:
            self.status_message = "You can only merge your own pieces."
            return
        if piece1.piece_type == 'K' or piece2.piece_type == 'K' or \
           'K' in piece1.combined_pieces or 'K' in piece2.combined_pieces:
            self.status_message = "The King cannot be merged."
            return
        if piece1.piece_type == 'Q' or piece2.piece_type == 'Q' or \
           'Q' in piece1.combined_pieces or 'Q' in piece2.combined_pieces:
            self.status_message = "The Queen cannot be merged."
            return
        if piece1.piece_type == piece2.piece_type:
            self.status_message = "Cannot merge two pieces of the same type."
            return
        if abs(p1_row - p2_row) > 1 or abs(p1_col - p2_col) > 1:
            self.status_message = "Pieces must be adjacent to merge."
            return
        
        # Perform the merge
        # piece2 is merged into piece1
        self.status_message = f"Merging {piece2.piece_type} into {piece1.piece_type} at {chr(97+p1_col)}{8-p1_row}"

        # The new piece keeps the primary piece type for display
        # but gains the abilities of the other
        new_combined_list = sorted(list(set([piece1.piece_type] + piece1.combined_pieces + \
                                            [piece2.piece_type] + piece2.combined_pieces)))

        piece1.combined_pieces = new_combined_list
        
        # For simplicity, we keep the original piece type, but you could create new ones
        # e.g., if 'R' and 'N' merge, the piece_type could become 'C' (Chancellor)
        display_type, is_special_combo = piece1.get_display_info()
        if is_special_combo:
            info = SPECIAL_PIECE_INFO.get(display_type)
            if info:
                self.last_merge_info = f"Created a {info['name']}! It moves {info['moves']}."
            else:
                self.last_merge_info = None
        else:
            self.last_merge_info = None

        self.board[p2_row][p2_col] = None # Remove the second piece
        self.merge_count[self.current_turn] += 1
        
        from_str = f"{chr(97+p1_col)}{8-p1_row}"
        to_str = f"{chr(97+p2_col)}{8-p2_row}"
        self.last_move = f"merge {from_str} {to_str}"
        
        self.switch_turn()

    def attempt_disintegrate(self, pos, target_pos):
        self.last_merge_info = None
        pos_row, pos_col = pos
        piece = self.board[pos_row][pos_col]

        # Validation for disintegration
        if not piece or not piece.is_combined():
            self.status_message = "There is no combined piece at this position."
            return
        if piece.color != self.current_turn:
            self.status_message = "You can only disintegrate your own pieces."
            return
        if abs(pos_row - target_pos[0]) > 1 or abs(pos_col - target_pos[1]) > 1:
            self.status_message = "Target square must be adjacent."
            return
        if self.board[target_pos[0]][target_pos[1]] is not None:
            self.status_message = "Target square must be empty."
            return

        # Perform disintegration
        primary_piece_type = piece.piece_type
        
        # The last piece added to the combined_pieces list is the one that's split off
        secondary_piece_type = piece.combined_pieces.pop(-1)

        # If the primary piece's own type was in the combined list, it should remain
        # The new combined list for the primary piece is everything minus the secondary piece type
        new_combined_list = [p for p in piece.combined_pieces if p != secondary_piece_type]

        # After splitting, if only one piece type is left in the list, it means it's no longer a combined piece
        if len(new_combined_list) == 1:
            piece.piece_type = new_combined_list[0]
            piece.combined_pieces = []
        elif len(new_combined_list) == 0: # This case handles splitting a piece with only two components
            # The piece keeps its original type, and the combined list is now empty.
            piece.combined_pieces = []
        else:
            # If there are still multiple pieces combined, we need to update the primary piece type
            # A simple approach is to set it to the first type in the new list.
            piece.piece_type = new_combined_list[0]
            piece.combined_pieces = new_combined_list

        # The primary piece moves to the target square
        self.board[target_pos[0]][target_pos[1]] = piece
        self.board[pos_row][pos_col] = Piece(secondary_piece_type, self.current_turn)
        
        self.status_message = f"Disintegrated into {piece.piece_type} and {secondary_piece_type}."
        self.last_move = f"disintegrate {chr(97+pos_col)}{8-pos_row} {chr(97+target_pos[1])}{8-target_pos[0]}"
        self.switch_turn()

    def switch_turn(self):
        self.current_turn = 'black' if self.current_turn == 'white' else 'white'

# The game loop will now be handled by the server
# if __name__ == "__main__":
#     game = SymbioticChessGame()
#     game.play_game()
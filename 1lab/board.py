from pawn import Pawn
from rook import Rook
from knight import Knight
from bishop import Bishop
from queen import Queen
from king import King


class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.setup_board()
        self.current_turn = 'white'
        self.selected_piece = None
        self.valid_moves = []
        self.valid_attacks = []
        self.white_king_pos = (7, 4)
        self.black_king_pos = (0, 4)
        self.check_squares = []
        self.move_history = []
        self.game_over = False
        self.game_over_message = ""

    def setup_board(self):
        for col in range(8):
            self.grid[6][col] = Pawn('white', 6, col)
            self.grid[1][col] = Pawn('black', 1, col)

        self.grid[7][0] = Rook('white', 7, 0)
        self.grid[7][7] = Rook('white', 7, 7)
        self.grid[0][0] = Rook('black', 0, 0)
        self.grid[0][7] = Rook('black', 0, 7)

        self.grid[7][1] = Knight('white', 7, 1)
        self.grid[7][6] = Knight('white', 7, 6)
        self.grid[0][1] = Knight('black', 0, 1)
        self.grid[0][6] = Knight('black', 0, 6)

        self.grid[7][2] = Bishop('white', 7, 2)
        self.grid[7][5] = Bishop('white', 7, 5)
        self.grid[0][2] = Bishop('black', 0, 2)
        self.grid[0][5] = Bishop('black', 0, 5)

        self.grid[7][3] = Queen('white', 7, 3)
        self.grid[0][3] = Queen('black', 0, 3)

        self.grid[7][4] = King('white', 7, 4)
        self.grid[0][4] = King('black', 0, 4)

    def get_piece(self, row, col):
        if 0 <= row < 8 and 0 <= col < 8:
            return self.grid[row][col]
        return None

    def is_empty(self, row, col):
        return self.get_piece(row, col) is None

    def select_piece(self, row, col):
        if self.game_over:
            return False

        piece = self.get_piece(row, col)
        if piece and piece.color == self.current_turn:
            self.selected_piece = (row, col)
            moves, attacks = piece.get_possible_moves(self)

            # Фильтруем ходы, которые оставляют короля под шахом
            all_valid_moves = []
            all_valid_attacks = []

            for move in moves:
                if self.is_move_safe(row, col, move[0], move[1]):
                    all_valid_moves.append(move)

            for attack in attacks:
                if self.is_move_safe(row, col, attack[0], attack[1]):
                    all_valid_attacks.append(attack)

            self.valid_moves = all_valid_moves
            self.valid_attacks = all_valid_attacks

            return True
        return False

    def is_move_safe(self, from_row, from_col, to_row, to_col):
        """Проверяет, не оставляет ли ход короля под шахом"""
        # Создаем копию доски
        temp_board = self.copy_board()

        # Делаем ход на копии
        piece = temp_board.grid[from_row][from_col]
        target = temp_board.grid[to_row][to_col]

        temp_board.grid[to_row][to_col] = piece
        temp_board.grid[from_row][from_col] = None

        if isinstance(piece, King):
            if piece.color == 'white':
                temp_board.white_king_pos = (to_row, to_col)
            else:
                temp_board.black_king_pos = (to_row, to_col)

        # Проверяем, не под шахом ли король после хода
        king_pos = temp_board.white_king_pos if piece.color == 'white' else temp_board.black_king_pos
        opponent = 'black' if piece.color == 'white' else 'white'

        return not temp_board.is_square_attacked(king_pos[0], king_pos[1], opponent)

    def copy_board(self):
        """Создает глубокую копию доски"""
        temp_board = Board()
        temp_board.grid = [[None for _ in range(8)] for _ in range(8)]

        for r in range(8):
            for c in range(8):
                piece = self.grid[r][c]
                if piece:
                    # Создаем новую фигуру того же типа
                    if isinstance(piece, Pawn):
                        temp_board.grid[r][c] = Pawn(piece.color, r, c)
                    elif isinstance(piece, Rook):
                        temp_board.grid[r][c] = Rook(piece.color, r, c)
                    elif isinstance(piece, Knight):
                        temp_board.grid[r][c] = Knight(piece.color, r, c)
                    elif isinstance(piece, Bishop):
                        temp_board.grid[r][c] = Bishop(piece.color, r, c)
                    elif isinstance(piece, Queen):
                        temp_board.grid[r][c] = Queen(piece.color, r, c)
                    elif isinstance(piece, King):
                        temp_board.grid[r][c] = King(piece.color, r, c)

                    temp_board.grid[r][c].has_moved = piece.has_moved

        temp_board.white_king_pos = self.white_king_pos
        temp_board.black_king_pos = self.black_king_pos
        temp_board.current_turn = self.current_turn

        return temp_board

    def move_piece(self, from_row, from_col, to_row, to_col):
        piece = self.get_piece(from_row, from_col)
        target = self.get_piece(to_row, to_col)

        if piece:
            move_data = {
                'piece': piece,
                'from_row': from_row,
                'from_col': from_col,
                'to_row': to_row,
                'to_col': to_col,
                'captured': target,
                'was_castling': False,
                'was_king_move': isinstance(piece, King),
                'old_has_moved': piece.has_moved,
                'old_white_king': self.white_king_pos,
                'old_black_king': self.black_king_pos,
                'old_turn': self.current_turn
            }

            if isinstance(piece, King) and abs(to_col - from_col) == 2:
                move_data['was_castling'] = True
                if to_col > from_col:
                    rook = self.get_piece(from_row, 7)
                    move_data['rook'] = rook
                    move_data['rook_from'] = (from_row, 7)
                    move_data['rook_to'] = (from_row, to_col - 1)
                else:
                    rook = self.get_piece(from_row, 0)
                    move_data['rook'] = rook
                    move_data['rook_from'] = (from_row, 0)
                    move_data['rook_to'] = (from_row, to_col + 1)
                move_data['old_rook_has_moved'] = rook.has_moved if rook else None

                self.perform_castling(piece, to_row, to_col)
            else:
                self.grid[to_row][to_col] = piece
                self.grid[from_row][from_col] = None
                piece.move(to_row, to_col)

            if isinstance(piece, King):
                if piece.color == 'white':
                    self.white_king_pos = (to_row, to_col)
                else:
                    self.black_king_pos = (to_row, to_col)

            self.move_history.append(move_data)

            self.current_turn = 'black' if self.current_turn == 'white' else 'white'
            self.selected_piece = None
            self.valid_moves = []
            self.valid_attacks = []

            # Проверяем на мат или пат после хода
            self.check_game_over()

            return True
        return False

    def check_game_over(self):
        """Проверяет, закончилась ли игра матом или патом"""
        if self.is_in_checkmate(self.current_turn):
            self.game_over = True
            winner = 'Черные' if self.current_turn == 'white' else 'Белые'
            self.game_over_message = f"МАТ! {winner} победили!"
        elif self.is_in_stalemate(self.current_turn):
            self.game_over = True
            self.game_over_message = "ПАТ! Ничья!"

    def is_in_checkmate(self, color):
        """Проверяет, мат ли цвету color"""
        if not self.is_in_check(color):
            return False

        return not self.has_any_legal_moves(color)

    def is_in_stalemate(self, color):
        """Проверяет, пат ли цвету color"""
        if self.is_in_check(color):
            return False

        return not self.has_any_legal_moves(color)

    def has_any_legal_moves(self, color):
        """Проверяет, есть ли у цвета хоть один легальный ход"""
        for r in range(8):
            for c in range(8):
                piece = self.get_piece(r, c)
                if piece and piece.color == color:
                    moves, attacks = piece.get_possible_moves(self)

                    for move in moves:
                        if self.is_move_safe(r, c, move[0], move[1]):
                            return True

                    for attack in attacks:
                        if self.is_move_safe(r, c, attack[0], attack[1]):
                            return True

        return False

    def undo_move(self):
        if not self.move_history:
            print("Нет ходов для отмены")
            return False

        self.game_over = False
        self.game_over_message = ""

        last_move = self.move_history.pop()

        self.grid[last_move['from_row']][last_move['from_col']] = last_move['piece']
        self.grid[last_move['to_row']][last_move['to_col']] = last_move['captured']

        last_move['piece'].has_moved = last_move['old_has_moved']

        if last_move['was_castling']:
            rook = last_move['rook']
            rook_from = last_move['rook_from']
            rook_to = last_move['rook_to']

            self.grid[rook_from[0]][rook_from[1]] = rook
            self.grid[rook_to[0]][rook_to[1]] = None
            if rook:
                rook.has_moved = last_move['old_rook_has_moved']
                rook.row, rook.col = rook_from

        self.white_king_pos = last_move['old_white_king']
        self.black_king_pos = last_move['old_black_king']

        self.current_turn = last_move['old_turn']

        self.selected_piece = None
        self.valid_moves = []
        self.valid_attacks = []

        print("Ход отменён!")
        return True

    def perform_castling(self, king, to_row, to_col):
        if to_col > king.col:
            rook_col = 7
            new_rook_col = to_col - 1
        else:
            rook_col = 0
            new_rook_col = to_col + 1

        rook = self.get_piece(king.row, rook_col)

        self.grid[to_row][to_col] = king
        self.grid[king.row][king.col] = None
        king.move(to_row, to_col)

        self.grid[king.row][new_rook_col] = rook
        self.grid[king.row][rook_col] = None
        if rook:
            rook.move(king.row, new_rook_col)

    def is_square_attacked(self, row, col, attacking_color):
        for r in range(8):
            for c in range(8):
                piece = self.get_piece(r, c)
                if piece and piece.color == attacking_color:
                    attacked = piece.get_attack_squares(self)
                    if (row, col) in attacked:
                        return True
        return False

    def is_in_check(self, color):
        king_pos = self.white_king_pos if color == 'white' else self.black_king_pos
        opponent = 'black' if color == 'white' else 'white'
        return self.is_square_attacked(king_pos[0], king_pos[1], opponent)

    def get_pieces_under_attack(self, color):
        under_attack = []
        opponent = 'black' if color == 'white' else 'white'

        for r in range(8):
            for c in range(8):
                piece = self.get_piece(r, c)
                if piece and piece.color == color:
                    if self.is_square_attacked(r, c, opponent):
                        under_attack.append((r, c))

        return under_attack

    def get_check_sources(self, color):
        check_sources = []
        king_pos = self.white_king_pos if color == 'white' else self.black_king_pos
        opponent = 'black' if color == 'white' else 'white'

        for r in range(8):
            for c in range(8):
                piece = self.get_piece(r, c)
                if piece and piece.color == opponent:
                    if (king_pos[0], king_pos[1]) in piece.get_attack_squares(self):
                        check_sources.append((r, c))

        return check_sources
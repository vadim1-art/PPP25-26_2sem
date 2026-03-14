from piece import Piece
from rook import Rook


class King(Piece):
    def __init__(self, color, row, col):
        image_name = f"{color}_king.png"
        super().__init__(color, row, col, image_name)

    def get_possible_moves(self, board):
        moves = []
        attacks = []
        king_moves = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]

        for drow, dcol in king_moves:
            new_row = self.row + drow
            new_col = self.col + dcol

            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target = board.get_piece(new_row, new_col)
                if target is None:
                    moves.append((new_row, new_col))
                elif target.color != self.color:
                    attacks.append((new_row, new_col))

        castling_moves = self.get_castling_moves(board)
        moves.extend(castling_moves)

        return moves, attacks

    def get_castling_moves(self, board):
        castling_moves = []

        if self.has_moved:
            return castling_moves

        rook_positions = [(self.row, 0), (self.row, 7)]

        for rook_row, rook_col in rook_positions:
            rook = board.get_piece(rook_row, rook_col)

            if rook and isinstance(rook, Rook) and not rook.has_moved:
                path_clear = True
                step = 1 if rook_col > self.col else -1

                for col in range(self.col + step, rook_col, step):
                    if not board.is_empty(self.row, col):
                        path_clear = False
                        break

                if path_clear:
                    king_dest_col = self.col + (2 if rook_col > self.col else -2)

                    if not board.is_square_attacked(self.row, self.col, self.get_opponent_color()):
                        if not board.is_square_attacked(self.row, self.col + step, self.get_opponent_color()):
                            if not board.is_square_attacked(self.row, king_dest_col, self.get_opponent_color()):
                                castling_moves.append((self.row, king_dest_col))

        return castling_moves

    def get_opponent_color(self):
        return 'black' if self.color == 'white' else 'white'

    def get_attack_squares(self, board):
        attacks = []
        king_moves = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]

        for drow, dcol in king_moves:
            new_row = self.row + drow
            new_col = self.col + dcol
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                attacks.append((new_row, new_col))

        return attacks
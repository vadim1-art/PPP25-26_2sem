from piece import Piece


class Knight(Piece):
    def __init__(self, color, row, col):
        image_name = f"{color}_knight.png"
        super().__init__(color, row, col, image_name)

    def get_possible_moves(self, board):
        moves = []
        attacks = []
        knight_moves = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]

        for drow, dcol in knight_moves:
            new_row = self.row + drow
            new_col = self.col + dcol

            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target = board.get_piece(new_row, new_col)
                if target is None:
                    moves.append((new_row, new_col))
                elif target.color != self.color:
                    attacks.append((new_row, new_col))

        return moves, attacks
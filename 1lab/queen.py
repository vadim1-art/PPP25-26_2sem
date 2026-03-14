from piece import Piece


class Queen(Piece):
    def __init__(self, color, row, col):
        image_name = f"{color}_queen.png"
        super().__init__(color, row, col, image_name)

    def get_possible_moves(self, board):
        moves = []
        attacks = []
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (-1, -1), (-1, 1), (1, -1), (1, 1)
        ]

        for drow, dcol in directions:
            new_row, new_col = self.row + drow, self.col + dcol

            while 0 <= new_row < 8 and 0 <= new_col < 8:
                target = board.get_piece(new_row, new_col)

                if target is None:
                    moves.append((new_row, new_col))
                elif target.color != self.color:
                    attacks.append((new_row, new_col))
                    break
                else:
                    break

                new_row += drow
                new_col += dcol

        return moves, attacks
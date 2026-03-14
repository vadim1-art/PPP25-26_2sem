from piece import Piece


class Pawn(Piece):
    def __init__(self, color, row, col):
        image_name = f"{color}_pawn.png"
        super().__init__(color, row, col, image_name)
        self.direction = -1 if color == 'white' else 1
        self.start_row = row

    def get_possible_moves(self, board):
        moves = []
        attacks = []
        new_row = self.row + self.direction

        if 0 <= new_row < 8 and board.is_empty(new_row, self.col):
            moves.append((new_row, self.col))

            if self.row == self.start_row:
                double_row = self.row + 2 * self.direction
                if board.is_empty(double_row, self.col):
                    moves.append((double_row, self.col))

        for dcol in [-1, 1]:
            new_col = self.col + dcol
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target = board.get_piece(new_row, new_col)
                if target and target.color != self.color:
                    attacks.append((new_row, new_col))

        return moves, attacks

    def get_attack_squares(self, board):
        attacks = []
        new_row = self.row + self.direction
        for dcol in [-1, 1]:
            new_col = self.col + dcol
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                attacks.append((new_row, new_col))
        return attacks
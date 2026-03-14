import pygame
import sys
from constants import *
from board import Board


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Chess Game")
        self.clock = pygame.time.Clock()
        self.board = Board()
        self.running = True

    def draw_board(self):
        for row in range(8):
            for col in range(8):
                color = LIGHT_BROWN if (row + col) % 2 == 0 else DARK_BROWN

                if self.board.selected_piece == (row, col):
                    color = HIGHLIGHT
                elif (row, col) in self.board.valid_moves:
                    color = HIGHLIGHT
                elif (row, col) in self.board.valid_attacks:
                    color = CAPTURE_HIGHLIGHT

                pygame.draw.rect(self.screen, color,
                                 (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        if not self.board.game_over:
            if self.board.is_in_check('white'):
                check_sources = self.board.get_check_sources('white')
                for r, c in check_sources:
                    s = pygame.Surface((CELL_SIZE, CELL_SIZE))
                    s.set_alpha(128)
                    s.fill(CHECK_HIGHLIGHT)
                    self.screen.blit(s, (c * CELL_SIZE, r * CELL_SIZE))

            if self.board.is_in_check('black'):
                check_sources = self.board.get_check_sources('black')
                for r, c in check_sources:
                    s = pygame.Surface((CELL_SIZE, CELL_SIZE))
                    s.set_alpha(128)
                    s.fill(CHECK_HIGHLIGHT)
                    self.screen.blit(s, (c * CELL_SIZE, r * CELL_SIZE))

            under_attack = self.board.get_pieces_under_attack(self.board.current_turn)
            for r, c in under_attack:
                s = pygame.Surface((CELL_SIZE, CELL_SIZE))
                s.set_alpha(100)
                s.fill(UNDER_ATTACK)
                self.screen.blit(s, (c * CELL_SIZE, r * CELL_SIZE))

    def draw_pieces(self):
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece(row, col)
                if piece:
                    if piece.image:
                        self.screen.blit(piece.image, (col * CELL_SIZE, row * CELL_SIZE))
                    else:
                        color = WHITE if piece.color == 'white' else BLACK
                        pygame.draw.circle(self.screen, color,
                                           (col * CELL_SIZE + CELL_SIZE // 2,
                                            row * CELL_SIZE + CELL_SIZE // 2),
                                           CELL_SIZE // 3)

    def draw_game_over(self):
        if self.board.game_over:
            s = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            s.set_alpha(128)
            s.fill(BLACK)
            self.screen.blit(s, (0, 0))

    def handle_click(self, pos):
        if self.board.game_over:
            return

        col = pos[0] // CELL_SIZE
        row = pos[1] // CELL_SIZE

        if 0 <= row < 8 and 0 <= col < 8:
            if self.board.selected_piece:
                if (row, col) in self.board.valid_moves or (row, col) in self.board.valid_attacks:
                    from_row, from_col = self.board.selected_piece
                    self.board.move_piece(from_row, from_col, row, col)
                else:
                    self.board.selected_piece = None
                    self.board.valid_moves = []
                    self.board.valid_attacks = []
                    self.board.select_piece(row, col)
            else:
                self.board.select_piece(row, col)

    def handle_key(self, key):
        if key == pygame.K_u:
            self.board.undo_move()
        elif key == pygame.K_r and self.board.game_over:
            self.board = Board()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(pygame.mouse.get_pos())
                elif event.type == pygame.KEYDOWN:
                    self.handle_key(event.key)

            self.draw_board()
            self.draw_pieces()
            self.draw_game_over()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
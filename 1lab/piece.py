import os
import pygame
from constants import CELL_SIZE, USE_IMAGES, IMAGE_PATH


class Piece:
    def __init__(self, color, row, col, image_name):
        self.color = color
        self.row = row
        self.col = col
        self.has_moved = False
        self.image = None

        if USE_IMAGES:
            try:
                image_file = os.path.join(IMAGE_PATH, image_name)
                if os.path.exists(image_file):
                    self.image = pygame.image.load(image_file)
                    self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))
                else:
                    print(f"Image not found: {image_file}")
                    self.image = None
            except Exception as e:
                print(f"Error loading image: {e}")
                self.image = None

    def get_possible_moves(self, board):
        return [], []

    def get_attack_squares(self, board):
        return []

    def move(self, new_row, new_col):
        self.row = new_row
        self.col = new_col
        self.has_moved = True
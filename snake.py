import pygame

class Snake:
    def __init__(self):
        self.snake_x = 20
        self.snake_y = 40
        self.snake_size = 15
        self.vel_x = 0
        self.vel_y = 0
        self.increment = 5
        self.snk_list = []
        self.snk_length = 1
        self.score = 0

    def reset(self):
        self.snake_x = 20
        self.snake_y = 40
        self.vel_x = 0
        self.vel_y = 0
        self.snk_list = []
        self.snk_length = 1
        self.score = 0

    def move(self):
        self.snake_x += self.vel_x
        self.snake_y += self.vel_y

    def lengthen(self):
        self.snk_length += 5
        self.score += 1

    def draw(self, gameWindow):
        head = [self.snake_x, self.snake_y]
        self.snk_list.append(head)

        if len(self.snk_list) > self.snk_length:
            del self.snk_list[0]

        for x, y in self.snk_list:
            pygame.draw.rect(gameWindow, (10, 100, 0), [x, y, self.snake_size, self.snake_size])

    def is_collision(self, width, height):
        if self.snake_x >= width or self.snake_x < 0 or self.snake_y >= height or self.snake_y < 0:
            return True

        if [self.snake_x, self.snake_y] in self.snk_list[:-1]:
            return True

        return False

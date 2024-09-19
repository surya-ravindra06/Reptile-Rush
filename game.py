import pygame
import random
from snake import Snake
from utils import load_highscore, save_highscore, display_text

class SnakeGame:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.width = 1000
        self.height = 500
        self.gameWindow = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake Game")

        self.bgimg = pygame.image.load("assets/back.png")
        self.bgimg = pygame.transform.scale(self.bgimg, (self.width, self.height)).convert_alpha()
        self.welimg = pygame.image.load("assets/welcome.png")
        self.welimg = pygame.transform.scale(self.welimg, (self.width, self.height)).convert_alpha()

        self.food_img = pygame.image.load("assets/red_egg.png")
        self.food_img = pygame.transform.scale(self.food_img, (35, 35)) 

        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.black = (0, 0, 0)

        self.snake = Snake()
        self.food_x = random.randint(50, self.width - 50)
        self.food_y = random.randint(150, self.height - 50)


        self.fps = 50
        self.clock = pygame.time.Clock()

        self.highscore = load_highscore()

    def reset_game(self):
        self.snake.reset()
        self.food_x = random.randint(50, self.width - 50)
        self.food_y = random.randint(150, self.height - 50)

    def start_game(self):
        self.show_welcome_screen()
        self.run_game()

    def show_welcome_screen(self):
        exit_game = False
        while not exit_game:
            self.gameWindow.fill((233, 210, 229))
            self.gameWindow.blit(self.welimg, (0, 0))

            display_text(self.gameWindow, "Welcome to Snake Game", 330, 50, 55, (10, 10, 255))
            display_text(self.gameWindow, "Press Enter To Start", 330, 400, 50, (0, 0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        pygame.mixer.music.load('assets/start.mp3')
                        pygame.mixer.music.play()
                        return

            pygame.display.update()
            self.clock.tick(60)

    def run_game(self):
        exit_game = False
        while not exit_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.snake.vel_x = self.snake.increment
                        self.snake.vel_y = 0
                    if event.key == pygame.K_LEFT:
                        self.snake.vel_x = -self.snake.increment
                        self.snake.vel_y = 0
                    if event.key == pygame.K_UP:
                        self.snake.vel_y = -self.snake.increment
                        self.snake.vel_x = 0
                    if event.key == pygame.K_DOWN:
                        self.snake.vel_y = self.snake.increment
                        self.snake.vel_x = 0

            self.snake.move()
            if abs(self.snake.snake_x - self.food_x) < 20 and abs(self.snake.snake_y - self.food_y) < 20:
                pygame.mixer.music.load('assets/point.mp3')
                pygame.mixer.music.play()
                self.snake.lengthen()
                if self.snake.score > int(self.highscore):
                    self.highscore = self.snake.score
                    save_highscore(self.highscore)
                self.food_x = random.randint(50, self.width - 50)
                self.food_y = random.randint(150, self.height - 50)

            self.gameWindow.fill(self.white)
            self.gameWindow.blit(self.bgimg, (0, 0))
            display_text(self.gameWindow, f"Score: {self.snake.score}   HighScore: {self.highscore}", 5, 5)
            self.gameWindow.blit(self.food_img, (self.food_x, self.food_y))

            self.snake.draw(self.gameWindow)

            if self.snake.is_collision(self.width, self.height):
                display_text(self.gameWindow, "Game Over!", self.width / 2 - 100, self.height / 2)
                pygame.display.update()
                pygame.mixer.music.load('assets/game_over.mp3')
                pygame.mixer.music.play()
                pygame.time.delay(1200)
                self.reset_game()
                self.start_game()
                return

            pygame.display.update()
            self.clock.tick(self.fps)

        pygame.quit()
        quit()

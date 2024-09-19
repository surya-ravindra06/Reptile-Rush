import pygame
import random

pygame.mixer.init()
pygame.init()

class SnakeGame:
    def __init__(self):

        self.width = 1000
        self.height = 500
        self.gameWindow = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake Game")

        self.bgimg = pygame.image.load("back.png")
        self.bgimg = pygame.transform.scale(self.bgimg, (self.width, self.height)).convert_alpha()
        self.welimg = pygame.image.load("welcome.png")
        self.welimg = pygame.transform.scale(self.welimg, (self.width, self.height)).convert_alpha()

        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.black = (0, 0, 0)

        self.reset_game_vars()

        self.clock = pygame.time.Clock()

        self.load_highscore()

    def reset_game_vars(self):
        self.Score = 0
        self.exit_game = False
        self.game_over = False
        self.snake_x = 20
        self.snake_y = 40
        self.snake_size = 15
        self.fps = 50
        self.vel_x = 0
        self.vel_y = 0
        self.increment = 5
        self.food_x = random.randint(50, self.width - 20)
        self.food_y = random.randint(150, self.height - 20)
        self.snk_list = []
        self.snk_length = 1

    def load_highscore(self):
        try:
            with open("highscore.txt", "x") as file:
                file.write("0")
        except:
            pass
        
        with open("highscore.txt", "r") as file:
            self.highscore = file.read()

    def plot_snake(self):
        for x, y in self.snk_list:
            pygame.draw.rect(self.gameWindow, (10, 100, 0), [x, y, self.snake_size, self.snake_size])

    def text_display(self, text, x, y):
        font = pygame.font.SysFont(None, 35)
        screen_text = font.render(text, True, (0, 0, 0))
        self.gameWindow.blit(screen_text, [x, y])

    def welcome(self):
        exit_game = False
        while not exit_game:
            self.gameWindow.fill((233, 210, 229))
            self.gameWindow.blit(self.welimg, (0, 0))

            font = pygame.font.SysFont(None, 55)
            screen_text = font.render("Welcome to Snake Game", True, (10, 10, 255))
            self.gameWindow.blit(screen_text, [330, 50])

            font = pygame.font.SysFont(None, 50)
            screen_text = font.render("Press Enter To Start", True, (0, 0, 0))
            self.gameWindow.blit(screen_text, [330, 400])

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pygame.mixer.music.load('start.mp3')
                        pygame.mixer.music.play()
                        exit_game = True
                        break

            pygame.display.update()
            self.clock.tick(60)

    def run_game(self):
        while not self.exit_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.vel_x = self.increment
                        self.vel_y = 0
                    if event.key == pygame.K_LEFT:
                        self.vel_x = -self.increment
                        self.vel_y = 0
                    if event.key == pygame.K_UP:
                        self.vel_y = -self.increment
                        self.vel_x = 0
                    if event.key == pygame.K_DOWN:
                        self.vel_y = self.increment
                        self.vel_x = 0

            self.snake_x += self.vel_x
            self.snake_y += self.vel_y

            if abs(self.snake_x - self.food_x) < 15 and abs(self.snake_y - self.food_y) < 15:
                pygame.mixer.music.load('point.mp3')
                pygame.mixer.music.play()
                self.Score += 1
                if self.Score > int(self.highscore):
                    self.highscore = self.Score
                    with open("highscore.txt", "w") as f:
                        f.write(str(self.highscore))
                self.snk_length += 5
                self.food_x = random.randint(10, self.width - 10)
                self.food_y = random.randint(10, self.height - 10)

            self.gameWindow.fill(self.white)
            self.gameWindow.blit(self.bgimg, (0, 0))
            self.text_display("Score: " + str(self.Score) + "   HighScore: " + str(self.highscore), 5, 5)
            pygame.draw.rect(self.gameWindow, (139, 69, 19), [self.food_x, self.food_y, self.snake_size, self.snake_size])
            pygame.draw.rect(self.gameWindow, self.black, [self.snake_x, self.snake_y, self.snake_size, self.snake_size])

            head = [self.snake_x, self.snake_y]
            self.snk_list.append(head)

            if len(self.snk_list) > self.snk_length:
                del self.snk_list[0]

            if (self.snake_x > self.width or self.snake_x < 0 or 
                self.snake_y > self.height or self.snake_y < 0 or 
                head in self.snk_list[:-1]):
                self.text_display("Game Over!", self.width / 2 - 100, self.height / 2)
                pygame.display.update()
                pygame.mixer.music.load('game_over.mp3')
                pygame.mixer.music.play()
                pygame.time.delay(1200)
                self.exit_game = True
                pygame.quit()
                quit()

            self.plot_snake()
            pygame.display.update()
            self.clock.tick(self.fps)

if __name__ == "__main__":
    game = SnakeGame()
    game.welcome()
    game.run_game()

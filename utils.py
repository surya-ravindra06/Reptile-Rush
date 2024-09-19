import pygame

def load_highscore():
    try:
        with open("highscore.txt", "r") as file:
            return file.read()
    except FileNotFoundError:
        with open("highscore.txt", "w") as file:
            file.write("0")
        return "0"

def save_highscore(highscore):
    with open("highscore.txt", "w") as file:
        file.write(str(highscore))

def display_text(gameWindow, text, x, y, font_size=35, color=(0, 0, 0)):
    font = pygame.font.SysFont(None, font_size)
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])

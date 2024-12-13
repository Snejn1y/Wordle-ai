import pygame
import random
import sys
from paramets import *

# Ініціалізація Pygame
pygame.init()

# Налаштування вікна
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wordle на Pygame")

# Шрифт
FONT = pygame.font.Font(None, 70)
KEYBOARD_FONT = pygame.font.Font(None, 40)
MESSAGE_FONT = pygame.font.Font(None, 50)

# Список слів
valid_words = set(words_list)  # Набір для швидкої перевірки
secret_word = random.choice(words_list).upper()

# Змінні гри
current_guess = ""
guesses = []
keyboard_state = {chr(k): GRAY for k in range(65, 91)}  # Стани літер клавіатури
message = ""

# Рендеринг тексту
def draw_text(text, x, y, color, font=FONT):
    rendered_text = font.render(text, True, color)
    WIN.blit(rendered_text, (x, y))

# Перевірка введеного слова
def check_guess(secret_word, guess):
    result = []
    for i, char in enumerate(guess):
        if char == secret_word[i]:
            result.append(GREEN)  # Правильна літера на правильному місці
            keyboard_state[char] = GREEN
        elif char in secret_word:
            result.append(YELLOW)  # Літера в слові, але на іншому місці
            if keyboard_state[char] != GREEN:
                keyboard_state[char] = YELLOW
        else:
            result.append(DARK_GRAY)  # Літера відсутня в слові
            keyboard_state[char] = DARK_GRAY
    return result

# Малювання клавіатури
def draw_keyboard():
    rows = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
    y_offsets = [660, 720, 780]
    key_width = 50
    key_height = 50
    spacing = 10

    for row, y in zip(rows, y_offsets):
        x_start = (WIDTH - (len(row) * (key_width + spacing) - spacing)) // 2
        for i, char in enumerate(row):
            x = x_start + i * (key_width + spacing)
            pygame.draw.rect(WIN, keyboard_state[char], (x, y, key_width, key_height), border_radius=5)
            draw_text(char, x + 12, y + 5, WHITE, font=KEYBOARD_FONT)

# Основний цикл гри
def main():
    global current_guess, guesses, message, secret_word, keyboard_state
    clock = pygame.time.Clock()
    running = True
    game_over = False

    while running:
        WIN.fill(WHITE)

        # Обробка подій
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            if not game_over:
                # Введення тексту
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        current_guess = current_guess[:-1]
                    elif event.key == pygame.K_RETURN:
                        if len(current_guess) == 5:
                            if current_guess not in valid_words:
                                message = "Цього слова немає в словнику!"
                            else:
                                guesses.append(current_guess)
                                if current_guess == secret_word:
                                    message = f"🎉 Ви вгадали слово: {secret_word}"
                                    game_over = True
                                current_guess = ""
                                if len(guesses) == attempts and guesses[-1] != secret_word:
                                    message = f"😞 Ви програли! Слово було: {secret_word}"
                                    game_over = True
                    elif len(current_guess) < 5 and event.unicode.isalpha():
                        current_guess += event.unicode.upper()
            else:
                # Перезапуск гри
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    current_guess = ""
                    guesses = []
                    secret_word = random.choice(words_list).upper()
                    print(secret_word)
                    keyboard_state = {chr(k): GRAY for k in range(65, 91)}
                    message = ""
                    game_over = False

        # Малювання введених слів
        for i, guess in enumerate(guesses):
            colors = check_guess(secret_word, guess)
            for j, char in enumerate(guess):
                pygame.draw.rect(WIN, colors[j], (j * 100 + 50, i * 100 + 50, 90, 90))
                draw_text(char, j * 100 + 75, i * 100 + 65, WHITE)

        # Малювання поточного слова
        if not game_over:
            for j, char in enumerate(current_guess):
                pygame.draw.rect(WIN, GRAY, (j * 100 + 50, len(guesses) * 100 + 50, 90, 90))
                draw_text(char, j * 100 + 75, len(guesses) * 100 + 65, WHITE)

        # Малювання рамок
        for i in range(attempts):
            for j in range(5):
                pygame.draw.rect(WIN, BLACK, (j * 100 + 50, i * 100 + 50, 90, 90), 2)

        # Малювання клавіатури
        draw_keyboard()

        # Відображення повідомлення
        if message:
            x = WIDTH // 2 - len(message) * 12
            if x < 0:
                x = 0
            draw_text(message, x, 10, RED, font=MESSAGE_FONT)  # Повідомлення зверху
            if game_over:
                draw_text("Натисніть 'R' для повтору", WIDTH // 2 - 150, HEIGHT - 50, BLACK,
                          font=MESSAGE_FONT)  # Повідомлення внизу

        pygame.display.update()
        clock.tick(30)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    print(secret_word)  # Для відладки
    main()
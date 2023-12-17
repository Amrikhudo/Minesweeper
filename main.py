import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Параметры игрового поля
GRID_SIZE = 15  # Больше ячеек
CELL_SIZE = 30  # Больший размер ячейки
WIDTH, HEIGHT = GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE + 50  # Больше окно

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (192, 192, 192)

# Создание игрового поля
grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
mines = random.sample(range(GRID_SIZE * GRID_SIZE), GRID_SIZE)

for mine in mines:
    row = mine // GRID_SIZE
    col = mine % GRID_SIZE
    grid[row][col] = -1  # -1 представляет мину


# Функция подсчета мин вокруг ячейки
def count_mines(row, col):
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if 0 <= row + i < GRID_SIZE and 0 <= col + j < GRID_SIZE:
                if grid[row + i][col + j] == -1:
                    count += 1
    return count


# Отображение числа мин вокруг каждой ячейки
for i in range(GRID_SIZE):
    for j in range(GRID_SIZE):
        if grid[i][j] != -1:
            grid[i][j] = count_mines(i, j)


# Функция отрисовки текста на экране
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)


# Создание окна Pygame
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Сапёр")

# Основной игровой цикл
# Функция открытия ячеек рекурсивно
mine_image = pygame.transform.scale(pygame.image.load("mine.png"), (CELL_SIZE, CELL_SIZE))
flag_image = pygame.transform.scale(pygame.image.load("flag.png"), (CELL_SIZE, CELL_SIZE))


# Функция открытия ячеек рекурсивно
def reveal_cells(row, col):
    revealed_cells.add((row, col))

    if grid[row][col] == 0:
        for i in range(-1, 2):
            for j in range(-1, 2):
                new_row, new_col = row + i, col + j
                if 0 <= new_row < GRID_SIZE and 0 <= new_col < GRID_SIZE and (new_row, new_col) not in revealed_cells:
                    reveal_cells(new_row, new_col)


# Создание окна Pygame
pygame.init()
pygame.display.set_caption("Сапёр")

# Основной игровой цикл
running = True
font = pygame.font.Font(None, 36)
revealed_cells = set()
flagged_cells = set()
mines_flagged = 0
mines_total = GRID_SIZE  # Измените это на количество мин, чтобы победить
score = 0  # Добавлен счет

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            row = y // CELL_SIZE
            col = x // CELL_SIZE

            if event.button == 1:  # Левая кнопка мыши
                if grid[row][col] == -1:
                    running = False
                else:
                    reveal_cells(row, col)
                    score += 1  # Увеличиваем счет при открытии безопасной ячейки
            elif event.button == 3:  # Правая кнопка мыши
                if (row, col) not in revealed_cells:
                    if (row, col) in flagged_cells:
                        flagged_cells.remove((row, col))
                        if grid[row][col] == -1:
                            mines_flagged -= 1
                    else:
                        flagged_cells.add((row, col))
                        if grid[row][col] == -1:
                            mines_flagged += 1

    # Отрисовка поля
    screen.fill(WHITE)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            cell_rect = pygame.Rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, GRAY, cell_rect, 1)

            if (i, j) in revealed_cells:
                if grid[i][j] == -1:
                    screen.blit(mine_image, cell_rect)
                else:
                    text = str(grid[i][j])
                    draw_text(text, font, BLACK, screen, j * CELL_SIZE + 10, i * CELL_SIZE + 10)

            if (i, j) in flagged_cells:
                screen.blit(flag_image, cell_rect)

    # Проверка на победу
    if mines_flagged == mines_total:
        draw_text("Поздравляю! Вы выиграли!", font, BLACK, screen, WIDTH // 2 - 150, HEIGHT // 2 - 25)
        draw_text(f"Ваш счет: {score}", font, BLACK, screen, WIDTH // 2 - 120, HEIGHT // 2 + 25)
        pygame.display.flip()
        pygame.time.wait(3000)  # Ждем 3 секунды после победы
        running = False

    # Если проигрыш - показываем счет и поздравление
    if not running:
        screen.fill((0, 0, 0))  # Очищаем экран перед салютом
        draw_text("Вы проиграли!", font, WHITE, screen, WIDTH // 2 - 150, HEIGHT // 2 - 25)
        draw_text(f"Ваш счет: {score}", font, WHITE, screen, WIDTH // 2 - 120, HEIGHT // 2 + 25)

        # Эффект "салюта"

        pygame.display.flip()
        pygame.time.wait(3000)  # Ждем 3 секунды перед завершением
        pygame.quit()
        sys.exit()

    # Эффект "салюта"

    # Обновление экрана
    pygame.display.flip()

# Завершение игры
pygame.quit()

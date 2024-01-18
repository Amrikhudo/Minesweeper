import pygame
import random
import sys

# Инициализация Pygame
pygame.init()
pygame.mixer.init()


# Параметры игрового поля
GRID_SIZE = 15 
CELL_SIZE = 30 
WIDTH, HEIGHT = GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE + 50  


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (192, 192, 192)
OLIVE = (128, 128, 0)


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


# картинки
mine_image = pygame.transform.scale(pygame.image.load("mine.png"), (CELL_SIZE, CELL_SIZE))
flag_image = pygame.transform.scale(pygame.image.load("flag.png"), (CELL_SIZE, CELL_SIZE))


# Звуковые эффекты
click_sound = pygame.mixer.Sound("click_sound.wav")
explosion_sound = pygame.mixer.Sound("explosion_sound.wav")


# Фоновая музыка
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.play(-1)  # -1 бесконечное воспроизведение



# Функция открытия ячеек рекурсивно
def reveal_cells(row, col):
    revealed_cells.add((row, col))

    if grid[row][col] == 0:
        for i in range(-1, 2):
            for j in range(-1, 2):
                new_row, new_col = row + i, col + j
                if 0 <= new_row < GRID_SIZE and 0 <= new_col < GRID_SIZE and (new_row, new_col) not in revealed_cells:
                    reveal_cells(new_row, new_col)


# Основной игровой цикл
running = True
font = pygame.font.Font(None, 36)
revealed_cells = set()
flagged_cells = set()
mines_flagged = 0
mines_total = 20  # это количество мин, чтобы победить
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
                    click_sound.play()
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
                            click_sound.play()

    
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


        def draw_gradient(screen, top_color, bottom_color):
            height = screen.get_height()
            for i in range(height):
                color = (
                    top_color[0] + (bottom_color[0] - top_color[0]) * i / height,
                    top_color[1] + (bottom_color[1] - top_color[1]) * i / height,
                    top_color[2] + (bottom_color[2] - top_color[2]) * i / height
                )
                pygame.draw.line(screen, color, (0, i), (screen.get_width(), i))

        # Голубой
                
        top_color = (102, 205, 170)
        # Черный

        bottom_color = (0, 0, 0)

        
        # блок отрисовки фона при проигрыше на:

        if not running:
            draw_gradient(screen, top_color, bottom_color)
            
            draw_text("Вы проиграли!", font, OLIVE, screen, WIDTH // 2 - 100, HEIGHT // 2 - 25)
            draw_text(f"Ваш счет: {score}", font, OLIVE, screen, WIDTH // 2 - 80, HEIGHT // 2 + 25)

            pygame.display.flip()
            pygame.time.wait(3000)
            pygame.quit()
            sys.exit()

        
        # И аналогично при выигрыше: 

        if mines_flagged == mines_total:
            draw_gradient(screen, top_color, bottom_color)

            draw_text("Поздравляю! Вы выиграли!", font, OLIVE, screen, WIDTH // 2 - 150, HEIGHT // 2 - 25)
            draw_text(f"Ваш счет: {score}", font, OLIVE, screen, WIDTH // 2 - 120, HEIGHT // 2 + 25)

            
            pygame.display.flip()
            pygame.time.wait(3000)
            running = False

    
    pygame.display.flip()


pygame.quit()

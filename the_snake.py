import random

import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
SPEED = 20

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов"""

    def __init__(self, position=None, body_color=None):
        self.position = position if position else (
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = body_color

    def draw(self, surface):
        """Отрисовка объекта"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс для яблока"""

    def __init__(self, occupied_positions=None):
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions=None):
        """Случайное размещение яблока на поле"""
        occupied_positions = occupied_positions if occupied_positions else []
        while True:
            x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            position = (x, y)

            if position not in occupied_positions:
                self.position = position
                return


class Snake(GameObject):
    """Класс для змейки"""

    def __init__(self):
        super().__init__(body_color=SNAKE_COLOR)
        self.reset()

    def get_head_position(self):
        """Возвращает позицию головы змейки"""
        return self.positions[0] if self.positions else self.position

    def reset(self):
        """Сброс змейки в начальное состояние"""
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.length = 1
        self.grow_to = 1

    def update_direction(self):
        """Обновление направления движения"""
        if self.next_direction:
            # Запрещаем разворот на 180 градусов
            if (self.next_direction[0] * -1,
                    self.next_direction[1] * -1) != self.direction:
                self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Движение змейки"""
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction
        new_x = (head_x + dir_x * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head_y + dir_y * GRID_SIZE) % SCREEN_HEIGHT
        new_position = (new_x, new_y)

        # Добавляем новую голову
        self.positions.insert(0, new_position)

        # Удаляем хвост, если не нужно расти
        if len(self.positions) > self.grow_to:
            self.positions.pop()

        self.length = len(self.positions)

    def draw(self, surface):
        """Отрисовка змейки"""
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

    def check_collision(self):
        """Проверка столкновений с собой"""
        return self.positions[0] in self.positions[1:]


def handle_keys(snake):
    """Обработка нажатий клавиш"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT:
                snake.next_direction = RIGHT
    return True


def main():
    """Основная игровая функция"""
    snake = Snake()
    apple = Apple(snake.positions)
    running = True

    while running:
        clock.tick(SPEED)

        running = handle_keys(snake)
        if not running:
            break

        snake.update_direction()
        snake.move()

        # Проверка столкновения с яблоком
        if snake.positions[0] == apple.position:
            snake.grow_to += 1
            apple.randomize_position(snake.positions)

        # Проверка столкновения с собой
        elif snake.check_collision():
            snake.reset()

        # Отрисовка
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw(screen)
        snake.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()

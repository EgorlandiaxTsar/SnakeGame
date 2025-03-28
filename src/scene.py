import random as r

import utils as u
from entities import SnakeDot, Apple, MovementDirection


class GameScene:
    def __init__(self, size, start_snake_length=5):
        self.__size = (u.require_int(size, 'size') / 2) - 1
        self.__start_snake_length = u.require_int(start_snake_length, 'start_snake_length')
        self.__snake = []
        self.__apples = []
        self.__movement_direction = MovementDirection.RIGHT
        for i in range(0, self.__start_snake_length):
            self.__snake.append(SnakeDot(i, 0))
        self.__snake[self.__start_snake_length - 1].set_head_dot()

    def __generate_apple_coords(self):
        max_attempts_count = self.__size * self.__size
        attempts_count = 0
        while attempts_count < max_attempts_count:
            x, y = r.randint(0, self.__size), r.randint(0, self.__size)
            if all(snake_dot.get_x() != x or snake_dot.get_y() != y for snake_dot in self.__snake):
                return {'x': x, 'y': y}

            attempts_count += 1
        return {'x': -1, 'y': -1}

    def __check_movement_direction(self, movement_direction):
        movement_direction = u.require_object(movement_direction, MovementDirection, 'movement_direction')
        match movement_direction:
            case MovementDirection.UP:
                if self.__movement_direction == MovementDirection.DOWN:
                    return self.__movement_direction
            case MovementDirection.DOWN:
                if self.__movement_direction == MovementDirection.UP:
                    return self.__movement_direction
            case MovementDirection.LEFT:
                if self.__movement_direction == MovementDirection.RIGHT:
                    return self.__movement_direction
            case MovementDirection.RIGHT:
                if self.__movement_direction == MovementDirection.LEFT:
                    return self.__movement_direction
        return movement_direction

    def __handle_apple_collision(self, head_dot):
        head_dot = u.require_object(head_dot, SnakeDot, 'head_dot')
        for apple in self.__apples:
            if apple.get_x() == head_dot.get_x() and apple.get_y() == head_dot.get_y():
                self.__eat_apple(apple)
                break

    def __eat_apple(self, apple):
        apple = u.require_object(apple, Apple, 'apple')
        self.__apples.remove(apple)
        last_snake_dot = self.__snake[0]
        new_snake_dot = SnakeDot(last_snake_dot.get_previous_x(), last_snake_dot.get_previous_y())
        self.__snake.insert(0, new_snake_dot)

    def spawn_apple(self):
        cords = self.__generate_apple_coords()
        self.__apples.append(Apple(cords['x'], cords['y']))

    def move_snake(self, movement_direction):
        movement_direction = u.require_object(movement_direction, MovementDirection, 'movement_direction')
        movement_direction = self.__check_movement_direction(movement_direction)
        next_position = None
        is_direction_changed = movement_direction != self.__movement_direction
        for snake_dot in reversed(self.__snake):
            if snake_dot.is_head_dot():
                match movement_direction:
                    case MovementDirection.UP:
                        snake_dot.move_y(snake_dot.get_y() - 1, is_direction_changed)
                    case MovementDirection.DOWN:
                        snake_dot.move_y(snake_dot.get_y() + 1, is_direction_changed)
                    case MovementDirection.LEFT:
                        snake_dot.move_x(snake_dot.get_x() - 1, is_direction_changed)
                    case MovementDirection.RIGHT:
                        snake_dot.move_x(snake_dot.get_x() + 1, is_direction_changed)

                next_position = snake_dot.get_previous_position()
                self.__handle_apple_collision(snake_dot)
            else:
                snake_dot.move(next_position['x'], next_position['y'])
                next_position = snake_dot.get_previous_position()
        self.__movement_direction = movement_direction

    def is_game_over(self):
        head_snake_dot = None
        for snake_dot in reversed(self.__snake):
            if snake_dot.is_head_dot():
                head_snake_dot = snake_dot
                break
        if head_snake_dot is None:
            return True
        if (
                head_snake_dot.get_x() > self.__size
                or head_snake_dot.get_y() > self.__size
                or head_snake_dot.get_x() < 0
                or head_snake_dot.get_y() < 0
        ):
            return True
        is_colliding_with_self = False
        for snake_dot in self.__snake:
            if (
                    not snake_dot.is_head_dot()
                    and snake_dot.get_x() == head_snake_dot.get_x()
                    and snake_dot.get_y() == head_snake_dot.get_y()
            ):
                is_colliding_with_self = True
        if is_colliding_with_self:
            return True
        return False

    def get_movement_direction(self):
        return self.__movement_direction

    def get_snake(self):
        return self.__snake

    def get_apples(self):
        return self.__apples

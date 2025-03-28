from enum import Enum

import utils as u


class SnakeDot:
    def __init__(self, x, y, is_head_dot=False):
        self.__x = u.require_int(x, 'x')
        self.__y = u.require_int(y, 'y')
        self.__is_head_dot = is_head_dot
        self.__previous_position = {'x': x, 'y': y}

    def set_head_dot(self, is_head_dot=True):
        self.__is_head_dot = is_head_dot

    def is_head_dot(self):
        return self.__is_head_dot

    def move(self, x, y):
        self.move_x(x)
        self.move_y(y)

    def move_x(self, x, is_direction_changed=False):
        y = self.__previous_position['y']
        if is_direction_changed:
            y = self.__y
        self.__previous_position = {'x': self.__x, 'y': y}
        self.__x = u.require_int(x, 'x')

    def move_y(self, y, is_direction_changed=False):
        x = self.__previous_position['x']
        if is_direction_changed:
            x = self.__x
        self.__previous_position = {'x': x, 'y': self.__y}
        self.__y = u.require_int(y, 'y')

    def get_position(self):
        return {'x': self.__x, 'y': self.__y}

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_previous_position(self):
        return self.__previous_position

    def get_previous_x(self):
        return self.__previous_position['x']

    def get_previous_y(self):
        return self.__previous_position['y']


class Apple:
    def __init__(self, x, y):
        self.__x = u.require_int(x, 'x')
        self.__y = u.require_int(y, 'y')

    def get_position(self):
        return {'x': self.__x, 'y': self.__y}

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y


class MovementDirection(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

import time as t
from concurrent.futures import ThreadPoolExecutor
from enum import Enum

import pygame as p

import utils as u
from entities import MovementDirection
from scene import GameScene


class Gameplay:
    def __init__(self):
        self.__action_on_close = ActionOnClose.CLOSE
        self.__scene_size = 64
        self.__game_scene = GameScene(self.__scene_size)
        self.__apple_color = 161, 22, 22
        self.__snake_color = 255, 255, 255
        self.__game_flow_color = 17, 17, 17
        self.__background_color = 34, 34, 34
        self.__game_flow_size = self.__scene_size * 10
        self.__grid_element_size = 20
        self.__run = True
        p.init()
        p.display.set_caption('Snake Game')
        p.display.set_icon(p.image.load('res/logo.png'))
        self.__font = p.font.SysFont('Helvetica', 24)
        self.__screen = p.display.set_mode((1280, 800), p.RESIZABLE)
        self.__game_flow = p.Rect(0, 0, self.__game_flow_size, self.__game_flow_size)

    def __render(self):
        p.display.update()
        screen_width, screen_height = p.display.get_surface().get_size()
        self.__screen.fill(self.__background_color)
        game_flow_position = (
            u.calculate_center_position(
                self.__game_flow_size, self.__game_flow_size,
                screen_width, screen_height
            )
        )
        self.__game_flow.update(
            game_flow_position['x'],
            game_flow_position['y'],
            self.__game_flow_size,
            self.__game_flow_size
        )
        p.draw.rect(self.__screen, self.__game_flow_color, self.__game_flow)
        self.__draw_snake(game_flow_position)
        self.__draw_apples(game_flow_position)
        self.__draw_text('Score: ' + str(len(self.__game_scene.get_snake()) * 100), self.__font, (255, 255, 255), 15,
                         15)
        self.__run = not self.__game_scene.is_game_over()
        self.__handle_events()

    def _game_over_render(self):
        p.display.update()
        self.__screen.fill(self.__background_color)
        self.__draw_text(
            'Game Over! Your score is: '
            + str(len(self.__game_scene.get_snake()) * 100)
            + ' points. Press \'R\' to restart or \'ESC\' to close the game',
            self.__font,
            (255, 255, 255),
            15,
            15
        )
        self.__handle_game_over_events()

    def __async_movement_update(self):
        while self.__run:
            self.__game_scene.move_snake(self.__game_scene.get_movement_direction())
            t.sleep(0.15)

    def __async_apple_spawner(self):
        while self.__run:
            self.__game_scene.spawn_apple()
            t.sleep(3.5)

    def __draw_snake(self, position):
        for snake_dot in self.__game_scene.get_snake():
            p.draw.rect(
                self.__screen,
                self.__snake_color,
                p.Rect(
                    (
                        snake_dot.get_x() * self.__grid_element_size + position['x'],
                        snake_dot.get_y() * self.__grid_element_size + position['y'],
                        self.__grid_element_size,
                        self.__grid_element_size
                    )
                )
            )

    def __draw_apples(self, position):
        for apple in self.__game_scene.get_apples():
            p.draw.rect(
                self.__screen,
                self.__apple_color,
                p.Rect(
                    (
                        apple.get_x() * self.__grid_element_size + position['x'],
                        apple.get_y() * self.__grid_element_size + position['y'],
                        self.__grid_element_size,
                        self.__grid_element_size
                    )
                )
            )

    def __draw_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        self.__screen.blit(img, (x, y))

    def __handle_events(self):
        for event in p.event.get():
            if event.type == p.QUIT:
                self.__run = False
            elif event.type == p.KEYUP:
                if (
                        (
                                event.key == p.K_a
                                or event.key == p.K_LEFT
                        )
                        and self.__game_scene.get_movement_direction() != MovementDirection.LEFT
                ):
                    self.__game_scene.move_snake(MovementDirection.LEFT)
                elif (
                        (
                                event.key == p.K_w
                                or event.key == p.K_UP
                        )
                        and self.__game_scene.get_movement_direction() != MovementDirection.UP
                ):
                    self.__game_scene.move_snake(MovementDirection.UP)
                elif (
                        (
                                event.key == p.K_s
                                or event.key == p.K_DOWN
                        )
                        and self.__game_scene.get_movement_direction() != MovementDirection.DOWN
                ):
                    self.__game_scene.move_snake(MovementDirection.DOWN)
                elif (
                        (
                                event.key == p.K_d
                                or event.key == p.K_RIGHT
                        )
                        and self.__game_scene.get_movement_direction() != MovementDirection.RIGHT
                ):
                    self.__game_scene.move_snake(MovementDirection.RIGHT)

    def __handle_game_over_events(self):
        for event in p.event.get():
            if event.type == p.QUIT:
                self.__run = False
            elif event.type == p.KEYUP:
                if event.key == p.K_ESCAPE:
                    self.__run = False
                elif event.key == p.K_r:
                    self.__action_on_close = ActionOnClose.RESTART
                    self.__run = False

    def run(self):
        pool = ThreadPoolExecutor(2)
        pool.submit(self.__async_movement_update)
        pool.submit(self.__async_apple_spawner)
        while self.__run:
            self.__render()
        pool.shutdown(False)
        self.__run = True
        while self.__run:
            self._game_over_render()
        p.quit()

    def get_action_on_close(self):
        return self.__action_on_close


class ActionOnClose(Enum):
    RESTART = 0
    CLOSE = 1

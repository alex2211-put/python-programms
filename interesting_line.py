#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import random
import math

SCREEN_DIM = (800, 600)


class Vec2d:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vec2d(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2d(self.x - other.x, self.y - other.y)

    def __mul__(self, a: float):
        return Vec2d(self.x * a, self.y * a)

    #def int_pair(self):
    #   return tuple((self.x, self.y))

    def len(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)


class Polyline:
    points = []
    speeds = []

    def add(self, vec2d: Vec2d, v: Vec2d):
        self.points.append(vec2d)
        self.speeds.append(v)

    def set_points(self):
        for p in range(len(self.points)):
            self.points[p] = self.points[p] + self.speeds[p]
            if self.points[p].x > SCREEN_DIM[0] or self.points[p].x < 0:
                self.speeds[p] = Vec2d(- self.speeds[p].x, self.speeds[p].y)
            if self.points[p].y > SCREEN_DIM[1] or self.points[p].y < 0:
                self.speeds[p] = Vec2d(self.speeds[p].x, -self.speeds[p].y)

    def draw_points(self, points, style="points", width=3, color=(255, 255, 255), ):
        if style == "line":
            for p_n in range(-1, len(points) - 1):
                pygame.draw.line(gameDisplay, color,
                                 (int(points[p_n].x), int(points[p_n].y)),
                                 (int(points[p_n + 1].x), int(points[p_n + 1].y)), width)

        elif style == "points":
            for p in self.points:
                pygame.draw.circle(gameDisplay, color,
                                   (int(p.x), int(p.y)), width)


class Knot(Polyline):
    steps = 35

    def add(self, vec2d: Vec2d, v: Vec2d):
        super().add(vec2d, v)
        self.get_knot()

    def draw_points(self, points, style="points", width=3, color=(255, 255, 255)):
        super().draw_points(self.get_knot(), style, width, color)

    def get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return Vec2d(points[deg].x * alpha, points[deg].y * alpha)\
               + Vec2d(self.get_point(points, alpha, deg - 1).x * (1 - alpha),
                       self.get_point(points, alpha, deg - 1).y * (1 - alpha))

    def get_points(self, base_points):
        alpha = 1 / self.steps
        res = []
        for i in range(self.steps):
            res.append(self.get_point(base_points, i * alpha))
        return res

    def get_knot(self):
        if len(self.points) < 3:
            return []
        res = []
        for i in range(-2, len(self.points) - 2):
            ptn = []
            ptn.append((self.points[i] + self.points[i + 1])
                       * 0.5)
            ptn.append(self.points[i + 1])
            ptn.append((self.points[i + 1] + self.points[i + 2]) * 0.5)

            res.extend(self.get_points(ptn))
        return res


def draw_help(k):
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = [["F1", "Show Help"], ["R", "Restart"], ["P", "Pause/Play"], ["Ctrl+", "More points"],
            ["Ctrl-", "Less points"], ["", ""], [str(k.steps), "Current points"]]
    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
        (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * i))


if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    working = True
    k = Knot()
    show_help = False
    pause = True

    hue = 0
    color = pygame.Color(0)
    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    k.points = []
                    k.speeds = []
                    pause = True
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    k.steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    k.steps -= 1 if k.steps > 1 else 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                k.add(Vec2d(event.pos[0], event.pos[1]), Vec2d(random.random() * 2, random.random() * 2))

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        k.draw_points(k.points, 'points')
        k.draw_points(k.points, "line", 3, color)
        if not pause:
            k.set_points()
        if show_help:
            draw_help(k)

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)

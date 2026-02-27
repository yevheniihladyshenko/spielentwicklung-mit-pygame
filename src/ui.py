import pygame as pg


class Menu:
    def __init__(self, title: str, items: list[str]):
        self.title = title
        self.items = items
        self.index = 0

    def move(self, delta: int) -> None:
        self.index = (self.index + delta) % len(self.items)

    def selected(self) -> str:
        return self.items[self.index]


def draw_center_text(screen: pg.Surface, text: str, font: pg.font.Font, y: int) -> None:
    surf = font.render(text, True, (240, 240, 240))
    rect = surf.get_rect(center=(screen.get_width() // 2, y))
    screen.blit(surf, rect)


def draw_menu(
    screen: pg.Surface,
    menu: Menu,
    font_title: pg.font.Font,
    font_item: pg.font.Font
) -> None:
    screen.fill((18, 18, 22))
    draw_center_text(screen, menu.title, font_title, 110)

    start_y = 220
    step = 44
    for i, item in enumerate(menu.items):
        prefix = "▶ " if i == menu.index else "  "
        color = (255, 255, 255) if i == menu.index else (170, 170, 170)

        surf = font_item.render(prefix + item, True, color)
        rect = surf.get_rect(center=(screen.get_width() // 2, start_y + i * step))
        screen.blit(surf, rect)

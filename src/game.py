import pygame as pg
from settings import Settings
from storage import load_highscore, save_highscore
from ui import Menu, draw_menu, draw_center_text

DIRS = {
    pg.K_UP: (0, -1),
    pg.K_DOWN: (0, 1),
    pg.K_LEFT: (-1, 0),
    pg.K_RIGHT: (1, 0),
}


def run() -> None:
    pg.init()
    s = Settings()
    screen = pg.display.set_mode((s.width, s.height))
    pg.display.set_caption("Spielentwicklung mit Python (Pygame)")
    clock = pg.time.Clock()

    font_title = pg.font.SysFont("Segoe UI", 44, bold=True)
    font_item = pg.font.SysFont("Segoe UI", 26)
    font_small = pg.font.SysFont("Segoe UI", 20)

    highscore = load_highscore()

    main_menu = Menu("Pygame Portfolio", ["Start", "Difficulty: Normal", "Exit"])
    state = "menu"  # menu | game | pause | gameover

    grid = s.grid
    cols = s.width // grid
    rows = s.height // grid

    snake: list[tuple[int, int]] = []
    direction = (1, 0)
    food = (0, 0)
    score = 0
    last_move_ms = 0

    def spawn_food() -> None:
        nonlocal food
        for i in range(500):
            x = (pg.time.get_ticks() * 37 + i * 13) % cols
            y = (pg.time.get_ticks() * 17 + i * 29) % rows
            if (x, y) not in snake:
                food = (x, y)
                return

    def new_game() -> None:
        nonlocal snake, direction, food, score, last_move_ms, state
        snake = [(cols // 2, rows // 2)]
        direction = (1, 0)
        food = (cols // 2 + 5, rows // 2)
        score = 0
        last_move_ms = 0
        state = "game"

    def draw_grid() -> None:
        for x in range(0, s.width, grid):
            pg.draw.line(screen, (28, 28, 34), (x, 0), (x, s.height))
        for y in range(0, s.height, grid):
            pg.draw.line(screen, (28, 28, 34), (0, y), (s.width, y))

    def draw_game() -> None:
        screen.fill((18, 18, 22))
        draw_grid()

        fx, fy = food
        pg.draw.rect(
            screen,
            (255, 120, 90),
            pg.Rect(fx * grid, fy * grid, grid, grid),
            border_radius=6,
        )

        for i, (x, y) in enumerate(snake):
            c = (120, 220, 170) if i == 0 else (90, 180, 140)
            pg.draw.rect(
                screen,
                c,
                pg.Rect(x * grid, y * grid, grid, grid),
                border_radius=6,
            )

        hud = font_small.render(
            f"Score: {score}   Highscore: {highscore}   Difficulty: {s.difficulty}",
            True,
            (210, 210, 210),
        )
        screen.blit(hud, (12, 10))

    running = True
    while running:
        clock.tick(s.fps)
        now = pg.time.get_ticks()

        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False

            if e.type == pg.KEYDOWN:
                if state == "menu":
                    if e.key in (pg.K_UP, pg.K_w):
                        main_menu.move(-1)
                    if e.key in (pg.K_DOWN, pg.K_s):
                        main_menu.move(1)

                    if e.key in (pg.K_RETURN, pg.K_KP_ENTER):
                        sel = main_menu.selected()
                        if sel == "Start":
                            new_game()
                        elif sel.startswith("Difficulty:"):
                            s.difficulty = {"Easy": "Normal", "Normal": "Hard", "Hard": "Easy"}[s.difficulty]
                            main_menu.items[1] = f"Difficulty: {s.difficulty}"
                        elif sel == "Exit":
                            running = False

                elif state == "game":
                    if e.key in DIRS:
                        nd = DIRS[e.key]
                        if nd != (-direction[0], -direction[1]):
                            direction = nd

                    if e.key == pg.K_p:
                        state = "pause"
                    if e.key == pg.K_ESCAPE:
                        state = "menu"

                elif state == "pause":
                    if e.key == pg.K_p:
                        state = "game"
                    if e.key == pg.K_ESCAPE:
                        state = "menu"

                elif state == "gameover":
                    if e.key == pg.K_r:
                        new_game()
                    if e.key == pg.K_ESCAPE:
                        state = "menu"

        if state == "game":
            if now - last_move_ms >= s.tick_ms():
                last_move_ms = now

                hx, hy = snake[0]
                dx, dy = direction
                nx, ny = hx + dx, hy + dy

                if nx < 0 or nx >= cols or ny < 0 or ny >= rows:
                    state = "gameover"
                else:
                    new_head = (nx, ny)
                    if new_head in snake:
                        state = "gameover"
                    else:
                        snake.insert(0, new_head)
                        if new_head == food:
                            score += 1
                            spawn_food()
                        else:
                            snake.pop()

                if state == "gameover":
                    if score > highscore:
                        highscore = score
                        save_highscore(highscore)

        if state == "menu":
            draw_menu(screen, main_menu, font_title, font_item)

        elif state == "game":
            draw_game()

        elif state == "pause":
            draw_game()
            overlay = pg.Surface((s.width, s.height), pg.SRCALPHA)
            overlay.fill((0, 0, 0, 140))
            screen.blit(overlay, (0, 0))
            draw_center_text(screen, "PAUSE", font_title, s.height // 2 - 30)
            draw_center_text(screen, "P: weiter   ESC: Menü", font_item, s.height // 2 + 30)

        elif state == "gameover":
            draw_game()
            overlay = pg.Surface((s.width, s.height), pg.SRCALPHA)
            overlay.fill((0, 0, 0, 170))
            screen.blit(overlay, (0, 0))
            draw_center_text(screen, "GAME OVER", font_title, s.height // 2 - 50)
            draw_center_text(screen, f"Score: {score}   Highscore: {highscore}", font_item, s.height // 2)
            draw_center_text(screen, "R: Neustart   ESC: Menü", font_item, s.height // 2 + 50)

        pg.display.flip()

    pg.quit()

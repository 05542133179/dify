import curses
import random
from typing import List, Tuple

# Directions
UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)
DIRECTIONS = {curses.KEY_UP: UP, curses.KEY_DOWN: DOWN,
              curses.KEY_LEFT: LEFT, curses.KEY_RIGHT: RIGHT}


class SnakeGame:
    """Simple terminal-based snake game using curses."""

    def __init__(self, stdscr: curses.window) -> None:
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()
        self.snake: List[Tuple[int, int]] = [
            (self.height // 2, self.width // 2 + i) for i in range(3)
        ]
        self.direction = LEFT
        self.food = self._new_food()
        self.stdscr.nodelay(True)
        curses.curs_set(0)

    def _new_food(self) -> Tuple[int, int]:
        while True:
            pos = (
                random.randint(1, self.height - 2),
                random.randint(1, self.width - 2),
            )
            if pos not in self.snake:
                return pos

    def _move(self) -> None:
        head_y, head_x = self.snake[0]
        dir_y, dir_x = self.direction
        new_head = (head_y + dir_y, head_x + dir_x)
        self.snake.insert(0, new_head)
        if new_head == self.food:
            self.food = self._new_food()
        else:
            self.snake.pop()

    def _draw(self) -> None:
        self.stdscr.clear()
        for y, x in self.snake:
            if 0 <= y < self.height and 0 <= x < self.width:
                self.stdscr.addch(y, x, "#")
        fy, fx = self.food
        self.stdscr.addch(fy, fx, "*")
        self.stdscr.refresh()

    def _collision(self) -> bool:
        head_y, head_x = self.snake[0]
        if (
            head_y in {0, self.height - 1}
            or head_x in {0, self.width - 1}
            or (head_y, head_x) in self.snake[1:]
        ):
            return True
        return False

    def run(self) -> None:
        while True:
            try:
                key = self.stdscr.getch()
                if key in DIRECTIONS:
                    new_dir = DIRECTIONS[key]
                    # prevent reversing directly
                    if (
                        new_dir[0] != -self.direction[0]
                        or new_dir[1] != -self.direction[1]
                    ):
                        self.direction = new_dir
                self._move()
                if self._collision():
                    break
                self._draw()
                curses.napms(100)
            except KeyboardInterrupt:
                break


def main(stdscr: curses.window) -> None:
    game = SnakeGame(stdscr)
    game.run()


if __name__ == "__main__":
    curses.wrapper(main)

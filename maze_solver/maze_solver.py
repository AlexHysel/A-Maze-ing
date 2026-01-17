from maze_generator.models import CellType, Maze, Cell
from collections import deque


class MazeSolver():
    def shortest_path(maze: Maze) -> list[tuple[int, int]]:
        entry = maze.get_entry()

        rows = maze.get_height()
        cols = maze.get_width()
        queue = deque([entry])

        parent = {entry: None}
        while queue:
            curr = queue.popleft()
            x, y = curr

            if maze.get_cell(x, y).get_type() == CellType.EXIT:
                path = []
                while curr is not None:
                    path.append(curr)
                    curr = parent[curr]
                return path[::-1]

            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nxt = (x + dx, y + dy)
                nx, ny = nxt

                if not (0 <= nx < cols and 0 <= ny < rows):
                    continue
                
                if nxt in parent:
                    continue

                can_move = False
                curr_cell = maze.get_cell(x, y)
                
                if dy == 1:
                    can_move = not curr_cell.bottom_wall
                elif dy == -1:
                    can_move = not maze.get_cell(nx, ny).bottom_wall
                elif dx == 1:
                    can_move = not curr_cell.right_wall
                elif dx == -1:
                    can_move = not maze.get_cell(nx, ny).right_wall

                if can_move:
                    parent[nxt] = curr
                    queue.append(nxt)

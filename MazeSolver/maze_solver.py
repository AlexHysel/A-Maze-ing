from maze_generator.models import CellType, Maze
from collections import deque


class MazeSolver():
    @staticmethod
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

    @staticmethod
    def get_path_str(path: list[tuple[int, int]]) -> str:
        path_str: str = ""
        for i in range(len(path) - 1):
            dx = path[i + 1][0] - path[i][0]
            dy = path[i + 1][1] - path[i][1]
            if dx == 0 and dy == -1:  # N
                path_str += 'N'
            elif dx == 1 and dy == 0:  # E
                path_str += 'E'
            elif dx == 0 and dy == 1:  # S
                path_str += 'S'
            elif dx == -1 and dy == 0:  # W
                path_str += 'W'
            else:
                raise Exception('Invalid move in path given')
        if len(path_str) < 1:
            raise Exception('Invalid path given')
        return path_str

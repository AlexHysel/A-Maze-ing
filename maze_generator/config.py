# andmarti
# a_maze_ing

from typing import Any


class Config:
    def __init__(
            self,
            width: int,
            height: int,
            entry_idx: int,
            exit_idx: int,
            output_file: str | None = None,
            is_perfect: bool | None = None,
            seed: int | None = None) -> None:
        self.width = width
        self.height = height
        self.entry_idx = entry_idx
        self.exit_idx = exit_idx
        self.output_file = output_file
        self.is_perfect = is_perfect
        self.seed = seed

    @classmethod
    def from_file(cls, filename: str) -> "Config":
        all_keys: dict[str, dict[str, Any]] = {
                "WIDTH": {
                    # PFunk
                    "p_func": cls._parse_int,
                    "required": True,
                    "val": None,
                },
                "HEIGHT": {
                    "p_func": cls._parse_int,
                    "required": True,
                    "val": None,
                },
                "ENTRY": {
                    "p_func": cls._parse_tuple,
                    "required": True,
                    "val": None,
                },
                "EXIT": {
                    "p_func": cls._parse_tuple,
                    "required": True,
                    "val": None,
                },
                "OUTPUT_FILE": {
                    "p_func": cls._parse_filename,

# andmarti

from typing import Any


class Config:
    def __init__(
            self,
            width: int,
            height: int,
            entry_pt: tuple[int, int],
            exit_pt: tuple[int, int],
            output_file: str | None = None,
            is_perfect: bool | None = None,
            seed: int | None = None) -> None:
        self.width = width
        self.height = height
        self.entry_pt = entry_pt
        self.exit_pt = exit_pt
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
                    "required": True,
                    "val": None,
                },
                "PERFECT": {
                    "p_func": cls._parse_bool,
                    "required": True,
                    "val": None,
                },
                "SEED": {
                    "p_func": cls._parse_seed,
                    "required": False,
                    "val": 'random',
                }
            }

        required_keys: set[str] = {
                key
                for key in all_keys.keys()
                if all_keys[key]["required"] is True
            }
        parsed_keys: set[str] = set()

        # check if has .txt ext
        filename_split: list[str] = filename.rsplit('.', 1)
        if filename_split[1] != 'txt':
            raise ValueError('file extension must be .txt for config file')

        # read the file
        key: str
        value_str: str
        with open(filename, 'r', encoding="utf-8") as f:
            for line in f:
                if line.strip() == "":
                    continue
                elif line[0] == '#':
                    continue
                key, value_str = line.split("=", 1)
                if key in parsed_keys:
                    raise ValueError('no duplicate configurations')
                elif key in required_keys:
                    parsed_keys.add(key)

                # actual assignment
                for i in all_keys.keys():
                    if key == i:
                        all_keys[i]["val"] = all_keys[i]["p_func"](value_str)

        # check that all mandatory keys were provided
        num_missing_keys = len(parsed_keys ^ required_keys)
        if num_missing_keys == 1:
            raise ValueError('1 mandatory key missing')
        elif num_missing_keys > 1:
            raise ValueError('{num_missing_keys} mandatory keys missing')

        return cls(
            all_keys["WIDTH"]["val"],
            all_keys["HEIGHT"]["val"],
            all_keys["ENTRY"]["val"],
            all_keys["EXIT"]["val"],
            all_keys["OUTPUT_FILE"]["val"],
            all_keys["PERFECT"]["val"],
            all_keys["SEED"]["val"]
        )

    @staticmethod
    def _parse_int(i_str: str) -> int:
        """use for width and height on config parser"""
        i: int = int(i_str.strip())
        if i <= 2:
            raise ValueError('value must be at least 2')
        return i

    @staticmethod
    def _parse_seed(s_str: str) -> str | int:
        """use for seed on config parser"""
        if s_str.strip().lower() == 'random':
            return 'random'
        return int(s_str.strip())

    @staticmethod
    def _coor_to_idx(coor: tuple[int, int], w: int, h: int) -> int:
        x: int
        y: int
        x, y = coor
        if x >= w:
            raise ValueError('coordinate out of range')
        if y >= h:
            raise ValueError('coordinate out of range')
        return x + y * w

    @staticmethod
    def _parse_tuple(t_str: str) -> tuple[int, int]:
        """use for entry and exit on config parser"""
        x: str | int
        y: str | int
        x, y = t_str.split(',', 1)
        x = int(x.strip())
        y = int(y.strip())
        return (x, y)

    @staticmethod
    def _parse_filename(f_str: str) -> str:
        """use for output_file on config parser"""
        f_str_split: list[str] = f_str.rsplit('.', 1)
        if f_str_split[1].strip() != 'txt':
            raise ValueError('file extension must be .txt for output filename')
        return f_str.strip()

    @staticmethod
    def _parse_bool(b_str: str) -> bool | None:
        """use for perfect on the config parser"""
        if b_str.strip().lower() == 'true':
            return True
        if b_str.strip().lower() == 'false':
            return False
        raise ValueError('key must be true or false')

    def print(self) -> None:
        print(f"output_file: {self.output_file}")
        print(f"dimensions: {self.width} x {self.height}")
        print(
            f"entry cell: {self.entry_pt % self.width} x " +
            f"{self.entry_pt // self.width}")
        print(
            f"exit cell: {self.exit_pt % self.width} x " +
            f"{self.exit_pt // self.width}")
        print(f"is_perfect: {self.is_perfect}")
        print(f"seed: {self.seed}")


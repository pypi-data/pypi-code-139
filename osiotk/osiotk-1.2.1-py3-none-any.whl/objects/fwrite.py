from dataclasses import dataclass, field


@dataclass(frozen=False, order=True)
class fwrite:
    name: str = field(init=True)
    content: str = field(init=True)
    is_abspath: bool = field(init=True)
    errors: str = field(init=True)
    encoding: str = field(init=True)
    exist_ok: bool = field(init=True)
    indent: int = field(init=True)

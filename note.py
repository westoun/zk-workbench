from typing import List, Tuple


class Note:
    text: str
    in_links: List["Note"]
    out_links: List["Note"]
    position: Tuple[float, float]

    def __init__(
        self,
        text: str,
        in_links: List["Note"] = [],
        out_links: List["Note"] = [],
        position: Tuple[float, float] = None,
    ):
        self.text = text
        self.in_links = in_links
        self.out_links = out_links
        self.position = position

    def __eq__(self, comparison: "Note"):
        return self.text == comparison.text

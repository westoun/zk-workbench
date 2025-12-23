import pickle
from random import random
import tkinter as tk
import tkinter.ttk as ttk
from typing import List

from note import Note


def determine_positions(notes: List[Note], parent_width: float, parent_height: float):
    # TODO: Remove duplicates, then compute positions
    # only for notes without.

    # TODO: Replace with more eloquent algorithm.

    for note in notes:
        if note.position is not None:
            continue

        random_x = random() * parent_width  # TODO: Add padding
        random_y = random() * parent_height

        note.position = (random_x, random_y)


class Whiteboard:
    name: str

    window: tk.Tk
    canvas: tk.Canvas
    canvas_width: float
    canvas_height: float
    notes: List[Note]

    def __init__(
        self, name: str, canvas_width: float = None, canvas_height: float = None
    ):
        self.name = name

        # TODO: Determine canvas width

        window = tk.Tk("Zettelkasten Workbench")
        # window.attributes('-fullscreen', True)

        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        window.geometry(f"{screen_width}x{screen_height}")

        if canvas_width is None:
            canvas_width = screen_width

        if canvas_height is None:
            canvas_height = screen_height

        canvas = tk.Canvas(window, bg="blue")
        canvas.pack(fill="both", expand=True)

        self.window = window
        self.canvas = canvas
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height

    def add_notes(self, notes: List[Note]) -> None:
        determine_positions(notes, self.canvas_width, self.canvas_height)

        self.notes = notes

        for note in notes:
            # TODO: Add rounded edges.
            label = tk.Label(self.canvas, text=note.text, padx=5, pady=5, bg="red")
            label.place(x=note.position[0], y=note.position[1])

            label._note = note

            label.bind("<Button-1>", self._on_drag_start)
            label.bind("<B1-Motion>", self._on_drag_motion)

        self._render_arrows()

    @classmethod
    def load(cls, path: str) -> "Whiteboard":
        # TODO: Determine canvas width
        pass

    def save(self, path: str) -> None:
        pass

    def run(self) -> None:
        # TODO: Raise exception if no
        self.window.mainloop()

    def _on_drag_start(self, event):
        widget = event.widget
        # widget.master.tag_raise(event.widget)  # Bring item to front
        widget._drag_start_x = event.x
        widget._drag_start_y = event.y

    def _on_drag_motion(self, event):
        widget = event.widget
        x = widget.winfo_x() - widget._drag_start_x + event.x
        y = widget.winfo_y() - widget._drag_start_y + event.y

        widget.place(x=x, y=y)
        widget._note.position = (x, y)

        self._render_arrows()

    def _render_arrows(self):
        # TODO: Conceive way to remove only affected arrows
        # according to https://blog.finxter.com/5-best-ways-to-delete-lines-from-a-python-tkinter-canvas/

        self.canvas.delete("arrow")

        for note in self.notes:
            for target_note in note.out_links:
                self.canvas.create_line(
                    note.position[0],
                    note.position[1],
                    target_note.position[0],
                    target_note.position[1],
                    arrow=tk.LAST,
                    tags=("arrow",),
                )

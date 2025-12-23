import pickle
from random import random
import tkinter as tk
import tkinter.ttk as ttk
from typing import List

from note import Note


def merge_notes(old_notes: List[Note], new_notes: List[Note]) -> List[Note]:
    merged_notes = []

    for old_note in old_notes:

        # Add new note, since it got more up to date
        # linkages.
        if old_note in new_notes:
            new_note_index = new_notes.index(old_note)
            new_note = new_notes[new_note_index]
            new_note.position = old_note.position

            merged_notes.append(new_note)
        else:
            merged_notes.append(old_note)

    for new_note in new_notes:
        if new_note not in merged_notes:
            merged_notes.append(new_note)

    return merged_notes


def update_note_positions(notes: List[Note], parent_width: float, parent_height: float):
    # TODO: Replace with more eloquent algorithm.

    for note in notes:
        # Compute positions only for notes that do not already
        # have a position.
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
        self,
        name: str = None,
        canvas_width: float = None,
        canvas_height: float = None,
    ):
        self.name = name

        # TODO: Determine canvas width

        if name is None:
            name = "Zettelkasten Workbench"

        window = tk.Tk(screenName=name)
        window.title(name)
        # window.attributes('-fullscreen', True)

        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        window.geometry(f"{screen_width}x{screen_height}")

        if canvas_width is None:
            canvas_width = screen_width

        if canvas_height is None:
            canvas_height = screen_height

        canvas = tk.Canvas(
            window,
            bg="blue",
        )
        canvas.pack(fill="both", expand=True)

        self.window = window
        self.canvas = canvas
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height

        self.notes = []

    def add_notes(self, notes: List[Note]) -> None:
        self.notes = merge_notes(self.notes, notes)

        update_note_positions(self.notes, self.canvas_width, self.canvas_height)

        for note in self.notes:
            # TODO: Add rounded edges.
            label = tk.Label(self.canvas, text=note.text, padx=10, pady=10, bg="red")
            label.place(x=note.position[0], y=note.position[1])

            label._note = note

            label.bind("<Button-1>", self._on_drag_start)
            label.bind("<B1-Motion>", self._on_drag_motion)

        self._render_arrows()

    @classmethod
    def load(cls, path: str) -> "Whiteboard":
        # TODO: Determine canvas width
        with open(path, "rb") as source_file:
            obj = pickle.load(source_file)
            whiteboard = Whiteboard(
                obj["name"], obj["canvas_width"], obj["canvas_height"]
            )
            whiteboard.add_notes(obj["notes"])
            return whiteboard

    def save(self, path: str) -> None:
        with open(path, "wb") as target_file:
            pickle.dump(
                {
                    "name": self.name,
                    "canvas_width": self.canvas_width,
                    "canvas_height": self.canvas_height,
                    "notes": self.notes,
                },
                target_file,
            )

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

from random import random
import tkinter as tk
import tkinter.ttk as ttk
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


def determine_positions(notes: List[Note], parent_width: float, parent_height: float):
    # TODO: Replace with more eloquent algorithm.

    for note in notes:
        if note.position is not None:
            continue

        random_x = random() * parent_width  # TODO: Add padding
        random_y = random() * parent_height

        note.position = (random_x, random_y)


def on_drag_start(event):
    widget = event.widget
    # widget.master.tag_raise(event.widget)  # Bring item to front
    widget._drag_start_x = event.x
    widget._drag_start_y = event.y


def on_drag_motion(event):
    widget = event.widget
    x = widget.winfo_x() - widget._drag_start_x + event.x
    y = widget.winfo_y() - widget._drag_start_y + event.y

    widget.place(x=x, y=y)
    widget._note.position = (x, y)

    render_arrows(canvas, notes)


def render_arrows(canvas: tk.Canvas, notes: List[Note]):
    # TODO: Conceive way to remove only affected arrows
    # according to https://blog.finxter.com/5-best-ways-to-delete-lines-from-a-python-tkinter-canvas/

    canvas.delete("arrow")

    for note in notes:
        for target_note in note.out_links:
            canvas.create_line(
                note.position[0],
                note.position[1],
                target_note.position[0],
                target_note.position[1],
                arrow=tk.LAST,
                tags=("arrow",),
            )


if __name__ == "__main__":

    # load zettels, tags, and related sources

    # TODO: Replace with actual data.
    note1 = Note("This is note 1")
    note2 = Note("This is note 2")
    note3 = Note("This is note 3")
    note4 = Note("This is note 4")
    note5 = Note("This is note 5")

    note1.out_links = [note2, note3]
    note2.out_links = [note3]

    notes = [note1, note2, note3, note4, note5]

    # filter them based on criteria
    # (in the future, make the filter criteria flexible)

    # transform to notes class with string and color.

    # render on whiteboard

    window = tk.Tk("Zettelkasten Workbench")

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    window.geometry(f"{screen_width}x{screen_height}")
    # window.attributes('-fullscreen', True)

    # TODO: Consider adjusting in the future
    canvas_width = screen_width
    canvas_height = screen_height

    canvas = tk.Canvas(window, bg="blue")
    canvas.pack(fill="both", expand=True)

    # compute relative position of notes
    determine_positions(notes, canvas_width, canvas_height)

    for note in notes:
        # TODO: Add rounded edges.
        label = tk.Label(canvas, text=note.text, padx=5, pady=5, bg="red")
        label.place(x=note.position[0], y=note.position[1])

        label._note = note

        label.bind("<Button-1>", on_drag_start)
        label.bind("<B1-Motion>", on_drag_motion)

    render_arrows(canvas, notes)

    # save results.

    window.mainloop()

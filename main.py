from typing import List

from note import Note
from whiteboard import Whiteboard


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

    whiteboard = Whiteboard("Test")

    whiteboard.add_notes(notes)
    whiteboard.run()

    # save results.

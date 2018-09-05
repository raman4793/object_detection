import os

import cv2
import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
import sqlite3

REVIEWABLE_SAFE = 'blue'
REVIEWED_SAFE = 'green'
REVIEWABLE_UNSAFE = 'orange'
REVIEWED_UNSAFE = 'red'

class HistoryWindow:

    items = []

    def __init__(self):
        self.conn = sqlite3.connect("test.db")
        self.item_count = self.conn.execute("SELECT COUNT(*) FROM history;").fetchone()[0]
        self.top = Tk()
        self.frame = VerticalScrolledFrame(self.top)
        self.frame.pack(fill=BOTH)
        self.top.geometry("1150x500")
        self.top.title("History")
        self.column_count = 3

        # Item(self.top, "history/safe_1536051647.7788084.jpg", 1, 0, 0)
        self.initialize()
        self.top.mainloop()

    def initialize(self):
        self.items = self.conn.execute("SELECT * FROM history")
        row = 0
        column = 0
        for item in self.items:
            item_frame = Item(self.frame.interior, os.path.join("history", item[1]), item[0], item[2], item[3], row, column)
            column += 1
            if self.column_count == column:
                row += 1
                column = 0
        self.conn.close()


class Item(Frame):
    verify_button = None
    mark_safe_button = None
    mark_unsafe_button = None
    mark_dont_care_button = None
    image_container = None
    image = None

    def __init__(self, parent, image_file, id, label, reviewed, row, column, width=300, height=200, borderwidth=2, relief="groove"):
        Frame.__init__(self, parent, width=width, height=height, borderwidth=borderwidth, relief=relief)
        self.row = row
        self.column = column
        self.reviewed = reviewed
        self.id = id
        self.label = 'safe' if label == 1 else 'unsafe'
        self.parent = parent
        self.image_file = image_file
        self.initialize()
        # print("row = {} column = {}".format(row, column))
        self.labels = {'1': 'safe', '2': 'unsafe'}

    def initialize(self):
        self.image = Image.open(self.image_file)
        self.image = self.image.resize((100, 100), Image.ANTIALIAS)
        # print(self.image)
        self.image = ImageTk.PhotoImage(self.image, size='100x100')
        # print(self.image)
        self.image_container = Label(self, image=self.image).grid(row=0, column=0, columnspan=2)
        self.class_label = Label(self, text=self.label).grid(row=0, column=2, columnspan=2)
        self.verify_button = Button(self, text="Verify", command=self.on_verify).grid(row=1, column=0)
        self.mark_safe_button = Button(self, text="Mark Safe", command=self.on_safe).grid(row=1, column=1)
        self.mark_unsafe_button = Button(self, text="Mark unsafe", command=self.on_unsafe).grid(row=1, column=2)
        self.mark_dont_care_button = Button(self, text="Mark don't care", command=self.on_dontcare).grid(row=1, column=3)
        self.set_background()
        self.grid(row=self.row, column=self.column)

    def on_verify(self):
        print("Verify")

    def on_safe(self):
        pass

    def on_unsafe(self):
        pass

    def on_dontcare(self):
        pass

    def set_background(self):
        background = REVIEWABLE_SAFE
        if self.label=='safe':
            if self.reviewed == 1:
                background = REVIEWED_SAFE
        elif self.label == 'unsafe':
            if self.reviewed == 1:
                background = REVIEWED_UNSAFE
            else:
                background = REVIEWABLE_UNSAFE
        else:
            background = 'white'
        self.config(background=background)



class VerticalScrolledFrame(Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling
    """
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw, borderwidth=4, relief='groove')

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        canvas = Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)

if __name__ == '__main__':
    history_window = HistoryWindow()

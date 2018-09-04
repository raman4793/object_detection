import os
import sqlite3
from tkinter import *

from PIL import ImageTk


class HistoryWindow:
    items = []

    def __init__(self):
        self.conn = sqlite3.connect("test.db")
        self.item_count = self.conn.execute("SELECT COUNT(*) FROM history;").fetchone()[0]
        self.top = Tk()
        self.top.geometry("1000x700")
        self.column_count = 3

        # Item(self.top, "history/safe_1536051647.7788084.jpg", 1, 0, 0)
        self.initialize()
        self.top.mainloop()

    def initialize(self):
        self.items = self.conn.execute("SELECT * FROM history")
        row = 0
        column = 0
        for item in self.items:
            item_frame = Item(self.top, os.path.join("history", item[1]), item[0], item[3], row, column)
            column += 1
            if (self.column_count % column) == 0:
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

    def __init__(self, parent, image_file, id, label, row, column, width=300, height=200, borderwidth=2,
                 relief="groove"):
        Frame.__init__(self, parent, width=width, height=height, borderwidth=borderwidth, relief=relief)
        self.row = row
        self.column = column
        self.id = id
        self.label = 'safe' if label == 1 else 'unsafe'
        self.parent = parent
        self.image_file = image_file
        self.initialize()
        self.labels = {'1': 'safe', '2': 'unsafe'}

    def initialize(self):
        self.image = ImageTk.PhotoImage(file=self.image_file)
        self.image_container = Label(self, image=self.image).grid(row=0, column=0, columnspan=2)
        self.image_container = Label(self, text=self.label).grid(row=0, column=2, columnspan=2)
        self.verify_button = Button(self, text="Verify").grid(row=1, column=0)
        self.mark_safe_button = Button(self, text="Mark Safe").grid(row=1, column=1)
        self.mark_unsafe_button = Button(self, text="Mark unsafe").grid(row=1, column=2)
        self.mark_dont_care_button = Button(self, text="Mark don't care").grid(row=1, column=3)
        self.grid(row=self.row, column=self.column)


history_window = HistoryWindow()

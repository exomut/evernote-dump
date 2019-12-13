import tkinter as tk
from tkinter import filedialog

from utilities.settings import Settings


class EvernoteDumpGui(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title = 'shit'
        self.filePaths = tk.filedialog.askopenfilenames()
        print(self.filePaths)


if __name__ == '__main__':
    EvernoteDumpGui().mainloop()
